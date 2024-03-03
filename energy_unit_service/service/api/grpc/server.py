import proto.energy_unit.energy_unit_pb2_grpc as pb2_grpc

from service.domain import Model

from service.api.grpc.energy_service import EnergyService


class GrpcServer:

    def __init__(self, model: Model):
        from concurrent import futures
        import grpc

        self.__is_started = False
        self.__server = grpc.server(futures.ThreadPoolExecutor(max_workers=2))

        pb2_grpc.add_EnergyUnitServiceServicer_to_server(
            EnergyService(model=model), self.__server
        )

    async def run(self, addr: str):
        import asyncio

        self.__server.add_insecure_port(addr)
        self.__server.start()

        self.__is_started = True

        while self.__is_started:
            await asyncio.sleep(1)

    def stop(self):
        self.__is_started = False
