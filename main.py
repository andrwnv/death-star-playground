from endpoints.api_v1.dev_api_router import DevToolsApiRouter
from usecases.abstract_scenario import AbstractScenario, AbstractAction
import logging
import os

import uvicorn
from fastapi import FastAPI, APIRouter, WebSocket
from fastapi.middleware.cors import CORSMiddleware
from usecases.battery_scenario.battery_scenario import BattertScenario, FirstActAction, SecondActAction, ThirdActAction

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

@app.websocket("/ws2")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    while True:
        data = await websocket.receive_text()
        await websocket.send_text(f"Message text was: {data}")


if __name__ == "__main__":
    import multiprocessing.pool

    from endpoints.api_v1 import EnergySystemApiRouter, RepairTeamApiRouter, EventWebSocketRouter
    from models import Model

    from usecases.api import EnergySystemApiManager
    from usecases.api import RepairTeamApiManager
    from usecases.scenarist import Scenarist
    from usecases.event_executor import EventExecutor

    thread_pool = multiprocessing.pool.ThreadPool(processes=16)

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
        # model_generator.push_strategy(battery_generator.DefaultGenerationStrategy(
        #     model=cell.battery, name=f'battery_generator-{name}'))

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

    scenario = BattertScenario(model=model)

    first_act = FirstActAction(
        name="First Act Action", event_executor=event_executor_usecase, model=model)
    scenario.push_action(first_act)

    second_act = SecondActAction(
        name="Second Act Action", event_executor=event_executor_usecase, model=model)
    scenario.push_action(second_act)

    third_act = ThirdActAction(
        name="Third Act Action", event_executor=event_executor_usecase, model=model)
    scenario.push_action(third_act)

    scenarist.set_scenario(scenario)

    def events_run():
        event_executor_usecase.start(event_ws_router.notify_about_event_start)

    def scenarist_run():
        scenarist.start(async_executor=thread_pool.apply_async)

    dev_tools_router = DevToolsApiRouter(
        scenario_start_method=scenarist_run, 
        events_start_method=events_run,
        model=model,
        prefix="/devtools")

    root_router.include_router(energy_system_router)
    root_router.include_router(repair_team_router)
    root_router.include_router(dev_tools_router)

    app.include_router(root_router)
    app.include_router(event_ws_router)

    @app.get("/")
    async def root():
        from datetime import datetime

        debugKeyExists = 'DEBUG' in os.environ

        return {
            'debug_mode': True if debugKeyExists and os.environ['DEBUG'] else False,
            'time': datetime.now().strftime("%d.%m.%YT%H:%M:%S"),
            'is_win': scenario.is_win(),
            'is_end': scenario.is_end()
        }

    uvicorn.run(app, host="0.0.0.0", port=2023, ws='websockets')
