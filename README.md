# Check My Plants

[![python](https://img.shields.io/static/v1?label=python&message=3.9%2B&color=informational&logo=python&logoColor=white)](https://www.python.org/)
[![black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/python/black)
![Continuous Integration and Delivery](https://github.com/tobiwankenobii/check-my-plants/workflows/Github%20Actions/badge.svg?branch=main)

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