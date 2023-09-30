import threading
import unittest
from models.histogram import Histogram
from read_inputs import read_intervals_and_samples
import os
from dotenv import load_dotenv

load_dotenv()


class ThreadSafety(unittest.TestCase):
    def setUp(self):
        # Initialize the Histogram instance
        self.histogram = Histogram()

    def insert_samples(self, samples):
        # Insert samples into the histogram
        self.histogram.insert_samples(samples)

    def test_thread_safety(self):
        # Load intervals and samples from a file
        input_file_path = os.getenv("INPUT_FILE_PATH")
        intervals, samples = read_intervals_and_samples(input_file_path)

        # Create multiple threads for inserting samples
        num_threads = 5  # configuring the number of threads to be 5
        threads = []

        for i in range(num_threads):
            start_idx = i * (len(samples) // num_threads)
            end_idx = (i + 1) * (len(samples) // num_threads)

            thread = threading.Thread(
                target=self.insert_samples, args=(samples[start_idx:end_idx],)
            )
            threads.append(thread)

        # Start all threads
        for thread in threads:
            thread.start()

        # Wait for all threads to finish
        for thread in threads:
            thread.join()

        # Calculate metrics after all threads have inserted samples
        self.histogram.calculate_metrics()


if __name__ == "__main__":
    unittest.main()

