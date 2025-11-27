# Use an official Python runtime as a parent image
FROM python:3.9-slim-buster

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file into the container at /app
COPY requirements.txt .

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Download NLTK data (stopwords and wordnet) during image build to avoid runtime downloads
RUN python -c "import nltk; nltk.download('stopwords', quiet=True); nltk.download('wordnet', quiet=True)"

# Create a directory for saved models inside the container
RUN mkdir -p /app/saved_models

# Copy the model and vectorizer files from datasets folder into the container
COPY Multinomial_Naive_Bayes_smote_model.joblib /app/saved_models/
COPY tfidf_title.joblib /app/saved_models/
COPY tfidf_text.joblib /app/saved_models/

# Copy the Flask application file into the container at /app
COPY app.py /app/

# Make port 5000 available to the world outside this container
EXPOSE 5000

# Run app.py when the container launches
CMD ["python", "app.py"]
