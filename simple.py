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

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/about')
def about():
    return render_template('About.html')

@app.route('/contact')
def contact():
    return render_template('Contact.html')


@app.route('/recommend', methods=['POST'])

def recommend():
    # Get the artist name and genre entered by the user
    artist_name = request.form['artist_name']
    genre_name = request.form['genre_name']

    # Filter the dataset by artist name and genre
    filtered_data = music_data[(music_data['artist_name'] == artist_name) & (music_data['genre'] == genre_name)]

    # If no results found, return an error message
    if filtered_data.empty:
        return render_template('no_music.html')

    # Get the index of the first song in the filtered dataset
    song_index = filtered_data.index.values[0]

    # Get the top 5 most similar songs
    similar_indices = cosine_similarities[song_index].argsort()[:-6:-1]
    similar_songs = [(music_data['track_name'][i], cosine_similarities[song_index][i]) for i in similar_indices]

    # Pass the results to the template
    return render_template('Recommendation.html', artist_name=artist_name, genre_name=genre_name, similar_songs=similar_songs)

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
        host='localhost',
        user='root',
        password='Steyr251198',
        database= 'musicrecommend'
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


# Define a route for the recommendation page
@app.route('/about')
def about():
    return render_template('About.html')

@app.route('/contact')
def contact():
    return render_template('Contact.html')



