from pydantic import BaseModel


class Interval(BaseModel):
    start: float
    end: float
    counts: int = 0

    # adding to_dict method to serialize the interval object while rendering the response.
    def to_dict(self):
        return {"start": self.start, "end": self.end, "counts": self.counts}

    # adding less than custom comparator for comparing two intervals.
    def __lt__(self, other):
        return self.start < other.start
