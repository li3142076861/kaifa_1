from flask import Flask, render_template, request, redirect
import pymysql

#登录板块

app = Flask("代办项网站")
def get_conn():
    # 建立与mysql连接
    conn = pymysql.connect(host="127.0.0.1", user="root", password="123456", db="超市仓储管理信息系统", charset="utf8")
    # c创建游标A
    cursor = conn.cursor()
    return conn, cursor

def close_conn(conn, cursor):  # 关闭模块
    if cursor:
        cursor.close()
    if conn:
        conn.close()

def query(sql, *args):  # 查询模块
    """
    :param sql:
    :param args:
    :return:
    """
    conn, cursor = get_conn()
    cursor.execute(sql, args)
    res1 = cursor.fetchall()
    conn.commit()
    close_conn(conn, cursor)
    return res1

def get_user1(username, password):  # 从数据库中查询用户名和密码
    sql = "select id from sys_user where username= '" + username + "' and password= '" + password + "'"
    res1 = query(sql)
    return res1

# 写一个函数来处理浏览器发送过的请求，请求到/是自动执行这个函数
@app.route('/')  # 必须加上路由，否则访问和函数没有关联,当访问到127.0.0.1：5000/，执行函数
def index0():
    return render_template('login.html')

@app.route('/login', methods=['post'])
def login():
    username = request.form.get('username')  # 接收form表单传参
    password = request.form.get('password')
    res1 = get_user1(username, password)
    if res1:
        return render_template('主页面.html')
    else:
        return render_template('login.html', msg='登录失败')

@app.route('/主页面')
def 主页面():
    return render_template('主页面.html')


def conn():
    conn = pymysql.connect(
        host="127.0.0.1",
        user='root',
        password='123456',
        port=3306,
        db='超市仓储管理信息系统',
        charset='utf8'
    )
    return conn

#入库管理
@app.route('/ruku')
def ruku():
    return render_template('入库管理.html')

#排序,修改数据库的信息
def paixu_rukudan():
    conn1 = conn()
    sql="""
    select * from rukudan
    order by id asc
    """
    cursor = conn1.cursor(pymysql.cursors.DictCursor)
    cursor.execute(sql)
    return cursor.fetchall()

def select_rukudan(id):
    conn1 = conn()
    #从数据库查询单条数据
    sql = f"""
        select * from rukudan
        where id = {id}
        """
    cursor = conn1.cursor(pymysql.cursors.DictCursor)
    cursor.execute(sql)
    return cursor.fetchone()

def insert_rukudan(xuhao, mingcheng, guige, danwei, shuliang,danjia,jine,beizhu):
    #新增数据到mysql
    conn1 = conn()
    sql =f"""
       insert into rukudan
       (xuhao, mingcheng, guige, danwei, shuliang,danjia,jine,beizhu)
       values('{xuhao}','{mingcheng}','{guige}','{danwei}','{shuliang}','{danjia}','{jine}','{beizhu}')
       """
    cursor = conn1.cursor()
    cursor.execute(sql)
    conn1.commit()

def update_rukudan(id,xuhao, mingcheng, guige, danwei, shuliang,danjia,jine,beizhu):
    #更新数据
    conn1 = conn()
    sql = f"""
        update rukudan
        set xuhao='{xuhao}',mingcheng='{mingcheng}',guige='{guige}',danwei='{danwei}',shuliang='{shuliang}',danjia='{danjia}',jine='{jine}',beizhu='{beizhu}'
        where id={id}
        """
    cursor = conn1.cursor()
    cursor.execute(sql)
    conn1.commit()

def delete_rukudan(id):
    #删除数据库id的记录
    conn1 = conn()
    sql = f"""
        delete from rukudan
        where id={id}
        """
    cursor = conn1.cursor()
    cursor.execute(sql)
    conn1.commit()

@app.route("/delete_rukudan", methods=["GET"])
def delete_ruku():
    id = request.args.get("id")
    delete_rukudan(id)
    return redirect("/rukudan")

