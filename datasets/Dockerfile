
# Use an official Python runtime as a parent image
FROM python:3.9-slim-buster

# Set the working directory in the container
WORKDIR /app

# Install system dependencies needed for NLTK (if any, typically not for basic NLTK usage, but good practice)
# RUN apt-get update && apt-get install -y --no-install-recommends \
#     build-essential \
#     && rm -rf /var/lib/apt/lists/*

# Copy the requirements file into the container at /app
COPY requirements.txt .

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Download NLTK data (stopwords and wordnet) during image build to avoid runtime downloads
RUN python -c "import nltk; nltk.download('stopwords', quiet=True); nltk.download('wordnet', quiet=True)"

# Create a directory for saved models inside the container
RUN mkdir -p /app/saved_models

# Copy the saved model and vectorizer files from the host into the container
# In a real scenario, you'd mount a volume or use cloud storage for large models
# For this Colab simulation, we assume these are in the same dir as the Dockerfile for COPY instruction
# We'll copy them from a relative path within the Colab environment for this example
# Adjust these paths if running locally or in a different environment
COPY ./saved_models/Multinomial_Naive_Bayes_smote_model.joblib /app/saved_models/
COPY ./saved_models/tfidf_title.joblib /app/saved_models/
COPY ./saved_models/tfidf_text.joblib /app/saved_models/

# Copy the Flask application file into the container at /app
COPY app.py .

# Make port 5000 available to the world outside this container
EXPOSE 5000

# Run app.py when the container launches
CMD ["python", "app.py"]
