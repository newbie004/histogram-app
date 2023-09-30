import os
import logging

from read_inputs import read_intervals_and_samples
from fastapi import FastAPI
from models.histogram import Histogram
from dotenv import load_dotenv

# setting the log level to debug.
logging.basicConfig(level=logging.DEBUG)

load_dotenv()  # loading the .env file
# creates the fast api instance, its name would be app.
app = FastAPI()

# This app instance of fast api will be used to create the end points.


# Now to define the end points
# fast api allows us to define the api end point using python functions
# decorated with HTTP method decorators
# Below I have defined the root end point with GET HTTP method


@app.get("/")
async def read_root():
    return {"message": "Welcome to the Histogram App!"}


histogram = Histogram()  # creating the instance globally
inputs = {}


def print_histogram_info(intervals, samples):
    # Print the intervals and samples
    print("Intervals:", intervals)
    print("Samples:", samples)


@app.get("/initialize")
async def initialize():
    # Load intervals and samples from the file
    input_file_path = os.getenv("INPUT_FILE_PATH")

    if input_file_path is None:
        raise ValueError("INPUT_FILE_PATH is not provided in the .env file")

    if input_file_path:
        intervals, samples = read_intervals_and_samples(input_file_path)

        inputs.__setitem__("intervals", intervals)
        inputs.__setitem__("samples", samples)

        logging.info("Intervals and Samples are extracted from the input file")

        print_histogram_info(intervals, samples)

        # Populate the histogram with intervals
        for interval in intervals:
            start, end = interval
            histogram.add_interval(start, end)
        logging.info("Intervals have been loaded into the histogram!")
        return {"message": "Histogram initialized with intervals successfully"}


@app.get("/insert-samples")
async def insert_samples_endpoint():
    if len(inputs) == 0:
        # if length of inputs hash is zero, means histogram has not been initialized yet!
        return {"message": "Histogram is not initialised yet!"}
    # Insert the sample data into the histogram
    histogram.insert_samples(inputs["samples"])
    print("State of Histogram after insertion of samples ", histogram)
    return {"message": "Samples inserted successfully"}


@app.get("/metrics")
async def metrics():
    print("Printing histogram in metrics method", histogram)
    return histogram.calculate_metrics()


def main():
    # Run the FastAPI app
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)


if __name__ == "__main__":
    main()
