import requests
from minsearch import Index

def load_faq_data():
    docs_url = 'https://datatalks.club/faq/json/courses.json'
    response = requests.get(docs_url)
    courses_raw = response.json()
    
    documents = []
    url_prefix = 'https://datatalks.club/faq'
    for course in courses_raw:
        course_url = f"{url_prefix}{course["path"]}"
        course_response = response.get(course_url)
        document = course_response.json()
        documents.extend(document)
        
    
    return documents


def build_index(documents):
    index = Index(
        text_fields = ['section','question','answer'],
        keyword_fields = ['course']
    )
    index.fit(documents)
    return index


    
    
        