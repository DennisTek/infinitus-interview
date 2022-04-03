# infinitus-interview
Interview Assignment for Infinitus

# Steps taken
1. Created initial Flask `app.py` shell, confirmed local "Hello World" on 5000 works.
2. Install Docker (on Windwos unfortunately...).
3. Create Dockerfile that installs Python, Flask, exposes port 5000, and runs
    the `app.py` file.
4. Confirm "Hello World" works once again on our Dockerized file with these steps:
* Build the image:
```
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
172.17.0.1 - - [01/Apr/2022 23:20:32] "GET / HTTP/1.1" 200 -
```

5. Create basic functions and endpoints.
6. Test with a simple POST request using the python `requests` module:
```Python
import requests
x = requests.post('http://127.0.0.1:5000/detect_intent/message=Ready+in+30')
```
or, better:
```Python
import requests
data = {'message': 'Ready in 30'}
x = requests.post('http://127.0.0.1:5000/detect_intent', data=data)
```

7. Start off with unit tests in `test_app.py`.

8. Create a simple shell of the git `pre-commit` with running `python app/test_app.py`.

9. TODO: add better Flask and (potentially) Docker testing.
