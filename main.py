from flask import Flask, render_template
import requests
import xml.etree.ElementTree as ET
from datetime import datetime
from database import init_db, get_papers, save_papers, needs_update

app = Flask(__name__)
init_db()

def fetch_arxiv_papers():
    base_url = 'http://export.arxiv.org/api/query?'
    query = 'cat:cs.CR'
    max_results = 10

    search_url = f'{base_url}search_query={query}&max_results={max_results}'
    response = requests.get(search_url)
    
    papers = []
    if response.status_code == 200:
        root = ET.fromstring(response.content)
        for entry in root.findall('{http://www.w3.org/2005/Atom}entry'):
            paper = (
                entry.find('{http://www.w3.org/2005/Atom}title').text,
                ', '.join([author.find('{http://www.w3.org/2005/Atom}name').text for author in entry.findall('{http://www.w3.org/2005/Atom}author')]),
                entry.find('{http://www.w3.org/2005/Atom}summary').text,
                entry.find('{http://www.w3.org/2005/Atom}id').text,
                datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            )
            papers.append(paper)
    return papers

@app.route('/')
def home():
    if needs_update():
        papers = fetch_arxiv_papers()
        save_papers(papers)
    else:
        papers = get_papers()
        
    papers = [{'title': p[1], 'authors': p[2], 'summary': p[3], 'link': p[4]} for p in papers]
    return render_template('index.html', papers=papers)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
