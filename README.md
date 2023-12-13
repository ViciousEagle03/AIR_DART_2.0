## Installing it in your own system

- Make sure you have Python installed in your system. You can check using

```bash
$ python3 --version
```

- Now clone the repo in the directory you want 

```bash
$ git clone https://github.com/ViciousEagle03/AIR_DART_2.0.git
```

- Make a virtual environment in the directory where you have cloned the repo

```bash
$ pipenv --python 3.11
```

- Now activate the virtual environment created by pipenv by 

```bash
$ pipenv shell
```

- Now install all the dependencies in the `requirements.txt` file by

```bash
$ pip install -r requirements.txt
```
- Now to run the game run the command in the activated virtual environment in the directory you have cloned the repo in

```bash
$ python AIR_DART_2.0/main.py
