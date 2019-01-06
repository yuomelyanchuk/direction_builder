from flask import Flask, jsonify, request
import json
import pika

with open('../init.json', 'r') as fp:
    init = json.load(fp)

parameters = pika.ConnectionParameters(
    host=init.get('host', 'localhost'), port=init.get('port', '5672'))


def send_message(message):
    connection = pika.BlockingConnection(parameters=parameters )
    channel = connection.channel()
    channel.basic_publish(exchange='',
                          routing_key='input',
                          body=json.dumps(message.update({'output_message': ''})))
    connection.close()


app = Flask(__name__)


@app.route('/input/v1/data', methods=['POST'])
def create_input():
    if not request.json:
        return 'not json'

    data = {}
    data.update({'input_data': request.json})
    send_message(data)
    return 'ok'



if __name__ == '__main__':
    app.run(debug=True)
