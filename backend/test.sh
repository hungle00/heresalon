# set openai api key or gemini api key or both before running this script
# export OPENAI_API_KEY=
# export GEMINI_API_KEY=
# export DATABASE_URL=

# FLASK_APP=src.entry:flask_app  flask run  # default port 5000

export BASE="http://localhost:5000/api/chat/"


curl -X POST "$BASE" \
  -H "Content-Type: application/json" \
  -d '{
    "conversation": [],
    "message": "Who are your staff?",
    "user_id": 1
  }'


curl -X POST "$BASE" \
  -H "Content-Type: application/json" \
  -d '{
    "conversation": [],
    "message": "Linh Phan có dịch vụ gì?",
    "user_id": 1
  }'

# curl -X POST "$BASE" -H "Content-Type: application/json" -d "{
#   \"conversation\": [],
#   \"message\": \"Any availability for a Gel Manicure on 2025-10-28 between 15:00 and 16:00? Any artist is fine.\"
# }"

# curl -X POST "$BASE" -H "Content-Type: application/json" -d "{
#   \"conversation\": [],
#   \"message\": \"Is Minh Anh free for a Gel Manicure on 2025-10-28 between 15:00 and 16:00?\"
# }"


# curl -X POST "$BASE" -H "Content-Type: application/json" -d "{
#   \"conversation\": [],
#   \"message\": \"Ngày 2025-10-29 từ 13:00 đến 15:00 có ai làm Gel-X được không?\"
# }"


# curl -X POST "$BASE" -H "Content-Type: application/json" -d "{
#   \"conversation\": [],
#   \"message\": \"Is there an opening for Gel Manicure with French Tips on 2025-10-28 between 14:00 and 15:30?\"
# }"


# curl -X POST "$BASE" -H "Content-Type: application/json" -d '{
#   "conversation": [],
#   "message": "I want to book a Gel Manicure on 2025-10-28 from 15:00 to 16:00. Any staff is okay.",
#   "user_id": 1
# }'


# curl -X POST "$BASE" -H "Content-Type: application/json" -d "{
#   \"conversation\": [
#     {\"role\": \"assistant\", \"content\": \"Please confirm: Service: Gel Manicure; Staff: any available; Date: 2025-10-28; Start: 15:00; End: 16:00. Shall I book it?\"}
#   ],
#   \"message\": \"Yes, please confirm the booking.\",
#   \"user_id\": 1
# }"


# curl -X POST "$BASE" -H "Content-Type: application/json" -d "{
#   \"conversation\": [],
#   \"message\": \"Book Gel Manicure on 2025-10-28 15:00–16:00 with Minh Anh if available, otherwise anyone.\",
#   \"user_id\": 1
# }"


# curl -X POST "$BASE" -H "Content-Type: application/json" -d '{
#   "conversation": [],
#   "message": "I’d like Gel-X on 2025-10-29 from 13:00 to 15:00. Any artist is OK."
# }'
