from crypt import methods
from urllib import request
from flask import Flask, jsonify, request, redirect
from flask_cors import CORS
from dotenv import load_dotenv
from mysqlx import DatabaseError
import psycopg2
import os

load_dotenv()

# PostgreSQL Database credentials loaded from the .env file
DATABASE = os.getenv('DATABASE')
DATABASE_USERNAME = os.getenv('DATABASE_USERNAME')
DATABASE_PASSWORD = os.getenv('DATABASE_PASSWORD')

app = Flask(__name__)

# CORS implemented so that we don't get errors when trying to access the server from a different server location
CORS(app)

try:
  con = psycopg2.connect(
    database=DATABASE, 
    user=DATABASE_USERNAME, 
    password=DATABASE_PASSWORD
  )

  cur = con.cursor()

  # GET: Fetch all movies from the database
  @app.route('/')
  def fetch_all_movies():
    cur.execute('SELECT * FROM movies')
    rows = cur.fetchall()
    print(rows)

    return jsonify(rows)

  # GET: Fetch movie by movieId from the database
  @app.route('/<int:movie_id>')
  def fetch_by_id(movie_id=None):
    cur.execute(f'SELECT * FROM movies WHERE movie_id={movie_id}')
    rows = cur.fetchall()
    print(rows)

    return jsonify(rows)

  # POST: Create movies and add them to the database
  @app.route('/add-movie', methods=['GET', 'POST'])
  def add_movie():
    if request.method == 'POST':
      data = request.form.to_dict()
      print(data)
      cur.execute("INSERT INTO movies (movie_name, img_url, release_year, summary, director, genre, rating, movie_runtime, meta_score) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)", 
                  (f"{data['movieName']}", f"{data['imgUrl']}", f"{data['releaseYear']}", f"{data['summary']}", f"{data['director']}", f"{data['genre']}", f"{data['rating']}", f"{data['movieRuntime']}", f"{data['metaScore']}"))
      con.commit()      
      return redirect('http://localhost:3000', code="200")
    else:
      return 'Form submission failed'

  # DELETE: Delete movie by movieId from the database
  @app.route('/delete-movie', methods=['GET', 'DELETE'])
  def delete_by_id():
    movie_id = request.form.to_dict()
    print(movie_id['movieId'])
    cur.execute(f"DELETE FROM movies WHERE movie_id = {movie_id['movieId']} RETURNING movie_name")
    con.commit()

    return 'Movie Deleted'
  
  # PUT: Update movie by movieId from the database
  @app.route('/update-movie', methods=['GET', 'PUT'])
  def update_by_id():
    cur.execute('UPDATE movies SET movie_name = \'Goldeneye\' WHERE movie_id = 1')
    con.commit()

    return 'Movie Updated'

except: 
  print('Error')