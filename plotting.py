from io import BytesIO
import base64
import matplotlib
matplotlib.use('Agg')  # Use 'Agg' backend for non-interactive plotting
import matplotlib.pyplot as plt
from wordcloud import WordCloud


def plot_scores(data):

    if 'Score' not in data.columns:
        raise ValueError("DataFrame must contain 'Score' column")

    # Plotting
    plt.figure(figsize=(10, 10))
    data['Score'].value_counts().plot(kind='bar', color='skyblue')
    plt.title('Distribution of Scores', fontsize=16, color="Black")
    plt.xlabel('Star Rating',fontsize=14, fontweight='bold', color='black')
    plt.ylabel('Count',fontsize=14, fontweight='bold', color='black')
    plt.grid(axis='y', linestyle='--', alpha=0.7)

    # Save plot to a BytesIO object
    img = BytesIO()
    plt.savefig(img, format='png')
    img.seek(0)
    plt.close()

    # Return the image data in base64 format
    img_base64 = base64.b64encode(img.getvalue()).decode('utf-8')
    return img_base64

def plot_sentiment(data):

    if 'Sentiment' not in data.columns:
        raise ValueError("DataFrame must contain 'Sentiment' column")
    
    #plotting   
    plt.figure(figsize=(10, 10))
    sentiment_counts = data['Sentiment'].value_counts()
    sentiment_counts.plot(kind='bar', color=['skyblue', 'salmon', 'lightgreen'])
    
    # Customizing the plot
    plt.title('Distribution of Sentiments', fontsize=16, color='black')
    plt.xlabel('Sentiment', fontsize=14, fontweight='bold', color='black')
    plt.ylabel('Count', fontsize=14, fontweight='bold', color='black')
    plt.grid(axis='y', linestyle='--', alpha=0.7, color='gray')

    # Save plot to a BytesIO object
    img = BytesIO()
    plt.savefig(img, format='png')
    img.seek(0)
    plt.close()

    # Return the image data in base64 format
    img_base64 = base64.b64encode(img.getvalue()).decode('utf-8')
    return img_base64

def generate_wordclouds_file(data):
    # Convert each list in 'Cleaned_Text' to a single string
    data['Cleaned_Text'] = data['Cleaned_Text'].apply(lambda x: ' '.join(x) if isinstance(x, list) else x)

    # Separate Positive, Neutral, and Negative Sentiment Texts
    positive_texts = ' '.join(data[data['Sentiment'] == 'positive']['Cleaned_Text'])
    neutral_texts = ' '.join(data[data['Sentiment'] == 'neutral']['Cleaned_Text'])
    negative_texts = ' '.join(data[data['Sentiment'] == 'negative']['Cleaned_Text'])
    
    # Generate word clouds
    positive_wordcloud = WordCloud(width=800, height=400, background_color='black').generate(positive_texts)
    neutral_wordcloud = WordCloud(width=800, height=400, background_color='black').generate(neutral_texts)
    negative_wordcloud = WordCloud(width=800, height=400, background_color='black').generate(negative_texts)
    
    plt.figure(figsize=(15, 5))
    #plt.title('Word Cloud for the given Reviews', fontsize=16, color='black')

    # Positive word cloud
    plt.subplot(1, 3, 1)
    plt.imshow(positive_wordcloud, interpolation='bilinear')
    plt.title('Positive Sentiments')
    plt.axis('off')
    

    # Neutral word cloud
    plt.subplot(1, 3, 2)
    plt.imshow(neutral_wordcloud, interpolation='bilinear')
    plt.title('Neutral Sentiments')
    plt.axis('off')

    # Negative word cloud
    plt.subplot(1, 3, 3)
    plt.imshow(negative_wordcloud, interpolation='bilinear')
    plt.title('Negative Sentiments')
    plt.axis('off')

    # Save the plot to a BytesIO object
    wordcloud_img = BytesIO()
    plt.savefig(wordcloud_img, format='png', bbox_inches='tight', pad_inches=0)
    wordcloud_img.seek(0)
    plt.close()

    # Encode the image to base64 for embedding in HTML
    img_base64 = base64.b64encode(wordcloud_img.getvalue()).decode('utf-8')
    return img_base64

def generate_wordcloud_text(text):
    wordcloud = WordCloud(width=800, height=400, background_color='black').generate(text)

    plt.figure(figsize=(15, 5))
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.title('Word Cloud for Input Text')
    plt.axis('off')

    # Save the plot to a BytesIO object
    wordcloud_img = BytesIO()
    plt.savefig(wordcloud_img, format='png', bbox_inches='tight', pad_inches=0)
    wordcloud_img.seek(0)
    plt.close()

    # Encode the image to base64 for embedding in HTML
    img_base64 = base64.b64encode(wordcloud_img.getvalue()).decode('utf-8')
    return img_base64

