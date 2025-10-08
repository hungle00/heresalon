from flask import Blueprint, request, jsonify
from src.openai_client import chat_with_bot, functions, SYSTEM_PROMPT
from src.models import User  # if you need to identify the user

blueprint = Blueprint('chat', __name__, url_prefix='/api')

@blueprint.route('/chat/', methods=['POST'])
def chat():
    data = request.get_json()
    conversation = data.get('conversation', [])
    user_message = data.get('message')
    conversation.append({"role": "user", "content": user_message})
    # prepend system prompt on first turn
    if not any(msg['role'] == 'system' for msg in conversation):
        conversation.insert(0, {"role": "system", "content": SYSTEM_PROMPT})
    assistant_msg = chat_with_bot(conversation)
    return jsonify(assistant_msg)