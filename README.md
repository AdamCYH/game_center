# game_center

## Setting up
1. Set up virtual environment, install packages, and start server
```
virtualenv -p python3 myenv
source myenv/bin/activate

pip install --requirement requirements.txt

python manage.py migrate
python manage.py runserver
```

2. In Chrome, open two browsers. One in normal mode, one in incognito mode. Visit http://localhost:8000
