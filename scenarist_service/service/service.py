import asyncio
import logging
import os

from fastapi import FastAPI, APIRouter, WebSocket
from fastapi.middleware.cors import CORSMiddleware

import uvicorn

from service.api.http.v2.energy_system import EnergySystemApiRouter
from service.api.http.v2.repair_team import RepairTeamApiRouter

from service.managers.api.energy_system_api_manager import EnergySystemApiManager
from service.managers.api.repair_team_api_manager import RepairTeamApiManager

from service.domain.models.model import Model

from service.config import Config

logger = logging.getLogger(__name__)


async def run(config: Config):
    async def timer():
        while True:
            logger.debug("im alive")
            await asyncio.sleep(1)

    app = FastAPI(
        title="Death Star Playground",
        description="Death Star Playground API",
        version="2.0.0",
        contact={
            "name": "Andrew G.",
            "url": "https://github.com/andrwnv/death-star-playground",
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

        debugKeyExists = "DEBUG" in os.environ

        return {
            "debug_mode": True if debugKeyExists and os.environ["DEBUG"] else False,
            "time": datetime.now().strftime("%d.%m.%YT%H:%M:%S"),
            "is_win": False,
            "is_end": False,
        }

    model = Model()
    model.start()

    energy_system_manager = EnergySystemApiManager(power_cells=model.power_cells)
    energy_system_router = EnergySystemApiRouter(
        manager=energy_system_manager, prefix="/energy-unit"
    )

    repair_team_manager = RepairTeamApiManager(
        teams=model.repair_teams,
        power_cells=model.power_cells,
        async_executor=lambda: print("call task"),
    )
    repair_team_router = RepairTeamApiRouter(
        manager=repair_team_manager, prefix="/teams"
    )

    root_router = APIRouter(prefix="/api/v2")

    debug = True
    scenario = None

    root_router.include_router(energy_system_router)
    root_router.include_router(repair_team_router)
    # root_router.include_router(dev_tools_router)

    app.include_router(root_router)
    # app.include_router(event_ws_router)

    log_config = uvicorn.config.LOGGING_CONFIG
    log_config["formatters"]["access"]["fmt"] = "[%(asctime)s][%(levelname)s]: %(message)s"
    log_config["formatters"]["default"]["fmt"] = "[%(asctime)s][%(levelname)s]: %(message)s"

    config = uvicorn.Config(app, port=2024, host="0.0.0.0", log_config=log_config)
    server = uvicorn.Server(config)

    await asyncio.gather(
        timer(),
        server.serve(),
    )
