# Infinitus Interview Assignment
This take-home project is a containerized restaurant analyzer service/API.
It has two main endpoints: `/health` and `/detect_intent`, which determines
the intent of a supplied `message` paremter, using Jaccard similarities.

See the included PDF for more details on the requirements.

# Usage (Docker)
From the root directory, build the image with:
```Bash
docker image build -t restaurant_analyzer ./app/
```
You can then run the local restaurant analyzer service from a container as:
```Bash
docker container run --name RA_test -d -p 5000:5000 restaurant_analyzer
```
The two endpoints should now be up and running on your localhost. You can easily
check the `/health` endpoint in browser, but the two endpoints can be tested
more easily using something like python `requests` or `curl`. See Python REPL
below:
```Python
>>> import requests
>>> r = requests.get('http://127.0.0.1:5000/health')
>>> print(r.status_code, r.text)
200 <p>Service is up and running!</p>

>>> data = {'message': 'OK, your order is a large pizza and garlic bread.'}
>>> x = requests.post('http://127.0.0.1:5000/detect_intent', data)
>>> print(x.status_code, x.text)
200 ConfirmItem

>>> invalid_req = requests.post('http://127.0.0.1:5000/detect_intent')
>>> print(invalid_req.status_code, invalid_req.text)
422 'message' parameter not found, please supply.
```
Lastly, you can see the app logs with the standard Docker command:
```Bash
docker container logs $container_name
```

## Pre-commit Hook
Since the `.git` directory isn't versioned, I just made a copy of this file in
the root directory. Simply move or copy the `pre-commit-copy` file to the
appropriate `.git/hooks/` directory on your local copy of the repo.

This could be done more properly via symlinking or creating a directory to store
hooks but this is a quick enough solution for a take-home assignment.

# Development Process & Possible Extensions
This section is primarily just documentation so that we can more easily discuss
the process, my thinking, etc. during the final interview.

## High Level Overview
1. Created initial Flask `app.py` shell, confirmed local "Hello World" on
    port 5000 works.
2. Install Docker (I'm on Windwos unfortunately so this took more time...).
3. Create Dockerfile to build our image that installs Python, Flask, copies
    files, exposes port 5000, and runs the `app.py` file.
4. Confirm "Hello World" works once again on our Dockerized file with these steps:
* Build the image:
```Bash
docker image build -t 'restaurant_analyzer' .
```

* Run the image and show that we get the same basic `localhost` functionality in browser and via `docker container logs`.
```
> docker container run --name RA_test -d -p 5000:5000 restaurant_analyzer
> docker container logs $container
 * Serving Flask app 'app' (lazy loading)
 * Environment: production
   WARNING: This is a development server. Do not use it in a production deployment.
   Use a production WSGI server instead.
 * Debug mode: off
 * Running on all addresses.
   WARNING: This is a development server. Do not use it in a production deployment.
 * Running on http://172.17.0.3:5000/ (Press CTRL+C to quit)
172.17.0.1 - - [01/Apr/2022 23:18:34] "GET / HTTP/1.1" 200 -
172.17.0.1 - - [01/Apr/2022 23:18:36] "GET / HTTP/1.1" 200 -
```

5. Create the `jaccard_similarity` function and the two Flask service endpoints.
6. Test all functions, here's an example with the `/detect_intent` endpoint:
```Python
import requests
data = {'message': 'Ready in 30'}
x = requests.post('http://127.0.0.1:5000/detect_intent', data=data)
```

7. Formalize these as unit tests in `test_app.py`.

8. Create a simple shell of the git `pre-commit` with running
    `python app/test_app.py`. I include this in the main directory just so
    that it's readily tracked in Github, with the real version needing to be in
    the standard `.git/hooks` directory.

9. Added better Flask testing using a mock client, still just `unittest` module.

## Potential Extensions
* Add live flask server testing. Example [here](https://dev.to/totally_chase/a-guide-to-testing-flask-applications-using-unittest-2k4n).
* Add live Docker image building and E2E testing.
* Organize the project structure more thoroughly, as described in the
    [Flask documentation](https://flask.palletsprojects.com/en/2.1.x/tutorial/layout/).
* Optimize/Extend pre-commit hook to include things like "option for skipping tests".
