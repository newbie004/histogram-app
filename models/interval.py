from pydantic import BaseModel
from typing import List


class Interval(BaseModel):
    start: float
    end: float
    counts: int = 0

    def to_dict(self):
        return {"start": self.start, "end": self.end, "counts": self.counts}


def sort_intervals(self: List[Interval]) -> List[Interval]:
    return sorted(self, key=lambda interval: interval.start)
