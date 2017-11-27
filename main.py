#coding:utf-8
from flask import Flask, request, render_template, jsonify,redirect,url_for
from modules import mod_search
from modules import mod_login
from modules import mod_adverse
from flask import jsonify

'''  BASICAL FUNCTIONS BEGIN  '''

app = Flask(__name__, static_url_path='')
app.config['SECRET_KEY'] = 'super secret key'

@app.route('/',methods=['GET', 'POST'])
def default():
    return redirect(url_for('tabs'))

@app.route('/index',methods=['GET', 'POST'])
def index():
    return redirect(url_for('tabs'))

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
    page_no=1
    page_size = 10
    query_word=""
    if request.method == 'GET':
        query_word=request.args.get('query',"")    
        page_no=int(request.args.get('no',1))    
        page_size=int(request.args.get('size',10))    
    if request.method == 'POST':
        query_word=request.form.get('query',"")    
        page_no=int(request.form.get('no',1))    
        page_size=int(request.form.get('size',10)) 
    start=(page_no-1)*page_size
    end=page_no*page_size
    model,query,recommend_keyword,adverses = mod_search.service(query_word,start,end)
    return render_template('search_result.html', articles=model[start:end], query=query, \
        recommend_keyword=recommend_keyword, num=len(model), no=page_no, size=page_size, total_size=len(model))

@app.route('/click_adverse', methods=['POST'])
def click_adverse():
    result=mod_adverse.service(request)
    return result 

@app.route('/searchpage', methods=['GET'])
def searchpage():
    page_no = int(request.args.get('no'))
    page_size = int(request.args.get('size'))
    start = (page_no - 1) * page_size
    end = page_no * page_size
    query = request.args.get('query')
    model,query,recommend_keyword,adverses = mod_search.service(query,start,end)
    if model != None:
        return render_template('search_result.html', articles=model[start:end], query=query, \
            recommend_keyword=recommend_keyword, no=page_no, size=page_size, total_size=len(model),adverses=adverses)
    else:
        print "no search result for query:",query
        return render_template('search_result.html', articles=model, query=query, \
            recommend_keyword=recommend_keyword,no=page_no, size=0, total_size=0,adverses=adverses)

@app.route('/tabs', methods=['GET', 'POST'])
def tabs():
    query=''
    page_no=1
    page_size=10
    if request.method == 'GET':
        page_no = int(request.args.get('no',1))
        page_size = int(request.args.get('size',10))
        query = request.args.get('tab', '0')
    else:
        page_no = int(request.form.get('no',1))
        page_size = int(request.form.get('size',10))
        query = request.form.get('tab', '0')
    start = (page_no - 1) * page_size
    end = page_no * page_size
    result,tag = mod_search.service_classify(query,start,end)
    if len(result) < page_no * page_size:
        end=len(result)
    print "search result:",len(result),"start:",start,"end:",end
    return render_template('index.html',result_list = result[start:end],\
        tag=query,no=page_no, size=page_size,total_size=len(result))

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
    app.run(host="0.0.0.0",port=5100,threaded=True)
