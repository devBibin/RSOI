import threading
import gatewayapp.models
from gatewayapp.writer import resend_messages
from time import sleep

def resend():
    while True:
        resend_messages()
        sleep(3)

t = threading.Thread(target=resend)
t.daemon = True
t.start()

