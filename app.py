from flask import Flask,render_template, request, send_file , session
from flask import Flask, render_template, request, send_file
import pandas as pd
from io import StringIO
import uuid
from sentiment_algorithm import SentimentAlgorithm
from plotting import plot_scores, plot_sentiment, generate_wordclouds_file, generate_wordcloud_text
from translator import translate_text, validate_text_length

app = Flask(__name__)

# Initialize the sentiment analysis algorithm
sentiment_algorithm = SentimentAlgorithm()

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/predict', methods=['POST'])
def predict():
    file = request.files.get('file_input')
    text = request.form.get('text_input')
    text_result = None
    file_result = None
    sentiment_distribution_result = None
    plot_score_base64 = None
    plot_img_base64 = None
    wordclouds_file_img_base64 = None
    wordcloud_text_img_base64 = None
    translation_limit_message = None
    

    if file and file.filename.endswith('.csv'):
        # Handle CSV file in memory
        file_content = file.read().decode('utf-8')
        data = pd.read_csv(StringIO(file_content))
        data = data[['Score','Text']]

        # Process the data
        data['Cleaned_Text'] = data['Text'].apply(lambda x: sentiment_algorithm.preprocess_paragraph(x))
        data['Sentiment_Score'] = data['Text'].apply(lambda x: sentiment_algorithm.calculate_sentiment(x))
        data['Sentiment'] = data['Text'].apply(lambda x: sentiment_algorithm.classify_sentiment(x))

        # Convert the processed DataFrame back to CSV
        output = StringIO()
        data.to_csv(output, index=False)
        output.seek(0)

        # Prepare the result to display and download
        file_result = {
            'csv_content': output.getvalue(),
            'columns': data.columns.tolist(),
            'rows': data.head(5).values.tolist()  # Display the first 5 rows as a preview
        }

        # Generate the plot
        plot_score_base64 = plot_scores(data)
        plot_img_base64 = plot_sentiment(data)
        #wordclouds_file_img_base64 = generate_wordclouds_file(data)

        # Debug: Check if the Cleaned_Text column has data
        print("Generating word cloud for file input...")
        print(data['Cleaned_Text'].head())

        wordclouds_file_img_base64 = generate_wordclouds_file(data)

        # Debug: Check if the wordcloud image is generated
        print(f"Word cloud generated: {bool(wordclouds_file_img_base64)}")

    elif text:

        translated_text= validate_text_length(text)
        
        text = translate_text(translated_text)

        sentiment_score = sentiment_algorithm.calculate_sentiment(text)
        sentiment = sentiment_algorithm.classify_sentiment(text)
        sentiment_scores, sentiment_labels = sentiment_algorithm.sentiment_distribution(text)


        wordcloud_text_img_base64 = generate_wordcloud_text(text)

        text_result = {
            'score': sentiment_score,
            'sentiment': sentiment
        }
        sentiment_distribution_result = {
            'scores': sentiment_scores,
            'labels': sentiment_labels
        }

    return render_template('result.html', text_result=text_result, file_result=file_result, sentiment_distribution_result=sentiment_distribution_result, plot_score_base64=plot_score_base64, 
                           plot_img_base64=plot_img_base64, wordclouds_file_img_base64 = wordclouds_file_img_base64, wordcloud_text_img_base64 = wordcloud_text_img_base64,
                             translation_limit_message=translation_limit_message)
        

@app.route('/download_csv', methods=['GET'])
def download_csv():
    csv_content = request.args.get('csv_content')
    if not csv_content:
        return "No CSV content available", 400
    
    # Create a file-like object from the CSV content
    output = StringIO(csv_content)
    output.seek(0)

    return send_file(output, mimetype='text/csv', as_attachment=True, download_name=f'results_{uuid.uuid4().hex[:8]}.csv')



if __name__ == '__main__':
    app.run(debug=True)
