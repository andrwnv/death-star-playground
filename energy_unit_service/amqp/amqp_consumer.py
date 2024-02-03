import logging

from abc import ABC, abstractmethod
from typing import Dict, List

logger = logging.getLogger(__name__)

logging.getLogger("pika").setLevel(logging.WARNING)


class IMessageConsumer(ABC):

    def __init__(self) -> None:
        raise NotImplemented

    @abstractmethod
    def consume(self, data: Dict[str, any]) -> None:
        raise NotImplemented


class AmqpConsumer(ABC):
    @abstractmethod
    def add_consumer(self, consumer: IMessageConsumer):
        raise NotImplemented

    @abstractmethod
    async def run(
        self, addr: str, port: str, username: str, password: str, queue_name: str
    ):
        raise NotImplemented

    @abstractmethod
    def stop(self):
        raise NotImplemented


class RmqConsumer(AmqpConsumer):
    def __init__(self) -> None:
        self.__consumers: List[IMessageConsumer] = []
        self.__is_started = False

    def add_consumer(self, consumer: IMessageConsumer):
        self.__consumers.append(consumer)

    async def run(
        self, addr: str, port: str, username: str, password: str, queue_name: str
    ):
        import pika

        credentials = pika.PlainCredentials(
            username=username,
            password=password,
        )

        connection = pika.BlockingConnection(
            pika.ConnectionParameters(
                host=addr,
                port=port,
                credentials=credentials,
            )
        )

        self.__queue_name = queue_name

        self.__channel = connection.channel()
        self.__channel.exchange_declare(
            exchange=self.__queue_name,
        )

        self.__channel.queue_declare(queue=self.__queue_name, passive=True)

        self.__is_started = True

        while self.__is_started:
            import asyncio

            method_frame, properties, body = self.__channel.basic_get(self.__queue_name)
            if method_frame is not None and properties is not None and body is not None:
                self.__consume(method_frame, properties, body)

            await asyncio.sleep(1)

    def __consume(self, method, properties, body):
        try:
            import json

            message = json.loads(body)
            for consumer in self.__consumers:
                consumer.consume(message)

            logger.debug(f"Got message from queue! Message={message}")

        except Exception:
            logger.error(
                f"Got unknown message type! Failed to parse it! Message={body}"
            )

    def stop(self):
        self.__channel.stop_consuming()
