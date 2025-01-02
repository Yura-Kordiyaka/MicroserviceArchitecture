from abc import ABC, abstractmethod

class BaseQueueHandle(ABC):
    @abstractmethod
    async def handle(self,data):
        pass