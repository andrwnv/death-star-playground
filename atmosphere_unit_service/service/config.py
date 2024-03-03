from dataclasses import dataclass

@dataclass
class AmpqProps:
    addr: str
    port: str
    username: str
    password: str
    queue_name: str

@dataclass
class SelfProps:
    grpc_addr: str
    grpc_port: str

    event_queue_props: AmpqProps

@dataclass
class ScenaristProps:
    event_queue_props: AmpqProps

class Config:

    def __init__(self) -> None:
        self.self_props = SelfProps(
            grpc_addr="0.0.0.0",
            grpc_port=4040,
            event_queue_props=AmpqProps(
                addr="0.0.0.0",
                port=5560,
                username="guest",
                password="guest",
                queue_name="scenarist_action_queue",
            ),
        )
        self.scenarist_props = ScenaristProps(
            event_queue_props=AmpqProps(
                addr="0.0.0.0",
                port=5560,
                username="guest",
                password="guest",
                queue_name="atmosphere_unit_action_queue",
            ),
        )
    
    def init_with_file(self, file: str):
        import yaml

        with open(file, "r") as file:
            cfg = yaml.safe_load(file)

            self.self_props.grpc_addr = cfg["grpc_addr"]
            self.self_props.grpc_port = cfg["grpc_port"]
            self.self_props.event_queue_props.addr = cfg["event_queue_addr"]
            self.self_props.event_queue_props.port = cfg["event_queue_port"]
            self.self_props.event_queue_props.username = cfg["event_queue_username"]
            self.self_props.event_queue_props.password = cfg["event_queue_password"]
            self.self_props.event_queue_props.queue_name = cfg["event_queue_name"]

            self.scenarist_props.event_queue_props.addr = cfg["scenarist"][
                "event_queue_addr"
            ]
            self.scenarist_props.event_queue_props.port = cfg["scenarist"][
                "event_queue_port"
            ]
            self.scenarist_props.event_queue_props.username = cfg["scenarist"][
                "event_queue_username"
            ]
            self.scenarist_props.event_queue_props.password = cfg["scenarist"][
                "event_queue_password"
            ]
            self.self_props.event_queue_props.queue_name = cfg["scenarist"][
                "event_queue_name"
            ]
