from dataclasses import dataclass


@dataclass
class Configuration:
    port: int = 23445
    host: str = "localhost"
    engine: str = "wsgiref"
