from io import BytesIO
from flask import Flask, jsonify, render_template, request, send_file
import pandas as pd
import matplotlib.pyplot as plt
import pickle
import base64
import nltk
import re
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from nltk.tokenize import word_tokenize
from nltk import pos_tag
from nltk.corpus import wordnet
import joblib

import warnings
warnings.filterwarnings('ignore')

#Downloading all neccessary nltk packages
nltk.download('stopwords')
nltk.download("punkt")
nltk.download('averaged_perceptron_tagger')
nltk.download("wordnet")

#Stopwords with custom words to be removed from the dataset
STOPWORDS = set(stopwords.words("english"))
custom_stopwords={"br"}
STOPWORDS.update(custom_stopwords)

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('landing.html')


@app.route('/predict', methods=['POST'])
def predict():
    pipeline = joblib.load("Models/sentiment_svc_model.pkl")
    label_encoder = joblib.load("Models/label_encoder.pkl")

    try:
        # Check if the request contains a file input or a text input

        if "file" in request.files:
            # prediction from CSV file
            file = request.files["file"]
            data = pd.read_csv(file)

            predictions, graph = csv_prediction(pipeline,label_encoder, data)

            response = send_file(
                predictions,
                mimetype="text/csv",
                as_attachment=True,
                download_name="Predictions.csv",
            )

            response.headers["X-Graph-Exists"] = "true"
            response.headers["X-Graph-Data"] = base64.b64encode(
                graph.getbuffer()
            ).decode("ascii")

            return response

        elif "text" in request.json:
            # Prediction for Text input
            text_input = request.json["text"]
            predicted_sentiment = text_prediction(pipeline,label_encoder, text_input)

            return jsonify({"prediction": predicted_sentiment})

    except Exception as e:
        return jsonify({"error": str(e)})
    

# Function to map NLTK POS tags to WordNet POS tags
def get_wordnet_pos(tag):
    if tag.startswith('J'):
        return wordnet.ADJ
    elif tag.startswith('V'):
        return wordnet.VERB
    elif tag.startswith('N'):
        return wordnet.NOUN
    elif tag.startswith('R'):
        return wordnet.ADV
    else:
        return wordnet.NOUN

def text_preprocessing(text):
    # Initialize WordNetLemmatizer
    lemmatizer = WordNetLemmatizer()
    review = re.sub("[^a-zA-Z]", " ", text)
    review = review.lower()
    review = word_tokenize(review)
    # POS tagging
    pos_tags = pos_tag(review)
    # Lemmatize with POS tags
    review = [lemmatizer.lemmatize(word, get_wordnet_pos(tag)) for word, tag in pos_tags if word not in STOPWORDS]
    return " ".join(review)


def text_prediction(pipeline,label_encoder, text_input):
    processed_text = text_preprocessing(text_input) 
    X_prediction = [processed_text] 
    y_predictions = pipeline.predict(X_prediction) 
    sentiment_label = label_encoder.inverse_transform(y_predictions)[0] 
    return sentiment_label
 

def csv_prediction(pipeline,label_encoder, data):
    data["Cleaned_Text"] = data["Sentence"].apply(text_preprocessing) 
    X_prediction = data["Cleaned_Text"] 
    y_predictions = pipeline.predict(X_prediction) 
    data["Predicted sentiment"] = label_encoder.inverse_transform(y_predictions) 
    predictions_csv = BytesIO() 
    data.to_csv(predictions_csv, index=False) 
    predictions_csv.seek(0) 
    graph = get_distribution_graph(data) 
    return predictions_csv, graph
    
    
def get_distribution_graph(data):
    fig = plt.figure(figsize=(5, 5))
    colors = ("green", "red", "blue")
    wp = {"linewidth": 1, "edgecolor": "black"}
    tags = data["Predicted sentiment"].value_counts()
    explode = (0.01, 0.01)

    tags.plot(
        kind="pie",
        autopct="%1.1f%%",
        shadow=True,
        colors=colors,
        startangle=90,
        wedgeprops=wp,
        explode=explode,
        title="Sentiment Distribution",
        xlabel="",
        ylabel="",
    )

    graph = BytesIO()
    plt.savefig(graph, format="png")
    plt.close()

    return graph




'''@app.route('/upload')
def predict():
    if 'file' not in request.files:
        return "No file part"
    file = request.files['file']
    if file.filename == '':
        return "No selected file"
    if file and file.filename.endswith('.csv'):
        df = pd.read_csv(file)
        return df.to_html()
    else:
        return "Invalid file type"
    
'''


if __name__ == "__main__":
    app.run(port=5000, debug=True)