from flask import Flask, request, jsonify
from flask_cors import CORS
from tools1 import smart_router

app = Flask(__name__)

# ✅ Temporarily allow all origins (for development/debugging)
CORS(app)

@app.route("/chat", methods=["POST"])
def chat():
    try:
        data = request.get_json()
        print("✅ Received payload:", data)  # ✅ Log incoming data

        user_id = data.get("user_id", "default_user")
        message = data.get("message", "").strip()
        emotion = data.get("emotion", "neutral")
        emotion_confidence = data.get("emotion_confidence", 0.0)

        if not message:
            return jsonify({"error": "Message cannot be empty"}), 400

        print(f"🎭 [User: {user_id}] Emotion: {emotion} ({emotion_confidence:.2f})")

        response = smart_router(user_id, message)
        return jsonify({"response": response})

    except Exception as e:
        print("🔥 Internal server error:", str(e))  # ✅ Log exceptions
        return jsonify({"error": f"Internal server error: {str(e)}"}), 500

if __name__ == "__main__":
    app.run(debug=True, port=5001)
