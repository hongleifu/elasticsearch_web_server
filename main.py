#coding:utf-8
from flask import Flask, request, render_template, jsonify,redirect,url_for
from modules import mod_search
from modules import mod_login

'''  BASICAL FUNCTIONS BEGIN  '''

app = Flask(__name__, static_url_path='')
app.config['SECRET_KEY'] = 'super secret key'

@app.route('/',methods=['GET', 'POST'])
def default():
    return redirect(url_for('tabs'))
    #model = [] 
    #return render_template('index.html', model=model)
    #return render_template('index.html', model=model)

@app.route('/index',methods=['GET', 'POST'])
def index():
    return redirect(url_for('tabs'))
   # model = [] 
   # return render_template('index.html', model=model)

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
    no=1
    size = 10
    query_word=""
    if request.method == 'GET':
      query_word=request.args.get('query',"")    
      no=request.args.get('no',1)    
      size=request.args.get('size',10)    
    if request.method == 'POST':
      query_word=request.form.get('query',"")    
      no=request.form.get('no',1)    
      size=request.form.get('size',10)    
    model,query,recommend_keyword = mod_search.service(query_word)
    return render_template('search_result.html', articles=model[(int(no)-1)*int(size):int(size)], query=query, recommend_keyword=recommend_keyword, num=len(model), no=no, size=size, total_size=len(model))
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
        return render_template('search_result.html', articles=model[start:end], query=query, recommend_keyword=recommend_keyword, no=page_no, size=page_size, total_size=len(model))
    else:
        print "no search result for query:",query
        return render_template('search_result.html', articles=model, query=query, recommend_keyword=recommend_keyword, no=page_no, size=0, total_size=0)

@app.route('/tabs', methods=['GET', 'POST'])
def tabs():
    query=''
    page_no=1
    page_size=10
    if request.method == 'GET':
      page_no = int(request.args.get('no',1))
      page_size = int(request.args.get('size',10))
      query = request.args.get('tab', '法规速递'.decode('utf8'))
    else:
      page_no = int(request.form.get('no',1))
      page_size = int(request.form.get('size',10))
      query = request.form.get('tab', '法规速递'.decode('utf8'))
    start = (page_no - 1) * page_size
    result,tag = mod_search.service_classify(query)
    end = page_no * page_size
    if len(result) < page_no * page_size:
      end=len(result)
    #return jsonify(result = result[start:end])
    return render_template('index.html',result = result[start:end],tag=query,no=page_no, size=page_size,total_size=len(result))

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
