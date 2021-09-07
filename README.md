# Symfall Messenger

[![Symfall CI/CD Flow](https://github.com/symfall/api/actions/workflows/aws.yml/badge.svg?branch=develop)](https://github.com/symfall/api/actions/workflows/aws.yml)

Symfall is a small messenger project. This project is a simple chat,
where you can correspond with friends and colleagues like Telegram or Viber, but this project don't have a call functions. 
We used Python framework Django for Back-end part. Symfall is not a commercial project but rather as a project for a portfolio.

## Start project:
To start the project you should create `env` file. You can copy values from `.env.dist`
and fill them by self values

After that you can start project by this command: 
```
make build-d
```
Build and start server may take some time ~5min

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

## Formatting:
To start format you need write
```
make perform
```