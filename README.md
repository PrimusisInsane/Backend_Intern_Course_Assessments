# Week 2- Using FastAPI and adding custom Starlette, add endpoints, middleware and updated docs
 
  ###  The project package contains middlewares, http exceptions, routers in its api, currently using fastapi and use CRUD operations on users (/users) and hospital tasks (/tasks) and also projects (/projects)


## Key Features

*  Creating, reading, updating and deleting users on the app
*  Creating, reading, updating and deleting tasks just as well
*  Uses pydantic and exceptions to clean out the proper looking error messages
*  Built in id_number as we assign users and tasks and user the id number to read, update or delete the information. 
* Starlette middleware to record response time, method, path etc

## Requirements

* Requirements.txt will give details of all those required files 


## End point Documentation 
* http://127.0.0.1:8000/users/1  This for example gives you the user's details if their id_number is 1. Simply replacing users with projects and tasks which give you the details for said task or project
for e.g.
* http://127.0.0.1:8000/tasks/1
 * http://127.0.0.1:8000/projects/1
* http://127.0.0.1:8000/projects
* http://127.0.0.1:8000/tasks
* http://127.0.0.1:8000/users
 * http://127.0.0.1:8000/users/1
* http://127.0.0.1:8000/docs - Just loads up FastAPI's Swagger UI

 ### Ofcourse you will have to create tables from the start for the .../1 endpoint to work, otherwise you will get .....not found error!!! 





 ## API Section

* Upon creating, let's say a user, we get something like this on the response
```JSON
{
  "message": "User created",
  "user": {
    "name": "Pratham",
    "email": "pratham432@gmail.com",
    "age": 25,
    "id": 1
  }
}
```

* Upon updating the very same user, this is the response
```JSON
{
  "message": "User updated",
  "user": {
    "name": "Pratham",
    "email": "pratham4342@gmail.com",
    "age": 25,
    "id": 1
  }
}
```


* And Deleting the user gets: 
```JSON
{
  "message": "User deleted",
  "user": {
    "name": "Pratham",
    "email": "pratham4342@gmail.com",
    "age": 25,
    "id": 1
  }
}
```

#### To just get to "Pratham" details the URL would be  

* http://127.0.0.1:8000/users/1    WE USE METHODS LIKE /PUT, /POST, /GET, /DELETE to operate these datas. 

