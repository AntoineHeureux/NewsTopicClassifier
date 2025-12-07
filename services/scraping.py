from newspaper import Article
import re

def process_article(article: str, nb_phrase = 5) -> str:
    article = re.sub(r'[\n\t\r]+', ' ', article)
    article = re.sub(r' +', ' ', article)
    article = re.sub(r"\"", "'", article)
    article = article.strip()
    article = re.split(r'(?<=[.!?]) +', article)
    article = [phrase for phrase in article if len(phrase)]
    return ' '.join(article[:nb_phrase])

def get_article(url: str) -> str:
    try:
        article = Article(url)
        article.download()
        article.parse()
        if article.title:
            article_title = article.title
            article = article_title + '. ' + article.text
        else:   
            article = article.text
        return process_article(article), article_title
    except:
        return None