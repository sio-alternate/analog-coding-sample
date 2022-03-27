import random
import string

from sms_simulator import messagebus

PHONE_FORMAT = '{}{}{}-{}{}{}-{}{}{}{}'


def produce_messages(message_count, message_size):
    messages = [
        (
            ''.join(
                [
                    random.choice(string.printable)
                    for _ in range(random.randint(1, message_size))
                ]
            ),
            PHONE_FORMAT.format(
                *[random.randint(1, 9) for _ in range(10)]
            )

        )
        for _ in range(message_count)
    ]
    messagebus.MessageBus.publish_messages(messages, 'input')
