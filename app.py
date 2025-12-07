import time
from services.summary import get_summary
from services.scraping import get_article
from services.topic import get_topic
from flask import Flask, request, jsonify
from flask_cors import CORS
from backend.create_db import db, ArticleResult

app = Flask(__name__)
CORS(app)

#config DB
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///articles.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

@app.route('/analyze', methods=['POST'])
def analyze():
    data = request.json
    url = data.get('url')
    if not url:
        return jsonify({'error': 'No URL provided'}), 400

    result = {}
    
    # Profiling scraping
    t1 = time.time()
    article_text, article_title = get_article(url)
    result['article_text'] = article_text
    result['article_title'] = article_title
    result['scraping_time'] = time.time() - t1

    
    if not article_text:
        return jsonify({'error': 'Failed to retrieve article'}), 500
    result['article_text'] = article_text

    # Profiling summary
    t2 = time.time()
    summary = get_summary(article_text)
    result['summary_time'] = time.time() - t2
    result['summary'] = summary

    # Profiling topic
    t3 = time.time()
    topic = get_topic(summary)
    result['topic_time'] = time.time() - t3
    result['topic'] = topic

    # Profiling total time
    result['total_time'] = result['scraping_time'] + result['summary_time'] + result['topic_time']

    print("scraping time: ", result['scraping_time'],
          "summary time: ", result['summary_time'],
          "topic time: ", result['topic_time'])

    # Save to DB
    record = ArticleResult(
        url=url,
        title=article_title,
        summary=summary,
        topic=topic
    )
    with app.app_context():
        db.session.add(record)
        db.session.commit()
        result['db_id'] = record.id
    
    return jsonify(result), 200

# get history
@app.route('/history', methods=['GET'])
def get_history():
    """Retourne l'historique des analyses (20 dernières)"""
    with app.app_context():
        records = ArticleResult.query.order_by(ArticleResult.created_at.desc()).limit(20).all()
        result = [
            {
                'id': r.id,
                'url': r.url,
                'summary': r.summary,
                'title': r.title,
                'topic': r.topic,
                'created_at': r.created_at.isoformat()
            }
            for r in records
        ]
        return jsonify(result), 200

#delete elemtents form history
@app.route('/delete/<int:item_id>', methods=['DELETE'])
def delete_item(item_id):
    """Supprime un élément de l'historique"""
    try:
        with app.app_context():
            record = ArticleResult.query.get(item_id)
            if not record:
                return jsonify({'error': 'Élément non trouvé'}), 404
            
            db.session.delete(record)
            db.session.commit()
            return jsonify({'message': 'Élément supprimé'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)