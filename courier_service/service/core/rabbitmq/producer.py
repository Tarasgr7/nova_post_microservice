import pika
import json
import time

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

def change_shipment_status_in_service(parsel):
    connection = get_connection()
    channel = connection.channel()
    
    channel.exchange_declare(exchange='courier_exchange', exchange_type='topic')
    channel.basic_publish(
        exchange='courier_exchange',
        routing_key='shipment.change_status',
        body = json.dumps(parsel)
    )
    connection.close()