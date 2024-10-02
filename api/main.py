from flask import Flask, request, jsonify
import pika
import json

app = Flask(__name__)

# RabbitMQ connection setup
def get_rabbitmq_channel():
    connection = pika.BlockingConnection(pika.ConnectionParameters(host='rabbitmq'))
    return connection.channel()

@app.route('/submit', methods=['POST'])
def submit_blog():
    data = request.get_json()
    blog_title = data.get('blog_title')
    blog_text = data.get('blog_text')
    user_id = data.get('user_id')

    if not all([blog_title, blog_text, user_id]):
        return jsonify({"error": "Missing fields"}), 400

    # Publish message to RabbitMQ
    channel = get_rabbitmq_channel()
    channel.queue_declare(queue='blog_queue', durable=True)

    blog_data = {
        'blog_title': blog_title,
        'blog_text': blog_text,
        'user_id': user_id
    }
    channel.basic_publish(
        exchange='',
        routing_key='blog_queue',
        body=json.dumps(blog_data),
        properties=pika.BasicProperties(delivery_mode=2)
    )

    return jsonify({"message": "Blog submitted successfully!"}), 200

@app.route('/search', methods=['GET'])
def search_blog():
    query = request.args.get('query')
    if not query:
        return jsonify({"error": "Query param is missing"}), 400

    es = Elasticsearch(['http://elasticsearch:9200'])
    response = es.search(index='blogs', body={
        'query': {
            'multi_match': {
                'query': query,
                'fields': ['blog_title', 'blog_text']
            }
        }
    })

    return jsonify(response['hits']['hits']), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
