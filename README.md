# Social Media Services
A simple social media service platform with micro service architecture contains following services:

1. Authentication and user management service
2. Post Service
3. User Interaction Service
4. Moderation and Analysis Service
5. User Engagement Service

This repository is structured as a mono repo for all micro services mentioned above.
Every service is located in a folder suffixed with the name `<SERVICE_NAME>-service`

No module is shared between any two services. Every service is almost containing the similar structure. And the common service structure is following:

```
|service1-root-folder
    |--main.py
    |--settings.py
    |--pyproject.toml
    |--requirements.in
    |--requirements.txt
    |--Dockerfile
    |--docker-compose.yaml
    |--apps
        |--migrations
        |--core
            |--__init__.py
            |--databases.py
            |--enums.py
            |--mail.py
            |--models.py
            |--redis.py
            |--security.py
            |--tests.py
        |__app1
            |--__init__.py
            |--models.py
            |--schemas.py
            |--signals.py
            |--views.py
            |--schedulers.py
            |--tests.py
            |--events
                |--__init__.py
                |--consumers.py
                |--processors.py
                |--producers.py
        |--app2
        |.......
        |.......
        |--appN
|service-2-root-folder
|service-3-root-folder
|service-4-root-folder
|service-5-root-folder

```

## Tools and Technologies
* Language: Python version 3.10
* Framework: FastAPI
* Database: Postgres
* Database ORM: Tortoise-orm (Fully Async)
* Cache Server: Redis
* Message Broker: Redis
* Server: uvicorn
* Scheduler: Python scheduler


## Execution
To fire up the microservices you need to execute following commands from the root of the project:

```shell
    docker compose -f docker-compose-local.yaml up --build
```


Starting up the servers you'll get following services running on different ports and their swagger docs can be found visiting following:

1. Authentication service (http://0.0.0.0:8000/docs)
2. Post service (http://0.0.0.0:8001/docs)
3. Interaction service (http://0.0.0.0:8002/docs)
4. Moderation service (http://0.0.0.0:8003/docs)
5. Engagement service (http://0.0.0.0:8004/docs)


## Available Service Features


### Authentication Service Features:
* Sign up
* Sign in
* Profile update
* Profile detail
* User connect and disconnect
* User connection lists
* Change Password
* Token Verify

### Post Service Features:
* Post create
* Post lists
* Post update
* Post delete

### Interaction Service Features:
* Comment add
* Comment update
* Comment delete
* Comment detail
* Reaction add
* Reaction delete
* Post view

### User Engagement Service Features:
* User Activity Profile


### Moderation and Analysis
Currently it has no visible functionality. All it is containing is bussiness logic
related functionality

### Funtionality test flow
```
Need user registration to add users into the system from the authentication service. Then users can obtain token from the login endpoint. After that they need to create Post using the post service. Then authenticated users can use user interaction endpoints to comment, react and view posts. Users can connect other users from authentication service. Authenticated users can also see their activity profile from the user engagement service.
```

## Service to Service Communication
We've used asynchronous event streaming to communicate between services. But to authenticate for all api endpoints we've used token verification from authentication service.

Services are producing and consuming different events independently from different micro services. Then whoever is
interested on those events listens and takes actions according to that.

Here we've used redis group messaging instead of Pubsub as we wanted to ensure services who are interested to certain events can get the message atleast once even if they were down for a certain duration. As soon as they are live, they'll get the last checkpoint from where they didn't listen any new events.

As these services need continuous and real time events, so we implemented our event consumers to listen events continously by running event listeners as cron jobs.
Event producers are connected on demand when they need to fire event message using the Redis client.

All the endpoints and database connections of these services are fully asynchronous to reduce waiting times for others.


## Limitations or rooms of improvements

There are lots of missing pieces for these microservices. Some of the vitals are as following:

1. We're missing the API gateway service to serve and secure all the available microservices efficiently.
2. Unit and integration tests are missing for all the services due to lack of allocated time
3. Linting, type checking and code quality related tests are not ensured
4. Package upgrade and management is not automatic
5. Although it is a social media service related application, still it is missing file handling or use of files.
6. Content analysis is faked with a random function that randomly choose a post or comment and take moderation actions like delelting the content. This should be replaced with a real content analysis functionality.
7. NFT model is genrated for posts with the status `POSTED`. And we've generated and saved the information for the blockhcain to mint it as a `ERC1155` NFT.
8. We're generating NFT data for Post and Post Comments' information as `data` in `PostNFT` and `CommentNFT` model but we're missing functionality for uploading it on any `IPFS` service and only then we'll get `tokenUri` for the `ERC1155` token. `tokenUri` will be the only unique aattribute for these NFTs saved in blockchain.
9. We're missing Service interface to integrate these microservices with blockchain.
10. User recommendation service is not integrated with existing services.
11. Needs to implement more fine tuned business logic to make features more smoother.
12. Notification frameworks like - Firebase or Apple notification could be used to notify users instantly on devices.