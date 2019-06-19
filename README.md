# Calc-service
A calculation service where a user can provide a binary tree, and the service will return the sum of the longest path.

1. user can register an account and login with username(email)/password
2. after user login, user will have the access to the service to do maxSum calculation
3. user can pass the tree to backend service
4. the whole application runs in an isolate docker environment
5. user can add new nodes to the tree.
5. the applicatiion makes use of json so it can hold a large tree in the browser. Mysql is on the server side so the server is also capable of holding large trees.
6. the system can be configured to run behind nginx and gnuserve to handle large numbers of users.

- create react app front end
- flask business layer
- mysql database

## To run in docker
`docker-compose up`

## To run on local file system

### Install python 3.7 virtual env
`virtualenv -p python3.7 dockflaskvenv`  
`source dockflaskvenv/bin/activate`  
`cd backend`  
`FLASK_APP=calcservice.py python -m flask run`  

## View

go to http://127.0.0.1:5000/

## React dev directory

The frontend directory holds the code used to build the react application.
There is no need to run the react the code in frontend unless you are going go modify the frontend.
React is built and then the build directory contents are copied over into the backend static directory.

## Testing

### backend
The backend uses the pytest testing framework.
To test the flask code run `pytest -v` from within a development virtual environment.

## frontend
The frontend uses the Jest and Enzyme testing frameworks.
The front end is written in create react app so you can run test with `yarn test`

