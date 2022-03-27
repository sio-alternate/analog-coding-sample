from sms_simulator import sender, messagebus


def test_consume_single_message():
    while messagebus.MessageBus.request('input'):
        pass
    while messagebus.MessageBus.request('output'):
        pass

    messagebus.MessageBus.publish_message(
        ('foo-bar-baz', '123-456-7890'),
        'input'
    )
    sender_obj = sender.Sender(0, 0)
    sender_obj.consume_single_message()

    assert messagebus.MessageBus.get_message_queue_len('input') == 0
    assert messagebus.MessageBus.get_message_queue_len('output') == 1

    messagebus.MessageBus.request('output')
    messagebus.MessageBus.publish_message(
        ('foo-bar-baz', '123-456-7890'),
        'input'
    )

    sender_obj = sender.Sender(0, 1)
    sender_obj.consume_single_message()

    assert messagebus.MessageBus.get_message_queue_len('input') == 1
    assert messagebus.MessageBus.get_message_queue_len('output') == 0
