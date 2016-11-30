from flask import Flask, request, render_template 

from modules import mod_search
from modules import mod_login

'''  BASICAL FUNCTIONS BEGIN  '''

app = Flask(__name__, static_url_path='')
app.config['SECRET_KEY'] = 'super secret key'

@app.route('/')
def default():
    model = [] 
    return render_template('index.html', model=model)

@app.route('/index')
def index():
    model = [] 
    return render_template('index.html', model=model)

@app.route('/error', methods=['GET', 'POST'])
def error():
    msg = request.args.get('msg')
    return render_template('error.html',msg=msg)

@app.errorhandler(404)
def page_not_found(e):
    return render_template('error.html',msg=e)


'''  BUSSINESS FUNCTIONS BEGIN  '''


@app.route('/search', methods=['GET', 'POST'])
def search():
    model,query,recommend_keyword = mod_search.service(request)
    return render_template('search_result.html', model=model,query=query,recommend_keyword=recommend_keyword)

@app.route('/tabs', methods=['POST'])
def tabs():
    model,query,recommend_keyword = mod_search.service(request)
    return render_template('index.html', model=model,query=query,recommend_keyword=recommend_keyword)

@app.route('/login',methods=['GET','POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')
    elif request.method == 'POST':
        model,recommend_content=mod_login.service(request)
        if model['result'] == True:
            return render_template('index.html', recommend_content=recommend_content)
        else:
            return render_template('error.html',msg='login error')

@app.route('/logout',methods=['GET','POST'])
def logout():
    return render_template('index.html')

'''  MAIN ENTRY  '''
if __name__ == '__main__':
    app.debug = True
    app.run(host="0.0.0.0",port=5100,processes=6)
