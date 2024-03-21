from environs import Env
from dataclasses import dataclass


@dataclass
class Bots:
    token: str
    admin_id: int


@dataclass
class Settings:
    bots: Bots


def get_settings(path: str):
    env = Env()
    env.read_env(path)

    return Settings(
        bots=Bots(
            token=env.str("TOKEN"),
            admin_id=env.int("ADMIN_ID")
        )
    )


settings = get_settings(".env")
