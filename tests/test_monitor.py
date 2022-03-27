from sms_simulator import messagebus, monitor


def test_get_display_data():
    messagebus.MessageBus.publish_messages(['foo', 'bar', 'baz'], 'input')
    messagebus.MessageBus.publish_messages(['blue', 'shoe'], 'errors')
    messagebus.MessageBus.publish_messages(
        [(7, '1234'), (3, '5678')],
        'output'
    )
    monitor_obj = monitor.ResourceMonitor(100)

    input_size, output_size, failed_size, average, latest_number = \
        monitor_obj.get_display_data()

    assert input_size == 3
    assert output_size == 2
    assert failed_size == 2
    assert average == 5.0
    assert latest_number == '5678'
