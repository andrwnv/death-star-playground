from threading import Event
from time import perf_counter
from typing import Any, Callable, Iterable, Mapping


class RepeatableTimer:
    def __init__(
        self,
        interval: float,
        callback: Callable[..., object],
        async_executor: Callable,
        args: Iterable[Any] | None = ...,
        kwargs: Mapping[str, Any] | None = ...,
        repeat_count: int = -1,
        auto_start: bool = True,
    ):

        if repeat_count == 0:
            raise ValueError("Invalid repeat count!")
        if callback is None:
            raise ValueError("Invalid function!")

        self.__async_executor = async_executor

        self.__interval = interval
        self.__callback = callback

        self.__args = args if args is not None else []
        self.__kwargs = kwargs if kwargs is not None else {}

        self.__repeat_count = repeat_count
        self.__counter = 0
        self.__stop_event = Event()
        self.__start_time = None
        self.__auto_start = auto_start
        self.__is_first_call = True

    def run(self) -> None:
        self.__async_executor(self.__run)

    def stop(self) -> None:
        self.__stop_event.set()

    def __run(self) -> None:
        self.__start_time = perf_counter()

        while True:
            if not (self.__is_first_call and not self.__auto_start):
                self.__callback(*self.__args, **self.__kwargs)
                self.__counter += 1
                if (self.__repeat_count >= 1) and (
                    self.__counter >= self.__repeat_count
                ):
                    self.__stop_event.set()

            if self.__is_first_call:
                self.__is_first_call = False

            if self.__stop_event.wait(
                self.__interval - (perf_counter() - self.__start_time) % self.__interval
            ):
                break


class NonBlockableTimer(object):
    def __init__(
        self,
        interval: float,
        async_executor: Callable,
        callback: Callable[..., object] = None,
        args: Iterable[Any] | None = None,
        kwargs: Mapping[str, Any] | None = None,
        repeat_count: int = -1,
        auto_start: bool = True,
    ):

        if repeat_count == 0:
            raise ValueError("Invalid repeat count!")
        if callback is None:
            raise ValueError("Invalid function!")

        self.__async_executor = async_executor

        self.__interval = interval
        self.__callback = callback
        self.__args = args
        self.__kwargs = kwargs
        self.__repeat_count = repeat_count
        self.__auto_start = auto_start

        self.__timer = None

    def start(self) -> None:
        try:
            self.__timer.stop()
        except AttributeError:
            pass

        self.__timer = RepeatableTimer(
            interval=self.__interval,
            async_executor=self.__async_executor,
            callback=self.__callback,
            args=self.__args,
            kwargs=self.__kwargs,
            repeat_count=self.__repeat_count,
            auto_start=self.__auto_start,
        )
        self.__timer.run()

    def stop(self) -> None:
        try:
            self.__timer.stop()
        except AttributeError:
            pass

    @property
    def interval(self) -> float:
        return self.__interval

    @interval.setter
    def interval(self, value) -> None:
        self.__interval = value
        try:
            self.__timer.__interval = value
        except AttributeError:
            pass

    @property
    def count(self) -> int:
        return self.__repeat_count

    @property
    def counter(self) -> int:
        try:
            return self.__timer.__counter
        except AttributeError:
            return 0

    @property
    def start_time(self) -> float | None:
        return self.__timer.__start_time
