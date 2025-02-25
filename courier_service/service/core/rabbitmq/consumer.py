import pika
import json
import time
from db.models.courier_models import Courier
from db.models.parcel_model import Parcel
from db.dependencies import get_db,logger
from service.controllers.v1.utils.parsel_utils import create_parcel

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


def start_consumer_for_auth():
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
  def update_courier(ch, method, properties, body):
    data=json.loads(body)
    courier_data=db.query(Courier).filter(Courier.user_id==data['user_id']).first()
    if courier_data:
      if data.get('vehicle'):
        courier_data.vehicle=data.get('vehicle')
      if data.get('branch_from'):
        courier_data.branch_from=data.get('branch_from')
      if data.get('active'):
        courier_data.active=data.get('active')
    db.commit()
    db.refresh(courier_data)

  def delete_courier(ch, method, properties, body):
      data=json.loads(body)
      courier_data=db.query(Courier).filter(Courier.user_id==data['user_id']).first()
      print(courier_data)
      if courier_data:
        db.delete(courier_data)
        db.commit()
  def create_shipment(ch, method, properties, body):
     data = json.loads(body)
     print(f"Shipment created: {data}")
     create_parcel(data.get('branch_from'), data.get('branch_to'), data.get('id'),db)
     logger.info(f"Created parcel: {data}")
  def delete_shipment(ch, method, properties, body):
      data=json.loads(body)
      shipment_data=db.query(Parcel).filter(Parcel.shipment_id==data['id']).first()
      if shipment_data:
        print(f"Delete{shipment_data}")
        db.delete(shipment_data)
        db.commit()

  connection = get_connection()
  channel = connection.channel()
  channel.exchange_declare(exchange='auth_exchange', exchange_type='topic')
  #Connect to Courier.create queue
  channel.queue_declare(queue='courier.create')
  channel.queue_bind(exchange='auth_exchange', queue='courier.create', routing_key='courier.create')
  channel.basic_consume(queue='courier.create', on_message_callback=create_courier, auto_ack=True)
  #Connect to Courier.update queue
  channel.queue_declare(queue='courier.update')
  channel.queue_bind(exchange='auth_exchange', queue='courier.update', routing_key='courier.update')
  channel.basic_consume(queue='courier.update', on_message_callback=update_courier, auto_ack=True)
  #Connect to Courier.delete queue
  channel.queue_declare(queue='courier.delete')
  channel.queue_bind(exchange='auth_exchange', queue='courier.delete', routing_key='courier.delete')
  channel.basic_consume(queue='courier.delete', on_message_callback=delete_courier, auto_ack=True)
  channel.exchange_declare(exchange='shipment_exchange', exchange_type='topic')
  #Connect to Shipment.create queue
  channel.queue_declare(queue='shipment.create')
  channel.queue_bind(exchange='shipment_exchange', queue='shipment.create', routing_key='shipment.create')
  channel.basic_consume(queue='shipment.create', on_message_callback=create_shipment, auto_ack=True)
  #Connect to Shipment.delete queue
  channel.queue_declare(queue='shipment.delete')
  channel.queue_bind(exchange='shipment_exchange', queue='shipment.delete', routing_key='shipment.delete')
  channel.basic_consume(queue='shipment.delete', on_message_callback=delete_shipment, auto_ack=True)

  channel.start_consuming()
