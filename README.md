# histogram-app
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
  
* Added black dependency to check and correct any formatting error 
* Command to run black -> `black .`
