from pymongo import MongoClient
db = MongoClient().shopjustice
import pika
connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
channel = connection.channel()
channel.queue_declare(queue='shopjustice')
for item in db.product_links.find():
    url = item.get('url')
    channel.basic_publish(exchange='',routing_key='shopjustice',body=str(url))
connection.close()










