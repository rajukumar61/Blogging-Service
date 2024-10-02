import pika
import json
from elasticsearch import Elasticsearch

# Connect to Elasticsearch
es = Elasticsearch(['http://elasticsearch:9200'])


def callback(ch, method, properties, body):
    blog_data = json.loads(body)

    # Index blog entry in Elasticsearch
    es.index(index='blogs', body={
        'blog_title': blog_data['blog_title'],
        'blog_text': blog_data['blog_text'],
        'user_id': blog_data['user_id']
    })
    ch.basic_ack(delivery_tag=method.delivery_tag)


# RabbitMQ connection setup
def consume_queue():
    connection = pika.BlockingConnection(pika.ConnectionParameters(host='rabbitmq'))
    channel = connection.channel()
    channel.queue_declare(queue='blog_queue', durable=True)

    channel.basic_consume(queue='blog_queue', on_message_callback=callback)
    print('Waiting for messages...')
    channel.start_consuming()


if __name__ == '__main__':
    consume_queue()
