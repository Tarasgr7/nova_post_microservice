# import pika
# import json

# def publish_shipment_created(shipment_data):
#     connection = pika.BlockingConnection(pika.ConnectionParameters('rabbitmq'))
#     channel = connection.channel()
#     channel.exchange_declare(exchange='shipment_exchange', exchange_type='topic')
#     channel.basic_publish(
#         exchange='shipment_exchange',
#         routing_key='shipment.created',
#         body=json.dumps(shipment_data)
#     )
#     connection.close()
# # -----------------------------------------
# def callback(ch, method, properties, body):
#     data = json.loads(body)
#     print("Received branch validation:", data)

# connection = pika.BlockingConnection(pika.ConnectionParameters('rabbitmq'))
# channel = connection.channel()
# channel.exchange_declare(exchange='branch_exchange', exchange_type='topic')
# channel.queue_declare(queue='branch.validate')
# channel.queue_bind(exchange='branch_exchange', queue='branch.validate', routing_key='branch.validate')
# channel.basic_consume(queue='branch.validate', on_message_callback=callback, auto_ack=True)
# channel.start_consuming()
# # -----------------------------------------
# # -----------------------------------------
# # -----------------------------------------
# def callback(ch, method, properties, body):
#     data = json.loads(body)
#     # Перевірка відділень
#     validation_result = validate_branch(data['branch_from'], data['branch_to'])
#     publish_branch_validation(validation_result)

# connection = pika.BlockingConnection(pika.ConnectionParameters('rabbitmq'))
# channel = connection.channel()
# channel.exchange_declare(exchange='shipment_exchange', exchange_type='topic')
# channel.queue_declare(queue='shipment.created')
# channel.queue_bind(exchange='shipment_exchange', queue='shipment.created', routing_key='shipment.created')
# channel.basic_consume(queue='shipment.created', on_message_callback=callback, auto_ack=True)
# channel.start_consuming()
# # -----------------------------------------
# def publish_branch_validation(validation_data):
#     connection = pika.BlockingConnection(pika.ConnectionParameters('rabbitmq'))
#     channel = connection.channel()
#     channel.exchange_declare(exchange='branch_exchange', exchange_type='topic')
#     channel.basic_publish(
#         exchange='branch_exchange',
#         routing_key='branch.validate',
#         body=json.dumps(validation_data)
#     )
#     connection.close()

