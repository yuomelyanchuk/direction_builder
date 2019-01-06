import pika

def create_queues(*args):
    connection = pika.BlockingConnection(pika.ConnectionParameters(
        host='localhost'))
    channel = connection.channel()

    for q_names in args:
        channel.queue_declare(queue=q_names)

    connection.close()


def delete_queues(*args):
    connection = pika.BlockingConnection(pika.ConnectionParameters(
        host='localhost'))
    channel = connection.channel()

    for q_names in args:
        channel.queue_delete(queue=q_names)

    connection.close()
