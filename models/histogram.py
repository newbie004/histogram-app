import bisect
from pydantic import BaseModel
from typing import List, Dict
from starlette.responses import JSONResponse
from models.interval import Interval  # Import the Interval model
import logging

# Initialize the logger
logger = logging.getLogger(__name__)


class Histogram(BaseModel):
    intervals: List[Interval] = []  # Use the Interval model as a data type
    sample_mean: float = 0.0
    sample_variance: float = 0.0
    outliers: List[float] = []

    def add_interval(self, start: float, end: float):
        # Create a new interval
        new_interval = Interval(start=start, end=end)

        # finding the insertion point for the new interval using binary search
        index = bisect.bisect_left(self.intervals, new_interval)

        # Check if the new interval overlaps with adjacent intervals
        if (index > 0 and new_interval.start < self.intervals[index - 1].end) or (
            index < len(self.intervals)
            and new_interval.end > self.intervals[index].start
        ):
            logger.error(
                f"Overlapping interval detected: [{start}, {end}) with existing interval(s)."
            )
        else:
            # insert the new interval at the correct position to maintain sorting
            self.intervals.insert(index, new_interval)

    def insert_samples(self, samples: List[float]):
        if not self.intervals:
            # no intervals defined yet, treat all samples as outliers
            self.outliers.extend(samples)
            return

        # Create a sorted list of interval start values for binary search
        start_values = [interval.start for interval in self.intervals]

        for sample in samples:
            # use bisect_left to find the index where the sample should be inserted
            index = bisect.bisect_left(start_values, sample)

            if index > 0:
                # Check the previous interval for containment
                prev_interval = self.intervals[index - 1]
                if prev_interval.start <= sample < prev_interval.end:
                    prev_interval.counts += 1
                    continue

            if index < len(self.intervals):
                # Check the next interval for containment
                next_interval = self.intervals[index]
                if next_interval.start <= sample < next_interval.end:
                    next_interval.counts += 1
                    continue

            # Sample did not fall within any interval, consider it an outlier
            self.outliers.append(sample)

    def calculate_metrics(self):
        result = {
            "intervals": [interval.to_dict() for interval in self.intervals],
            "sample_mean": 0.0,
            "sample_variance": 0.0,
            "outliers": sorted(self.outliers),
        }

        if not self.intervals:
            return result

        counts_in_intervals = [interval.counts for interval in self.intervals]

        if not counts_in_intervals:
            return JSONResponse(content=result)

        sample_count = sum(counts_in_intervals)
        if sample_count == 0:
            return JSONResponse(content=result)

        # Calculate sample mean
        mean_sum = 0.0
        for count, interval in zip(counts_in_intervals, self.intervals):
            mean_sum += count * ((interval.start + interval.end) / 2)

        self.sample_mean = mean_sum / sample_count
        result["sample_mean"] = round(self.sample_mean, 2)

        # Calculate sample variance
        squared_diffs = 0.0
        for count, interval in zip(counts_in_intervals, self.intervals):
            squared_diffs += (
                count * ((interval.start + interval.end) / 2 - self.sample_mean) ** 2
            )
        self.sample_variance = squared_diffs / (sample_count - 1)

        result["sample_variance"] = round(self.sample_variance, 2)

        return JSONResponse(content={"result": result})
