# Check My Plants

[![python](https://img.shields.io/static/v1?label=python&message=3.9%2B&color=informational&logo=python&logoColor=white)](https://www.python.org/)
[![black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/python/black)
![Continuous Integration and Delivery](https://github.com/tobiwankenobii/check-my-plants/workflows/Github%20Actions/badge.svg?branch=develop)

Simple application for cataloging and viewing home plants made using FastAPI framework. This is a very spontaneous
project, which is a result of having too much free time and being fascinated with FastAPI. Plants are the main topic of
this project because I wanted to get my girlfriend interested in the application, as she has a lot of potted plants and
keeps information about their cultivation in a database named "plants.docx".

### Technological goals

As mentioned above, I'm really excited about using FastAPI framework as it is very modern, it has many great features
and also there a lot of interesting addons, like Tortoise ORM, which is very similar to Django ORM.

I've decided to split the application into 2 parts:

* application, which is handling pretty much everything for regular user - displaying plants, creating them etc,
* admin panel, for superusers purpose only - accepting / deleting users, plants etc.

The first part will be handled fully by FastAPI backend using Jinja templates. Admin panel is meant to be a classic REST
Api which will be used by React frontend in another repo.

I also plan to get it connected via Kubernetes and deployed on AWS.

### Getting started

The local setup is made with docker-compose. Example and working `.env` file is in `secrets` folder and it's connected
by default in compose file.

Building the images

```shell
docker-compose build
```

Running the containers

```shell
docker-compose up
```

Generating the database schemas

```shell
docker-compose exec fastapi make schema
```

And you should be good to go.

In `server` folder there is also a `Makefile` file, which makes it easier to run some command. Feel free to check it
out.

### TODOs:

There are some things that I didn't really take care about, because I just wanted backend side to be finished. And these
are:

* parametrizing tests
* mypy
* mdbootstrap color pallete
* aerich migrations
* view dependency, which would deal with 403 / 404 by default

### Conclusions

What I've learned while making this project (beside many interesting aspects and features of FastAPI) is that jinja
templates are very easy to setup, and they deliver the results quickly, but imo it's much cleaner and more convenient to
stay with regular REST Api + React / Angular setup. It just doesn't feel right to have the app structured like this,
where one half of the api is serving some HTML files, and the other half connected with some frontend. Yet, that was the
original idea which I really wanted to try, and still that was an interesting experience. Also, I found out that im
easily getting distracted by some other technologies.
