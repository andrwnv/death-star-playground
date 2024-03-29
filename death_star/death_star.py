import multiprocessing.pool
import logging
import os

import uvicorn

from fastapi import FastAPI, APIRouter, WebSocket
from fastapi.middleware.cors import CORSMiddleware
from death_star.rmq.publisher import RmqPublisher

from death_star.routes.api.v1.dev_api_router import DevToolsApiRouter
from death_star.routes.api.v1.energy_system import EnergySystemApiRouter
from death_star.routes.api.v1.repair_team import RepairTeamApiRouter
from death_star.routes.api.v1.websocket.events import EventWebSocketRouter

from death_star.generators.generator import ModelPropertiesGenerator
from death_star.generators import (
    cooling_generator,
    magnet_generator,
    plasma_heater_generator,
    vacuum_vessel_generator)

from death_star.scenarist.scenarist import Scenarist
from death_star.scenarist.event_executor import EventExecutor
from death_star.scenarios.test_scenario import TestScenario
from death_star.scenarios.battery_scenario import (
    BattertScenario,
    FirstActAction,
    SecondActAction,
    ThirdActAction)

from death_star.entities.models import Model

from death_star.managers.api.energy_system_api_manager import EnergySystemApiManager
from death_star.managers.api.repair_team_api_manager import RepairTeamApiManager


def run():
    logging.config.fileConfig('logging.conf', disable_existing_loggers=False)

    app = FastAPI(
        title="Death Star ACS",
        description="Death Star ACS API",
        version="1.1.0",
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

    thread_pool = multiprocessing.pool.ThreadPool(processes=16)

    root_router = APIRouter(prefix='/api/v1')

    model = Model()
    model.start()

    model_generator =  ModelPropertiesGenerator()

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

    debug = True
    scenario = None

    if debug:
        scenario = TestScenario(model=model, event_publisher=RmqPublisher("rabbitmq_service"))
    else:
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

    if debug:
        event_executor_usecase.start(event_ws_router.notify_about_event_start)
        scenarist.start(async_executor=thread_pool.apply_async)

    app.include_router(root_router)
    app.include_router(event_ws_router)

    uvicorn.run(app, host="0.0.0.0", port=2023, ws='websockets')
