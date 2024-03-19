# agi-publisher

Primary goal of `agi-publisher` is to leverage LLM as team of AGI working together to develop publishcation ready content.

![Preview](docs/screen-home.png)

## Get Started
1. Create project

```
mkdir myproject
cd myproject
git clone https://github.com/code-poineer/agi-publisher.git .
```

2. Create Virtual Environment
```
python -m venv venv
source venv/bin/activate
```

3. Install packages
```
pip install --upgrade pip
pip install -r requirements.txt
```
4. Sign up for OpenAI API Key: https://platform.openai.com/api-keys

5. Sign up for https://serper.dev and get your api key.
   
6.  Environment Settings
   ```
   Copy `sample-dot-env.txt` as `.env`
   Open `.env` and set appropriate values
    1.  update OpenAI API Key
    2.  Update Serper API Key
   ```

7. Setup database
```
python manage.py migrate
```

1. Setup admin account
```
python manage.py createsuperuser
```

1. Run Unit Test Case
```
python manage.py test
```

1.  Start server
```
python manage.py runserver --insecure
```