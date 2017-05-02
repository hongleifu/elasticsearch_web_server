from flask import Flask, request, render_template, jsonify
from modules import mod_search
from modules import mod_login

'''  BASICAL FUNCTIONS BEGIN  '''

app = Flask(__name__, static_url_path='')
app.config['SECRET_KEY'] = 'super secret key'

@app.route('/')
def default():
    model = [] 
    return render_template('index.html', model=model)
    #return render_template('index.html', model=model)

@app.route('/index')
def index():
    model = [] 
    return render_template('index.html', model=model)
    #return render_template('index.html', model=model)

@app.route('/error', methods=['GET', 'POST'])
def error():
    msg = request.args.get('msg')
    return render_template('error.html',msg=msg)

@app.errorhandler(404)
def page_not_found(e):
    return render_template('error.html',msg=e)


'''  BUSSINESS FUNCTIONS BEGIN  '''

@app.route('/search', methods=['GET','POST'])
def search():
    size = 10
    query_word=""
    if request.method == 'GET':
      query_word=request.args.get('query',"")    
    if request.method == 'POST':
      query_word=request.form.get('query',"")    
    model,query,recommend_keyword = mod_search.service(query_word)
    return render_template('search_result.html', articles=model[:size], query=query, recommend_keyword=recommend_keyword, num=len(model), no=1, size=size, totalsize=len(model))
    #return render_template('search_result.html', articles=model[:size], query=query, recommend_keyword=recommend_keyword, num=len(model), no=1, size=size, totalsize=len(model))

@app.route('/searchpage', methods=['GET'])
def searchpage():
    page_no = int(request.args.get('no'))
    page_size = int(request.args.get('size'))
    start = (page_no - 1) * page_size
    end = page_no * page_size
    query = request.args.get('query')
    model,query,recommend_keyword = mod_search.service(query)
    if model != None:
        return render_template('search_result.html', articles=model[start:end], query=query, recommend_keyword=recommend_keyword, no=page_no, size=page_size, totalsize=len(model))
    else:
        return render_template('search_result.html', articles=model, query=query, recommend_keyword=recommend_keyword, no=page_no, size=0, totalsize=0)

@app.route('/tabs', methods=['GET', 'POST'])
def tabs():
    query=''
    page_no=1
    page_size=10
    if request.method == 'GET':
      page_no = int(request.args.get('no','1'))
      page_size = int(request.args.get('size','10'))
      query = request.args.get('tab', '')
    else:
      page_no = int(request.form.get('no','1'))
      page_size = int(request.form.get('size','10'))
      query = request.form.get('tab', '')
    start = (page_no - 1) * page_size
    end = page_no * page_size
    result,tag = mod_search.service_classify(query)
    #return jsonify(result = result[start:end])
    return render_template('index.html',result = result[start:end],tag=tag)

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
    app.run(host="jinrongdao.com",port=5100,processes=6)
