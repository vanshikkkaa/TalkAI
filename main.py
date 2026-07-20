import argparse
import random
import string
import subprocess
import sys


def ensure_nltk():
    try:
        import nltk
    except ModuleNotFoundError:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "nltk"])
        import nltk

    try:
        nltk.download("punkt", quiet=True)
        nltk.download("wordnet", quiet=True)
        nltk.download("punkt_tab", quiet=True)
    except Exception:
        pass

    return nltk


nltk = ensure_nltk()
from nltk.stem import WordNetLemmatizer
from nltk.tokenize import word_tokenize

# Initialize NLP tools
lemmatizer = WordNetLemmatizer()

# Chatbot knowledge base
responses = {
    "greeting": [
        "Hello! How can I help you?",
        "Hi there! What can I do for you?",
        "Greetings! Ask me anything."
    ],

    "name": [
        "I am Sophie, an AI chatbot built using Natural Language Processing.",
        
    ],

    "nlp": [
        "NLP stands for Natural Language Processing. It helps computers understand human language."
    ],

    "python": [
        "Python is a popular programming language used for AI, data science, and web development."
    ],

    "ai": [
        "Artificial Intelligence enables machines to perform tasks that normally require human intelligence."
    ],

    "thanks": [
        "You're welcome!",
        "Happy to help!"
    ],

    "goodbye": [
        "Goodbye! Have a great day.",
        "See you later!"
    ]
}


# Keywords for intent detection
patterns = {
    "greeting": ["hello", "hi", "hey", "good morning","hii"],
    "name": ["your name", "who are you", "what are you"],
    "nlp": ["nlp", "natural language processing"],
    "python": ["python", "programming"],
    "ai": ["ai", "artificial intelligence"],
    "thanks": ["thank", "thanks"],
    "goodbye": ["bye", "exit", "quit"]
}


def preprocess(text):
    """
    Tokenizes and lemmatizes user input
    """
    tokens = word_tokenize(text.lower())

    cleaned_words = []

    for word in tokens:
        if word not in string.punctuation:
            cleaned_words.append(lemmatizer.lemmatize(word))

    return cleaned_words


def get_response(user_input):
    words = preprocess(user_input)

    for intent, keywords in patterns.items():
        for keyword in keywords:
            keyword_words = preprocess(keyword)

            if any(word in words for word in keyword_words):
                return random.choice(responses[intent])

    return "Sorry, I don't understand that. Can you ask something else?"


def chatbot(input_questions=None):
    print("================================")
    print("      NLP AI CHATBOT")
    print("Type 'bye' to exit (if interactive mode)")
    print("================================")

    if input_questions:
        for question in input_questions:
            print(f"\nYou: {question}")
            answer = get_response(question)
            print("Bot:", answer)
    else:
        while True:
            user_input = input("\nYou: ")

            if user_input.lower() in ["bye", "exit", "quit"]:
                print("Bot:", random.choice(responses["goodbye"]))
                break

            answer = get_response(user_input)
            print("Bot:", answer)


# Start chatbot
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run the NLP chatbot")
    parser.add_argument("--demo", action="store_true", help="Run a short predefined conversation")
    args = parser.parse_args()

    if args.demo:
        auto_questions = [
            "hi",
            "what is your name",
            "what is nlp",
            "tell me about python",
            "thank you",
            "bye"
        ]
        chatbot(auto_questions)
    else:
        chatbot()

