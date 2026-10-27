from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app, resources={r"/chat": {"origins": [
    "http://localhost", "http://127.0.0.1"
]}})

FAQS = {
    "courses": "We offer Information Technology, Cybersecurity, Software Development and Business Information Systems.",
    "admission": "Open the Apply page, complete all required fields and submit your application.",
    "fees": "Please contact the college admissions office for the current official fee structure.",
    "contact": "Please replace this message with your college's approved phone number and email address.",
    "duration": "Course duration depends on the programme. Check the Courses page for the sample duration."
}

def get_reply(message: str) -> str:
    text = message.lower()
    if any(word in text for word in ["hello", "hi", "hey"]):
        return "Hello! Welcome to CollegeConnect. Ask me about courses, admission, fees or contact details."
    for keyword, answer in FAQS.items():
        if keyword in text:
            return answer
    return "I do not have that information yet. Please contact the college office for assistance."

@app.post("/chat")
def chat():
    data = request.get_json(silent=True) or {}
    message = data.get("message", "")
    if not isinstance(message, str) or not message.strip():
        return jsonify({"reply": "Please type a question."}), 400
    if len(message) > 300:
        return jsonify({"reply": "Please keep your question under 300 characters."}), 400
    return jsonify({"reply": get_reply(message)})

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=False)
