from flask import Flask, render_template, jsonify
from scholarly import scholarly

app = Flask(__name__)

articles = []
SEARCH_KEYWORD = "machine learning"  # Set your default keyword here

def search_google_scholar():
    search_query = scholarly.search_pubs(SEARCH_KEYWORD)
    articles.clear()
    
    while len(articles) < 5:
        try:
            pub = next(search_query)
            if len(articles) == 0 or (len(articles) > 0 and pub['pub_url'] != articles[-1]['URL']):
                data = {
                    'Title': pub['bib']['title'],
                    'Citation': pub.get('num_citations', 'N/A'),
                    'URL': pub.get('pub_url', 'N/A')
                }
                articles.append(data)
        except StopIteration:
            break

@app.route('/')
def index():
    search_google_scholar()
    return render_template('index.html', articles=articles)

if __name__ == '__main__':
    app.run(debug=True)