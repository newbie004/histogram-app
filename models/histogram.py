from pydantic import BaseModel
from typing import List, Dict
from models.interval import Interval  # Import the Interval model

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

    # method to insert samples falling in the existing intervals
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
        if not self.intervals:
            return "", "sample mean: 0.0", "sample variance: 0.0", "outliers:"

        counts_in_intervals = [interval.counts for interval in self.intervals]

        if not counts_in_intervals:
            return "", "sample mean: 0.0", "sample variance: 0.0", "outliers:"

        sample_count = sum(counts_in_intervals)
        if sample_count == 0:
            return "", "sample mean: 0.0", "sample variance: 0.0", "outliers:"

        # Calculate sample mean
        total_sum = sum(sample_count * [interval.counts for interval in self.intervals])
        self.sample_mean = total_sum / sample_count

        # Calculate sample variance
        squared_diffs = [(count - self.sample_mean) ** 2 for count in counts_in_intervals]
        self.sample_variance = sum(squared_diffs) / (sample_count - 1)

        # Find outliers
        self.outliers = [sample for sample in self.outliers if
                         abs(sample - self.sample_mean) > 2 * self.sample_variance]

        # Build interval strings
        interval_strings = [f"[{interval.start}, {interval.end}): {interval.counts}" for interval in self.intervals]

        # Build the final output
        metrics_output = "\n".join(interval_strings) + "\n\n"
        metrics_output += f"sample mean: {self.sample_mean:.3f}\n"
        metrics_output += f"sample variance: {self.sample_variance:.3f}\n"
        metrics_output += "outliers: " + ", ".join([f"{outlier:.2f}" for outlier in self.outliers])

        return metrics_output
