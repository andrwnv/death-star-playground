from abc import abstractmethod
from typing import Any, Dict


class AmqpPublisher:
    def __init__(self) -> None:
        pass

    @abstractmethod
    def publish() -> bool:
        raise NotImplementedError

    @abstractmethod
    def run(self, addr: str, port: str, username: str, password: str, queue_name: str):
        raise NotImplemented

    @abstractmethod
    def stop(self):
        raise NotImplemented


class RmqPublisher(AmqpPublisher):
    def __init__(self) -> None:
        super().__init__()

    def __del__(self):
        self.stop()

    def run(self, addr: str, port: str, username: str, password: str, queue_name: str):
        import pika

        credentials = pika.PlainCredentials(
            username=username,
            password=password,
        )

        self.__connection = pika.BlockingConnection(
            pika.ConnectionParameters(
                host=addr,
                port=port,
                credentials=credentials,
                socket_timeout=None,
            )
        )

        self.__queue_name = queue_name

        self.__channel = self.__connection.channel()
        self.__channel.queue_declare(queue=self.__queue_name, durable=True)

    def stop(self):
        self.__channel.cancel()
        self.__connection.close()

    def publish(self, msg: Dict[str, Any]) -> bool:
        import json
        import pika

        try:
            self.__channel.basic_publish(
                exchange="",
                routing_key=self.__queue_name,
                body=json.dumps(msg),
                properties=pika.BasicProperties(
                    delivery_mode=2,
                ),
            )
        except Exception:
            return False

        return True
