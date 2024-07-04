from flask import Flask, jsonify
from flask import request
import pandas as pd
import random
from nltk.corpus import stopwords
import nltk
import requests
from JobRecommender import Recommender
import string
from flask_cors import CORS

# RUN ONCE
# nltk.download("stopwords")
# stop = set(stopwords.words("english"))

app = Flask(__name__)
CORS(app, resources={r"*": {"origins": "*"}})

skills_global = []
def load_skills():
    return pd.read_csv("job-descriptions-final.csv")

def get_random_skill(skills_df):
    skill_row = skills_df.iloc[random.randint(0, skills_df.shape[0] - 1), 2]
    return random.choice(skill_row.split())

def random_string_generator():
    return ''.join(random.choice(string.ascii_letters) for x in range(32))

def downloadCvFile(url:str):
    response = requests.get(url)
    #to avoid dupes
    filename=random_string_generator()
    if response.status_code == 200:
        with open(f"./cvfiles/CV_{filename}.pdf", "wb") as file:
            file.write(response.content)
            return f"CV_{filename}.pdf"

#fetch the user using his token from the Spring backend
@app.route("/recommend", methods=['GET'])
def recommend():
    token = request.headers.get('Authorization')
    if token is None:
        return jsonify({
            "code":"403",
            "message": "No token provided"
        })
    req = requests.get('http://localhost:8080/api/v1/user',
                           headers={
                               "Authorization": token,
                               "Content-Type": "application/json"
                           })
    user = req.json()
    #download the file and save it locally
    recommender = Recommender(f"./cvfiles/{downloadCvFile(user['cvFile'])}", user['skills'])
    recommendations = recommender.Recommend()
    return jsonify({
        'recommendations':recommendations
    })

#Generate random skills from the csv for the front end
@app.route("/skills")
def skills():
    skills_global.clear()
    skills_df = load_skills()
    for i in range(20):
        skill = get_random_skill(skills_df)
        skills_global.append(skill)
    return jsonify({'skills': skills_global})

if __name__ == "__main__":
    app.run(debug=True)
