from usecases.abstract_scenario import AbstractScenario, AbstractAction
import logging
import os

import uvicorn
from fastapi import FastAPI, APIRouter, WebSocket
from fastapi.middleware.cors import CORSMiddleware

from usecases.generators import battery_generator, cooling_generator, magnet_generator, plasma_heater_generator, vacuum_vessel_generator
from usecases.generators.generator import ModelPropertiesGenerator
from usecases.test_action import DebugBreakAction
from usecases.test_event import TestEvent

logging.config.fileConfig('logging.conf', disable_existing_loggers=False)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="Death Star ACS",
    description="Death Star ACS API",
    version="0.0.1",
    contact={
        "name": "Andrew G.",
        "url": "https://github.com/andrwnv/death_star_acs",
        "email": "glazynovand@gmail.com",
    },
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def root():
    from datetime import datetime

    debugKeyExists = 'DEBUG' in os.environ

    return {
        'debug_mode': True if debugKeyExists and os.environ['DEBUG'] else False,
        'time': datetime.now().strftime("%d.%m.%YT%H:%M:%S")
    }


@app.websocket("/ws2")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    while True:
        data = await websocket.receive_text()
        await websocket.send_text(f"Message text was: {data}")


class TestAction(AbstractAction):
    def __init__(self, name: str, event_executor, is_extra: bool = False, period: float = 1.0) -> None:
        super().__init__(name)
        self.__is_extra = is_extra
        self._period = period
        self.__event_executor = event_executor
        self.__event_executor.push_event(TestEvent())

    def __call__(self) -> bool:
        logger.info(f"Execute {self._name}. Extra = {self.__is_extra}")
        return True

    def is_end(self) -> bool:
        logger.debug(f'{self.name()} #{self.__counter} tick')
        self.__counter += 1
        return self.__counter > 3

    def is_extra_action(self) -> bool:
        return self.__is_extra

    __is_extra: bool
    __counter = 0


class TestScenario(AbstractScenario):
    def __init__(self, model, period: float) -> None:
        super().__init__()
        self.__period = period
        self.__model = model

    def is_end(self) -> bool:
        if self._action_queue.qsize() == 0:
            for cell in self.__model.power_cells.values():
                self.push_action(DebugBreakAction(
                    name=f'DebugBreakAction', battery=cell.battery))
        return self._action_queue.qsize() == 0

    def is_win(self) -> bool | None:
        return None

    def next_action_period(self) -> float:
        return self.__period

    __period: float = 1


if __name__ == "__main__":
    import multiprocessing.pool

    from endpoints.api_v1 import EnergySystemApiRouter, RepairTeamApiRouter, EventWebSocketRouter
    from models import Model

    from usecases.api import EnergySystemApiManager
    from usecases.api import RepairTeamApiManager
    from usecases.scenarist import Scenarist
    from usecases.event_executor import EventExecutor

    thread_pool = multiprocessing.pool.ThreadPool(processes=6)

    root_router = APIRouter(prefix='/api/v1')

    model = Model()
    model.start()

    model_generator = ModelPropertiesGenerator()

    for name, cell in model.power_cells.items():
        model_generator.push_strategy(cooling_generator.DefaultGenerationStrategy(
            model=cell.cooling_system, name=f'cooling_generator-{name}'))
        model_generator.push_strategy(vacuum_vessel_generator.DefaultGenerationStrategy(
            model=cell.vacuum_vessel, name=f'vacuum_vessel_generator-{name}'))
        model_generator.push_strategy(magnet_generator.DefaultGenerationStrategy(
            model=cell.magnet_system, name=f'magnet_generator-{name}'))
        model_generator.push_strategy(plasma_heater_generator.DefaultGenerationStrategy(
            model=cell.plasma_heater, name=f'plasma_heater_generator-{name}'))
        model_generator.push_strategy(battery_generator.DefaultGenerationStrategy(
            model=cell.battery, name=f'battery_generator-{name}'))

    model_generator.start(interval=1.0, executor=thread_pool.apply_async)

    energy_system_manager = EnergySystemApiManager(
        power_cells=model.power_cells)
    energy_system_router = EnergySystemApiRouter(
        manager=energy_system_manager, prefix="/energy")

    repair_team_manager = RepairTeamApiManager(
        teams=model.repair_teams, power_cells=model.power_cells, async_executor=thread_pool.apply_async)
    repair_team_router = RepairTeamApiRouter(
        manager=repair_team_manager, prefix="/repair")

    event_executor_usecase = EventExecutor(
        interval=0.1, async_executor=thread_pool.apply_async)

    event_ws_router = EventWebSocketRouter(
        manager=event_executor_usecase)

    scenarist = Scenarist(event_executor=event_executor_usecase)
    scenario = TestScenario(period=6, model=model)

    # scenario.push_action(TestAction(
    #     name="test1", event_executor=event_executor_usecase, period=5))
    # scenario.push_action(TestAction(
    #     name="test2", event_executor=event_executor_usecase, period=5))
    # scenario.push_action(TestAction(
    #     name="test3", event_executor=event_executor_usecase, is_extra=True))
    # scenario.push_action(TestAction(
    #     name="test4", event_executor=event_executor_usecase, is_extra=True))
    # scenario.push_action(TestAction(
    #     name="test5", event_executor=event_executor_usecase, period=5))
    # scenario.push_action(TestAction(
    #     name="test6", event_executor=event_executor_usecase, period=5))
    # scenario.push_action(TestAction(
    #     name="test7", event_executor=event_executor_usecase, is_extra=True))
    # scenario.push_action(TestAction(
    #     name="test8", event_executor=event_executor_usecase, is_extra=True))
    # scenario.push_action(TestAction(
    #     name="test9", event_executor=event_executor_usecase, period=5))

    event_executor_usecase.start(event_ws_router.notify_about_event_start)

    scenarist.set_scenario(scenario)
    scenarist.start(async_executor=thread_pool.apply_async)

    root_router.include_router(energy_system_router)
    root_router.include_router(repair_team_router)

    app.include_router(root_router)
    app.include_router(event_ws_router)

    uvicorn.run(app, host="0.0.0.0", port=2023, ws='websockets')
