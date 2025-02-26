import pika
import json
import time
from service.controllers.v1.utils.shipment_utils import change_shipment_status
from sqlalchemy.orm import Session
RABBITMQ_HOST = "rabbitmq"
RABBITMQ_USER = "admin"
RABBITMQ_PASS = "admin"

def get_connection(retries=100, delay=5):
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


def start_consumer():
  def change_shipment_statuses(ch, method, properties, body):
      data=json.loads(body)
      change_shipment_status(data.get('shipment_id'),data.get('status'))
      print(f"Змінено статус замовлення {data.get('shipment_id')} на {data.get('status')}")
      
  connection = get_connection()
  channel = connection.channel()
  #Декларування каналу
  channel.exchange_declare(exchange='courier_exchange', exchange_type='topic')
  # Декларування черги
  channel.queue_declare(queue='shipment.change_status')
  channel.queue_bind(exchange='courier_exchange', queue='shipment.change_status', routing_key='shipment.change_status')
  channel.basic_consume(queue='shipment.change_status', on_message_callback=change_shipment_statuses, auto_ack=True)
  # Запуск прослуховування черг
  channel.start_consuming()
