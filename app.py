from flask import Flask, render_template, request, jsonify
import openai
import fitz  # PyMuPDF
import os
from dotenv import load_dotenv

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

app = Flask(__name__)

# PDF text extractor
def extract_text_from_pdf(pdf_file):
    text = ""
    with fitz.open(stream=pdf_file.read(), filetype="pdf") as doc:
        for page in doc:
            text += page.get_text()
    return text

@app.route("/")
def index():
    return render_template("index.html")

# Summarize PDF
@app.route("/summarize", methods=["POST"])
def summarize():
    file = request.files["pdf"]
    raw_text = extract_text_from_pdf(file)

    prompt = f"Summarize this PDF text for a college student:\n\n{raw_text[:4000]}"
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}]
    )
    summary = response["choices"][0]["message"]["content"]
    return jsonify({"summary": summary})

# Ask a question
@app.route("/ask", methods=["POST"])
def ask():
    question = request.form["question"]
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[{"role": "user", "content": question}]
    )
    answer = response["choices"][0]["message"]["content"]
    return jsonify({"answer": answer})

# Teach Me This
@app.route("/teach", methods=["POST"])
def teach():
    topic = request.form["topic"]
    prompt = f"""
    You're an expert tutor. Create a short, beginner-friendly lesson plan on: "{topic}".
    Break it into 3 simple parts:
    1. What it is
    2. Why it's important
    3. How to understand or apply it (examples if possible)

    Make it concise but clear, and easy enough for a student to grasp in 5 minutes.
    """
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}]
    )
    lesson = response["choices"][0]["message"]["content"]
    return jsonify({"lesson": lesson})

if __name__ == "__main__":
    app.run(debug=True)
