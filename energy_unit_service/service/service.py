import asyncio

from amqp.amqp_consumer import RmqConsumer
from amqp.amqp_publisher import RmqPublisher

from service.generator.generator import DomainGenerator
from service.api.grpc.server import GrpcServer
from service.config import Config
from service.domain.model import Model


async def run(config: Config):
    async def periodic_publish(rmq_publisher):
        message = {"id": 1, "name": "name1"}

        while True:
            if rmq_publisher.publish(message):
                print(" [x] Sent %r" % message)

            await asyncio.sleep(1)

    model = Model()
    domain_generator = DomainGenerator(model=model)

    rmq_consumer = RmqConsumer()
    rmq_publisher = RmqPublisher()

    grpc_server = GrpcServer(model=model)

    rmq_publisher.run(
        addr=config.self_props.event_queue_props.addr,
        port=config.self_props.event_queue_props.port,
        username=config.self_props.event_queue_props.username,
        password=config.self_props.event_queue_props.password,
        queue_name=config.self_props.event_queue_props.queue_name,
    )

    await asyncio.gather(
        # periodic_publish(rmq_publisher),
        domain_generator.run(),
        grpc_server.run(
            addr=f"{config.self_props.grpc_addr}:{config.self_props.grpc_port}"
        ),
        rmq_consumer.run(
            addr=config.scenarist_props.event_queue_props.addr,
            port=config.scenarist_props.event_queue_props.port,
            username=config.scenarist_props.event_queue_props.username,
            password=config.scenarist_props.event_queue_props.password,
            queue_name=config.self_props.event_queue_props.queue_name,
        ),
    )
