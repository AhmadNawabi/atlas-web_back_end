#!/usr/bin/env python3
""" API v1 views package initialization """
from flask import Blueprint

app_views = Blueprint("app_views", __name__, url_prefix="/api/v1")

from api.v1.views.index import *
from api.v1.views.users import *

User.load_from_file()

# Import session_auth views to register the routes
from api.v1.views.session_auth import *
