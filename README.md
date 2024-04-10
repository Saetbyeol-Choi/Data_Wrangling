# Careating website using FastAPI

# Run the application using Uvicorn:
pip install uvicorn

# Execute the Uvicorn to run the app:
uvicorn main:app --reload

If main.py is under the folder
uvicorn (folder_name).main:app --reload

# Access the app:
By default, the FastAPI application will be served on http://127.0.0.1:8000. You can open this URL in your web browser. If you defined a route like /"route_name", you can access it directly at http://127.0.0.1:8000/route_name.

