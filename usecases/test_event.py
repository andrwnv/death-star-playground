from datetime import timedelta, datetime
import logging
from usecases.abstract_event import AbstractEvent

logger = logging.getLogger(__name__)


class TestEvent(AbstractEvent):
    def __init__(self) -> None:
        super().__init__()

        import uuid
        self._name = str(uuid.uuid4())
        self._description = 'Guys, theres no need to open up on this subject. Youre young, youre joking, its easy for you. This isnt it. This isnt Chikatilo or even the secret service archives. Its better to stay out of it. Seriously, any of you will regret it. Better close the thread and forget what was written here. I quite understand that this message will cause additional interest, but I want to warn the inquisitive at once - stop. The rest simply will not find.'
        self._description += f'  {self._name} xd'
        self._start_time = datetime.now() + timedelta(seconds=5)
        self._duration = timedelta(seconds=5)

    def positive_effect(self) -> None:
        logger.info(f'positive_effect of {self._name}')

    def negative_effect(self) -> None:
        logger.info(f'negative_effect of {self._name}')
