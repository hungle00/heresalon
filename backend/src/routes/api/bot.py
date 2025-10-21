from typing import Any, Dict, List, Optional
import json
import os
import requests

from openai import OpenAI
from src.settings import Settings

# ---- OpenAI client & system prompt ----
client = OpenAI(api_key=Settings.OPENAI_API_KEY)

SYSTEM_PROMPT = (
    "You are a helpful, friendly salon assistant for HereSalon.\n"
    "You can check availability, create/update/cancel appointments, and look up a user's appointments.\n"
    "Before creating or updating an appointment, ALWAYS confirm the date (YYYY-MM-DD), start time, end time, staff, and service.\n"
    "For guests, remind them you'll need a phone number if they are not signed in.\n"
    "Use tools whenever you need salon data or to take actions."
)

# ---- Runtime config to reach your Flask API ----
API_BASE_URL = getattr(Settings, "API_BASE_URL", None) or os.getenv("API_BASE_URL", "http://127.0.0.1:8000")
# Your Flask blueprint uses url_prefix='/api' in appointments.py
APPT_BASE = f"{API_BASE_URL}/api/appointments"

# ---- Tool (function) schemas exposed to GPT-4o ----
TOOLS: List[Dict[str, Any]] = [
    {
        "type": "function",
        "function": {
            "name": "get_appointments",
            "description": "Get all appointments for the current user. Requires auth token to determine role.",
            "parameters": {
                "type": "object",
                "properties": {},
                "required": []
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "create_appointment",
            "description": "Create a new appointment for either an authenticated user or a guest.",
            "parameters": {
                "type": "object",
                "properties": {
                    "staff_id":       {"type": "integer"},
                    "service_id":     {"type": "integer"},
                    "date":           {"type": "string", "description": "YYYY-MM-DD"},
                    "start_time":     {"type": "string", "description": "HH:MM (24h)"},
                    "end_time":       {"type": "string", "description": "HH:MM (24h)"},
                    "customer_phone": {"type": "string", "description": "Required if guest/unauthenticated", "nullable": True},
                    "status":         {"type": "string", "enum": ["pending", "confirmed", "cancelled"], "nullable": True},
                },
                "required": ["staff_id", "service_id", "date", "start_time", "end_time"]
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "get_appointment",
            "description": "Get a single appointment by ID. Auth required for permission checks.",
            "parameters": {
                "type": "object",
                "properties": {
                    "appointment_id": {"type": "integer"}
                },
                "required": ["appointment_id"]
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "update_appointment",
            "description": "Update fields on an appointment (date, start_time, end_time, status). Auth required.",
            "parameters": {
                "type": "object",
                "properties": {
                    "appointment_id": {"type": "integer"},
                    "date":           {"type": "string", "description": "YYYY-MM-DD", "nullable": True},
                    "start_time":     {"type": "string", "description": "HH:MM (24h)", "nullable": True},
                    "end_time":       {"type": "string", "description": "HH:MM (24h)", "nullable": True},
                    "status":         {"type": "string", "enum": ["pending", "confirmed", "cancelled"], "nullable": True},
                },
                "required": ["appointment_id"]
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "delete_appointment",
            "description": "Delete an appointment by ID. Auth required and permissions enforced.",
            "parameters": {
                "type": "object",
                "properties": {
                    "appointment_id": {"type": "integer"}
                },
                "required": ["appointment_id"]
            },
        },
    },
]

def _auth_headers(user_token: Optional[str]) -> Dict[str, str]:
    """Attach Bearer token when provided (for @token_required / @optional_token_required)."""
    headers = {"Content-Type": "application/json"}
    if user_token:
        headers["Authorization"] = f"Bearer {user_token}"
    return headers

# ---- Tool executors: call your Flask API ----
def _tool_get_appointments(user_token: Optional[str]) -> Dict[str, Any]:
    r = requests.get(f"{APPT_BASE}/", headers=_auth_headers(user_token), timeout=15)
    return _normalize_response(r)

def _tool_create_appointment(args: Dict[str, Any], user_token: Optional[str]) -> Dict[str, Any]:
    payload = {
        "staff_id": args["staff_id"],
        "service_id": args["service_id"],
        "date": args["date"],
        "start_time": args["start_time"],
        "end_time": args["end_time"],
    }
    # Optional fields
    if args.get("customer_phone"):
        payload["customer_phone"] = args["customer_phone"]
    if args.get("status"):
        payload["status"] = args["status"]

    r = requests.post(f"{APPT_BASE}/", headers=_auth_headers(user_token), data=json.dumps(payload), timeout=20)
    return _normalize_response(r)

def _tool_get_appointment(args: Dict[str, Any], user_token: Optional[str]) -> Dict[str, Any]:
    appt_id = args["appointment_id"]
    r = requests.get(f"{APPT_BASE}/{appt_id}/", headers=_auth_headers(user_token), timeout=15)
    return _normalize_response(r)

def _tool_update_appointment(args: Dict[str, Any], user_token: Optional[str]) -> Dict[str, Any]:
    appt_id = args["appointment_id"]
    payload: Dict[str, Any] = {}
    for k in ("date", "start_time", "end_time", "status"):
        if k in args and args[k] is not None:
            payload[k] = args[k]

    r = requests.put(f"{APPT_BASE}/{appt_id}/", headers=_auth_headers(user_token), data=json.dumps(payload), timeout=20)
    return _normalize_response(r)

def _tool_delete_appointment(args: Dict[str, Any], user_token: Optional[str]) -> Dict[str, Any]:
    appt_id = args["appointment_id"]
    r = requests.delete(f"{APPT_BASE}/{appt_id}/", headers=_auth_headers(user_token), timeout=15)
    return _normalize_response(r)

def _normalize_response(r: requests.Response) -> Dict[str, Any]:
    """Convert HTTP response to a consistent dict for the model."""
    try:
        data = r.json()
    except Exception:
        data = {"error": "Non-JSON response", "text": r.text}

    return {
        "ok": r.ok,
        "status": r.status_code,
        "data": data
    }

# ---- Public entrypoint ----
def chat_with_bot(
    messages: List[Dict[str, str]],
    user_token: Optional[str] = None,
) -> Dict[str, Any]:
    """
    Send messages to GPT-4o. If it requests a tool call, execute it against your Flask API,
    append the tool result, and continue the loop until we get a final assistant message.
    """
    chat: List[Dict[str, Any]] = [{"role": "system", "content": SYSTEM_PROMPT}] + messages

    # Allow the model to call multiple tools if needed (bounded to avoid infinite loops)
    for _ in range(3):
        resp = client.chat.completions.create(
            model="gpt-4o",
            messages=chat,
            tools=TOOLS,
            tool_choice="auto",
            temperature=0.3,
        )

        msg = resp.choices[0].message
        # If the model wants to call a tool
        if msg.tool_calls:
            for tc in msg.tool_calls:
                name = tc.function.name
                try:
                    args = json.loads(tc.function.arguments or "{}")
                except json.JSONDecodeError:
                    # Pass raw arguments to help debugging
                    args = {"_raw": tc.function.arguments}

                # Run the tool
                tool_result = _dispatch_tool(name, args, user_token)

                # Append the tool result so the model can see it
                chat.append({
                    "role": "assistant",
                    "tool_calls": [tc],  # echo back the call
                })
                chat.append({
                    "role": "tool",
                    "tool_call_id": tc.id,
                    "name": name,
                    "content": json.dumps(tool_result),
                })
            # Loop again so the model can incorporate tool results
            continue

        # No tool call -> final answer
        return {
            "role": msg.role,
            "content": msg.content,
        }

    # Safety net if the model keeps asking for tools (should be rare)
    return {
        "role": "assistant",
        "content": "Sorry, I couldn't finish the request. Please try again."
    }

def _dispatch_tool(name: str, args: Dict[str, Any], user_token: Optional[str]) -> Dict[str, Any]:
    try:
        print("Calling function", name, "user_token", user_token)
        # if name == "get_appointments":
        #     return _tool_get_appointments(user_token)
        # if name == "create_appointment":
        #     return _tool_create_appointment(args, user_token)
        # if name == "get_appointment":
        #     return _tool_get_appointment(args, user_token)
        # if name == "update_appointment":
        #     return _tool_update_appointment(args, user_token)
        # if name == "delete_appointment":
        #     return _tool_delete_appointment(args, user_token)
        return {"ok": False, "status": 400, "data": {"error": f"Unknown tool: {name}"}}
    except requests.RequestException as e:
        return {"ok": False, "status": 502, "data": {"error": f"Network error: {e}"}}
    except Exception as e:
        return {"ok": False, "status": 500, "data": {"error": f"Tool dispatch error: {e}"}}

if __name__ == "__main__":
    import os
    import textwrap

    # ---- Config for examples ----
    STAFF_ID   = "STAFF_ID"
    SERVICE_ID = "SERVICE_ID"
    USER_TOKEN = "USER_TOKEN"

    def show(title: str, content: str):
        print("\n" + "=" * 80)
        print(title)
        print("-" * 80)
        print(textwrap.fill(content or "(no content)", width=88))
        print("=" * 80 + "\n")

    # ------------------------------
    # Example 1: Guest booking (includes phone number)
    # ------------------------------
    guest_messages = [
        {"role": "user", "content": (
            f"I want to book service {SERVICE_ID} with staff {STAFF_ID} on 2025-10-28 "
            "from 10:00 to 11:00. My phone number is 555-123-4567."
        )}
    ]
    result = chat_with_bot(guest_messages)  # user_token=None
    show("Example 1: Guest booking", result.get("content", ""))

    # ------------------------------
    # Example 2: Authenticated: list my appointments
    # ------------------------------
    auth_list_messages = [
        {"role": "user", "content": "Show my upcoming appointments."}
    ]
    result = chat_with_bot(auth_list_messages, user_token=USER_TOKEN)
    show("Example 2: Auth user lists appointments", result.get("content", ""))

    # ------------------------------
    # Example 3: Authenticated: create an appointment (model should confirm details)
    # ------------------------------
    auth_create_messages = [
        {"role": "user", "content": (
            f"Book a classic manicure (service {SERVICE_ID}) with staff {STAFF_ID} "
            "on 2025-11-02 from 14:30 to 15:30."
        )}
    ]
    result = chat_with_bot(auth_create_messages, user_token=USER_TOKEN)
    show("Example 3: Auth user creates appointment", result.get("content", ""))


    # ------------------------------
    # Example 4: Update then cancel (the bot should call update/delete tools)
    # Note: This assumes the bot will reference a specific appointment in context.
    # You can also prompt it with an explicit appointment ID.
    # ------------------------------
    update_then_cancel = [
        {"role": "user", "content": "Reschedule my 2025-11-02 manicure to 15:00–16:00."},
        {"role": "user", "content": "Actually, cancel that appointment."},
    ]
    result = chat_with_bot(update_then_cancel, user_token=USER_TOKEN)
    show("Example 4: Update then cancel", result.get("content", ""))

    # ------------------------------
    # Example 5: Validation error demo (end_time before start_time)
    # ------------------------------
    bad_time_messages = [
        {"role": "user", "content": (
            f"Book service {SERVICE_ID} with staff {STAFF_ID} on 2025-10-28 "
            "from 11:00 to 10:00 (oops). My phone is 555-123-4567."
        )}
    ]
    result = chat_with_bot(bad_time_messages)
    show("Example 5: Validation error path", result.get("content", ""))
