from fastapi import FastAPI, Request, APIRouter, Query, HTTPException, Response
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import matplotlib.pyplot as plt
from tabulate import tabulate
import requests
from bs4 import BeautifulSoup


import os
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

app = FastAPI(debug=True)

# Correct BASE_DIR to be the directory, not the path to main.py
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Set the correct path for the static directory
static_dir = os.path.join(BASE_DIR, "static")
app.mount("/static", StaticFiles(directory=static_dir), name="static")


# app = FastAPI(debug=True)
templates_dir = os.path.join(BASE_DIR, "templates")
templates = Jinja2Templates(directory=templates_dir)

# templates = Jinja2Templates(directory="templates")
# app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/", response_class=HTMLResponse)
def homepage(request: Request):
    content = {'request': request}
    return templates.TemplateResponse("homepage.html", content)

@app.get("/tablet_json", response_class=HTMLResponse)
def SB_json(request: Request):
    content = {'request': request}
    return templates.TemplateResponse("json_content_sb.html", content)

@app.get("/tablet_html", response_class=HTMLResponse)
def NY_html(request: Request):
    content = {'request': request}
    return templates.TemplateResponse("html_content_sb.html", content)

#app for web crawling
@app.get("/SB_tablet_report", response_class=HTMLResponse)
def SB_aggregation(request: Request):
    content = {'request': request}
    return templates.TemplateResponse("html_website_sb.html", content)