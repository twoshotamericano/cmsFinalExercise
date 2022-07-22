from collections import namedtuple
import json
import os
from flask import Flask, render_template, request, url_for, redirect
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import func


class Post(dict):
  def __init__(self,title,author,created_date):
    dict.__init__(self, title=title, author=author, created_date=created_date)   

  def __repr__(self):
    return f"Post({self.title},{self.author},{self.created_date})"


# a=Post("a","b","c")

# Post=namedtuple("Post","title author created_date")
# posts=[
#   Post("Multivariate Stats","Bryan","drr date"),
#   Post("Linear ALgebra","Ankerst","drr date"),
#   Post("Convex Optimisation","Boyd","drr date")
#   ]

# print(json.dumps(posts))