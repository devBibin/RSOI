from statsapp.models import RequestInfo
import json
from statsapp.serializers import RequestInfoSerializer
import pika
from django.db.models import Count
from datetime import datetime, timedelta

rabbitConnection = None
rabbit_channel = None

import threading
import statsapp.consumer as c


def connect():
    try:
        print('connecting to rabbit')

        global rabbitConnection
        global rabbit_channel

        rabbitConnection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost', heartbeat=0))
        rabbit_channel = rabbitConnection.channel()
        rabbit_channel.queue_declare('responses')
        rabbit_channel.exchange_declare('message', 'topic')
        rabbit_channel.queue_bind('responses', 'message', 'responses')
        rabbit_channel.confirm_delivery()

    except Exception as E:
        print(E)


connect()


def get_responce_log(message, valid=True, errors=None, req_status=200, data_erorrs={}):
    status = None
    if valid:
        status = 'processed'
    else:
        status = 'failed'
    payload = json.dumps({'guid': message['guid'], 'status': status, 'errors': json.dumps(errors), 'code': req_status,
                          'data_errors': json.dumps(data_erorrs)})
    try:
        status = rabbit_channel.basic_publish(exchange='message', routing_key='responses', body=payload, mandatory=True,
                                              immediate=False)
        print(status)
    except Exception as E:
        print(E)
        connect()
        rabbit_channel.basic_publish(exchange='message', routing_key='responses', body=payload, mandatory=True,
                                     immediate=False)


# Create your views here.

def save_request_info(data):
    data['timestamp'] = datetime.strptime(data['timestamp'], '%Y-%m-%d %H:%M:%S.%f')
    if RequestInfo.objects.filter(guid=data['guid']).count() == 0:
        serialized = RequestInfoSerializer(data=data)
        if serialized.is_valid():
            serialized.save()
        get_responce_log(data, serialized.is_valid(), serialized.errors, data['status'], data['errors'])
    else:
        get_responce_log(data, True, {}, data['status'])


def run():
    c.logging.basicConfig(level=c.logging.INFO, format=c.LOG_FORMAT)
    async_consumer = c.AsyncConsumer('amqp://guest:guest@localhost:5672/%2F', save_request_info)
    async_consumer.run()


t = threading.Thread(target=run)
t.start()
