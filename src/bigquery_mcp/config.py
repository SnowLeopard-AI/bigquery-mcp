from __future__ import annotations

import os
from dataclasses import dataclass, field
from typing import List, Optional


@dataclass
class Config:
    dataset: List[str] = field(default_factory=list)
    project: Optional[str] = os.environ.get('BQ_PROJECT')


class ConfigWrapper:
    config: Config = Config()