@app.route("/入库单修改", methods=["GET", "POST"])
def edit_rukudan():
    id = request.args.get("id")
    data = select_rukudan(id)
    if request.method == "POST":
        xuhao = request.form.get("xuhao")
        mingcheng = request.form.get("mingcheng")
        guige = request.form.get("guige")
        danwei = request.form.get("danwei")
        shuliang = request.form.get("shuliang")
        danjia = request.form.get("danjia")
        jine = request.form.get("jine")
        beizhu = request.form.get("beizhu")
        update_rukudan(id,xuhao, mingcheng, guige, danwei, shuliang,danjia,jine,beizhu)
        return redirect("/rukudan")

    return render_template("入库管理---入库单修改.html", data=data)

@app.route('/rukudan', methods=["GET","POST"])
def index_rukudan():
    if request.method == "POST":
        xuhao = request.form.get("xuhao")
        mingcheng = request.form.get("mingcheng")
        guige = request.form.get("guige")
        danwei = request.form.get("danwei")
        shuliang = request.form.get("shuliang")
        danjia = request.form.get("danjia")
        jine = request.form.get("jine")
        beizhu = request.form.get("beizhu")
        insert_rukudan(xuhao, mingcheng, guige, danwei, shuliang,danjia,jine,beizhu)
    datas=paixu_rukudan()
    return render_template("入库管理---生成入库单.html", datas=datas)

@app.route('/生成入库单', methods = ["GET", "POST"])
def rukudanchaxun():
    datas = paixu_rukudan()
    return render_template("入库管理---生成入库单.html", datas=datas)



#出库管理
@app.route('/chuku')
def chuku():
    return render_template('出库管理.html')

#排序,修改数据库的信息
def paixu_chukudan():
    conn1 = conn()
    sql="""
    select * from chukudan
    order by id asc
    """
    cursor = conn1.cursor(pymysql.cursors.DictCursor)
    cursor.execute(sql)
    return cursor.fetchall()

def select_chukudan(id):
    #从数据库查询单条数据
    conn1 = conn()
    sql = f"""
        select * from chukudan
        where id = {id}
        """
    cursor = conn1.cursor(pymysql.cursors.DictCursor)
    cursor.execute(sql)
    return cursor.fetchone()

def insert_chukudan(xuhao,mingcheng,guige,danwei,shuliang,danjia,jine,beizhu):
    #新增数据到mysql
    conn1 = conn()
    sql =f"""
       insert into chukudan
       (xuhao,mingcheng,guige,danwei,shuliang,danjia,jine,beizhu)
       values('{xuhao}','{mingcheng}','{guige}','{danwei}','{shuliang}','{danjia}','{jine}','{beizhu}')
       """
    cursor = conn1.cursor()
    cursor.execute(sql)
    conn1.commit()

def delete_chukudan(id):
    #删除数据库id的记录
    conn1 = conn()
    sql = f"""
        delete from chukudan
        where id={id}
        """
    cursor = conn1.cursor()
    cursor.execute(sql)
    conn1.commit()

def update_chukudan(id,xuhao,mingcheng,guige,danwei,shuliang,danjia,jine,beizhu):
    #修改数据
    conn1 = conn()
    sql = f"""
        update chukudan
        set xuhao='{xuhao}',mingcheng='{mingcheng}',guige='{guige}',danwei='{danwei}',shuliang='{shuliang}',danjia='{danjia}',jine='{jine}',beizhu='{beizhu}'
        where id={id}
        """
    cursor = conn1.cursor()
    cursor.execute(sql)
    conn1.commit()

#删除数据
@app.route("/delete_chukudan", methods=["GET"])
def delete_chuku():
    id = request.args.get("id")
    delete_chukudan(id)
    return redirect("/chukudan")

#修改数据
@app.route("/出库单修改", methods=["GET", "POST"])
def edit_chukudan():
    id = request.args.get("id")
    data = select_chukudan(id)
    if request.method == "POST":
        xuhao = request.form.get("xuhao")
        mingcheng = request.form.get("mingcheng")
        guige = request.form.get("guige")
        danwei = request.form.get("danwei")
        shuliang = request.form.get("shuliang")
        danjia = request.form.get("danjia")
        jine = request.form.get("jine")
        beizhu = request.form.get("beizhu")
        update_chukudan(id,xuhao, mingcheng, guige, danwei, shuliang,danjia,jine,beizhu)
        return redirect("/chukudan")

    return render_template("出库管理---出库单修改.html", data=data)

