from abc import ABC, abstractmethod
from typing import Iterable, Mapping


class ITracker(ABC):

    @abstractmethod
    def track(self,
              content_feed: str,
              roi: Iterable[list[int]] = None) -> Mapping[str, int]:
        pass
