from fastapi import APIRouter, WebSocket, WebSocketDisconnect
import logging
import asyncio
import uuid
from usecases.abstract_event import AbstractEvent

from usecases.event_executor import IEventExecutorManager


logger = logging.getLogger(__name__)

class EventWebSocketRouter(APIRouter):
    def __init__(self, manager: IEventExecutorManager, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.__event_manager = manager

        self.add_api_websocket_route(
            path='/ws', endpoint=self.__loop, name='Соединение по WebSocket-у')

    def notify_about_event_start(self, event: AbstractEvent):
        if self.__websocket:
            asyncio.run(self.__websocket.send_json({
                'events': {
                    'name': event.name(),
                    'desc': event.description(),
                    'start_time': str(event.start_time()),
                    'is_ready': event.is_ready(),
                    'duration': str(event.duration())
                }}))

    async def __loop(self, websocket: WebSocket):
        self.__websocket = websocket
        await self.__websocket.accept()

        _uuid = uuid.uuid4()
        await self.__websocket.send_json({
            'connection': True,
            'session_cookie': str(_uuid)
        })

        try:
            while True:
                json_data = await self.__websocket.receive_json()
                match json_data['method']:
                    case 'get-all':
                        await self.__websocket.send_json({
                            'events': [{
                                'name': event.name(),
                                'desc': event.description(),
                                'start_time': str(event.start_time()),
                                'is_ready': event.is_ready(),
                                'duration': str(event.duration())
                            } for event in self.__event_manager.active_events()]
                        })
        except WebSocketDisconnect as ex:
            logger.info(f'User {_uuid} disconnected')
            self.__websocket = None
            logger.error(ex)
        
        if self.__websocket:
            await self.__websocket.close(1000, f'User {_uuid} close call')
            self.__websocket = None
    
    __websocket: WebSocket = None
    __event_manager: IEventExecutorManager = None