#增加数据
@app.route('/chukudan', methods=["GET","POST"])
def index_chukudan():
    if request.method == "POST":
        xuhao = request.form.get("xuhao")
        mingcheng = request.form.get("mingcheng")
        guige = request.form.get("guige")
        danwei = request.form.get("danwei")
        shuliang = request.form.get("shuliang")
        danjia = request.form.get("danjia")
        jine = request.form.get("jine")
        beizhu = request.form.get("beizhu")
        insert_chukudan(xuhao, mingcheng, guige, danwei, shuliang,danjia,jine,beizhu)
    datas=paixu_chukudan()
    return render_template("出库管理---生成出库单.html", datas=datas)

@app.route('/生成出库单', methods = ["GET", "POST"])
def chukudanchaxun():
    datas = paixu_chukudan()
    return render_template("出库管理---生成出库单.html", datas=datas)


#在库管理
@app.route('/zaiku')
def zaiku():
    return render_template('在库管理.html')

#排序,修改数据库的信息
def paixu_pandiandan():
    conn1 = conn()
    sql="""
    select * from pandiandan
    order by id asc
    """
    cursor = conn1.cursor(pymysql.cursors.DictCursor)
    cursor.execute(sql)
    return cursor.fetchall()

def select_pandiandan(id):
    #从数据库查询单条数据
    conn1 = conn()
    sql = f"""
        select * from pandiandan
        where id = {id}
        """
    cursor = conn1.cursor(pymysql.cursors.DictCursor)
    cursor.execute(sql)
    return cursor.fetchone()

def insert_pandiandan(xuhao,chanpinmingcheng,chanpinguige,zhangmianshuliang,shicunshuliang,chazhi,baozhiqi,daoqiri,beizhu):
    #新增数据到mysql
    conn1 = conn()
    sql =f"""
       insert into pandiandan
       (xuhao,chanpinmingcheng,chanpinguige,zhangmianshuliang,shicunshuliang,chazhi,baozhiqi,daoqiri,beizhu)
       values('{xuhao}','{chanpinmingcheng}','{chanpinguige}','{zhangmianshuliang}','{shicunshuliang}','{chazhi}','{baozhiqi}','{daoqiri}','{beizhu}')
       """
    cursor = conn1.cursor()
    cursor.execute(sql)
    conn1.commit()

def delete_pandiandan(id):
    #删除数据库id的记录
    conn1 = conn()
    sql = f"""
        delete from pandiandan
        where id={id}
        """
    cursor = conn1.cursor()
    cursor.execute(sql)
    conn1.commit()

def update_pandiandan(id,xuhao,chanpinmingcheng,chanpinguige,zhangmianshuliang,shicunshuliang,chazhi,baozhiqi,daoqiri,beizhu):
    #修改数据
    conn1 = conn()
    sql = f"""
        update pandiandan
        set xuhao='{xuhao}',chanpinmingcheng='{chanpinmingcheng}',chanpinguige='{chanpinguige}',zhangmianshuliang='{zhangmianshuliang}',shicunshuliang='{shicunshuliang}',chazhi='{chazhi}',baozhiqi='{baozhiqi}',daoqiri='{daoqiri}',beizhu='{beizhu}'
        where id={id}
        """
    cursor = conn1.cursor()
    cursor.execute(sql)
    conn1.commit()

#删除数据
@app.route("/delete_pandiandan", methods=["GET"])
def delete_pandian():
    id = request.args.get("id")
    delete_pandiandan(id)
    return redirect("/pandiandan")

#修改数据
@app.route("/盘点单修改", methods=["GET", "POST"])
def edit_pandiandan():
    id = request.args.get("id")
    data = select_pandiandan(id)
    if request.method == "POST":
        xuhao = request.form.get("xuhao")
        chanpinmingcheng = request.form.get("chanpinmingcheng")
        chanpinguige = request.form.get("chanpinguige")
        zhangmianshuliang = request.form.get("zhangmianshuliang")
        shicunshuliang = request.form.get("shicunshuliang")
        chazhi = request.form.get("chazhi")
        baozhiqi = request.form.get("baozhiqi")
        daoqiri = request.form.get("daoqiri")
        beizhu = request.form.get("beizhu")
        update_pandiandan(id,xuhao, chanpinmingcheng, chanpinguige, zhangmianshuliang, shicunshuliang,chazhi,baozhiqi,daoqiri,beizhu)
        return redirect("/pandiandan")

    return render_template("在库管理---盘点单修改.html", data=data)

