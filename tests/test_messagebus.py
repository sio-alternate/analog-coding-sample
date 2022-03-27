from sms_simulator.messagebus import MessageBus


def test_publish_messages():
    assert MessageBus.get_message_queue_len('input') == 0
    MessageBus.publish_messages(['foo', 'bar', 'baz'], 'input')
    assert MessageBus.get_message_queue_len('input') == 3

    assert MessageBus.request('input') == 'foo'
    assert MessageBus.request('input') == 'bar'
    assert MessageBus.request('input') == 'baz'


def test_ack():
    MessageBus.ack_message(True, 'bazbar', 'input')
    MessageBus.ack_message(False, 'barbaz', 'input')

    assert MessageBus.get_message_queue_len('input') == 1
    assert MessageBus.request('input') == 'barbaz'

