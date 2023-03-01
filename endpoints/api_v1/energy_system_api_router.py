from fastapi import APIRouter, HTTPException, status

from usecases.api.energy_system_api_manager import EnergySystemApiManager


class EnergySystemApiRouter(APIRouter):
    def __init__(self, manager: EnergySystemApiManager, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

        self.__manager = manager

        self.add_api_route(path='/names',
                           methods=['GET'], endpoint=self.get_cell_list, tags=['Энергетический модуль'], name='Получение списка энергетических модулей')
        self.add_api_route(path='/state/{power_cell_name}',
                           methods=['GET'], endpoint=self.get_cell_state, tags=['Энергетический модуль'], name='Получение общей информации об энергетический модуле')
        self.add_api_route(path='/state/{power_cell_name}/cooling_system',
                           methods=['GET'], endpoint=self.get_cooling_system_state, tags=['Энергетический модуль'], name='Получение информации о системы охлаждения')
        self.add_api_route(path='/state/{power_cell_name}/magnet_system',
                           methods=['GET'], endpoint=self.get_magnet_system_state, tags=['Энергетический модуль'], name='Получение информации о магнитной системы')
        self.add_api_route(path='/state/{power_cell_name}/plasma_heater',
                           methods=['GET'], endpoint=self.get_plasma_heater_state, tags=['Энергетический модуль'], name='Получение информации о нагревателе плазмы')
        self.add_api_route(path='/state/{power_cell_name}/vacuum_vessel',
                           methods=['GET'], endpoint=self.get_vacuum_vessel_state, tags=['Энергетический модуль'], name='Получение информации о вакуумной системе')
        self.add_api_route(path='/state/{power_cell_name}/fuel_storage',
                           methods=['GET'], endpoint=self.get_fuel_storage_state, tags=['Энергетический модуль'], name='Получение информации о топливном хранилище')
        self.add_api_route(path='/state/{power_cell_name}/battery',
                           methods=['GET'], endpoint=self.get_battery_state, tags=['Энергетический модуль'], name='Получение информации об аккумуляторном блоке')

    async def get_cell_list(self):
        try:
            return {
                'power_cell_names': self.__manager.get_list()
            }
        except HTTPException as ex:
            raise HTTPException(status_code=ex.status_code)
        except Exception as ex:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=ex)

    async def get_cell_state(self, power_cell_name: str):
        try:
            result = self.__manager.get_state(name=power_cell_name)
            fields = list(result.__dict__.keys())
            fields.remove('power')

            if result is None:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST_BAD_REQUEST)

            status_fields = ['is_on', 'alarm', 'durability']
            default_devices = [
                device for device in fields if device not in ['name'] + status_fields]
            only_durability_devices = ['fuel_storage']

            return {
                result.name: {
                    'state': result.to_json(fields=status_fields),
                    'devices_state': {
                        device_name: getattr(result, device_name).to_json(
                            fields=['is_on', 'alarm', 'durability'])
                        if device_name not in only_durability_devices
                        else getattr(result, device_name).to_json(fields=['durability'])
                        for device_name in default_devices
                    },
                    'power': result.power
                }
            }
        except HTTPException as ex:
            raise HTTPException(status_code=ex.status_code)
        except Exception as ex:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=ex)

    async def get_cooling_system_state(self, power_cell_name: str):
        try:
            result = self.__manager.get_colling_system_state(
                name=power_cell_name)
            if result is None:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST_BAD_REQUEST)

            return {
                power_cell_name: {
                    "cooling_system": result.to_json()
                }
            }
        except HTTPException as ex:
            raise HTTPException(status_code=ex.status_code)
        except Exception as ex:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=ex)

    async def get_magnet_system_state(self, power_cell_name: str):
        try:
            result = self.__manager.get_magnet_system_state(
                name=power_cell_name)
            if result is None:
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST)

            return {
                power_cell_name: {
                    "magnet_system": result.to_json()
                }
            }
        except HTTPException as ex:
            raise HTTPException(status_code=ex.status_code)
        except Exception as ex:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=ex)

    async def get_plasma_heater_state(self, power_cell_name: str):
        try:
            result = self.__manager.get_plasma_heater_state(
                name=power_cell_name)
            if result is None:
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST)

            return {
                power_cell_name: {
                    "plasma_heater": result.to_json()
                }
            }
        except HTTPException as ex:
            raise HTTPException(status_code=ex.status_code)
        except Exception as ex:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=ex)

    async def get_vacuum_vessel_state(self, power_cell_name: str):
        try:
            result = self.__manager.get_vacuum_vessel_state(
                name=power_cell_name)
            if result is None:
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST)

            return {
                power_cell_name: {
                    "vacuum_vessel": result.to_json()
                }
            }
        except HTTPException as ex:
            raise HTTPException(status_code=ex.status_code)
        except Exception as ex:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=ex)

    async def get_fuel_storage_state(self, power_cell_name: str):
        try:
            result = self.__manager.get_fuel_storage_state(
                name=power_cell_name)
            if result is None:
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST)

            return {
                power_cell_name: {
                    "fuel_storage": result.to_json()
                }
            }
        except HTTPException as ex:
            raise HTTPException(status_code=ex.status_code)
        except Exception as ex:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=ex)

    async def get_battery_state(self, power_cell_name: str):
        try:
            result = self.__manager.get_battery_state(
                name=power_cell_name)

            if result is None:
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST)

            json_data = {
                power_cell_name: {
                    "battery": result.to_json()
                }
            }

            json_data[power_cell_name]['battery']['durability'] = sum([capacitor.durability for capacitor in result.capacitors]) / len(result.capacitors)

            return json_data
        except HTTPException as ex:
            raise HTTPException(status_code=ex.status_code)
        except Exception as ex:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=ex)

    __manager: EnergySystemApiManager
