from flask import Blueprint, jsonify, request

from src.routes.api.bot import chat_with_bot, SYSTEM_PROMPT

blueprint = Blueprint("chat", __name__, url_prefix="/api")

@blueprint.route("/chat/", methods=["POST"])
def chat():
    """Primary chat endpoint for the salon assistant.

    The request JSON should include:

    * ``conversation``: a list of prior messages (dictionaries with
      ``role`` and ``content``).
    * ``message``: the user’s new message to append.
    * ``user_id``: (optional) authenticated user identifier.  When
      provided, appointment data will be scoped to this user.

    The response is a JSON object containing the assistant’s message.
    """
    data = request.get_json(force=True) or {}
    conversation = data.get("conversation", [])
    user_message = data.get("message", "")
    user_id = data.get("user_id")
    # Append the new user message
    conversation = list(conversation)  # make a copy
    if user_message:
        conversation.append({"role": "user", "content": user_message})
    # Delegate to the chat bot
    assistant_msg = chat_with_bot(conversation, user_id=user_id)
    print(f"Assistant message: {assistant_msg}")
    return jsonify(assistant_msg)