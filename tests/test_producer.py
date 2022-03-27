from sms_simulator import producer, messagebus


def test_produce_messages():
    while messagebus.MessageBus.request('input'):
        pass

    message_len = 5
    message_count = 15
    producer.produce_messages(message_count, message_len)

    assert messagebus.MessageBus.get_message_queue_len(
        'input'
    ) == message_count

    while True:
        input_msg = messagebus.MessageBus.request('input')

        if input_msg is None:
            break

        message, num = input_msg

        assert len(message) <= message_len
        assert len(num) == 12
