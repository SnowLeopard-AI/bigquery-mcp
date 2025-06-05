from __future__ import annotations

from dataclasses import dataclass
from multiprocessing import Lock
from typing import List, Optional

from google.cloud import bigquery
from google.cloud.bigquery.enums import QueryApiMethod


@dataclass
class Config:
    datasets: List[str]
    tables: List[str]
    project: Optional[str]
    api_method: QueryApiMethod
    enable_schema_tool: bool = True
    enable_list_tables_tool: bool = True
    _client: bigquery.Client = None
    _lock: Lock = Lock()

    def get_client(self) -> bigquery.Client:
        if not self._client:
            with self._lock:
                if not self._client:
                    kwargs = {}
                    if self.project:
                        kwargs["project"] = self.project

                    self._client = bigquery.Client(**kwargs)
        return self._client
