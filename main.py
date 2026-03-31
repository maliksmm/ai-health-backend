import os
import google.generativeai as genai
from flask import Flask, request, jsonify
from flask_cors import CORS
from PIL import Image
import io

app = Flask(__name__)
# CORS allow karega ki frontend isse securely connect kar sake
CORS(app)

# 🔑 TERI GOOGLE AI API KEY YAHAN HAI
genai.configure(api_key="AIzaSyBbnS9RzsTWdedHQhboIm7rxnb8n9AoDK8")

# Hum Gemini ka 1.5 Flash model use kar rahe hain (Speed + Vision ke liye best)
model = genai.GenerativeModel('gemini-1.5-flash')

@app.route("/", methods=["GET"])
def home():
    return "🔥 MALIK AI HEALTHCARE SERVER IS LIVE! DUNIYA HILNE WALI HAI! 🔥"

@app.route("/api/analyze", methods=["POST"])
def analyze_disease():
    # Check karna ki photo aayi hai ya nahi
    if 'image' not in request.files:
        return jsonify({"error": "⚠️ Koi photo upload nahi hui!"}), 400

    file = request.files['image']
    
    try:
        # Photo ko AI ke padhne laayak format me convert karna
        image = Image.open(io.BytesIO(file.read()))
        
        # 🧠 THE MASTER PROMPT (AI ko kya karna hai)
        prompt = """
        You are an advanced Medical AI assistant built for rural India.
        Look at the uploaded image of a skin condition, wound, or visible disease carefully.
        Give the answer in BOTH simple Hindi and English.
        Provide the response in this structure:
        1. 🦠 **Possible Condition (Kya ho sakta hai):** (Name the disease/condition)
        2. 🩺 **Basic First Aid / Home Remedy (Gharelu Nuskha):** (What to do immediately)
        3. ⚠️ **Disclaimer:** This is an AI prediction. Please consult a real human doctor for confirmed medical advice.
        """
        
        # AI ko photo aur prompt ek sath bhejna
        response = model.generate_content([prompt, image])
        
        # Jo result aaya wo wapas app me bhej dena
        return jsonify({"status": "success", "result": response.text})
        
    except Exception as e:
        return jsonify({"error": f"Server Error: {str(e)}"}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)

