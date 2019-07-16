[![Build Status](https://travis-ci.org/tonymontaro/mentorci.svg?branch=master)](https://travis-ci.org/tonymontaro/mentorci)

# MentorCI API

## About

Automate and Track CI Mentorship sessions.

## Features

App available here; http://mentorci.ga/

- organize all student data in central location
- easily view previous logs for a student
- log sessions without having to copy/paste certain fields (e.g student-email )
- view summary information per month
- generate invoice pdf at the end of the month

## Technology stack

Tools used;

- [Django](https://www.djangoproject.com) - a python web framework
- [Django REST Framework](http://www.django-rest-framework.org) - a flexible toolkit to build web APIs
- [SQLite](https://www.sqlite.org/) - local development DBMS
- [MySQL](https://www.mysql.com/) - production DBMS
- [AWS](http://aws.amazon.com/) - for deployment/hosting the backend/api
- [Netlify](https://www.netlify.com/) - for deployment/hosting the client
- [Docker](https://www.docker.com/) - Build, Ship, and Run Any App, Anywhere.
- [Vue JS](https://vuejs.org/) - client side framework
- [ReportLab](https://www.reportlab.com/) - used for generating PDF document

## Requirements

- Use Python 3.x.x+
- Use Django 2.x.x+

## Tests

"Code without tests is broken as designed", said Jacob Kaplan-Moss. To run tests, enter the following command

### BackEnd Tests

- On the root folder, run

```bash
$ python manage.py test
```

### Client Tests (E2E)

- Navigate to the client folder (`client/`) and run

```bash
$ npm test
```

## Install and Run Locally

To run this application, clone the repository on your local machine and execute the following command.

```bash
$ cd mentorci
```

- Install and Run the API

```bash
$ virtualenv -p python env && source env/bin/activate
$ pip install -r requirements.txt
$ cp env_sample .env
$ python manage.py makemigrations && python manage.py migrate
$ python manage.py runserver
```

- Install and Run the Vue Client, open a new terminal and run

```bash
$ cd mentorci/client
$ npm install
$ npm start
```

## Deployment

### Backend(API)

The API should be deployed with a hosting service that supports Docker containers (AWS was used).

- Create an instance and clone the repository content
- create a .env file and ensure that the following environmental variables are specified; DB_NAME, DB_USER, DB_PASSWORD, DB_HOST, DB_URL, GMAIL, and GMAIL_PASSWORD.
- Change instances of "api.mentorci.ga" to your domain name the **init-letsencrypt.sh** and **data/nginx/app.conf** files
- Run; `./init-letsencrypt.sh`
- finally start the server with `docker-compose up` or it's equivalent in your deployment environment.

### Client

The client side was deployed with Netlify with the following deploy settings;

```text
Base directory: client
Build command: npm run build
Publish directory: client/dist
```

Deploying the client is straight-forward.

- move into the client; `cd mentorci/client`
- generate production static files

```bash
npm run build
```

- host the generated **dist** folder.

### Contributing

Contributions are most welcome!

- fork this repository
- Create and checkout a feature branch
- Commit and push your changes
- create a new Pull Request to the master branch

Found a bug/issue? Please create an **issue** on github.

## Credits

- Emmanuel King Kasulani - [Let’s build an API with Django REST Framework](https://medium.com/backticks-tildes/lets-build-an-api-with-django-rest-framework-32fcf40231e5)
- Jason Watmore - [Vue.js + Vuex - JWT Authentication Tutorial & Example](https://jasonwatmore.com/post/2018/07/06/vue-vuex-jwt-authentication-tutorial-example)
- Philipp - [Nginx and Let’s Encrypt with Docker in Less Than 5 Minutes](https://medium.com/@pentacent/nginx-and-lets-encrypt-with-docker-in-less-than-5-minutes-b4b8a60d3a71)
- [PyInvoice](https://github.com/CiCiApp/PyInvoice) source code

### Inspiration

- Antonija Šimić - [Student Sessions](https://github.com/tonkec/student_sessions)

### License

[MIT](https://github.com/tonymontaro/mentorci/blob/master/LICENSE)
