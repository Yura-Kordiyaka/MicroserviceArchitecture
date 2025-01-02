import logging
from handle_queues.base import BaseQueueHandle
class MessageProcessor:
    def __init__(self):
        self.handlers = {}

    def register_handler(self, queue_name: str, handler: BaseQueueHandle):
        self.handlers[queue_name] = handler

    async def process_message(self, queue_name: str, data: dict):
        handler = self.handlers.get(queue_name)
        if handler:
            await handler.handle(data)
        else:
            logging.warning(f"No handler registered for queue: {queue_name}")