#增加数据
@app.route('/pandiandan', methods=["GET","POST"])
def index_pandiandan():
    if request.method == "POST":
        xuhao = request.form.get("xuhao")
        chanpinmingcheng = request.form.get("chanpinmingcheng")
        chanpinguige = request.form.get("chanpinguige")
        zhangmianshuliang = request.form.get("zhangmianshuliang")
        shicunshuliang = request.form.get("shicunshuliang")
        chazhi = request.form.get("chazhi")
        baozhiqi = request.form.get("baozhiqi")
        daoqiri = request.form.get("daoqiri")
        beizhu = request.form.get("beizhu")
        insert_pandiandan(xuhao, chanpinmingcheng, chanpinguige, zhangmianshuliang, shicunshuliang,chazhi,baozhiqi,daoqiri,beizhu)
    datas=paixu_pandiandan()
    return render_template("在库管理---生成盘点单.html", datas=datas)

@app.route('/生成盘点单', methods = ["GET", "POST"])
def pandiandanchaxun():
    datas = paixu_pandiandan()
    return render_template("在库管理---生成盘点单.html", datas=datas)

#缺货单

def paixu_quehuodan():
    conn1 = conn()
    sql="""
    select * from quehuodan
    order by id asc
    """
    cursor = conn1.cursor(pymysql.cursors.DictCursor)
    cursor.execute(sql)
    return cursor.fetchall()

def select_quehuodan(id):
    #从数据库查询单条数据
    conn1 = conn()
    sql = f"""
        select * from quehuodan
        where id = {id}
        """
    cursor = conn1.cursor(pymysql.cursors.DictCursor)
    cursor.execute(sql)
    return cursor.fetchone()

def insert_quehuodan(xuhao,chanpinmingcheng,guige,danwei,quehuoshuliang,danjia,zuidichuliang,suoxuzijin,beizhu):
    #新增数据到mysql
    conn1 = conn()
    sql =f"""
       insert into quehuodan
       (xuhao,chanpinmingcheng,guige,danwei,quehuoshuliang,danjia,zuidichuliang,suoxuzijin,beizhu)
       values('{xuhao}','{chanpinmingcheng}','{guige}','{danwei}','{quehuoshuliang}','{danjia}','{zuidichuliang}','{suoxuzijin}','{beizhu}')
       """
    cursor = conn1.cursor()
    cursor.execute(sql)
    conn1.commit()

def delete_quehuodan(id):
    #删除数据库id的记录
    conn1 = conn()
    sql = f"""
        delete from quehuodan
        where id={id}
        """
    cursor = conn1.cursor()
    cursor.execute(sql)
    conn1.commit()

def update_quehuodan(id,xuhao,chanpinmingcheng,guige,danwei,quehuoshuliang,danjia,zuidichuliang,suoxuzijin,beizhu):
    #修改数据
    conn1 = conn()
    sql = f"""
        update quehuodan
        set xuhao='{xuhao}',chanpinmingcheng='{chanpinmingcheng}',guige='{guige}',danwei='{danwei}',quehuoshuliang='{quehuoshuliang}',danjia='{danjia}',zuidichuliang='{zuidichuliang}',suoxuzijin='{suoxuzijin}',beizhu='{beizhu}'
        where id={id}
        """
    cursor = conn1.cursor()
    cursor.execute(sql)
    conn1.commit()

#删除数据
@app.route("/delete_quehuodan", methods=["GET"])
def delete_quehuo():
    id = request.args.get("id")
    delete_quehuodan(id)
    return redirect("/quehuodan")

#修改数据
@app.route("/缺货单修改", methods=["GET", "POST"])
def edit_quehuodan():
    id = request.args.get("id")
    data = select_quehuodan(id)
    if request.method == "POST":
        xuhao = request.form.get("xuhao")
        chanpinmingcheng = request.form.get("chanpinmingcheng")
        guige = request.form.get("guige")
        danwei = request.form.get("danwei")
        quehuoshuliang = request.form.get("quehuoshuliang")
        danjia = request.form.get("danjia")
        zuidichuliang = request.form.get("zuidichuliang")
        suoxuzijin = request.form.get("suoxuzijin")
        beizhu = request.form.get("beizhu")
        update_quehuodan(id,xuhao,chanpinmingcheng,guige,danwei,quehuoshuliang,danjia,zuidichuliang,suoxuzijin,beizhu)
        return redirect("/quehuodan")

    return render_template("在库管理---缺货单修改.html", data=data)

