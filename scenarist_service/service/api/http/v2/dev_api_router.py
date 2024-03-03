from fastapi import APIRouter, HTTPException

from service.domain.models.model import Model


class DevToolsApiRouter(APIRouter):
    def __init__(
        self, scenario_start_method, events_start_method, model: Model, *args, **kwargs
    ) -> None:
        super().__init__(*args, **kwargs)

        self.__scenario_start_method = scenario_start_method
        self.__events_start_method = events_start_method
        self.__model = model

        self.add_api_route(
            path="/{secret_key}",
            methods=["GET"],
            endpoint=self.manipulate,
            tags=["DEV"],
            name="Хммммм, a что же это кхм-кхм-кхм",
        )

    async def manipulate(self, secret_key: str):
        try:
            status = False

            match secret_key:
                case "tusur-chempion":
                    status = "tusur-chempion command success"
                    self.__events_start_method()
                    self.__scenario_start_method()
                case "ban-him":
                    status = "ban-him command success"
                    for power_cell in self.__model.power_cells.values():
                        battery = power_cell.battery
                        for capicator in battery.capacitors:
                            if capicator.durability >= 0:
                                capicator.durability = 0
                                break
                            else:
                                continue
                case "help-him":
                    status = "help-him command success"
                    for power_cell in self.__model.power_cells.values():
                        battery = power_cell.battery
                        for capicator in battery.capacitors:
                            if capicator.durability >= 50:
                                continue
                            else:
                                capicator.durability = 50
                                break
                case _:
                    status = "ne lez' ono tebya ubiot"

            return {"executed_status": status}
        except HTTPException as ex:
            raise HTTPException(status_code=ex.status_code)
        except Exception as ex:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=ex
            )
