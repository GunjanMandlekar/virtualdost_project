from flask import Flask, render_template, request
import pandas as pd
import nltk
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# Ensure required NLTK data is available
nltk.download('punkt')

# Load the mental health dataset
data = pd.read_csv("mental_health_data.csv")

# Extract Questions and Answers
questions = data["Question"].tolist()
answers = data["Answer"].tolist()

# Convert text into numerical format using TF-IDF
vectorizer = TfidfVectorizer()
question_vectors = vectorizer.fit_transform(questions)

# Flask App
app = Flask(__name__)

def get_response(user_input):
    user_vector = vectorizer.transform([user_input])
    similarities = cosine_similarity(user_vector, question_vectors)
    
    # Find the most relevant question
    best_match_index = similarities.argmax()
    
    # If similarity is low, return a generic response
    if similarities[0, best_match_index] < 0.2:
        return "I'm here for you. Could you explain a bpyit more?"
    
    return answers[best_match_index]

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/get", methods=["POST"])
def chatbot_response():
    user_text = request.form["msg"]
    response = get_response(user_text)
    return response

if __name__ == "__main__":
    app.run(debug=True)