#增加数据
@app.route('/quehuodan', methods=["GET","POST"])
def index_quehuodan():
    if request.method == "POST":
        xuhao = request.form.get("xuhao")
        chanpinmingcheng = request.form.get("chanpinmingcheng")
        guige = request.form.get("guige")
        danwei = request.form.get("danwei")
        quehuoshuliang = request.form.get("quehuoshuliang")
        danjia = request.form.get("danjia")
        zuidichuliang = request.form.get("zuidichuliang")
        suoxuzijin = request.form.get("suoxuzijin")
        beizhu = request.form.get("beizhu")
        insert_quehuodan(xuhao,chanpinmingcheng,guige,danwei,quehuoshuliang,danjia,zuidichuliang,suoxuzijin,beizhu)
    datas=paixu_quehuodan()
    return render_template("在库管理---生成缺货单.html", datas=datas)

@app.route('/生成缺货单', methods = ["GET", "POST"])
def quehuodanchaxun():
    datas = paixu_quehuodan()
    return render_template("在库管理---生成缺货单.html", datas=datas)

#基础资料
@app.route('/ziliao')
def ziliao():
    return render_template('基础资料.html')

#供应商资料
def paixu_gongyingshang():
    conn1 = conn()
    sql="""
    select * from gongyingshangziliao
    order by id asc
    """
    cursor = conn1.cursor(pymysql.cursors.DictCursor)
    cursor.execute(sql)
    return cursor.fetchall()

def select_gongyingshang(id):
    #从数据库查询单条数据
    conn1 = conn()
    sql = f"""
        select * from gongyingshangziliao
        where id = {id}
        """
    cursor = conn1.cursor(pymysql.cursors.DictCursor)
    cursor.execute(sql)
    return cursor.fetchone()

@app.route('/gongyingshang', methods = ["GET", "POST"])
def gongyingshangchaxun():
    datas = paixu_gongyingshang()
    return render_template("基础资料---供应商资料.html", datas=datas)

#产品资料
def paixu_chanpin():
    conn1 = conn()
    sql="""
    select * from chanpinziliao
    order by id asc
    """
    cursor = conn1.cursor(pymysql.cursors.DictCursor)
    cursor.execute(sql)
    return cursor.fetchall()

def select_chanpin(id):
    conn1 = conn()
    #从数据库查询单条数据
    sql = f"""
        select * from chanpinziliao
        where id = {id}
        """
    cursor = conn1.cursor(pymysql.cursors.DictCursor)
    cursor.execute(sql)
    return cursor.fetchone()

@app.route('/chanpin', methods = ["GET", "POST"])
def chanpinchaxun():
    datas = paixu_chanpin()
    return render_template("基础资料---产品资料.html", datas=datas)

#员工信息
def paixu_yuangong():
    conn1 = conn()
    sql="""
    select * from yuangongxinxi
    order by id asc
    """
    cursor = conn1.cursor(pymysql.cursors.DictCursor)
    cursor.execute(sql)
    return cursor.fetchall()

def select_yuangong(id):
    conn1 = conn()
    #从数据库查询单条数据
    sql = f"""
        select * from yuangongxinxi
        where id = {id}
        """
    cursor = conn1.cursor(pymysql.cursors.DictCursor)
    cursor.execute(sql)
    return cursor.fetchone()

@app.route('/yuangong', methods = ["GET", "POST"])
def yuangongchaxun():
    datas = paixu_yuangong()
    return render_template("基础资料---员工信息.html", datas=datas)

#仓库信息
def paixu_cangku():
    conn1 = conn()
    sql="""
    select * from cangkuxinxi
    order by id asc
    """
    cursor = conn1.cursor(pymysql.cursors.DictCursor)
    cursor.execute(sql)
    return cursor.fetchall()

def select_cangku(id):
    conn1 = conn()
    #从数据库查询单条数据
    sql = f"""
        select * from cangkuxinxi
        where id = {id}
        """
    cursor = conn1.cursor(pymysql.cursors.DictCursor)
    cursor.execute(sql)
    return cursor.fetchone()

