import requests
import os
from flask import Flask, request, jsonify

app = Flask(__name__)

# Read MCP API URL from environment variable
MCP_API_URL = os.environ.get("MCP_API_URL")
if not MCP_API_URL:
    raise ValueError("MCP_API_URL environment variable not set.")


# create a route to store the input from request body to a file named input.txt
@app.route("/store_input", methods=["POST"])
def store_input():
    try:
        data = request.get_json()
        input_text = data.get("input_text")

        if not input_text:
            return jsonify({"error": "Missing input_text"}), 400

        # Store the input to a file
        with open("input.txt", "w") as f:
            f.write(input_text)

        return jsonify({"message": "Input stored successfully"}), 200

    except Exception as e:
        print(f"Error: {e}")
        return jsonify({"error": str(e)}), 500

# create a route to call claude for input that we have stored in input.txt
@app.route("/claude_from_file", methods=["GET"])
def claude_from_file():
    try:
        # Read input from file
        try:
            with open("input.txt", "r") as f:
                prompt_text = f.read()
        except FileNotFoundError:
            return jsonify({"error": "input.txt not found. Please store input first."}), 400

        # Call Claude through MCP
        url = MCP_API_URL + "/predict"  # Assuming your MCP endpoint is /predict
        headers = {"Content-Type": "application/json"}
        data = {"prompt": prompt_text}

        response = requests.post(url, headers=headers, json=data)

        if response.status_code == 200:
            claude_response = response.json()["result"]
            return jsonify({"claude_response": claude_response}), 200
        else:
            print(f"Error: MCP API returned status code {response.status_code}")
            return jsonify({"error": f"MCP API error: {response.status_code}"}), 500

    except requests.exceptions.RequestException as e:
        print(f"Error: Connection error to MCP API: {e}")
        return jsonify({"error": str(e)}), 500
    except Exception as e:
        print(f"Error: {e}")
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=int(os.environ.get("PORT", 5000))) # Different port
