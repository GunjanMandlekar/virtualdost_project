import pandas as pd
from flask import Flask, request, jsonify, render_template

app = Flask(__name__)

# Load the updated dataset
df = pd.read_csv("mental_health_professional.csv")

def get_response(user_input):
    user_input = user_input.lower()

    for _, row in df.iterrows():
        if row["Mental_Health_Issue"].lower() in user_input:
            advice = row["Professional_Advice"]
            supplements = row["Recommended_Supplements"]
            when_to_see_doctor = row["When_to_See_a_Doctor"]
            return f"{advice}\n\nRecommended Supplements: {supplements}\n\nWhen to See a Doctor: {when_to_see_doctor}"
    
    return "I'm sorry, I couldn't find relevant information. Please consult a professional."

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/get", methods=["POST"])
def chatbot_response():
    user_msg = request.form["msg"]
    response = get_response(user_msg)
    return response

if __name__ == "__main__":
    app.run(debug=True)
