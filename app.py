from flask import Flask, render_template, request, jsonify
import pandas as pd
import nltk
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression

# Unduh resource NLTK jika belum ada
nltk.download('punkt')
nltk.download('wordnet')

lemmatizer = WordNetLemmatizer()

# Load dataset
dataset = pd.read_csv("data/chatbot_dataset.csv")

# Preprocessing: Lemmatization function
def lemmatize_text(text):
    tokens = word_tokenize(text.lower())
    lemmas = [lemmatizer.lemmatize(token) for token in tokens]
    return " ".join(lemmas)  # Gabungkan kembali jadi string

# Terapkan preprocessing ke kolom pattern untuk data training
dataset['pattern_lemma'] = dataset['pattern'].apply(lemmatize_text)

# Siapkan fitur dan label
X_text = dataset['pattern_lemma'].tolist()
y = dataset['intent'].tolist()

# Vectorizer dan model
vectorizer = TfidfVectorizer()
X = vectorizer.fit_transform(X_text)

model = LogisticRegression()
model.fit(X, y)

# Fungsi prediksi intent dari input pengguna
def predict_intent(user_input):
    user_input_lemma = lemmatize_text(user_input)
    user_vec = vectorizer.transform([user_input_lemma])
    intent_pred = model.predict(user_vec)[0]
    return intent_pred

# Fungsi ambil response berdasarkan intent
def get_response(user_input):
    intent = predict_intent(user_input)
    responses = dataset[dataset['intent'] == intent]['response'].tolist()
    if responses:
        return responses[0]  # Bisa juga random.choice jika ingin variasi
    else:
        return "Maaf, saya belum mengerti pertanyaan Anda. Silakan hubungi admin."

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/ask", methods=["POST"])
def ask():
    data = request.get_json()
    user_input = data.get("user_input", "")
    response = get_response(user_input)
    return jsonify({"response": response})

if __name__ == "__main__":
    app.run(debug=True)
