import json
from sms_simulator.monitor import ResourceMonitor
from sms_simulator.producer import produce_messages
from sms_simulator.sender import instantiate_sender

CONFIG_VALUES = {
    'MESSAGE_COUNT': '1000',
    'MESSAGE_CHARACTERS': '100',
    'MONITOR_REFRESH_RATE_SECONDS': '0.5'
}

if __name__ == '__main__':
    print(
        'Default values for producer/monitor are as follows. Type '
        '"<DEFAULT NAME> <VALUE>" to change a default value, and '
        'then/or ENTER to continue.'
    )
    print(json.dumps(CONFIG_VALUES, indent=2))

    while in_val := input().strip(' '):
        key, val = in_val.split(' ')
        CONFIG_VALUES[key] = val

    print(
        'Enter a string in the following format to create a sender object, '
        'or ENTER to continue. Actual consumption times/failure rates will '
        'vary randomly with a range half of the given value.'
    )
    input_format = '<CONSUME RATE (seconds)> <FAILURE RATE (float)>: '
    while in_val := input(input_format).strip(' '):
        consume_rate, failure_rate = in_val.split(' ')
        instantiate_sender(
            float(consume_rate),
            float(failure_rate)
        )

    produce_messages(
        int(CONFIG_VALUES['MESSAGE_COUNT']),
        int(CONFIG_VALUES['MESSAGE_CHARACTERS'])
    )

    print(
        'Use Ctrl+C to exit the progress monitor. Note that "INPUT QUEUE SIZE"'
        ' does not account for messages still being processed.'
    )
    monitor = ResourceMonitor(
        float(CONFIG_VALUES['MONITOR_REFRESH_RATE_SECONDS'])
    )
    monitor.start_display()
