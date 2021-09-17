# bunkalog-backend
API server for bunkalog app

## Build Instructions
Use the given Dockerfile to build the container and run
```bash
docker build -t bunkalog-backend .
```

## Deployment Instructions
The app is deployed as a container using heroku.
```bash
heroku container:push web
heroku container:release web
```

For local execution, either execute directly or build docker container and run.

## Execution Instructions
The app needs two environment variables to execute

* PORT
This is used by heroku to specify the port on which the app must serve.
Since the port is always read, export PORT when working on local system.
* MONGODB\_PASSWORD
This is used to specify the password to access the database.
Set it in env file if running locally and use heroku config to set it on production.

