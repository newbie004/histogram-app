from pydantic import BaseModel
from typing import List, Dict

from starlette.responses import JSONResponse

from models.interval import Interval, sort_intervals  # Import the Interval model

import logging

# Initialize the logger
logger = logging.getLogger(__name__)


class Histogram(BaseModel):
    intervals: List[Interval] = []  # Use the Interval model as a data type
    sample_mean: float = 0.0
    sample_variance: float = 0.0
    outliers: List[float] = []

    # adding a new interval
    def add_interval(self, start: float, end: float):
        # Create a flag to track if there's an overlap
        has_overlap = False

        # Iterate through existing intervals
        for existing_interval in self.intervals:
            if start < existing_interval.end and end > existing_interval.start:
                # Overlap detected; set the flag and log the error
                has_overlap = True
                logger.error(
                    f"Overlapping interval detected: [{start}, {end}) with existing interval "
                    f"[{existing_interval.start}, {existing_interval.end}).")

        # Only add the new interval if there was no overlap
        if not has_overlap:
            new_interval = Interval(start=start, end=end)
            self.intervals.append(new_interval)

    def insert_samples(self, samples: List[float]):
        if not self.intervals:
            # No intervals defined, treat all samples as outliers
            self.outliers.extend(samples)
            return

        for sample in samples:
            matched_interval = None
            for interval in self.intervals:
                if interval.start <= sample < interval.end:
                    interval.counts += 1
                    matched_interval = interval
                    break
            if not matched_interval:
                # Sample did not fall within any interval, consider it an outlier
                self.outliers.append(sample)

    def calculate_metrics(self):

        result = {
            "intervals": [interval.to_dict() for interval in sort_intervals(self.intervals)],
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
            squared_diffs += count * ((interval.start + interval.end) / 2 - self.sample_mean) ** 2
        self.sample_variance = squared_diffs / (sample_count - 1)

        result["sample_variance"] = round(self.sample_variance, 2)

        return JSONResponse(content={"result": result})
