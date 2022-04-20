from typing import Iterable, Mapping

import random

from src.application.i_tracker import ITracker


class ConsoleTracker(ITracker):

    def __init__(self, **kwargs):
        pass

    def track(self,
              content_feed: str,
              roi: Iterable[list[int]] = None) -> Mapping[str, int]:

        return {
            'car': random.randint(1, 100),
            'length': "420sek",
            'truck': random.randint(0, 50)
        }
