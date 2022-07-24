from asyncio.log import logger
from datetime import datetime
from os import environ
from pathlib import Path
from flask import Flask, render_template,jsonify,flash,redirect,request, url_for,session
from flask_session import Session  # https://pythonhosted.org/Flask-Session
import msal
import app_config
import datetime
from collections import namedtuple
import json
from objects.Post import Post as BlogPost
import logger
import os
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import func
from werkzeug.utils import secure_filename
from azure.storage.blob import BlobServiceClient

ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

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
app.config.from_object(app_config)
db = SQLAlchemy(app)
Session(app)
blob_container = app.config['BLOB_CONTAINER']
storage_url = "https://{}.blob.core.windows.net/".format(app.config['BLOB_ACCOUNT'])
blob_service = BlobServiceClient(account_url=storage_url, credential=app.config['BLOB_STORAGE_KEY'])
imageSourceUrl = 'https://'+ app.config['BLOB_ACCOUNT']  + '.blob.core.windows.net/' + app.config['BLOB_CONTAINER']  + '/'

class dbPost(db.Model):
  __tablename__='posts'

  id = db.Column(db.Integer, primary_key=True)
  title = db.Column(db.String(100), nullable=False)
  author = db.Column(db.String(100), nullable=False)    
  created_date = db.Column(db.DateTime(timezone=True),server_default=func.now())
  filename = db.Column(db.String(100), nullable=False)    

  def __repr__(self):
         return '<dbPost {}>'.format(self.body)

  def save_changes(self, file=None):
    if file:            
        filename = secure_filename(file.filename)
        fileExtension = filename.rsplit('.', 1)[1]
        randomFilename = str(uuid.uuid1())
        filename = randomFilename + '.' + fileExtension
        try:
            blob_client=blob_service.get_blob_client(container=blob_container,blob=filename)
            blob_client.upload_blob(file)
            if self.image_path:
                blob_client=blob_service.get_blob_client(container=blob_container,blob=self.image_path)
                blob_client.delete_blob()

        except Exception as err:
            flash(err)
        self.image_path = filename
    db.session.commit()

from werkzeug.middleware.proxy_fix import ProxyFix
app.wsgi_app = ProxyFix(app.wsgi_app, x_proto=1, x_host=1)

@app.route("/")
@app.route("/list")
def posts():
  if not session.get("user"):
    return redirect(url_for("login"))  
  else:
    data=dbPost.query.all()  
  return render_template("list.html",posts=data, imageSource=imageSourceUrl)

@app.route('/delete')
def delete():
  try:
    title=request.args['title']
    data = dbPost.query.filter_by(title=title).first()
    db.session.delete(data)
    db.session.commit()
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
        post=dbPost()
        post.title=title
        post.author=author
        post.created_date=datetime.datetime.strptime(created_date,'%d/%m/%y')

        db.session.add(post)
        db.session.commit()
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
        post=dbPost()
        post.title=title
        post.author=author
        post.created_date=created_date        
        db.session.add(post)
        db.session.commit()
        return redirect(url_for('posts'))
    else:     
      title=request.args['title']             
  except Exception as e:
    app.logger.error(str(e))
    return render_template("error.html",data=str(e))

  data=dbPost.query.filter_by(title=title).first()
  db.session.delete(data)
  db.session.commit()
  return render_template("edit.html",data=data)

@app.route("/upload",methods=("GET","POST"))
def upload(): 
  title=request.args['title']
  if request.method == 'POST':
      # check if the post request has the file part
      if 'file' not in request.files:
          flash('No file part')
          return redirect(request.url)
      file = request.files['file']
      # If the user does not select a file, the browser submits an
      # empty file without a filename.
      if file.filename == '':
          flash('No selected file')
          return redirect(request.url)
      if file and allowed_file(file.filename):
          filename = secure_filename(str(Path(Path.cwd(),file.filename)))
          record=dbPost.query.filter_by(title=title).first()
          try:
                blob_client=blob_service.get_blob_client(container=blob_container,blob=filename)
                blob_client.upload_blob(file)
                if record.filename:
                  try:
                    blob_client=blob_service.get_blob_client(container=blob_container,blob=record.filename)
                    blob_client.delete_blob()
                  except:
                    pass

          except Exception as err:
                flash(err)
          
          record.filename=filename
          db.session.add(record)
          db.session.commit()
          return redirect(url_for('posts'))    
  return render_template("upload.html",data=title)

@app.route("/post")
def post():
    return render_template("post.html")

@app.route("/login")
def login():
    # Technically we could use empty list [] as scopes to do just sign in,
    # here we choose to also collect end user consent upfront
    session["flow"] = _build_auth_code_flow(scopes=app_config.SCOPE)
    session["auth_url"]=session["flow"]["auth_uri"]
    return render_template("login.html", auth_url=session["flow"]["auth_uri"], version=msal.__version__)

@app.route(app_config.REDIRECT_PATH)  # Its absolute URL must match your app's redirect_uri set in AAD
def authorized():
    try:
        cache = _load_cache()
        result = _build_msal_app(cache=cache).acquire_token_by_auth_code_flow(
            session.get("flow", {}), request.args)
        if "error" in result:
            return render_template("auth_error.html", result=result)
        session["user"] = result.get("id_token_claims")
        _save_cache(cache)
    except ValueError:  # Usually caused by CSRF
        pass  # Simply ignore them
    return redirect(url_for("posts",_external=True))

@app.route("/logout")
def logout():
    session.clear()  # Wipe out user and its token cache from session
    return redirect(  # Also logout from your tenant's web session
        app_config.AUTHORITY + "/oauth2/v2.0/logout" +
        "?post_logout_redirect_uri=" + url_for("posts", _external=True))

@app.route("/graphcall")
def graphcall():
    token = _get_token_from_cache(app_config.SCOPE)
    if not token:
        return redirect(url_for("login"))
    graph_data = requests.get(  # Use token to call downstream service
        app_config.ENDPOINT,
        headers={'Authorization': 'Bearer ' + token['access_token']},
        ).json()
    return render_template('display.html', result=graph_data)


def _load_cache():
    cache = msal.SerializableTokenCache()
    if session.get("token_cache"):
        cache.deserialize(session["token_cache"])
    return cache

def _save_cache(cache):
    if cache.has_state_changed:
        session["token_cache"] = cache.serialize()

def _build_msal_app(cache=None, authority=None):
    return msal.ConfidentialClientApplication(
        app_config.CLIENT_ID, authority=authority or app_config.AUTHORITY,
        client_credential=app_config.CLIENT_SECRET, token_cache=cache)

def _build_auth_code_flow(authority=None, scopes=None):
    return _build_msal_app(authority=authority).initiate_auth_code_flow(
        scopes or [],
        redirect_uri=url_for("authorized", _external=True))

def _get_token_from_cache(scope=None):
    cache = _load_cache()  # This web app maintains one cache per session
    cca = _build_msal_app(cache=cache)
    accounts = cca.get_accounts()
    if accounts:  # So all account(s) belong to the current signed-in user
        result = cca.acquire_token_silent(scope, account=accounts[0])
        _save_cache(cache)
        return result

app.jinja_env.globals.update(_build_auth_code_flow=_build_auth_code_flow)  # Used in template



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
  