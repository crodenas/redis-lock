
Simple Redis based distributed lock.

Start a local redis server:

```shell
docker run -p 6379:6379 --name redis -d redis
```
Setup the virtuial env:
```shell
$ python3 -m venv venv
$ . ./venv/bin/activate
$ pip install -U pip
$ pip install -r requirements.txt
```

Then in 2, or more, activated terminals start the tests.

```shell
$ python test_lock.py
```