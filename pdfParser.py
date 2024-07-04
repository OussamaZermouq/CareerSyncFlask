from pydparser import ResumeParser
import spacy

nlp = spacy.load('en_core_web_sm')

def ExtractFromPdf(file:str):
    data = ResumeParser(file).get_extracted_data()
    return data['skills']
