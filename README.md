# Symfall Messenger

[![Symfall API CI/CD](https://github.com/symfall/api/actions/workflows/app.yml/badge.svg?branch=develop)](https://github.com/symfall/api/actions/workflows/app.yml)

Symfall is a small messenger project. This project is a simple chat,
where you can correspond with friends and colleagues like Telegram or Viber, but this project don't have a call functions. 
We used Python framework Django for Back-end part. Symfall is not a commercial project but rather as a project for a portfolio.

## Start project:
After installing the project to run it, you need to write command: 
```
make build
```
and wait for the server to start in localhost.

## Run tests:
To start tests you need write 
```
make test

# or single TestCase
make test e=authentication/tests.py::AddUserViewTest

# or single Test
make test e=authentication/tests.py::AddUserViewTest::test_user_logout
```
To start test health_check you need write 
```
make health-check
```

## Linting:
To start linter you need write
```
make lint
```

## Formatting
To start format you need write
```shell
make perform
```