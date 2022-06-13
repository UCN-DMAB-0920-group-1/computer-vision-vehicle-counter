from typing import Iterable, Mapping

import random

from interfaces.i_tracker import ITracker


class DummyTracker(ITracker):

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
