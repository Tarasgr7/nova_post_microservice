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

def send_message(shipment_data):
    connection = get_connection()
    channel = connection.channel()
    
    channel.exchange_declare(exchange='shipment_exchange', exchange_type='topic')
    channel.basic_publish(
        exchange='shipment_exchange',
        routing_key='shipment.create',
        body=json.dumps(shipment_data)
    )
    connection.close()

def reverse_message(shipment_data):
    connection = get_connection()
    channel = connection.channel()
    
    channel.exchange_declare(exchange='shipment_exchange', exchange_type='topic')
    channel.basic_publish(
        exchange='shipment_exchange',
        routing_key='shipment.update',
        body=json.dumps(shipment_data)
    )
    connection.close()

# def start_worker():
#     connection = get_connection()
#     channel = connection.channel()
#     channel.queue_declare(queue=REQUEST_QUEUE)
#     channel.queue_declare(queue=RESPONSE_QUEUE)

#     def on_request(ch, method, props, body):
#         request = json.loads(body)
#         text = request.get("text", "")
#         length = len(text)

#         response = json.dumps({"length": length})
        
#         ch.basic_publish(
#             exchange='',
#             routing_key=props.reply_to,
#             properties=pika.BasicProperties(correlation_id=props.correlation_id),
#             body=response
#         )
#         ch.basic_ack(delivery_tag=method.delivery_tag)

#     channel.basic_consume(queue=REQUEST_QUEUE, on_message_callback=on_request)
#     channel.start_consuming()
