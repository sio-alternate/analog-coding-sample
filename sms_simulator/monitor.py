import time
from sms_simulator import messagebus


class ResourceMonitor:
    def __init__(self, refresh_rate):
        self.refresh_rate = refresh_rate
        self.messages_sent = 0
        self.output_metrics = []

    def start_display(self):
        print(
            'INPUT QUEUE SIZE | MESSAGES SENT | MESSAGES FAILED | '
            'AVERAGE PROCESS TIME (seconds) | LATEST NUMBER CONTACTED'
        )
        while True:
            input_size, messages_sent, messages_failed, running_average, \
                latest_number = self.get_display_data()
            output_message = f'{input_size} | {messages_sent} | ' \
                             f'{messages_failed} | {running_average} | ' \
                             f'{latest_number}'
            print(output_message, end='')
            print('\r', end='')
            time.sleep(self.refresh_rate)

    def get_display_data(self):
        input_size = messagebus.MessageBus.get_message_queue_len('input')
        failed_size = messagebus.MessageBus.get_message_queue_len('errors')
        latest_number = ''

        while metric_msg := messagebus.MessageBus.request('output'):
            process_time, latest_number = metric_msg
            self.output_metrics.append(process_time)

        output_size = len(self.output_metrics)
        average = sum(self.output_metrics) / output_size if output_size else 0

        return input_size, output_size, failed_size, average, latest_number
