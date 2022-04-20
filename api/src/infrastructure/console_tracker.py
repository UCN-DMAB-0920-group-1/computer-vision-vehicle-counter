from typing import Iterable, Mapping

from api.src.tracking_module.tracker import Tracker
import random


class ConsoleTracker(Tracker):

    def track(self,
              content_feed: str,
              roi: Iterable[list[int]] = None) -> Mapping[str, int]:

        return {
            'car': random.randint(1, 100),
            'length': "420sek",
            'truck': random.randint(0, 50)
        }
