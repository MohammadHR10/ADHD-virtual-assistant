from flask import Flask, request, jsonify
from flask_cors import CORS
from dotenv import load_dotenv
import os
from tools1 import talk_with_user  # ✅ make sure this is the correct path

# Load environment variables
load_dotenv()
groq_api_key = os.getenv("GROQ_API_KEY")

# Flask app setup
app = Flask(__name__)
CORS(app, resources={r"/chat": {"origins": "http://localhost:8501"}})

@app.route("/chat", methods=["POST"])
def chat():
    try:
        data = request.get_json()

        if not data or "user_id" not in data or "message" not in data:
            return jsonify({"error": "Both 'user_id' and 'message' are required"}), 400

        user_id = data["user_id"]
        message = data["message"]

        if not message.strip():
            return jsonify({"error": "Message cannot be empty"}), 400

        # Format input for LangChain tool
        formatted_input = f"User ID: {user_id}. User input: {message}"
        response = talk_with_user(formatted_input)

        return jsonify({"response": response})

    except Exception as e:
        print(f"Backend error: {str(e)}")
        return jsonify({"error": f"Internal server error: {str(e)}"}), 500

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5001)
