from dataclasses import dataclass,field
from typing import Any


@dataclass
class Stage:
    name: str
    value: Any


@dataclass
class Trace:
    stages: list[Stage] = field(default_factory=list)

    def stage(self, name: str, value: Any) -> None:
        self.stages.append(
            Stage(name=name, value=value)
        )