import time
import random
from threading import Thread

from sms_simulator import messagebus


def instantiate_sender(consume_rate, failure_rate):
    sender_obj = Sender(consume_rate, failure_rate)
    thread = Thread(
        target=sender_obj.consume_messages,
        daemon=True
    )
    thread.start()


class Sender:
    def __init__(self, consume_rate, failure_rate):
        self.consume_rate = consume_rate
        self.consume_rate_range = self.consume_rate / 2
        self.failure_rate = failure_rate
        self.failure_rate_range = failure_rate / 2

    def consume_messages(self):
        while True:
            self.consume_single_message()

    def consume_single_message(self):
        start_time = time.time()

        message = messagebus.MessageBus.request('input')

        if message is None:
            return

        message_contents, phone_number = message

        try:
            self.send_message(message_contents, phone_number)
            output_topic = 'output'
            success = True
        except RuntimeError:
            output_topic = 'errors'
            success = False

        process_time = time.time() - start_time
        messagebus.MessageBus.publish_message(
            (process_time, phone_number),
            output_topic
        )
        messagebus.MessageBus.ack_message(success, message, 'input')

    def send_message(self, message, phone_number):
        time.sleep(
            self.consume_rate +
            random.uniform(
                -self.consume_rate_range,
                self.consume_rate
            )
        )

        failure_check = random.random() + random.uniform(
            -self.failure_rate_range,
            self.failure_rate_range
        )

        if failure_check <= self.failure_rate:
            raise RuntimeError('Respecting the do-not-call list.')
