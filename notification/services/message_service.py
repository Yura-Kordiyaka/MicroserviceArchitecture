import logging
class MessageProcessor:
    async def process_message(self, queue_name: str, data: dict):
        if queue_name == "notification_create_user":
            await self.handle_queue_1(data)
        elif queue_name == "queue_2":
            await self.handle_queue_2(data)
        else:
            print(f"Unhandled queue: {queue_name}")

    async def handle_queue_1(self, data):
        print(f"Processing queue_1 message: {data}")
        logging.info('hello handle_queue_1')
        # Логіка для queue_1

    async def handle_queue_2(self, data):
        print(f"Processing queue_2 message: {data}")
        # Логіка для queue_2
