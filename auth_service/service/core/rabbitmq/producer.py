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

def create_courier_in_service(courier):
    connection = get_connection()
    channel = connection.channel()
    courier_data = courier.to_dict()
    
    channel.exchange_declare(exchange='auth_exchange', exchange_type='topic')
    channel.basic_publish(
        exchange='auth_exchange',
        routing_key='courier.create',
        body=json.dumps(courier_data)
    )
    connection.close()

def update_courier_in_service(courier):
    connection = get_connection()
    channel = connection.channel()
    courier_data = courier.to_dict()
    
    channel.exchange_declare(exchange='auth_exchange', exchange_type='topic')
    channel.basic_publish(
        exchange='auth_exchange',
        routing_key='courier.update',
        body=json.dumps(courier_data)
    )
    connection.close()

def delete_courier_in_service(courier):
    connection = get_connection()
    channel = connection.channel()
    courier_data = courier.to_dict()
    
    channel.exchange_declare(exchange='auth_exchange', exchange_type='topic')
    channel.basic_publish(
        exchange='auth_exchange',
        routing_key='courier.delete',
        body=json.dumps(courier_data)
    )
    connection.close()
