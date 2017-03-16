#!/usr/bin/env python
# coding:utf-8
import sys
import MySQLdb as mysql
from flask import  Flask,request,render_template,redirect
import time
import traceback
import logging
#new app
app = Flask(__name__)

conn = mysql.connect(db='reboot',user='root',passwd='123456',host='127.0.0.1',port=3306,charset="utf8")
conn.autocommit(True)
cur = conn.cursor()
#用户列表
@app.route('/userlist')
def index():
    users=[]
    fileds=['id','username','name_cn','email','mobile']
    try:
        sql = 'select  %s from user'% ','.join(fileds)
        cur.execute(sql)
        result = cur.fetchall()
        # for row in result:
        #     user = {}
        #     for i , k  in enumerate(fileds):
        #         user[k] = row[i]
        #     users.append(user)
        users=[dict((k,row[i]) for i ,k in enumerate(fileds)) for row in result]
        return  render_template('userlist.html',users=users)
    except:
        errmsg= 'select userlist failed'
        print traceback.print_exc()
        return  render_template('userlist.html',result=errmsg)

#注册
@app.route('/register',methods=['GET','POST'])
def register():
    if request.method =='POST':
        data = {}
        data['username'] = request.form.get('username',None)
        data['name_cn'] = request.form.get('name_cn',None)
        data['email'] = request.form.get('email')
        data['mobile'] = request.form.get('mobile')
        data['role'] = request.form.get('role')
        data['status'] = request.form.get('status')
        data['password'] = request.form.get('password',None)
        data['repass']=request.form.get('repass',None)
        data['create_time']=time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
        #data = request.get_json()
        #print data
        fields =['username','name_cn','email','mobile','role','status','password','create_time']
        if not data['username'] or not data['password'] or not data['role']:
            errmsg = 'username or passwd or role not null'
            return render_template('register.html',result=errmsg)
        if data['password'] != data['repass']:
            errmsg = 'error'
            return render_template('register.html',result=errmsg)
        try:
            #print ','.join(fileds)
            #print ','.join(["%s" %data[x]for x in fileds])
            #data= [data[x]for x in fileds]
            #print data
            #print ','.join(data)
            #print type(data[0])
            sql = 'insert into user(%s) values (%s)' %(','.join(fields),','.join(['"%s"' % data[x] for x in fields]))
            #sql ="insert into user(username,name_cn,email,mobile,role,status,password,create_time) values ('333','2','2','8','admin','0','2','2017-03-11 09:51:40')"
            print sql
            cur.execute(sql)
            #return 'Some response'
            return redirect('/userinfo?username=%s' %data['username'])
            #return render_template('register.html')
        except:
            errmsg = 'insert failed'
            print traceback.print_exc()
            render_template('register.html',result=errmsg)
    else:
        return render_template('register.html')


#获取单个用户信息，注册成功传username作为where条件，查询这条数据 更新操作需传id来获取数据
@app.route('/userinfo')
def userinfo():
    where={}
    where['id']=request.args.get('id',None)
    where['username']=request.args.get('username',None)
    #print  where['username'], where['id']
    if not where['id'] and not where['username']:
        errmsg = 'must hava a where'
        return render_template('userinfo.html',result=errmsg)
    if where['id'] and not where['username']:
        condition = 'id = "%(id)s"' %where
    if where['username'] and not where ['id']:
        condition = 'username="%(username)s"' %where
    fields = ['id','username','name_cn','email','mobile']
    try:
        sql = 'select %s from user where %s' %(','.join(fields),condition)
        cur.execute(sql)
        res = cur.fetchone()
        user={}
        for i ,k in enumerate(fields):
            user[k]=res[i]
        #字典生成式的方式
        #user=dict((k,res[i]) for i ,k in enumerate(fields))
        return  render_template('userinfo.html',user=user)
    except:
        errmsg = 'get one failed'
        print traceback.print_exc()
        return  render_template('userinfo.html',request=errmsg)
@app.route('/update',methods=['GET','POST'])
def update():
    if request.method == 'POST':
        print request.form
        data = dict(request.form)#这个会返回一个字典
        #print data
        conditions = ["%s='%s'" %(k,v[0]) for k,v in data.items()]
        sql = 'update user set %s where id = %s' %(','.join(conditions),data['id'][0])
        print sql
        cur.execute(sql)
        return  redirect('/userlist')
    else:
        id = request.args.get('id',None)
        if not id:
            errmsg = "must have id"
            return render_template("update.html",result=errmsg)
        fileds = ['id','username','name_cn','email','mobile']
        try:
            sql = "select %s from user where id = %s" %(','.join(fileds),id)
            cur.execute(sql)
            res = cur.fetchone()
            # user = {}
            # for i,k in enumerate(fileds):
            #     user[k] = res[i]
            user = dict((k,res[i])for i,k in enumerate(fileds))
            return render_template('update.html',user=user)
        except:
            errmsg = "get one faild"
            print traceback.print_exc()
            return render_template('update.html',result=errmsg)

@app.route('/delete',methods=['GET','POST'])
def delete():
    id = request.args.get('id',None)
    if not id:
        errmsg = "must have id"
        return render_template("update.html",result=errmsg)
    else:
        sql = 'delete from user where id= %s'%id
        cur.execute(sql)
        return redirect('/userlist')

if __name__=='__main__':
    app.run(host='127.0.0.1',port=9092,debug=True)
