from fastapi import APIRouter, Body, HTTPException, status

from usecases.api.repair_team_api_manager import RepairTeamApiManager
from endpoints.dto.repair_team_dto import SendTeamDto


class RepairTeamApiRouter(APIRouter):
    def __init__(self, manager: RepairTeamApiManager, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

        self.__manager = manager

        self.add_api_route(path='/teams',
                           methods=['GET'], endpoint=self.get_all, tags=['Ремонтные бригады'], name='Получение списка ремонтных бригад')
        self.add_api_route(path='/team/{team_name}',
                           methods=['GET'], endpoint=self.get_team_info, tags=['Ремонтные бригады'], name='Получение информации о ремонтной бригаде')
        self.add_api_route(path='/start',
                           methods=['POST'], endpoint=self.send_team, tags=['Ремонтные бригады'], name='Отправка ремонтной бригаде на объект')
        self.add_api_route(path='/stop',
                           methods=['POST'], endpoint=self.send_team, response_model=None, tags=['Ремонтные бригады'], name='Отзыв ремонтной бригаде с объекта')

    async def get_all(self):
        try:
            result = self.__manager.team_list()
            return {
                device_name: result[device_name].to_json(
                    exclude=['name'])
                for device_name, value in result.items()
            }
        except HTTPException as ex:
            raise HTTPException(status_code=ex.status_code)
        except Exception as ex:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=ex)

    async def get_team_info(self, team_name: str):
        try:
            result = self.__manager.team_info(team_name)

            if not result:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST_BAD_REQUEST)

            return result.to_json()
        except HTTPException as ex:
            raise HTTPException(status_code=ex.status_code)
        except Exception as ex:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=ex)

    async def send_team(self, dto: SendTeamDto = Body()):
        try:
            result = self.__manager.send_team(dto.team_name, dto.location)
            return {
                'execution_status': result
            }
        except HTTPException as ex:
            raise HTTPException(status_code=ex.status_code)
        except Exception as ex:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=ex)

    __manager: RepairTeamApiManager
