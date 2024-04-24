

# Execute the Uvicorn to run the app:
uvicorn main:app --reload

If main.py is under the folder
uvicorn (folder_name).main:app --reload



# FastAPI Application Setup Guide

This README provides instructions for setting up and running a FastAPI application with Uvicorn as the ASGI server.

## Prerequisites

Before you start, ensure you have Python installed on your system. You can download Python from [python.org](https://www.python.org/downloads/).

## Installation

First, you need to install Uvicorn, which will serve as our ASGI server. Install it using pip:

```
pip install uvicorn
```

## Project Structure

Your project directory should be structured as follows. This example assumes your application's entry point is `main.py` located within a folder named `folder_name`:

```
/your-project-folder
    /folder_name
        main.py
```

## Running the Application
To start the server and run your FastAPI application, follow these instructions:

If main.py is in the root of your project folder, execute:


`uvicorn main:app --reload`

If main.py is under a specific folder (e.g., folder_name), use:

```
uvicorn folder_name.main:app --reload
```

The --reload option makes the server restart after code changes, which is helpful during development.

## Accessing the Application

By default, the application will run on localhost at port 8000. Open your web browser and go to:

```
http://127.0.0.1:8000
```

To access specific routes directly, append the route name to the URL. For example, for a route named `route_name`, visit:

```
http://127.0.0.1:8000/route_name
```

## Additional Resources

- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [Uvicorn Documentation](https://www.uvicorn.org/)
