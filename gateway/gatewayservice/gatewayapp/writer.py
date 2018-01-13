import requests
import json
import logging
import pika
from uuid import uuid1
from datetime import datetime, timedelta
import consumer as c
import threading
from django.http import HttpResponse
from copy import deepcopy

rabbitConnection = None
rabbit_channel = None

unprocessed_messages = dict()
attempts = dict()
ttl = dict()

def connect():
    print('connecting to rabbit')

    global rabbitConnection
    global rabbit_channel

    rabbitConnection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
    rabbit_channel = rabbitConnection.channel()
    rabbit_channel.queue_declare('requests')
    rabbit_channel.exchange_declare('message', 'topic')
    rabbit_channel.queue_bind('requests', 'message', 'requests')
    rabbit_channel.queue_declare('responses')


connect()

def get_request_log(request, status=200, errors={}):
    uri_path = request.get_full_path()
    method = request.method
    guid = uuid1().hex
    data = None
    if request.method == 'GET':
        data = request.GET
    elif request.method == 'POST':
        data = request.POST

    payload = {'guid': guid, 'uri': uri_path, 'method': method, 'params': json.dumps(data),
               'timestamp': str(datetime.utcnow()), 'status': status, 'errors': json.dumps(errors)}
    unprocessed_messages[guid] = payload
    attempts[guid] = 1
    ttl[guid] = datetime.now()
    print payload
    send_message(payload)


def send_message(message):
    payload = json.dumps(message)
    try:
        status = rabbit_channel.basic_publish(exchange='message', routing_key='requests', body=payload, mandatory=False,
                                              immediate=False)
    except Exception as E:
        print(E)
        connect()
        rabbit_channel.basic_publish(exchange='message', routing_key='requests', body=payload, mandatory=False,
                                     immediate=False)

def resend_messages():
    copied_unprocessed_messages = deepcopy(unprocessed_messages)
    for k, v in copied_unprocessed_messages.items():
        if attempts[k] < 5 and ttl[k] < datetime.now() - timedelta(seconds=5):
            print "message resended"
            attempts[k] = attempts[k] + 1
            ttl[k] = datetime.now()
            send_message(v)


def confirmation(data):
    if data['status'] == 'failed' or (data['code'] not in (200, 201, 204)):
        print('message errors ' + str(data['errors']) + '\n' + 'status ' + str(data['code']) + '\n' + 'req errors ' + str(data['data_errors']))
    unprocessed_messages.pop(data['guid'], None)
    attempts.pop(data['guid'], None)
    ttl.pop(data['guid'], None)

    print('popped ' + data['guid'])
    return HttpResponse(status=200)


def run():
    c.logging.basicConfig(level=c.logging.INFO, format=c.LOG_FORMAT)
    async_consumer = c.AsyncConsumer('amqp://guest:guest@localhost:5672/%2F', confirmation)
    async_consumer.run()


t = threading.Thread(target=run)
t.daemon = True
t.start()