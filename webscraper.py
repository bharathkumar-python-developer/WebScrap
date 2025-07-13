#C:\Users\91984\AppData\Local\Programs\Python\Python313\Scripts
#https://jsonplaceholder.typicode.com/users
#https://jsonplaceholder.typicode.com/posts
#https://jsonplaceholder.typicode.com/comments
import pandas as pd
import sqlite3
import matplotlib
import json
import requests

users_data = requests.get("https://jsonplaceholder.typicode.com/users").json()

post_data = requests.get("https://jsonplaceholder.typicode.com/posts").json()

comment_data = requests.get("https://jsonplaceholder.typicode.com/comments").json()

conn = sqlite3.connect("webscrap.db")
cursor = conn.cursor()

cursor.execute('''
    CREATE TABLE IF NOT EXISTS users(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        username TEXT,
        email TEXT,
        street TEXT,
        suite TEXT,
        city TEXT,
        zipcode TEXT,
        geo_lat TEXT,
        geo_lon TEXT, 
        phone TEXT,
        website TEXT,
        company_name TEXT,
        company_catchPhrase TEXT,
        company_bs TEXT
    )
''')
cursor.execute('''
    CREATE TABLE IF NOT EXISTS posts(
        userId INTEGER,
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT,
        body TEXT
)''')

cursor.execute('''
    CREATE TABLE IF NOT EXISTS comments(
        postId INTEGER,
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        email TEXT,
        body TEXT
)''')
for data in users_data:
    try:
        cursor.execute('''
            INSERT OR IGNORE INTO users (
                id, name, username, email,
                street, suite, city, zipcode,
                geo_lat, geo_lon,
                phone, website,
                company_name, company_catchPhrase, company_bs
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''', (
            data["id"],
            data["name"],
            data["username"],
            data["email"],
            data["address"]["street"],
            data["address"]["suite"],
            data["address"]["city"],
            data["address"]["zipcode"],
            data["address"]["geo"]["lat"],
            data["address"]["geo"]["lng"],
            data["phone"],
            data["website"],
            data["company"]["name"],
            data["company"]["catchPhrase"],
            data["company"]["bs"]
        ))
    except KeyError as e:
        print(f"Missing key: {e} in data: {data.get('id', 'Unknown')}")

        
for pos in post_data:
    try:
        cursor.execute('''
            INSERT OR IGNORE INTO posts (userId, id, title, body) VALUES (?, ?, ?, ?)''', (pos["userId"], 
    pos["id"], 
    pos["title"], 
    pos["body"]))
    except KeyError as e:
        print(f"Missing key: {e} in pos: {pos.get('id', 'Unknown')}")
        
for comments in comment_data:
    try:
        cursor.execute('''
            INSERT OR IGNORE INTO comments (postId, id, name, email, body)
        VALUES (?, ?, ?, ?, ?)
    ''', (comments["postId"], 
    comments["id"], 
    comments["name"], 
    comments["email"], 
    comments["body"]))
    except KeyError as e:
        print(f"Missing key: {e} in comments: {comments.get('id', 'Unknown')}")

conn.commit()
conn.close()
print("Data inserted successfully into SQLite!")