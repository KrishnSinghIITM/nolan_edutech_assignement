import joblib
import os
import re
import nltk
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from scipy.sparse import hstack
from flask import Flask, request, jsonify

# Allow cross-origin requests from the web app
from flask_cors import CORS

app = Flask(__name__)

# Enable CORS for all routes (adjust origins in production)
CORS(app)

# --- Configuration --- #
# Set the path where models and vectorizers are stored
# In Docker container, these files will be copied into /app/saved_models
# In local testing, they are inside the 'models' directory of the repo

save_dir = os.path.join(os.path.dirname(__file__), 'models')  # updated from saved_models → models

# Fallback for Colab environment if not run within Docker directly (for testing deployment script)
if not os.path.exists(save_dir):
    save_dir = '/content/drive/MyDrive/nolan_edutech_assignement/models/'  # updated fallback path

model_path = os.path.join(save_dir, 'Multinomial_Naive_Bayes_smote_model.joblib')
tfidf_title_path = os.path.join(save_dir, 'tfidf_title.joblib')
tfidf_text_path = os.path.join(save_dir, 'tfidf_text.joblib')

# --- Load Model and Vectorizers --- #
try:
    loaded_model = joblib.load(model_path)
    loaded_tfidf_title = joblib.load(tfidf_title_path)
    loaded_tfidf_text = joblib.load(tfidf_text_path)
    print("✅ Models and vectorizers loaded successfully!")
except Exception as e:
    print(f"❌ Error loading model or vectorizers: {e}")
    exit(1)

# --- NLTK Setup --- #
try:
    nltk.data.find('corpora/stopwords')
except LookupError:
    nltk.download('stopwords', quiet=True)
try:
    nltk.data.find('corpora/wordnet')
except LookupError:
    nltk.download('wordnet', quiet=True)

stop_words = set(stopwords.words('english'))
lemmatizer = WordNetLemmatizer()

# --- Preprocessing Function --- #
def preprocess_text(text):
    text = str(text).lower()
    text = re.sub(r'[^a-z\s]', '', text)
    tokens = text.split()
    tokens = [lemmatizer.lemmatize(word) for word in tokens if word not in stop_words]
    return ' '.join(tokens)

# --- Prediction Endpoint --- #
@app.route('/predict', methods=['POST'])
def predict_sentiment_api():
    data = request.get_json(force=True)
    review_title = data.get('review_title', '')
    review_text = data.get('review_text', '')

    if not review_text and not review_title:
        return jsonify({'error': 'Please provide review_title or review_text.'}), 400

    cleaned_title = preprocess_text(review_title)
    cleaned_text = preprocess_text(review_text)

    X_title_transformed = loaded_tfidf_title.transform([cleaned_title])
    X_text_transformed = loaded_tfidf_text.transform([cleaned_text])

    X_combined = hstack([X_title_transformed, X_text_transformed])

    prediction = loaded_model.predict(X_combined)

    sentiment_map = {0: 'Negative 😠', 1: 'Neutral 😐', 2: 'Positive 😀'}
    predicted_sentiment = sentiment_map[prediction[0]]

    return jsonify({
        'review_title': review_title,
        'review_text': review_text,
        'predicted_sentiment': predicted_sentiment
    })

# --- Health Check Endpoint --- #
@app.route('/health', methods=['GET'])
def health_check():
    return jsonify({'status': 'ok', 'message': 'API is running'}), 200

if __name__ == '__main__':
    # Listen on all interfaces so Docker can map the port
    app.run(host='0.0.0.0', port=5000)
