import mysql
from flask import Flask, request, render_template
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

app = Flask(__name__)

# Load the dataset
music_data = pd.read_csv("Dataset/music.csv")

# Clean the data by filling missing values with 0
music_data = music_data.fillna(0)

# Define the vectorizer
vectorizer = TfidfVectorizer(stop_words='english')

# Vectorize the data
music_vectors = vectorizer.fit_transform(music_data['lyrics'])

# Compute the pairwise cosine similarities
cosine_similarities = cosine_similarity(music_vectors)



@app.route('/recommend', methods=['POST'])
def recommend():
    # Get the artist name entered by the user
    artist_name = request.form['artist_name']

    # Check if artist name is present in the dataset
    if artist_name not in music_data['artist_name'].unique():
        return render_template('no_music.html')

    # Get the index of the artist
    artist_index = music_data[music_data['artist_name'] == artist_name].index.values[0]

    # Get the top 5 most similar songs
    similar_indices = cosine_similarities[artist_index].argsort()[:-6:-1]
    similar_songs = [(music_data['track_name'][i], cosine_similarities[artist_index][i]) for i in similar_indices]

    # Round off similarity scores
    similar_songs = [(song[0], round(song[1], 2)) for song in similar_songs]

    # Render the template with the recommended songs
    return render_template('Recommendation.html', artist=artist_name, songs=similar_songs)

if __name__ == '__main__':
    app.run(debug=True)


@app.route('/contact-us', methods=['POST'])
def contact_us():
    # Get contact form data
    name = request.form['name']
    email = request.form['email']
    subject = request.form['subject']
    message = request.form['message']

    # Create a connection to the MySQL database
    db = mysql.connector.connect(
        host="localhost",
        user="root",
        password="Steyr251198",
        database="musicrecommend"
    )

    # Create a cursor to execute SQL queries
    cursor = db.cursor()

    # Define the SQL query to insert contact form data
    sql = "INSERT INTO contacts (name, email, subject, message) VALUES (%s, %s, %s, %s)"

    # Execute the query with the data
    values = (name, email, subject, message)
    cursor.execute(sql, values)

    # Commit the changes to the database
    db.commit()

    # Close the database connection and cursor
    cursor.close()
    db.close()

    return """
                <script>alert("Thank you for your message! We will get back to you soon."); 
                window.location.href = '/';</script>
                """

@app.route('/')
def home():
    return render_template('home.html')

# Define a route for the recommendation page
@app.route('/about')
def about():
    return render_template('About.html')

@app.route('/contact')
def contact():
    return render_template('Contact.html')

@app.route('/recommendation')
def contact():
    return render_template('Recommendation.html')



