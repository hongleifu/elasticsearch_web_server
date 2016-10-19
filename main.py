from flask import Flask, request, render_template 
from flask import redirect, url_for

import os
import os.path

from modules import mod_search
from modules import mod_login
from modules import mod_logout

'''  BASICAL FUNCTIONS BEGIN  '''

app = Flask(__name__, static_url_path='')
#app.secret_key = "super secret key"
app.config['SECRET_KEY'] = 'super secret key'

@app.route('/')
#@interceptor(login_required=True)
def default():
  model = [] 
  return render_template('index.html', model=model)

@app.route('/index')
#@interceptor(login_required=False)
def index():
  model = [] 
  return render_template('index.html', model=model)

@app.route('/error', methods=['GET', 'POST'])
#@interceptor(login_required=False)
def error():
  msg = request.args.get('msg')
  return render_template('error.html',msg=msg)

@app.errorhandler(404)
def page_not_found(e):
  return render_template('error.html',msg=e)


'''  BUSSINESS FUNCTIONS BEGIN  '''


@app.route('/search', methods=['GET', 'POST'])
#@interceptor(login_required=True)
def search():
  model,query,recommend_keyword = mod_search.service(request)
  return render_template('search_result.html', model=model,query=query,recommend_keyword=recommend_keyword)

@app.route('/login',methods=['GET','POST'])
def login():
  #if method is get, then show login page only.if post, then deal login request
  if request.method == 'GET':
    return render_template('login.html')
  elif request.method == 'POST':
    model,recommend_content=mod_login.service(request)
    if model['result'] == True:
      return render_template('index.html', recommend_content=recommend_content)
    else:
      return render_template('error.html',msg='login error')
      #return render_template('index.html',model=model,recommend=recommend_content)

@app.route('/logout',methods=['GET','POST'])
def logout():
  model=mod_logout.service(request)
  return render_template('index.html')

'''  MAIN ENTRY  '''
if __name__ == '__main__':
  app.debug = True
  app.run(host="127.0.0.1",port=5100,processes=6)
