from typing import Any, Dict, List, Optional

from src.services.chatbot_service import ChatBotService

# Instantiate a singleton ChatBotService.  Because the service holds
# configuration and an LLM client, it should be created once at module
# import time.
_chatbot = ChatBotService()

# Re‑export the system prompt and tool definitions for compatibility
SYSTEM_PROMPT: str = ChatBotService.SYSTEM_PROMPT
TOOLS: List[Dict[str, Any]] = ChatBotService.TOOLS

def chat_with_bot(messages: List[Dict[str, Any]], user_id: Optional[int] = None) -> Dict[str, Any]:
    """Public entry point to converse with the salon assistant.

    :param messages: A list of message dictionaries with ``role`` and
        ``content`` keys.  Do **not** include the system prompt in
        this list; it will be prepended automatically by the
        ChatBotService.
    :param user_id: Optionally pass the authenticated user’s id.  If
        provided, appointment functions will tie results to this user.
    :return: The assistant’s final message as returned from the
        underlying :class:`ChatBotService`.
    """
    return _chatbot.chat(messages, user_id)

# For compatibility with older code that expected a ``functions``
# mapping, we expose a dictionary mapping tool names to the
# corresponding callables on the ChatBotService instance.  While
# newer code should use ``chat_with_bot`` directly, this can be used
# for manual invocation of tools.
functions: Dict[str, Any] = {
    "get_appointments": lambda args, user_id: _chatbot._tool_get_appointments(args, user_id),
    "create_appointment": lambda args, user_id: _chatbot._tool_create_appointment(args, user_id),
    "list_services": lambda args, user_id: _chatbot._tool_list_services(args, user_id),
    "list_staff": lambda args, user_id: _chatbot._tool_list_staff(args, user_id),
    "find_available_staff": lambda args, user_id: _chatbot._tool_find_available_staff(args, user_id),
}