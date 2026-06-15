

## Scripts 



### app/main.py

* Starts the FastAPI app and connects everything together.
* Creates the FastAPI instance
* Loads config (app name, debug)
* Registers routers (users, tasks, health)
* Adds middleware (request timing)
* Adds global exception handlers
* Defines root endpoint /

### app/core/config.py
* Handles environment settings.
* Loads .env file using python-dotenv
* Stores app configuration like:
* APP_NAME
* DEBUG
* Provides settings object used in main.py


### app/api/routers/health.py
* Simple system check endpoint.
* Returns API status (e.g. "API is running")
* Used to verify server is alive


### app/api/routers/users.py
* User CRUD logic (in-memory).
* Stores users in users_db list
* Supports:
- Create user (POST)
- Get all users (GET)
- Get user by ID (GET)
- Update user (PUT)
- Delete user (DELETE)
* Adds background task logging for user creation


### app/api/routers/tasks.py
* Task CRUD logic (in-memory).
* Stores tasks in tasks_db list
* Supports:
- Create task (POST)
- Get all tasks (GET)
- Get task by ID (GET)
- Update task (PUT)
- Delete task (DELETE)



### app/api/routers/project.py
* Project CRUD logic (in-memory).
* Stores projects in prjects_db list
* Suports: 
- Create project(POST)
- Get all projects( GET)
- Get project by ID (GET)
- Update project (PUT)
- Delete project(DELETE)



### app/middleware/middleware_1.py
* Request timing middleware.
* Measures how long each request takes
* Logs:
* HTTP method
* URL path
* response time
* Runs automatically on every request


### app/exceptions/exception_handlers.py
* Custom error formatting layer.
* Handles:
* HTTP exceptions (404, 400, etc.)
* Validation errors (bad JSON / wrong types)
* Returns consistent JSON error format instead of default FastAPI errors


### .env
* Environment variables file.
* Stores config like:
* APP_NAME
* DEBUG
* Keeps config separate from code


### requirements.txt
* Lists dependencies.
* FastAPI
* Uvicorn
* Pydantic
* python-dotenv
etc.