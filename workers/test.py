import utils.queue_managments as qm
from workers.GenericWorker import GenericWorker
import pika

if __name__ == "__main__":
    qq = 'hello'

    qm.create_queues(qq)
    worker = GenericWorker()
    worker.run_listner()
    qm.send_message(qq, 'hello world')
