# Django Scheduling

An API for task and schedule management written with Python and Django. The backend uses PostgresSQL for storing
data and Redis for per-user cacheing of schedules. The entire setup is containerized and can be run with a single
command using Docker.

## Installation

Install docker for your operating system:
https://docs.docker.com/get-started/get-docker/

## Usage

Open a linux terminal application, such as shell via WSL or Konsole, and run the following command:
```sudo docker compose up```

The server will be available for requests on localhost port 8000. The Django Admin panel can also be
accessed to monitor and edit model objects on localhost:8000/admin/.

## API Documentation

https://documenter.getpostman.com/view/18040691/2sB3B7NDTy
https://documenter.getpostman.com/view/18040691/2sB3B7NDTx

## License

[MIT](https://choosealicense.com/licenses/mit/)
