from dataclasses import dataclass


@dataclass
class AmqpProps:
    addr: str
    port: str
    username: str
    password: str
    queue_name: str


@dataclass
class SelfProps:
    grpc_addr: str
    grpc_port: str

    http_addr: str
    http_port: str

    event_queue_props: AmqpProps

class Config:

    def __init__(self) -> None:
        self.self_props = SelfProps(
            grpc_addr="0.0.0.0",
            grpc_port=4040,
            http_addr="0.0.0.0",
            http_port=2024,
            event_queue_props=AmqpProps(
                addr="0.0.0.0",
                port=5560,
                username="guest",
                password="guest",
                queue_name="scenariste_action_queue",
            ),
        )

    def init_with_file(self, file: str):
        import yaml

        with open(file, "r") as file:
            cfg = yaml.safe_load(file)

            self.self_props.grpc_addr = cfg["grpc_addr"]
            self.self_props.grpc_port = cfg["grpc_port"]

            self.self_props.http_addr = cfg["http_addr"]
            self.self_props.http_port = cfg["http_port"]

            self.self_props.event_queue_props.addr = cfg["event_queue_addr"]
            self.self_props.event_queue_props.port = cfg["event_queue_port"]
            self.self_props.event_queue_props.username = cfg["event_queue_username"]
            self.self_props.event_queue_props.password = cfg["event_queue_password"]
            self.self_props.event_queue_props.queue_name = cfg["event_queue_name"]
