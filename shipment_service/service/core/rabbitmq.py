import pika
import json
import time
import uuid

RABBITMQ_HOST = "127.0.0.1"
RABBITMQ_USER = "admin"
RABBITMQ_PASS = "admin"
REQUEST_QUEUE = "request_queue"
RESPONSE_QUEUE = "response_queue"

def get_connection(retries=5, delay=5):
    credentials = pika.PlainCredentials(RABBITMQ_USER, RABBITMQ_PASS)
    for i in range(retries):
        try:
            connection = pika.BlockingConnection(
                pika.ConnectionParameters(host=RABBITMQ_HOST, credentials=credentials)
            )
            return connection
        except pika.exceptions.AMQPConnectionError:
            print(f"RabbitMQ недоступний, спроба {i + 1}/{retries}... Чекаємо {delay} секунд.")
            time.sleep(delay)
    raise Exception("Не вдалося підключитися до RabbitMQ.")


def start_worker():
  def callback(ch, method, properties, body):
      data = json.loads(body)
      # Перевірка відділень
      print(data)
  def reverse(ch, method, properties, body):
      data = json.loads(body)
      # Перевірка відділень
      print(data)

  connection = get_connection()
  channel = connection.channel()
  channel.exchange_declare(exchange='shipment_exchange', exchange_type='topic')
  channel.queue_declare(queue='shipment.update')
  channel.queue_declare(queue='shipment.create')
  channel.queue_bind(exchange='shipment_exchange', queue='shipment.update', routing_key='shipment.update')
  channel.queue_bind(exchange='shipment_exchange', queue='shipment.create', routing_key='shipment.create')
  channel.basic_consume(queue='shipment.update', on_message_callback=reverse, auto_ack=True)
  channel.basic_consume(queue='shipment.create', on_message_callback=callback, auto_ack=True)
  channel.start_consuming()


# def start_worker():
#     connection = get_connection()
#     channel = connection.channel()
#     channel.queue_declare(queue=REQUEST_QUEUE)
#     channel.queue_declare(queue=RESPONSE_QUEUE)

#     def on_request(ch, method, props, body):
#         request = json.loads(body)
#         print(request)

#     channel.basic_consume(queue=REQUEST_QUEUE, on_message_callback=on_request)
#     channel.start_consuming()