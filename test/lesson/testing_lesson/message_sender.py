import pika

connection = pika.BlockingConnection(pika.ConnectionParameters(
    host='localhost'))
channel = connection.channel()


def send_message(q_name, message):
    channel.basic_publish(exchange='',
                          routing_key=q_name,
                          body=message)
