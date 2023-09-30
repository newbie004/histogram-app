# histogram-app
Project Setup
* To create a virtual environment
   * `python3 -m venv myenv`
* Source the current venv
   * `source myenv/bin/activate`
* Install all the dependencies in this virtual environment
   * `pip install -r requirements.txt`

Steps to run this application
* There is a file named `sample.txt` in the project directory.
* Input the data for intervals and sample to be binned.
* Start the server by running `python3 main.py`.
* Hit the async initialize web service.
    * This api will read the intervals from the `sample.txt` file
    * Initialize the histogram and will add the intervals into the histogram.
    * Invalid/Overlapping intervals are taken care and will be discarded.
    * END POINT [GET] - http://localhost:8000/initialize
 
    * Response -> {"message": "Histogram initialized with intervals successfully"}

* Hit the async insert-samples web service.
    * This api will add the samples to the corresponding intervals.
    * END POINT [GET] - http://localhost:8000/insert-samples
    * Response -> {"message": "Samples inserted successfully"}

* Hit the async metrics web service.
    * This api will compute and return the mean and variance for the histogram data.
    * END POINT [GET] - http://localhost:8000/metrics
    * Response -> 
  ``` json
    {
      "result": {
          "intervals": [
              {
                  "start": 0.0,
                  "end": 1.1,
                  "counts": 1
              },
              {
                  "start": 3.0,
                  "end": 4.1,
                  "counts": 0
              },
              {
                  "start": 8.5,
                  "end": 8.7,
                  "counts": 0
              },
              {
                  "start": 31.5,
                  "end": 41.27,
                  "counts": 2
              }
          ],
          "sample_mean": 24.44,
          "sample_variance": 428.05,
          "outliers": [
              4.2,
              8.1,
              8.2,
              30.0,
              41.27
          ]
      }
    }
  ```
  
* Added black dependency to check and correct any formatting errors in the current project directory.
   * Command to run black -> `black .`

* Add thread safety test file in `/tests`.
* To test the thread safety, run -> `python -m unittest tests.test_thread_safety` 
* Output if the thread safety test passes
  ``` json
    Ran 1 test in 0.000s
    OK
  ```


