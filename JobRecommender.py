import csv
import re
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
from pdfParser import ExtractFromPdf

class Recommender:
    #RUN ONCE
    # nltk.download('punkt')
    # nltk.download('stopwords')
    # nltk.download('wordnet')
    def __init__(self, cvFile, skills):
        self.cvFile = cvFile
        self.skills = skills

    def Recommend(self):
        def preprocess_text(text):
            text = re.sub(r'\W', ' ', text)
            text = text.lower()
            tokens = word_tokenize(text)
            tokens = [word for word in tokens if word not in stopwords.words('english')]
            lemmatizer = WordNetLemmatizer()
            tokens = [lemmatizer.lemmatize(word) for word in tokens]
            return ' '.join(tokens)

        def load_job_descriptions_from_csv(file_path):
            job_descriptions = {}
            with open(file_path, newline='') as csvfile:
                reader = csv.DictReader(csvfile)
                for row in reader:
                    job_title = row['Job Title']
                    skills = row['skills']
                    job_descriptions[job_title] = skills
            return job_descriptions

        file_path = 'job-descriptions-final.csv'
        job_descriptions = load_job_descriptions_from_csv(file_path)

        if isinstance(job_descriptions, list):
            raise ValueError("Expected job descriptions to be a dictionary, got a list.")

        cleaned_job_descriptions = {job: preprocess_text(desc) for job, desc in job_descriptions.items()}

        resume_text = ' '.join(str(e) for e in ExtractFromPdf(self.cvFile))

        clean_resume = preprocess_text(resume_text)

        # Add the other inputs here like the skills.
        all_texts = [clean_resume] + list(cleaned_job_descriptions.values())
        vectorizer = TfidfVectorizer()
        tfidf_matrix = vectorizer.fit_transform(all_texts)

        resume_vector = tfidf_matrix[0]
        job_vectors = tfidf_matrix[1:]

        similarity_scores = cosine_similarity(resume_vector, job_vectors).flatten()

        N = 10
        top_n_indices = np.argsort(similarity_scores)[::-1][:N]
        recommended_jobs = [(list(cleaned_job_descriptions.keys())[i], job_descriptions[list(cleaned_job_descriptions.keys())[i]]) for i in top_n_indices]
        
        return recommended_jobs

    
# rec = Recommender('./cvfiles/cviXmZaoakjRMGbHiDBisuZnIZdsJFhUuz.pdf',['machine learning'])
# out = rec.Recommend()
# print(out)