Hello everybody and welcome to Symfall project!
This README file has a description of the project and a launch instruction
==========================================================================>
ABOUT PROJECT:
Symfall is a small startapp messenger project. This project is a simple chat,
where you can correspond with friends and colleagues like Telegram or Viber, but this project don't have a call functions. We used Python framework Django for Back-end
part. Symfall is not a commercial project but rather as a project for a portfolio.
==========================================================================>
SETUP PROJECT:
You need write "git clone https://github.com/symfall/api" in you're terminal and log into your git account.
!WARNING:
YOU WILL NOT BE ABLE TO INSTALL THE PROJECT IF YOU ARE NOT A PARTICIPANT IN THE DEVELOPMENT OR TEAM-LEAD!
==========================================================================>
START PROJECT:
After installing the project to run it, you need to write command: "docker-compose up" in you're terminal
and wait for the server to start in localhost.
==========================================================================>
STOP PROJECT:
To stop the server you need to press: "Ctrl/C" combination.
==========================================================================>
START TEST:
To start tests you need write 'docker-compose run web python /code/symfall/manage.py test' in you're terminal.
To start test health_check you need write 'docker-compose run web python /code/symfall/manage.py health_check' in you're terminal.
==========================================================================>
SETUP LINTER:
Write command "poetry add pylint" in you're terminal.
!WARNING:
YOU MUST HAVE POETRY PACKAGE INSTALLED!
==========================================================================>
START LINTER:
To start linter you need write 'pylint "python file name like models.py"' in you're terminal or console.