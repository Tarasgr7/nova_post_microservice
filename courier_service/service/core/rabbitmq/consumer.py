import pika
import json
import time
from db.models.courier_models import Courier
from db.dependencies import get_db
from sqlalchemy.orm import Session
RABBITMQ_HOST = "127.0.0.1"
RABBITMQ_USER = "admin"
RABBITMQ_PASS = "admin"

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


def start_consumer():
  db: Session = next(get_db())
  def create_courier(ch, method, properties, body):
      data = json.loads(body)
      courier = Courier(
        user_id=data['user_id'],
        vehicle=data.get('vehicle', None),
        branch_from=data['branch_from'],
        active=data.get('active',True)
      )
      # Перевірка відділень
      try:
        # Додаємо об'єкт в сесію
        db.add(courier)
        # Комітимо зміни, щоб зберегти об'єкт у БД
        db.commit()
        # Оновлюємо об'єкт, щоб отримати згенерований id
        db.refresh(courier)
        
        print(f"Courier saved with ID: {courier.id}")
      except Exception as e:
        db.rollback()
        print(f"Error saving courier: {e}")
      finally:
        db.close()


  connection = get_connection()
  channel = connection.channel()
  channel.exchange_declare(exchange='auth_exchange', exchange_type='topic')
  channel.queue_declare(queue='courier.create')
  channel.queue_bind(exchange='auth_exchange', queue='courier.create', routing_key='courier.create')
  channel.basic_consume(queue='courier.create', on_message_callback=create_courier, auto_ack=True)

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