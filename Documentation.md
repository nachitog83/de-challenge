## Resolution

#### Introduction

For this challenge, the approach was to create a simple, Flask app to store Locations.

To design this app, I followed a Repository Pattern (which, to be honest, I'm a big fan of).

Essentially, it provides an abstraction of data, so that your application can work with a simple abstraction that has an interface approximating that of a collection. Adding, removing, updating, and selecting items from this collection is done through a series of straightforward methods, without the need to deal with database concerns like connections, commands, cursors, or readers. Using this pattern can help achieve loose coupling and can keep domain objects persistence ignorant.

This Repository pattern is a simplifying abstraction over data storage, allowing us to decouple our model layer from the data layer, reduce code duplication, among other pros.

#### Approach

Basically I misread at the beginning the task, so I had to redo the logic for the average requests data.

The approach I took (basically out of pure ignorace on tools to handle requests and average them), was to set up a Redis cache database, store all incoming requests with a TTL, and run a RedisEventHandler on a separate thread to listen to Redis messages on when KEYS are going to expire. When this happens, the handler runs a service to store the average of requests per minute and user_id to a MongoDB collection.

Because of the misinterpretation I run into at the beggining (basically I thought we needed to limit incoming requests, so I set up a Limiter on the /location endpoint to throttle the API endpoint on 1 call per minute), I lost valuable time and couldn't finish all unit tests I had in mind for the actual resolution. I would gladly run you by what I tought tests could be.

Caveats: I know this is not the most efficient way to store the values asked, but given the time and the limited knowledge of tools to handle these type scenarios, is the best I could come up with. Redis is a very efficient cache database, but such approach would not be scalable in the long run.

I chose mongodb for being the easiest to set up for the challenge.

#### Code Structure

```
.
├── api
│   ├── application
│   │   ├── __init__.py
│   │   ├── resources.py
│   │   └── routes.py
│   ├── domain
│   │   ├── dtos
│   │   │   ├── __init__.py
│   │   │   └── locations.py
│   │   ├── exceptions
│   │   │   ├── exceptions.py
│   │   │   └── __init__.py
│   │   ├── __init__.py
│   │   ├── models
│   │   │   ├── __init__.py
│   │   │   └── location.py
│   │   ├── repositories
│   │   │   ├── __init__.py
│   │   │   └── locations.py
│   │   └── services
│   │       ├── __init__.py
│   │       ├── locations.py
│   │       └── redis_event_handler.py
│   ├── infrastructure
│   │   ├── database
│   │   │   ├── __init__.py
│   │   │   ├── mongo.py
│   │   │   └── redis.py
│   │   └── __init__.py
│   ├── __init__.py
│   └── main.py
├── docker-compose.yaml
├── Dockerfile
├── Documentation.md
├── LICENSE.md
├── poetry.lock
├── pyproject.toml
├── README.md
├── requirements.txt
├── simulation
│   ├── data
│   │   ├── user_a1_location.csv
│   │   └── user_b2_location.csv
│   ├── __init__.py
│   └── simulate.py
└── tests
    ├── __init__.py
    └── test_api.py


```

#### Infrastructure

##### Database

1. MongoDB: to store and persist Locations.
2. Redis: For caching incoming requests and get the average.

##### Framework

Flask.


##### Application

Application is containerized with docker and docker compose.

To install and run application, run the following command: `docker-compose up --build` from the source directory where files where uncompressed.
