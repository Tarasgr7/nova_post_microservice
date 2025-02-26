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

def create_shipment_in_service(shipment):
    connection = get_connection()
    channel = connection.channel()
    shipment_data = shipment.to_dict()
    
    channel.exchange_declare(exchange='shipment_exchange', exchange_type='topic')
    channel.basic_publish(
        exchange='shipment_exchange',
        routing_key='shipment.create',
        body=json.dumps(shipment_data)
    )
    connection.close()




def delete_shipment_in_service(shipment):
    connection = get_connection()
    channel = connection.channel()
    shipment_data = shipment.to_dict()
    
    channel.exchange_declare(exchange='shipment_exchange', exchange_type='topic')
    channel.basic_publish(
        exchange='shipment_exchange',
        routing_key='shipment.delete',
        body=json.dumps(shipment_data)
    )
    connection.close()