@app.route('/cangku', methods = ["GET", "POST"])
def cangkuchaxun():
    datas = paixu_cangku()
    return render_template("基础资料---仓库信息.html", datas=datas)


#报表管理
@app.route('/baobiao')
def baobiao():
    return render_template('报表管理.html')


#数据管理
@app.route('/shuju')
def shuju():
    return render_template('数据管理.html')

#货物状态
@app.route('/huowu')
def huowu():
    return render_template('货物状态.html')
#排序,修改数据库的信息
def paixu_buhuodan():
    conn1 = conn()
    sql="""
    select * from buhuodan
    order by id asc
    """
    cursor = conn1.cursor(pymysql.cursors.DictCursor)
    cursor.execute(sql)
    return cursor.fetchall()

def select_buhuodan(id):
    conn1 = conn()
    #从数据库查询单条数据
    sql = f"""
        select * from buhuodan
        where id = {id}
        """
    cursor = conn1.cursor(pymysql.cursors.DictCursor)
    cursor.execute(sql)
    return cursor.fetchone()

def insert_buhuodan(xuhao, chanpinmingcheng, danwei, shuliang,danjia,zongji,beizhu):
    #新增数据到mysql
    conn1 = conn()
    sql =f"""
       insert into buhuodan
       (xuhao, chanpinmingcheng, danwei, shuliang,danjia,zongji,beizhu)
       values('{xuhao}','{chanpinmingcheng}','{danwei}','{shuliang}','{danjia}','{zongji}','{beizhu}')
       """
    cursor = conn1.cursor()
    cursor.execute(sql)
    conn1.commit()

def update_buhuodan(id,xuhao, chanpinmingcheng, danwei, shuliang,danjia,zongji,beizhu):
    #更新数据
    conn1 = conn()
    sql = f"""
        update buhuodan
        set xuhao='{xuhao}',chanpinmingcheng='{chanpinmingcheng}',danwei='{danwei}',shuliang='{shuliang}',danjia='{danjia}',zongji='{zongji}',beizhu='{beizhu}'
        where id={id}
        """
    cursor = conn1.cursor()
    cursor.execute(sql)
    conn1.commit()

def delete_buhuodan(id):
    #删除数据库id的记录
    conn1 = conn()
    sql = f"""
        delete from buhuodan
        where id={id}
        """
    cursor = conn1.cursor()
    cursor.execute(sql)
    conn1.commit()

@app.route("/delete_buhuodan", methods=["GET"])
def delete_buhuo():
    id = request.args.get("id")
    delete_buhuodan(id)
    return redirect("/buhuodan")

@app.route("/补货单修改", methods=["GET", "POST"])
def edit_buhuodan():
    id = request.args.get("id")
    data = select_buhuodan(id)
    if request.method == "POST":
        xuhao = request.form.get("xuhao")
        chanpinmingcheng = request.form.get("chanpinmingcheng")
        danwei = request.form.get("danwei")
        shuliang = request.form.get("shuliang")
        danjia = request.form.get("danjia")
        zongji = request.form.get("zongji")
        beizhu = request.form.get("beizhu")
        update_buhuodan(id,xuhao, chanpinmingcheng, danwei, shuliang,danjia,zongji,beizhu)
        return redirect("/buhuodan")

    return render_template("货物状态---补货单修改.html", data=data)

@app.route('/buhuodan', methods=["GET","POST"])
def index_buhuodan():
    if request.method == "POST":
        xuhao = request.form.get("xuhao")
        chanpinmingcheng = request.form.get("chanpinmingcheng")
        danwei = request.form.get("danwei")
        shuliang = request.form.get("shuliang")
        danjia = request.form.get("danjia")
        zongji = request.form.get("zongji")
        beizhu = request.form.get("beizhu")
        insert_buhuodan(xuhao, chanpinmingcheng,danwei, shuliang,danjia,zongji,beizhu)
    datas=paixu_buhuodan()
    return render_template("货物状态---生成补货单.html", datas=datas)

@app.route('/生成补货单', methods = ["GET", "POST"])
def shengchengbuhuodan():
    datas = paixu_buhuodan()
    return render_template("货物状态---生成补货单.html", datas=datas)

app.run(debug=True)