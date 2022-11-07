- The frontend is deployed with Vercel

The backend is deployed to AWS Lambda

- Create an AWS Lambda.
- Create a zip file for the code for the Lambda and upload it:

  ```
  python3.9 -m venv .venv
  source .venv/bin/activate
  pip install -r requirements
  ```

  ```
  cd ./venv/lib/python3.9/site-packages/
  zip -r ../../../../out.zip * -x pip/\* -x setuptools/\*
  cd ../../../../
  zip out.zip retrackchanges.py docxlib.py
  ```

- Create an API Gateway of type HTTP and create a route for `retrackchanges/remove_timestamps` for OPTIONS and POST pointing to the lambda
