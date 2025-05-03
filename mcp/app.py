from flask import Flask, request, jsonify
import os
from gemini_model import get_gemini_response # import the class with the logic for gemini responses

app = Flask(__name__)

# Read API key from file (NOT RECOMMENDED FOR PRODUCTION!)
# Replace with environment variable in production
try:
    with open("api_key.txt", "r") as f:
        GOOGLE_API_KEY = f.read().strip()
except FileNotFoundError:
    print("Error: api_key.txt not found. Please create this file with your Google Gemini API key (NOT RECOMMENDED FOR PRODUCTION! Use environment variables instead)")
    GOOGLE_API_KEY = None

if GOOGLE_API_KEY is None:
    raise Exception ("api_key.txt not found or is empty, please create it with Google Gemini API key and restart")


@app.route("/predict", methods=["POST"])
def predict():
    try:
        data = request.get_json()
        prompt = data.get("prompt")

        if not prompt:
            return jsonify({"error": "Missing prompt"}), 400

        # Call Gemini
        gemini_model = get_gemini_response(GOOGLE_API_KEY)
        response = gemini_model.generate_content(prompt)

        if response is None:
             return jsonify({"error": "Gemini API error"}), 500

        return jsonify({"result": response}), 200 # changed structure

    except Exception as e:
        print(f"Error: {e}")
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))