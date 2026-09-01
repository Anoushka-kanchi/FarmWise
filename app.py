from flask import Flask, request, jsonify, render_template

from ai.chatbot import ask_ai
from ai.recommendations import recommend_crops
from ai.crop_analysis import analyze_crop_issue


app = Flask(__name__)


# -----------------------------------
# Home Page
# -----------------------------------

@app.route("/")
def home():
    return render_template("index.html")


# -----------------------------------
# AI Chatbot
# -----------------------------------

@app.route("/api/chat", methods=["POST"])
def chat():

    try:
        data = request.get_json()

        if not data:
            return jsonify({
                "error": "No data received."
            }), 400

        question = data.get("message")

        if not question:
            return jsonify({
                "error": "Please provide a message."
            }), 400

        answer = ask_ai(question)

        return jsonify({
            "response": answer
        })

    except Exception as e:

        print("Chat API Error:", e)

        return jsonify({
            "error": "Unable to process your request."
        }), 500


# -----------------------------------
# Crop Recommendation
# -----------------------------------

@app.route("/api/recommend-crops", methods=["POST"])
def recommend():

    try:
        data = request.get_json()

        if not data:
            return jsonify({
                "error": "No farm data received."
            }), 400

        soil_type = data.get("soil_type")
        temperature = data.get("temperature")
        rainfall = data.get("rainfall")
        season = data.get("season")
        water_availability = data.get("water_availability")

        if not all([
            soil_type,
            temperature,
            rainfall,
            season,
            water_availability
        ]):
            return jsonify({
                "error": "Please provide all farm details."
            }), 400

        result = recommend_crops(
            soil_type,
            temperature,
            rainfall,
            season,
            water_availability
        )

        return jsonify({
            "recommendations": result
        })

    except Exception as e:

        print("Crop Recommendation Error:", e)

        return jsonify({
            "error": "Unable to generate crop recommendations."
        }), 500


# -----------------------------------
# Crop Issue Analysis
# -----------------------------------

@app.route("/api/analyze-crop", methods=["POST"])
def analyze_crop():

    try:
        data = request.get_json()

        if not data:
            return jsonify({
                "error": "No crop data received."
            }), 400

        crop = data.get("crop")
        symptoms = data.get("symptoms")

        if not crop or not symptoms:
            return jsonify({
                "error": "Please provide crop and symptoms."
            }), 400

        result = analyze_crop_issue(
            crop,
            symptoms
        )

        return jsonify({
            "analysis": result
        })

    except Exception as e:

        print("Crop Analysis Error:", e)

        return jsonify({
            "error": "Unable to analyze the crop issue."
        }), 500


# -----------------------------------
# Start Flask
# -----------------------------------

if __name__ == "__main__":
    app.run(debug=True)