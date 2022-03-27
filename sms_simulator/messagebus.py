from queue import Queue, Empty


class MessageBus:
    __queues = {
        'input': Queue(),
        'output': Queue(),
        'errors': Queue(),
        'metrics': Queue()
    }

    @staticmethod
    def publish_messages(msgs, topic):
        for msg in msgs:
            MessageBus.publish_message(msg, topic)

    @staticmethod
    def publish_message(msg, topic):
        MessageBus.__queues[topic].put(msg)

    @staticmethod
    def request(topic):
        try:
            return MessageBus.__queues[topic].get(block=False)
        except Empty:
            return None

    @staticmethod
    def ack_message(success, msg, topic):
        if not success:
            MessageBus.__queues[topic].put(msg)

    @staticmethod
    def get_message_queue_len(topic):
        return MessageBus.__queues[topic].qsize()

    @staticmethod
    def get_dead_letter_len():
        return MessageBus.__dead_letters.qsize()
