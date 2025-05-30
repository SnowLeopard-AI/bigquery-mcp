from __future__ import annotations

from dataclasses import dataclass
from typing import List, Optional

from google.cloud import bigquery
from google.cloud.bigquery.enums import QueryApiMethod


@dataclass
class Config:
    datasets: List[str]
    project: Optional[str]
    api_method: QueryApiMethod

    def get_client(self) -> bigquery.Client:
        kwargs = {}
        if self.project:
            kwargs["project"] = Config.project
        return bigquery.Client(**kwargs)

    @staticmethod
    def get() -> Config:
        return ConfigWrapper.config


class ConfigWrapper:
    config: Optional[Config] = None
