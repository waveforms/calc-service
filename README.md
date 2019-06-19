# calc-service

## to run in docker
`docker-compose up`

## to run on local file system

### install python 3.7 virtual env
`virtualenv -p python3.7 dockflaskvenv`  
`source dockflaskvenv/bin/activate`  
`cd backend`  
`FLASK_APP=calcservice.py python -m flask run`  

## View

go to http://127.0.0.1:5000/

## React dev directory
The frontend directory holds the code used to build the react application.
React is built and then the build directory contents are copied over into the backend static directory.


