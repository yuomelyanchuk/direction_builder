import pika
import json


class GenericWorker:
    '''Generic worker class'''

    def __init__(self):
        with open('../init.json', 'r') as fp:
            self.init = json.load(fp)

        self.worker_name = self.init.get('name', '')
        self.yes_section = self.init.get('yes_section', '')
        self.no_section = self.init.get('no_section', '')
        self.always_section = self.init.get('always_section', '')
        self.listen_queue = self.init.get('listen_queue', '')
        self.body = {}
        self.task_result = None
        self.parameters = pika.ConnectionParameters(
            host=self.init.get('host', 'localhost'), port=self.init.get('port', '5672'))
        self.connection = pika.SelectConnection(parameters=self.parameters,
                                                on_open_callback=self.on_open)

    def callback(self, channel, method, properties, body):
        self.body.update(json.loads(body))
        self.perform_task()
        if 'error' not in self.task_result:
            self.task_result_processor()

        print(body)
        channel.basic_ack(delivery_tag=method.delivery_tag)

    def on_open(self, connection):
        connection.channel(self.on_channel_open)

    def on_channel_open(self, channel):
        channel.basic_qos(prefetch_count=1)
        for name in self.listen_queue:
            channel.basic_consume(self.callback, queue=name)

    def run_listner(self):
        try:
            self.connection.ioloop.start()
        except KeyboardInterrupt:
            self.connection.close()

    def send_message_to_worker(self, to_workers):
        connection = pika.BlockingConnection(parameters=self.parameters)
        channel = connection.channel()
        for to_worker in to_workers:
            channel.basic_publish(exchange='',
                                  routing_key=str.format('{0}_{1}', self.worker_name, to_worker),
                                  body=json.dumps(self.body),
                                  properties=pika.BasicProperties(
                                      delivery_mode=2,
                                  )
                                  )
        connection.close()

    '''execute works'''

    def perform_task(self):
        try:

            import random
            self.task_result = random.uniform(0, 1) > 0.7

        except Exception as e:
            self.task_result = 'error'
            self.body = {self.worker_name: e}
            self.send_message_to_worker(['errors'])

    def task_result_processor(self):
        if self.yes_section and self.task_result:
            self.body['output_message'] = self.body['output_message'].update(
                {self.worker_name: self.yes_section['message']})
            self.send_message_to_worker(self.yes_section['send_message'])

        if self.no_section and not self.task_result:
            self.body['output_message'] = self.body['output_message'].update(
                {self.worker_name: self.no_section['message']})
            self.send_message_to_worker(self.no_section['send_message'])

        if self.always_section:
            self.body['output_message'] = self.body['output_message'].update(
                {self.worker_name: self.always_section['message']})
            self.send_message_to_worker(self.always_section['send_message'])


if __name__ == "__main__":
    # import utils.queue_managments as qm
    qq = 'hello'
    w = GenericWorker()
    w.run_listner()
    # qm.create_queues(qq)
    # qm.send_message(qq, 'hello world')
