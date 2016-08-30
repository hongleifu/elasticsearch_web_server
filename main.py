from flask import Flask, request, render_template 
from flask import redirect, url_for

import os
import os.path

from modules import mod_search

'''  BASICAL FUNCTIONS BEGIN  '''

app = Flask(__name__, static_url_path='')

@app.route('/')
#@interceptor(login_required=True)
def default():
#	model = mod_index.service(request)
	model = [] 
	return render_template('index.html', model=model)

@app.route('/index')
#@interceptor(login_required=False)
def index():
	#model = mod_index.service(request)
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
	#return render_template('search_result.html', model=model)
#        print model
#	print render_template('search_result.html', model=model,query=query)
	return render_template('search_result.html', model=model,query=query,recommend_keyword=recommend_keyword)



'''  MAIN ENTRY  '''
if __name__ == '__main__':
	app.debug = True
	app.run(host="127.0.0.1",port=5100)
