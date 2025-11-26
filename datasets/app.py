
import joblib
import os
import re
import nltk
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from scipy.sparse import hstack
from flask import Flask, request, jsonify

app = Flask(__name__)

# --- Configuration --- #
# Set the path where models and vectorizers are stored
# In a production Docker container, these files would be copied into the image
# For local testing, we might load them directly if they are in the current working directory
# For this example, assume they are accessible in the same directory as app.py or a mounted volume

save_dir = os.path.join(os.path.dirname(__file__), 'saved_models') # Adjust if your structure is different

# Fallback for Colab environment if not run within Docker directly (for testing deployment script)
# In a real Docker environment, the 'saved_models' directory would be copied into the container
if not os.path.exists(save_dir):
    # This block is primarily for local Colab testing of the app.py script content
    # In a Docker environment, the 'saved_models' directory would be copied into the container
    save_dir = '/content/drive/MyDrive/nolan_edutech_assignement/saved_models/'

model_path = os.path.join(save_dir, 'Multinomial_Naive_Bayes_smote_model.joblib')
tfidf_title_path = os.path.join(save_dir, 'tfidf_title.joblib')
tfidf_text_path = os.path.join(save_dir, 'tfidf_text.joblib')

# --- Load Model and Vectorizers --- #
# These are loaded once when the application starts to improve performance
try:
    loaded_model = joblib.load(model_path)
    loaded_tfidf_title = joblib.load(tfidf_title_path)
    loaded_tfidf_text = joblib.load(tfidf_text_path)
    print("✅ Models and vectorizers loaded successfully!")
except Exception as e:
    print(f"❌ Error loading model or vectorizers: {e}")
    # In a real app, you might want to exit or handle this more robustly
    exit(1)

# --- NLTK Setup --- #
# Download necessary NLTK data (if not already downloaded in the Docker image build process)
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
    text = str(text).lower()  # Convert to string and lowercase
    text = re.sub(r'[^a-z\s]', '', text)  # Remove non-alphabetic characters
    tokens = text.split()  # Tokenize
    tokens = [lemmatizer.lemmatize(word) for word in tokens if word not in stop_words]  # Lemmatize and remove stopwords
    return ' '.join(tokens)

# --- Prediction Endpoint --- #
@app.route('/predict', methods=['POST'])
def predict_sentiment_api():
    data = request.get_json(force=True)
    review_title = data.get('review_title', '')
    review_text = data.get('review_text', '')

    if not review_text and not review_title:
        return jsonify({'error': 'Please provide review_title or review_text.'}), 400

    # Preprocess the input review title and text
    cleaned_title = preprocess_text(review_title)
    cleaned_text = preprocess_text(review_text)

    # Vectorize the cleaned title and text
    X_title_transformed = loaded_tfidf_title.transform([cleaned_title])
    X_text_transformed = loaded_tfidf_text.transform([cleaned_text])

    # Combine the features
    X_combined = hstack([X_title_transformed, X_text_transformed])

    # Predict sentiment
    prediction = loaded_model.predict(X_combined)

    # Map numerical prediction to sentiment labels
    sentiment_map = {0: 'Negative 😠', 1: 'Neutral 😐', 2: 'Positive 😀'}
    predicted_sentiment = sentiment_map[prediction[0]]

    return jsonify({
        'review_title': review_title,
        'review_text': review_text,
        'predicted_sentiment': predicted_sentiment
    })

# --- Health Check Endpoint (Optional but Recommended) --- #
@app.route('/health', methods=['GET'])
def health_check():
    return jsonify({'status': 'healthy', 'model_loaded': True})

# --- Run the Flask app --- #
if __name__ == '__main__':
    # Use 0.0.0.0 to make the server accessible from outside the container
    app.run(host='0.0.0.0', port=5000)
