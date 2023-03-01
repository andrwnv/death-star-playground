import abc
from datetime import datetime, timedelta
import logging
import time

logger = logging.getLogger(__name__)


class AbstractEvent(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def positive_effect(self) -> None:
        raise NotImplementedError

    @abc.abstractmethod
    def negative_effect(self) -> None:
        raise NotImplementedError

    def name(self) -> str:
        return self._name

    def description(self) -> str:
        return self._description

    def start_time(self) -> datetime:
        return self._start_time

    def duration(self) -> timedelta:
        return self._duration

    def is_ready(self) -> bool:
        return self._start_time + self._duration <= datetime.now()

    def is_soon(self) -> timedelta:
        return datetime.fromtimestamp(time.time()) - self._start_time - self._duration

    _name: str
    _description: str
    _start_time: datetime
    _duration: timedelta
