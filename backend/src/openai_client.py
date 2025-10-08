import openai
from src.settings import Settings

openai.api_key = Settings.OPENAI_API_KEY

functions = [
  {
    "name": "list_services",
    "description": "Return a list of all available salon services",
    "parameters": {"type": "object", "properties": {}}
  },
  {
    "name": "check_availability",
    "description": "Return free time slots for a service on a given date",
    "parameters": {
      "type": "object",
      "properties": {
        "service_id": {"type": "integer"},
        "date": {"type": "string", "format": "date"}
      },
      "required": ["service_id", "date"]
    }
  },
  {
    "name": "create_appointment",
    "description": "Create a confirmed appointment",
    "parameters": {
      "type": "object",
      "properties": {
        "user_id": {"type": "integer"},
        "staff_id": {"type": "integer"},
        "service_id": {"type": "integer"},
        "date": {"type": "string", "format": "date"},
        "start_time": {"type": "string", "format": "date-time"},
        "end_time": {"type": "string", "format": "date-time"}
      },
      "required": ["user_id","staff_id","service_id","date","start_time","end_time"]
    }
  }
]



SYSTEM_PROMPT = "You are a helpful salon assistant ..."

def chat_with_bot(messages: list[dict]) -> dict:
    response = openai.ChatCompletion.create(
        model="gpt-4-turbo",
        messages=messages,
        functions=functions,
        function_call="auto"
    )
    return response.choices[0].message


def list_services() -> list[dict]:
    return [s.to_dict() for s in Service.query.all()]

def check_availability(service_id: int, date: str) -> list[dict]:
    # TODO: 
    raise NotImplementedError

def create_appointment(user_id: int, staff_id: int, service_id: int,
                       date: str, start_time: str, end_time: str) -> dict:
    # TODO: 
    raise NotImplementedError