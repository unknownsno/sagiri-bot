import os
import yaml
from abc import ABC
from pathlib import Path
from pydantic import BaseModel
from typing import Type, List, Dict
from typing_extensions import TypedDict

from creart import exists_module
from creart import add_creator
from creart.creator import AbstractCreator, CreateTargetInfo


class PluginConfig(TypedDict):
    prefix: List[str]
    alias: List[str]


class GlobalConfig(BaseModel):
    bot_qq: int
    host_qq: int
    mirai_host: str = "http://localhost:8080"
    verify_key: str = "1234567890"
    db_link: str = "sqlite+aiosqlite:///data.db"
    web_manager_api: bool = False
    web_manager_auto_boot: bool = False
    image_path: dict = {}
    proxy: str = "proxy"
    commands: Dict[str, PluginConfig]
    functions: dict = {
        "tencent": {
            "secret_id": "secret_id",
            "secret_key": "secret_key"
        },
        "saucenao_api_key": "saucenao_api_key",
        "lolicon_api_key": "lolicon_api_key",
        "wolfram_alpha_key": "wolfram_alpha_key",
        "github": {
            "username": "username",
            "token": "token"
        },
    }
    log_related: dict = {
        "error_retention": 14,
        "common_retention": 7
    }
    data_related: dict = {
        "lolicon_image_cache": True,
        "network_data_cache": False,
        "automatic_update": False,
        "data_retention": False
    }


class ConfigClassCreator(AbstractCreator, ABC):
    targets = (
        CreateTargetInfo("sagiri_bot.config", "GlobalConfig"),
    )

    @staticmethod
    def available() -> bool:
        return exists_module("sagiri_bot.config")

    @staticmethod
    def create(create_type: Type[GlobalConfig]) -> GlobalConfig:
        with open(Path(os.getcwd()) / "config.yaml", "r", encoding='utf-8') as f:
            configs = yaml.load(f.read(), Loader=yaml.BaseLoader)
            return GlobalConfig(**configs)


add_creator(ConfigClassCreator)
