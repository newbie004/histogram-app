from pydantic import BaseModel


class Interval(BaseModel):
    start: float
    end: float
    counts: int = 0
    # counts track the number of samples falling in this particular interval.
