# /home/dcsadmin/Documents/PersonalisedGreeting/GeneratedImages/6368Card1.png

import os
import pandas as pd
from api_util import get_generated_card
from flask import Flask, request, send_file, jsonify
import sqlite3

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = "/home/dcsadmin/Documents/PersonalisedGreeting/Potraits"
# Connect to the database (or create it if it doesn't exist)


@app.route('/create-user',methods=["POST"])
def create_user():
  conn = sqlite3.connect('mydatabase.db')
  cursor = conn.cursor()
  # Create the table
  cursor.execute('''CREATE TABLE IF NOT EXISTS employee (
                      NGS	INTEGER PRIMARY KEY,
                      NAME	TEXT NOT NULL,
                      FOOD	TEXT NOT NULL,
                      TRAVEL	TEXT NOT NULL,
                      COLOUR	TEXT NOT NULL,
                      RITU	TEXT NOT NULL,
                      FLOWER	TEXT NOT NULL,
                      MUSIC	TEXT NOT NULL,
                      ACTIVITY TEXT NOT NULL
                  )''')
  ngs = request.form.get("ngs")
  name = request.form.get("name")
  food = request.form.get("food")
  travel = request.form.get("travel")
  colour = request.form.get("colour")
  ritu = request.form.get("ritu")
  flower = request.form.get("flower")
  music = request.form.get("music")
  activity = request.form.get("activity")
  if not ngs or not name or not food or not travel or not colour or not ritu or not flower or not music or not activity:
    return jsonify({'error': 'MIssing Data'}), 400
  # User Image
  if 'image' not in request.files:
        return "No image part", 400

  file = request.files['image']
  if file.filename == '':
    return "No selected file", 400

  if file:
    unique_filename = f"{ngs}Image.jpg"
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], unique_filename)
    file.save(filepath)
    
  # User bag image
  if 'bgimage' not in request.files:
        return "No image part", 400

  file = request.files['bgimage']
  if file.filename == '':
    return "No bg selected file", 400

  if file:
    unique_filename = f"{ngs}Image-removebg-preview.png"
    filepath = os.path.join(app.config['UPLOAD_FOLDER'],"MaskedPotraits", unique_filename)
    file.save(filepath)
    
  try:
    cursor.execute("INSERT INTO employee (NGS, NAME,FOOD,TRAVEL,COLOUR,RITU,FLOWER,MUSIC,ACTIVITY ) VALUES (?,?,?,?,?,?,?,?,?)", (ngs,name,food,travel,colour,ritu,flower,music,activity))
    conn.commit()
    conn.close()
  except:
    return "Error while create user, check user info"
  return "User CReated"
  
@app.route('/del-user', methods=['POST'])
def del_user():
    conn = sqlite3.connect('mydatabase.db')
    cursor = conn.cursor()
    data = request.json
    ngs = data.get('ngs')
    try:
      cursor.execute(f"DELETE FROM employee WHERE NGS = {ngs};")
      conn.commit()
      conn.close()
    except:
      return "User Not Found"
    return "User deleted"


@app.route('/gen-image', methods=['POST'])
def gen_image():
    conn = sqlite3.connect('mydatabase.db')
    data = request.json

    # Extract ngin, even, and images from the JSON payload
    ngin = data.get('ngin')
    even = data.get('even')
    numimages = data.get('numimages')

    if not ngin or not even or not numimages:
        return jsonify({'error': 'Missing ngin, even, or images in the request'}), 400

    # For simplicity, we'll just return the first image in the list
    df = pd.read_sql_query("SELECT * from employee", conn)
    get_generated_card(ngin,even,numimages,df)
    conn.close()
    return "card Generated"

@app.route('/get-image',methods=['POST'])
def get_image():
    data = request.json
    imagenumber = data.get('inum')
    
    image_dir = "/home/dcsadmin/Documents/PersonalisedGreeting/GeneratedImages/"
    image_path = os.path.join(image_dir, imagenumber)

    if not os.path.exists(image_path):
        return jsonify({'error': 'Image not found'}), 404

    return send_file(image_path, mimetype='image/jpeg')


if __name__ == '__main__':
    app.run(debug=True,host="0.0.0.0")
