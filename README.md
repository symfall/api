# Symfall Messenger

## ABOUT PROJECT:
Symfall is a small startapp messenger project. This project is a simple chat,
where you can correspond with friends and colleagues like Telegram or Viber, but this project don't have a call functions. We used Python framework Django for Back-end
part. Symfall is not a commercial project but rather as a project for a portfolio.

## START PROJECT:
After installing the project to run it, you need to write command: 
```
make build
```
and wait for the server to start in localhost.

## Run tests:
To start tests you need write 
```
docker-compose run web python /code/symfall/manage.py test
```
To start test health_check you need write 
```
docker-compose run web python /code/symfall/manage.py health_check
```

## Linting:
To start linter you need write 'pylint "python file name like models.py"' in you're terminal or console.