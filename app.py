from asyncio.log import logger
from datetime import datetime
from os import environ
from flask import Flask, render_template,jsonify,flash,redirect,request, url_for
import datetime
from collections import namedtuple
import json
from objects.Post import Post as BlogPost
import logger
import os

#Post=namedtuple("Post","title author created_date")
data=[
  BlogPost("Multivariate Stats","Bryan",datetime.date.today()),
  BlogPost("Convex Optimisation","Best",datetime.date.today()),
   BlogPost("Linear ALgebra","Nadine",datetime.date.today()),
  ]

def clear_message(title):
  global data
  data=[post for post in data if post['title']!=title]

def get_message(title):
  global data
  return [post for post in data if post['title']==title][0]

app = Flask(__name__)
app.config['SECRET_KEY'] = os.urandom(24).hex()

@app.route("/")
@app.route("/list")
def posts():    
  return render_template("list.html",posts=data)

@app.route('/delete')
def delete():
  try:
    title=request.args['title']
    clear_message(title)
    return redirect(url_for('posts'))
  except Exception as e:
    app.logger.error(str(e))
    return render_template("error.html",data=str(e))

@app.route('/create/', methods=('GET','POST'))
def create():
  try:
    if request.method=='POST':
      title=request.form['title']
      author=request.form['author']
      created_date=request.form['created_date']

      if not title:
        flash("title is required!")
      elif not author:
        flash("author is required")
      elif not created_date:
        flash("crated_date is required")
      else:      
        data.append(BlogPost(title,author,created_date))
        return redirect(url_for('posts'))       
  except Exception as e:
    app.logger.error(str(e))
    return render_template("error.html",data=str(e))
 
  return render_template('create.html')

@app.route("/edit",methods=("GET","POST"))
def edit():
  try:
    if request.method=='POST':
      title=request.form['title']
      author=request.form['author']
      created_date=request.form['created_date']

      if not title:
        flash("title is required!")
      elif not author:
        flash("author is required")
      elif not created_date:
        flash("crated_date is required")
      else:
        data.append(BlogPost(title,author,created_date))
        return redirect(url_for('posts'))
    else:     
      title=request.args['title']
      post=get_message(title)
      clear_message(title)
  except Exception as e:
    app.logger.error(str(e))
    return render_template("error.html",data=str(e))

  return render_template("edit.html",data=post)

@app.route("/post")
def post():
    return render_template("post.html")

@app.before_request 
def before_request_callback(): 
  method = request.method 
  path = request.path 
  app.logger.info(f"{method} called on {path} ")



if __name__=='__main__':
  HOST=environ.get('SERVER_HOST','localhost')
  try:
    PORT=int(environ.get('SERVER_PORT','5555'))
  except ValueError:
    PORT=5555
  app.run(HOST, PORT, debug=True)
  