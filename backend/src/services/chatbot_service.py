import json
from datetime import datetime, date, time
from typing import Any, Dict, List, Optional

from flask import current_app

from src.models import Staff, Service
from src.services.appointment_service import AppointmentService
from src.settings import Settings

try:
    import openai  # type: ignore
except ImportError:
    openai = None  # will be checked at runtime

try:
    import google.generativeai as genai  # type: ignore
except ImportError:
    genai = None  # optional Gemini support
from twilio.rest import Client

class ChatBotService:
    """Conversational assistant for HereSalon.

    The chatbot is initialized with an LLM provider based on the
    ``Settings.LLM_PROVIDER`` flag.  It exposes a public :meth:`chat`
    method that accepts a list of prior messages and optional user and
    salon identifiers.  The method returns either a final assistant
    message or a dictionary with error information.
    """

    # System prompt guides the model’s behaviour.  It explains the
    # salon domain, the available tools, and how to interact with
    # customers.  The model should always call tools when data is
    # required and confirm booking details before creating an
    # appointment.
    # System prompt: multilingual + tool-aware
    SYSTEM_PROMPT = (
        "You are HereSalon’s helpful and friendly salon assistant.\n"
        "\n"
        "LANGUAGE & STYLE\n"
        "- Auto-detect the customer’s language from their latest message and respond in that language "
        " (e.g., English, Vietnamese, Spanish). If they switch languages, follow the latest one.\n"
        "- Keep proper nouns (brand, staff names, service names) in their original form; optionally add a short "
        " translation/explanation in parentheses when helpful.\n"
        "- Be concise, polite, and professional.\n"
        "\n"
        "DATES, TIMES, UNITS\n"
        "- Always show and request dates as YYYY-MM-DD and times in 24h HH:MM.\n"
        "- When uncertain about timezones, say you’re using the salon’s local time and ask if the customer "
        " wants a different time.\n"
        "\n"
        "WHAT YOU CAN DO\n"
        "- Answer questions about services and staff, suggest appointments, and book appointments.\n"
        "- Never invent schedules or availability—always call a tool when information is required.\n"
        "\n"
        "TOOLS (function calling)\n"
        "- Use `list_services` to list salon services.\n"
        "- Use `list_staff` to list staff members. If `service_id` is given, only staff in that service’s salon.\n"
        "- Use `find_available_staff` to suggest staff for a service at a specific date/time window.\n"
        "- Use `get_appointments` to retrieve the user’s appointments.\n"
        "- Use `get_current_appointments` to retrieve upcoming appointments only.\n"
        "- Use `create_appointment` to book only after explicit confirmation.\n"
        "- Use `update_appointment` to modify an existing appointment (confirm the new details first).\n"
        "- Use `delete_appointment` to cancel an existing appointment (confirm the id/date/time first).\n"
        "BOOKING FLOW\n"
        "1) If details are missing (service, date, start/end time, preferred staff), ask for them in the customer’s language.\n"
        "2) When suggesting times, provide 1–3 options if possible.\n"
        "3) Before calling a write tool, summarize and ask to confirm:\n"
        "   • For create/update: Service, Staff, Date, Start, End, Phone (guests only)\n"
        "   • For delete: Appointment ID (and show date/time)\n"
        "4) For guests (no user_id), collect a phone number and include it in `create_appointment`.\n"
        "\n"
        "ERROR HANDLING\n"
        "- If a tool returns an error, apologize in the customer’s language, briefly explain the issue, and offer a next step.\n"
    )


    # Tool specifications for the OpenAI function calling interface.  Each
    # tool includes a JSON schema describing its parameters.  When the
    # model emits a call to one of these tools, the dispatcher will
    # invoke the corresponding `_tool_*` method.
    TOOLS: List[Dict[str, Any]] = [
        {
            "type": "function",
            "function": {
                "name": "get_appointments",
                "description": (
                    "Get all appointments for the current user. "
                    "Returns a list of appointment objects with fields such as "
                    "id, staff_id, user_id, service_id, phone_number, status, "
                    "date, start_time and end_time."
                ),
                "parameters": {
                    "type": "object",
                    "properties": {},
                    "required": [],
                },
            },
        },
        {
            "type": "function",
            "function": {
                "name": "create_appointment",
                "description": (
                    "Create a new appointment for an authenticated user or a "
                    "guest.  If the user is a guest (no user_id), a "
                    "customer_phone field must be provided.  The appointment "
                    "will be validated for date, time formats, and time conflicts."
                ),
                "parameters": {
                    "type": "object",
                    "properties": {
                        "staff_id": {"type": "integer"},
                        "service_id": {"type": "integer"},
                        "date": {"type": "string", "description": "YYYY-MM-DD"},
                        "start_time": {"type": "string", "description": "HH:MM (24h)"},
                        "end_time": {"type": "string", "description": "HH:MM (24h)"},
                        "customer_phone": {"type": "string", "description": "Required if guest", "nullable": True},
                    },
                    "required": ["staff_id", "service_id", "date", "start_time", "end_time"],
                },
            },
        },
        {
            "type": "function",
            "function": {
                "name": "list_services",
                "description": (
                    "List services offered by the salon.  Returns an array of service objects. "
                    "If a salon_id is provided, the results are limited to that salon; "
                    "otherwise all services are returned."
                ),
                "parameters": {
                    "type": "object",
                    "properties": {
                        "salon_id": {"type": "integer", "description": "ID of the salon", "nullable": True},
                    },
                    "required": [],
                },
            },
        },
        {
            "type": "function",
            "function": {
                "name": "list_staff",
                "description": (
                    "List staff members at the salon.  Returns an array of staff objects. "
                    "If a salon_id is provided, limits results to that salon.  "
                    "An optional service_id may be supplied; in that case, only staff "
                    "from the same salon as the service are returned."
                ),
                "parameters": {
                    "type": "object",
                    "properties": {
                        "salon_id": {"type": "integer", "description": "ID of the salon", "nullable": True},
                        "service_id": {"type": "integer", "description": "Restrict staff to those in the same salon as this service", "nullable": True},
                    },
                    "required": [],
                },
            },
        },
        {
            "type": "function",
            "function": {
                "name": "find_available_staff",
                "description": (
                    "Find staff members who are available for a given service and time slot. "
                    "The time slot is specified by date, start_time and end_time.  The "
                    "service_id is used to determine the salon, then all staff in that salon "
                    "are checked for time conflicts.  Returns an array of available staff objects."
                ),
                "parameters": {
                    "type": "object",
                    "properties": {
                        "service_id": {"type": "integer", "description": "ID of the service the customer wants"},
                        "date": {"type": "string", "description": "Desired appointment date (YYYY-MM-DD)"},
                        "start_time": {"type": "string", "description": "Desired start time (HH:MM)"},
                        "end_time": {"type": "string", "description": "Desired end time (HH:MM)"},
                    },
                    "required": ["service_id", "date", "start_time", "end_time"],
                },
            },
        },
        {
            "type": "function",
            "function": {
                "name": "get_current_appointments",
                "description": "Get upcoming appointments (start_time >= now) for the current user.",
                "parameters": {"type": "object", "properties": {}, "required": []},
            },
        },
        {
            "type": "function",
            "function": {
                "name": "update_appointment",
                "description": (
                    "Update an appointment owned by the current user (date/start_time/end_time/status). "
                    "All times are HH:MM 24h; date is YYYY-MM-DD. Confirms no time conflicts."
                ),
                "parameters": {
                    "type": "object",
                    "properties": {
                        "appointment_id": {"type": "integer"},
                        "date": {"type": "string", "nullable": True, "description": "YYYY-MM-DD"},
                        "start_time": {"type": "string", "nullable": True, "description": "HH:MM (24h)"},
                        "end_time": {"type": "string", "nullable": True, "description": "HH:MM (24h)"},
                        "status": {"type": "string", "nullable": True, "enum": ["pending","confirmed","completed","canceled"]},
                        "customer_phone": {"type": "string", "nullable": True, "description": "Optional; overrides saved phone for SMS"},
                    },
                    "required": ["appointment_id"],
                },
            },
        },
        {
            "type": "function",
            "function": {
                "name": "delete_appointment",
                "description": "Delete/cancel an appointment owned by the current user.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "appointment_id": {"type": "integer"},
                        "customer_phone": {"type": "string", "nullable": True, "description": "Optional; overrides saved phone for SMS"},
                    },
                    "required": ["appointment_id"],
                },
            },
        },        
        
    ]

    def __init__(self) -> None:
        """Initialise the chatbot with the configured LLM provider."""
        provider = (Settings.LLM_PROVIDER or "openai").lower()
        self.provider = provider
        if provider == "openai":
            if openai is None:
                raise ImportError("openai package is not installed")
            self.client = openai.OpenAI(api_key=Settings.OPENAI_API_KEY)
        elif provider == "gemini":
            # Gemini configuration expects an API key set in Settings.GEMINI_API_KEY
            if genai is None:
                raise ImportError("google.generativeai package is not installed")
            if not Settings.GEMINI_API_KEY:
                raise ValueError("GEMINI_API_KEY environment variable is not set")
            genai.configure(api_key=Settings.GEMINI_API_KEY)
            self.client = genai
        else:
            raise ValueError(f"Unsupported LLM provider: {provider}")

    # ------------------------------------------------------------------
    # Tool implementations
    #
    # Each of the following methods executes the logic for a tool.  They
    # accept a dict of arguments and an optional user_id.  They return a
    # JSON‑serialisable Python object (list or dict) which will be
    # passed back to the LLM as the tool result.
    # ------------------------------------------------------------------

    def _tool_get_appointments(self, args: Dict[str, Any], user_id: Optional[int]) -> Any:
        """Return all appointments belonging to the user."""
        if user_id is None:
            # Without a user_id we cannot look up appointments.  Return an empty list.
            return []
        appointments = AppointmentService.get_appointments(user_id)
        return [appt.to_dict() for appt in appointments]

    def _tool_create_appointment(self, args: Dict[str, Any], user_id: Optional[int]) -> Any:
        data: Dict[str, Any] = {
            "staff_id": args.get("staff_id"),
            "service_id": args.get("service_id"),
            "date": args.get("date"),
            "start_time": args.get("start_time"),
            "end_time": args.get("end_time"),
        }
        if args.get("customer_phone"):
            data["customer_phone"] = args["customer_phone"]

        appointment, error = AppointmentService.create_appointment(data, user_id)
        if error:
            return {"error": error}

        # ✅ send SMS via AppointmentService
        try:
            AppointmentService.send_confirmation(
                appointment=appointment,
                action="created",
                user_id=user_id,
                customer_phone=args.get("customer_phone"),
            )
        except Exception as e:
            current_app.logger.error(f"SMS (create) failed: {e}")

        return appointment.to_dict()

    def _tool_update_appointment(self, args: Dict[str, Any], user_id: Optional[int]) -> Any:
        appt_id = args.get("appointment_id")
        if not appt_id:
            return {"error": "appointment_id is required"}

        # Prepare update payload (only include provided keys)
        payload: Dict[str, Any] = {}
        for k in ("date", "start_time", "end_time", "status"):
            if args.get(k) is not None:
                payload[k] = args[k]

        appt, err = AppointmentService.update_appointment(appt_id, payload, user_id)
        if err:
            return {"error": err}

        # ✅ send SMS via AppointmentService
        try:
            AppointmentService.send_confirmation(
                appointment=appt,
                action="updated",
                user_id=user_id,
                customer_phone=args.get("customer_phone"),
            )
        except Exception as e:
            current_app.logger.error(f"SMS (update) failed: {e}")

        return appt.to_dict()

    def _tool_delete_appointment(self, args: Dict[str, Any], user_id: Optional[int]) -> Any:
        appt_id = args.get("appointment_id")
        if not appt_id:
            return {"error": "appointment_id is required"}

        # Fetch appointment first to craft message after deletion
        appt_before, err = AppointmentService.get_appointment_by_id(appt_id, user_id)
        if err:
            return {"error": err}

        ok, del_err = AppointmentService.delete_appointment(appt_id, user_id)
        if not ok:
            return {"error": del_err or "Failed to delete appointment"}

        # ✅ send SMS via AppointmentService using details from appt_before
        try:
            if appt_before:
                AppointmentService.send_confirmation(
                    appointment=appt_before,
                    action="deleted",
                    user_id=user_id,
                    customer_phone=args.get("customer_phone"),
                )
        except Exception as e:
            current_app.logger.error(f"SMS (delete) failed: {e}")

        return {"success": True, "deleted_appointment_id": appt_id}

    def _tool_list_services(self, args: Dict[str, Any], user_id: Optional[int]) -> Any:
        """Return a list of services, optionally filtered by salon."""
        salon_id = args.get("salon_id")
        # If salon_id is provided, we could join through SalonService to fetch only
        # services available at that salon.  Otherwise, return all services.
        if salon_id:
            # Prevent circular import by importing SalonService within the function
            from src.models.salon_service import SalonService  # type: ignore
            from src.models import Salon
            salon = Salon.get(id=salon_id)
            if not salon:
                return {"error": "Salon not found"}
            salon_services = SalonService.query.filter_by(salon_id=salon_id).all()
            services = [ss.service for ss in salon_services]
        else:
            services = Service.query.all()
        return [svc.to_dict() for svc in services]

    def _tool_list_staff(self, args: Dict[str, Any], user_id: Optional[int]) -> Any:
        """Return a list of staff members, optionally filtered by salon or service."""
        salon_id = args.get("salon_id")
        service_id = args.get("service_id")
        staff_query = Staff.query
        if service_id:
            # If a service_id is supplied, limit the staff to those in the same salon
            service = Service.get(id=service_id)
            if not service:
                return {"error": "Service not found"}
            staff_query = staff_query.filter_by(salon_id=service.salon_id)
        elif salon_id:
            staff_query = staff_query.filter_by(salon_id=salon_id)
        staff_members = staff_query.all()
        return [member.to_dict() for member in staff_members]

    def _tool_find_available_staff(self, args: Dict[str, Any], user_id: Optional[int]) -> Any:
        """Find staff who are free during the requested time slot for a service."""
        service_id = args.get("service_id")
        date_str = args.get("date")
        start_time_str = args.get("start_time")
        end_time_str = args.get("end_time")
        # Validate service
        service = Service.get(id=service_id)
        if not service:
            return {"error": "Service not found"}
        # Parse date and times
        try:
            appointment_date = date.fromisoformat(date_str)
        except Exception:
            return {"error": "Invalid date format. Use YYYY-MM-DD"}
        if not self._validate_time_format(start_time_str) or not self._validate_time_format(end_time_str):
            return {"error": "Invalid time format. Use HH:MM (24h)"}
        start_time_obj = time.fromisoformat(start_time_str)
        end_time_obj = time.fromisoformat(end_time_str)
        start_dt = datetime.combine(appointment_date, start_time_obj)
        end_dt = datetime.combine(appointment_date, end_time_obj)
        if start_dt >= end_dt:
            return {"error": "start_time must be earlier than end_time"}
        # Find staff in the same salon
        staff_members = Staff.query.filter_by(salon_id=service.salon_id).all()
        available: List[Dict[str, Any]] = []
        for staff in staff_members:
            conflict = AppointmentService.check_time_conflict(
                staff_id=staff.id,
                start_time=start_dt,
                end_time=end_dt,
                exclude_appointment_id=None,
            )
            if not conflict:
                available.append(staff.to_dict())
        return available

    # ------------------------------------------------------------------
    # Core chat loop
    # ------------------------------------------------------------------

    def chat(self, messages: List[Dict[str, Any]], user_id: Optional[int] = None) -> Dict[str, Any]:
        """
        Engage with the LLM to continue a conversation.

        :param messages: A list of message dicts with ``role`` and ``content`` keys.
                         The list should *not* include the system prompt; it
                         will be prepended automatically.
        :param user_id:  Optional authenticated user id.  When provided,
                         appointment retrieval and creation will be tied to
                         this user.  When not provided, booking as a guest
                         requires a ``customer_phone``.
        :return: A dict representing the final assistant message.  If errors
                 occur, an ``error`` field is included.
        """
        provider = self.provider
        # Prepend system prompt
        chat: List[Dict[str, Any]] = [{"role": "system", "content": self.SYSTEM_PROMPT}] + messages
        # Limit the number of tool invocations to avoid infinite loops
        for _ in range(5):
            if provider == "openai":
                try:
                    resp = self.client.chat.completions.create(
                        model="gpt-4o",
                        messages=chat,
                        tools=self.TOOLS,
                        tool_choice="auto",
                        temperature=0.3,
                    )
                except Exception as e:
                    return {"error": f"LLM request failed: {e}"}
                msg = resp.choices[0].message
                # When the model decides to call a function, handle it here
                if msg.tool_calls:
                    for tool_call in msg.tool_calls:
                        name = tool_call.function.name
                        try:
                            args = json.loads(tool_call.function.arguments or "{}")
                        except json.JSONDecodeError:
                            args = {"_raw": tool_call.function.arguments}
                        result = self._dispatch_tool(name, args, user_id)
                        # Append the original tool call for context
                        chat.append({
                            "role": "assistant",
                            "tool_calls": [tool_call],
                        })
                        # Append the tool result so the model can use it
                        chat.append({
                            "role": "tool",
                            "tool_call_id": tool_call.id,
                            "name": name,
                            "content": json.dumps(result),
                        })
                    # Continue loop so the model can incorporate tool results
                    continue
                # No tool call means the model has produced a final answer
                return {"role": msg.role, "content": msg.content}
            elif provider == "gemini":
                # Basic implementation for Gemini: send messages and tools as
                # context.  Note: Gemini does not natively support function
                # calling.  We simply return the generated text.
                try:
                    prompt = "\n".join([f"{m['role']}: {m['content']}" for m in chat])
                    gemini_resp = self.client.generate_content(prompt)
                    return {"role": "assistant", "content": gemini_resp.text}
                except Exception as e:
                    return {"error": f"Gemini request failed: {e}"}
        # If we exit the loop without returning, we likely hit a tool call loop
        return {"error": "Sorry, I couldn't complete the request after several tries."}

    # ------------------------------------------------------------------
    # Internal helpers
    # ------------------------------------------------------------------

    def _dispatch_tool(self, name: str, args: Dict[str, Any], user_id: Optional[int]) -> Any:
        """Dispatch a tool call by name to the appropriate method."""
        print(f"🔧 Calling tool: {name}")
        try:
            if name == "get_appointments":
                return self._tool_get_appointments(args, user_id)
            if name == "get_current_appointments":
                return self._tool_get_current_appointments(args, user_id)
            if name == "create_appointment":
                return self._tool_create_appointment(args, user_id)
            if name == "update_appointment":
                return self._tool_update_appointment(args, user_id)
            if name == "delete_appointment":
                return self._tool_delete_appointment(args, user_id)
            if name == "list_services":
                return self._tool_list_services(args, user_id)
            if name == "list_staff":
                return self._tool_list_staff(args, user_id)
            if name == "find_available_staff":
                return self._tool_find_available_staff(args, user_id)
            return {"error": f"Unknown tool: {name}"}
        except Exception as e:
            current_app.logger.error(f"Error in tool {name}: {e}")
            return {"error": f"Tool execution error: {e}"}

    @staticmethod
    def _validate_time_format(time_str: str) -> bool:
        """Validate a time string in HH:MM format."""
        try:
            time.fromisoformat(time_str)
            return True
        except Exception:
            return False