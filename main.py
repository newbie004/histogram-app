import os
import logging
from read_inputs import read_intervals_and_samples
from fastapi import FastAPI
from models.histogram import Histogram
from dotenv import load_dotenv

logging.basicConfig(level=logging.DEBUG)

# import the fast api class.
load_dotenv()  # loading the .env file
app = FastAPI()


# creates the fast api instance, its name would be app.
# This app instance of fast api will be used to create the end points.


# Now to define the end points
# fast api allows us to define the api end point using python functions
# decorated with HTTP method decorators
# Below I have defined the root end point with GET HTTP method


@app.get("/")
async def read_root():
    return {"message": "Welcome to the Histogram Service!"}


def print_histogram_info(intervals, samples):
    # Print the intervals and samples
    print("Intervals:", intervals)
    print("Samples:", samples)


if __name__ == "__main__":
    import uvicorn

    # Load intervals and samples from the file
    input_file_path = os.getenv("INPUT_FILE_PATH")

    if input_file_path is None:
        raise ValueError("INPUT_FILE_PATH is not provided in the .env file")

    if input_file_path:
        intervals, samples = read_intervals_and_samples(input_file_path)

        logging.info("Intervals and Samples are extracted from the input file")

        print_histogram_info(intervals, samples)

        histogram = Histogram()

        logging.info("Histogram instance created")

        for interval in intervals:
            start, end = interval
            histogram.add_interval(start, end)
        logging.info("Intervals have been loaded into the histogram!")
    uvicorn.run(app, host="0.0.0.0", port=8000)
