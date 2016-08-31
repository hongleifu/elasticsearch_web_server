from flask import session

def service(request):
  model = {}
  name = request.form['name']
  password = request.form['password']
  session['userinfo'] = {'name':name}
  model['result'] = True
  recommend=[]
  return model,recommend
  #user = mysqldb.User.query.filter_by(name=name,password=password).first()
 # if user is not None:
 # 	session['userinfo'] = {'name':user.name, 'id':user.id}
 # 	model['ret'] = True
 # else:
 # 	model['ret'] = False
