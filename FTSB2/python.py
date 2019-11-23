from flask import Blueprint, flash, jsonify
from Form import Login_Form, Register_Form, change_password_Form
from usermodel import Users, Words
from usermodel import Records
from flask_login import login_user, logout_user
from Start import db
import os
import sys
import time
import pickle
import save_xml
import save_wenzi
from PIL import Image
import tensorflow as tf
import ocr
from operator import or_, and_
from flask import render_template, request, Flask, url_for, Response
from keras.models import model_from_json
import numpy as np
from pdf_to_png import doPdftoPicture,compress
import imutils
import cv2
blog = Flask(__name__)
sys.path.append('../')
sys.setrecursionlimit(10000)  # set the maximum depth as 10000
blog = Blueprint('blog', __name__)
MODEL_LABELS_FILENAME = "model//labels_tr_ch_11.27.dat"
with open(MODEL_LABELS_FILENAME, "rb") as f:
    lb = pickle.load(f)
#    当前用户
NowUser = ''
merge = ''
name = ''
global model, graph
basedir = os.path.abspath(os.path.dirname(__file__))
# def cv2ImgAddText(img, text, left, top, textColor=(0, 255, 0), textSize=20):
#     if (isinstance(img, np.ndarray)):       # 判断是否OpenCV图片类型
#         img = Image.fromarray(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))     #array转换成image
#     draw = ImageDraw.Draw(img)              #创建一个可以在给定图像上绘图的对象
#     fontText = ImageFont.truetype(          #加载一个TrueType字体文件，并且创建一个字体对象
#         "font/simsun.ttc", textSize, encoding="utf-8")
#     draw.text((left, top), text, textColor, font=fontText)             #在图片上添加文字
#     return cv2.cvtColor(np.asarray(img), cv2.COLOR_RGB2BGR)


def init():
    json_file = open('model//model_12.20_gen.json', 'r')      #可以考虑使用with open
    loaded_model_json = json_file.read()
    json_file.close()
    loaded_model = model_from_json(loaded_model_json)       #加载模型
    loaded_model.load_weights("model//model_12.20_gen.h5")
    print("Loaded Model from disk")
    graph = tf.get_default_graph()      #获取当前默认计算图。
    return loaded_model, graph

model, graph = init()

def recg_images(img):			#将图片识别为文字
    letter_image = resize_to_fit(img, 64, 64)
    letter_image = np.expand_dims(letter_image, axis=0)     #用于扩展数组的形状，表示在0位置添加数据
    with graph.as_default():        #获取他的上下文管理器
        prediction = model.predict(letter_image)        #对图像进行分类
    letter = lb.inverse_transform(prediction)[0]
    return str(letter)


def resize_to_fit(image, width, height):
    """
    A helper function to resize an image to fit within a given size
    :param image: image to resize
    :param width: desired width in pixels
    :param height: desired height in pixels
    :return: the resized image
    """

    # grab the dimensions of the image, then initialize
    # the padding values
    (h, w) = image.shape[:2]

    # if the width is greater than the height then resize along
    # the width
    if w > h:
        image = imutils.resize(image, width=width)

    # otherwise, the height is greater than the width so resize
    # along the height
    else:
        image = imutils.resize(image, height=height)

    # determine the padding values for the width and height to
    # obtain the target dimensions
    padW = int((width - image.shape[1]) / 2.0)
    padH = int((height - image.shape[0]) / 2.0)

    # pad the image then apply one more resizing to handle any
    # rounding issues
    image = cv2.copyMakeBorder(image, padH, padH, padW, padW,
        cv2.BORDER_CONSTANT, value=(255, 255, 255))
    image = cv2.resize(image, (width, height))

    # return the pre-processed image
    return image


@blog.route('/')
def index():
    return render_template('index0.html')


@blog.route('/index')
def l_index():
    return render_template('index0.html')


@blog.route('/index1')
def index1():
    return render_template('index1.html')


@blog.route('/shibie', methods=['GET'])
def shiBie():
    return render_template('index1.html')


@blog.route('/turnRecord')
def turnRecordFun():
    return render_template('record.html')


# 五个页面的响应
@blog.route('/firstPage')
def firstPage():
    return render_template('index0.html', UserName=NowUser)


@blog.route('/second-AboutUs')  # 网址还没改，等着再改
def secondAboutUs():
    return render_template('aboutus.html', UserName=NowUser)


@blog.route('/students')
def Student():
    return render_template('aboutus-students.html', UserName=NowUser)


@blog.route('/personal', methods=['GET', 'POST'])
def personal():
    record =  Records.query.filter(and_((Records.type==1),(Records.userID==NowUser))).all()
    num1 = len(record)+1
    record =  Records.query.filter(and_((Records.type==0),(Records.userID==NowUser))).all()
    num2=0
    for i in record:
        num2 += Records.get_num(i)
    user = Users.query.filter_by(userID=NowUser).first()
    user.PDF = num1
    user.photo = num2
    db.session.commit()
    return render_template('my.html', var1=num1, var2=num2, UserName=NowUser)


@blog.route('/backstage')
def backstage():
	return render_template('backstage.html')


@blog.route('/message')
def message():
    return render_template('my_message.html', UserName=NowUser)


@blog.route('/change')
def change():
    user = Users.query.filter_by(userID=NowUser).first()
    money_wait = Users.get_money_wait(user)
    money = Users.get_money(user)
    db.session.commit()
    return render_template('my_change.html', var1=money_wait, var2=money, UserName=NowUser)


@blog.route('/member')
def member():
    return render_template('my_member.html', UserName=NowUser)


@blog.route('/book')
def book():
    return render_template('my_book.html', UserName=NowUser)


@blog.route('/photo')
def photo():
    return render_template('my_photo.html', UserName=NowUser)


@blog.route('/earn')
def earn():
    return render_template('my_earn.html', UserName=NowUser)


@blog.route('/money',methods=['GET', 'POST'])
def money():
    money_wait = request.form.get('data1')
    user = Users.query.filter_by(userID=NowUser).first()
    money_wait = float(money_wait)/100 + Users.get_money_wait(user)
    Users.set_money_wait(user, money_wait)
    db.session.commit()
    money = Users.get_money(user)
    return render_template('my_change.html', var1=money_wait, var2=money, UserName=NowUser)


@blog.route('/recharge',methods=['GET', 'POST'])
def recharge():
	num = request.form.get('RMB1')
	user = Users.query.filter_by(userID=NowUser).first()
	money =  int(num) + Users.get_money(user)
	Users.set_money(user, money)
	db.session.commit()
	money_wait = Users.get_money_wait(user)
	return render_template('my_change.html', var1=money_wait, var2=money , UserName=NowUser)


@blog.route('/DevelopmentProcess')
def DevelopmentProcessF():
    return render_template('aboutus-DevelopmentProcess.html', UserName=NowUser)


@blog.route('/three-shibie')
def threeShiBie():
    user = Users.query.filter_by(userID=NowUser).first()
    if user is not None:
        return render_template('three-recog.html', UserName=NowUser , isVip=user.isVip)
    else :
        return render_template('three-recog.html', UserName=NowUser , isVip=0)


@blog.route('/loginq')
def loginq():
    form = Login_Form()
    return render_template('login-flask.html', UserName=NowUser, form=form)


@blog.route('/logina', methods=['GET', 'POST'])
def logina():
    return render_template('head-flask.html', UserName=NowUser)


# 设置响应头
def Response_headers(content):
    resp = Response(content)
    resp.headers['Access-Control-Allow-Origin'] = '*'
    return resp


@blog.route('/quitLogin', methods=['POST'])
def QuitLogin():
    logout_user()
    global NowUser
    NowUser = ''
    form = Login_Form()
    flash('你已退出登录')
    return render_template('head-flask.html', UserName=NowUser, form=form)



@blog.route('/sendjson2',methods=['POST'])
def sendjson2():
    a= record_form_select(NowUser)
    list = []
    for e in a:
        info = {}
        info["user"] = e[0]
        info["record"] = e[1]
        info["time"] = e[2]
        ###################################
        info["type"] = e[3]
        info["num"] = e[4]
        info["name"] = e[5]
        ###################################
        list.append(info)
    # print(list)
    return jsonify(list)


@blog.route('/sendjson3',methods=['POST'])
def sendjson3():
	userEles =  Users.query.all()
	list = []
	for e in userEles:
		info = {}
		info["userID"] = e.userID
		info["money"] = e.money
		info["money_wait"] = e.money_wait
		info["PDF"] = e.PDF
		info["photo"] = e.photo
		list.append(info)
	return jsonify(list)


@blog.route('/sendjson4',methods=['POST'])
def sendjson4():
    recordEles = Records.query.all()
    list = []
    for e in recordEles:
        info = {}
        info["user"] = e.userID
        info["record"] = e.record
        info["time"] = e.dateTime
        info["type"] = e.type
        info["num"] = e.num
        info["name"] = e.name
        list.append(info)
    return jsonify(list)


@blog.route('/checkRecordFormAction', methods=['POST'])
def check_record_pythonFunction():
    return render_template('FZTSB_Record.html', UserName=NowUser)

#
# @blog.route('/charge', methods=['POST'])
# def charge():
#     return render_template('FZTSB_Record.html', UserName=NowUser)


@blog.route('/login', methods=['GET', 'POST'])
def getLoginRequest():
    global NowUser
    form = Login_Form()
    if form.validate_on_submit():
        user = Users.query.filter_by(userID=form.userID.data).first()
        if user is not None and user.password == form.password.data:
            login_user(user)
            NowUser = form.userID.data
            return render_template('three-recog.html', UserName=NowUser , isVip=user.isVip)
        else:
            flash('用户名不存在或密码错误')
    return render_template('login-flask.html', form=form)


@blog.route('/register', methods=['GET', 'POST'])
def register():
    form = Register_Form()
    if form.validate_on_submit():
        user = Users(userID=form.userID.data, password=form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('注册成功')
        form = Login_Form()
        return render_template('login-flask.html', form=form)
    return render_template('register-flask.html', form=form)


@blog.route('/change_password', methods=['GET', 'POST'])
def change_password():
    form = change_password_Form()
    if form.validate_on_submit():
        user = Users.query.filter_by(userID=NowUser).first()
        Users.set_passwrod(user, form.new_password.data)
        db.session.commit()
        flash('修改密码成功')
        form = Login_Form()
        return render_template('login-flask.html', form=form)
    return render_template('change-password-flask.html', form=form)


def findcountours(n, img):          #识别文字功能，打框
    img = cv2.imread(img)
    image = np.rot90(img)
    cv2.imwrite(basedir + "/image/0.jpg", image)
    img = ".\\image\\0.jpg"
    list = ocr.model(img)	#img是逆时针旋转90°的图
    list = np.array(list)
    return list


def record_form_add(record,userID,dateTime,type,num,name):
    recordEle = Records(record=record,userID=userID,dateTime=dateTime,type=type,num=num,name=name)
    db.session.add(recordEle)
    db.session.commit()


def add_word(no, word, graph, record):
	wordEle = Words(no=no, word=word, graph=graph, record=record)
	db.session.add(wordEle)
	db.session.commit()


def record_form_select(userID):
    recordEles =  Records.query.filter_by(userID=userID).order_by(Records.dateTime).all()
    myList = [([] * 6) for i in range(len(recordEles))]
    for i in range(len(recordEles)):
        myList[i].append(recordEles[i].userID)
        myList[i].append(recordEles[i].record)
        myList[i].append(recordEles[i].dateTime)
        ###################################
        myList[i].append(recordEles[i].type)
        ################################
        myList[i].append(recordEles[i].num)
        myList[i].append(recordEles[i].name)
    return myList

########################################################################################
@blog.route('/up_pdf', methods=['POST'])#上传pdf
def up_pdf():
    now = time.time()
    date = time.localtime(now)
    ISFORMAT = "%Y-%m-%d %H:%M:%S"
    datestr = time.strftime(ISFORMAT, date)
    srtrr = (int(now * 1000))
    name = request.form.get('filesname2')
    record_form_add(str(srtrr), NowUser, datestr, 1, 1, name)
    user = Users.query.filter_by(userID=NowUser).first()
    pdf = user.PDF+1
    Users.set_pdf(user, pdf)
    db.session.commit()
    img = request.files.get('pdf')
    path = basedir + "/static/photo/"+NowUser+"/pdf/"+str(srtrr)+"/"
    zpath = basedir + "/static/photo/"+NowUser+"/pdf/"
    if not os.path.exists(path):
        os.makedirs(path)
    name1 = name.strip(';').split(';')
    file_path = path + name1[0]
    img.save(file_path)
    doPdftoPicture(path, name1[0][:-4])
    compress(zpath, srtrr)
    return render_template('index1.html',UserName=NowUser)





@blog.route('/up_photo', methods=['POST'])#更新杨旭裁图片
def up_photo():
    date = time.localtime(time.time())
    datestr = time.strftime("%Y-%m-%d %H:%M:%S", date)         #time.asctime( time.localtime(time.time()) )
    srtrr = (int(time.time() * 1000))
    img_list = request.files.getlist('photo')            #接收上传的文件
    global name
    name = request.form.get('filesname')
    path = basedir + "/static/photo/" + NowUser + "/" + str(srtrr) + "/"
    if not os.path.exists(path):
        os.makedirs(path)
    global img_length
    img_length = len(img_list)
    record_form_add(str(srtrr), NowUser, datestr, 0, img_length, name)
    if img_length == 1:
        file_path = path + '1.jpg'
        file_path_c = path +  "1/"
        img_list[0].save(file_path)

        if(request.form.get('x') and request.form.get('y')):        #获取坐标，分割图片
            x = int(float(request.form.get('x')))
            y = int(float(request.form.get('y')))
            img_1 = cv2.imread(file_path)
            sp = img_1.shape
            height = sp[0]
            width = sp[1]
            cropped_1 = img_1[0:y, 0:x]
            cropped_2 = img_1[0:y, x:width]
            cropped_3 = img_1[y:height, 0:x]
            cropped_4 = img_1[y:height, x:width]
            if not os.path.exists(file_path_c):
                os.makedirs(file_path_c)
            cv2.imwrite(file_path_c + "1.jpg", cropped_1)
            cv2.imwrite(file_path_c + "2.jpg", cropped_2)
            cv2.imwrite(file_path_c + "3.jpg", cropped_3)
            cv2.imwrite(file_path_c + "4.jpg", cropped_4)
        if os.path.exists(file_path_c):
            data1 = findcountours(3, file_path_c + "1.jpg")
            data = data1.flatten()
            path = os.path.join(os.getcwd(), file_path_c + "1.jpg")
            img1 = Image.open(path)
            data2 = img1.size
            return render_template('index.html', var1=data, var2=data2[0], var3=data2[1], var4=img_length,  UserName=NowUser, photoname=str(srtrr)+"/1/1")	
        else:
            data1 = findcountours(3, file_path)
            data = data1.flatten()
            path = os.path.join(os.getcwd(), file_path)
            img1 = Image.open(path)
            data2 = img1.size
            return render_template('index.html', var1=data, var2=data2[0], var3=data2[1], var4=img_length,  UserName=NowUser, photoname=str(srtrr)+"/1")
    else:
        file_path_c = path + "1.jpg"
        for i in range(img_length):
            file_path = path + str(i+1) + ".jpg"
            img_list[i].save(file_path)
        data1 = findcountours(3, file_path_c)
        data = data1.flatten()
        path = os.path.join(os.getcwd(), file_path_c)
        img1 = Image.open(path)
        data2 = img1.size
        return render_template('index.html', var1=data, var2=data2[0], var3=data2[1],var4=img_length,  UserName=NowUser, photoname=str(srtrr) + "/1")


@blog.route('/update', methods=['get', 'POST'])
def update():
    data4 = request.form.get('photoname')
    global model
    path = basedir + "/static/photo/" + NowUser + "/"
    file_path = basedir + "/static/photo/" + NowUser + "/" + data4 + '.jpg'
    anno = save_xml.GEN_Annotations(data4)
    image = cv2.imread(file_path)
    high, wide, tongdao = image.shape
    data = request.form.get('ss')
    xli = request.form.get('xli')
    yli = request.form.get('yli')
    data1 = OnlyCharNum(data)
    s = ''
    if data1 != "":
        data1 = data1.split(",")
        for i in range(len(data1)):
            if i % 4 == 0:
                x1 = fto(data1[i], xli)
                x2 = fto(data1[i + 1], yli)
                w = fto(data1[i + 2], xli)
                h = fto(data1[i + 3], yli)
                x3 = x1 + w
                if float(x3) > wide:
                    x3 = wide
                x4 = x2 + h
                if float(x4) > high:
                    x4 = high
                img = image[int(x2):int(x4), int(x1):int(x3)]			#截出单字
                word = recg_images(img)				#将图片转化为文字
                anno.add_pic_attr(word, str(x1), str(x2), str(x3), str(x4))
                s = s + word + " " + str(x1) + " " + str(x2) + " " + str(x3) + " " + str(x4) + " "			#（中文字，起始x，起始y，结束x，结束y）
    cv2.imwrite(file_path, image)
    anno.set_size(wide, high, tongdao)
    p = os.path.join(path, data4 + ".xml")
    anno.savefile(p)
    return render_template('FTSB.html', data=s, data1=img_length,data4=data4, final_txt=merge, UserName=NowUser)



def OnlyCharNum(s, oth=''):
    s2 = s.lower()
    fomart = ',.0123456789'
    for c in s2:
        if not c in fomart:
            s = s.replace(c, '')
    return s


def fto(a, b):
    return float(float(a) / float(b) / float(b))


@blog.route('/cuncu', methods=['POST'])
def cuncu():			#将识别的每一个字保存到D盘的FTZSB文件夹，并对切割的后三张图进行处理
    h1data = request.form.get('h1data')      #图片路径
    h2data = request.form.get('h2data')      #文字及其坐标
    h3data = request.form.get('h3data')      #图片名字
    ################################以下代码改动######################################
    data1 = h2data.strip().split(" ")
    if len(data1)!=1:
        for i in range(len(data1)):
            if i % 5 == 0:
                word = data1[i]
                x1 = int(float(data1[i + 1]))
                x2 = int(float(data1[i + 2]))
                w = int(float(data1[i + 3]))
                h = int(float(data1[i + 4]))
                save_wenzi.ss(word, x1, x2, w, h, h1data)
    if h3data[-2:] == '/1':
        path = basedir + "/static/photo/" + NowUser + "/"
        file_path = path + h3data[0:-2] + "/2.jpg"
        data1 = findcountours(3, file_path)
        data = data1.flatten()
        path = os.path.join(os.getcwd(), file_path)
        img1 = Image.open(path)
        data2 = img1.size
        return render_template('index.html', var1=data, var2=data2[0], var3=data2[1], var4=img_length, UserName=NowUser,photoname=h3data[0:-2] + "/2")
    elif h3data[-2:] == '/2':
        path = basedir + "/static/photo/" + NowUser + "/"
        file_path = path + h3data[0:-2] + "/3.jpg"
        data1 = findcountours(3, file_path)
        data = data1.flatten()
        path = os.path.join(os.getcwd(), file_path)
        img1 = Image.open(path)
        data2 = img1.size
        return render_template('index.html', var1=data, var2=data2[0], var3=data2[1],var4=img_length, UserName=NowUser,photoname=h3data[0:-2] + "/3")
    elif h3data[-2:] == '/3':
        path = basedir + "/static/photo/" + NowUser + "/"
        file_path = path + h3data[0:-2] + "/4.jpg"
        data1 = findcountours(3, file_path)
        data = data1.flatten()
        path = os.path.join(os.getcwd(), file_path)
        img1 = Image.open(path)
        data2 = img1.size
        return render_template('index.html', var1=data, var2=data2[0], var3=data2[1], var4=img_length, UserName=NowUser,photoname=h3data[0:-2] + "/4")
    return render_template('index1.html', registSuceess='恭喜您注册成功', UserName=NowUser)


@blog.route('/cuncu2', methods=['POST'])
def cuncu2():			#将识别的每一个字保存到D盘的FTZSB文件夹，并对切割的后三张图进行处理
    h1data = request.form.get('h1data')		#图片路径
    h2data = request.form.get('h2data')		#文字及其坐标
    h3data = request.form.get('h3data')		#图片名字
    global merge, name
    merge  = request.form.get('h4data')		#切割部分的文字和坐标
    data1 = h2data.strip().split(" ")
    name1 = name.strip(';').split(';')
    user = Users.query.filter_by(userID=NowUser).first()
    photo = user.photo+1
    Users.set_photo(user, photo)
	#获取word表需要的数据
    number = h3data[-1]	
    word_record = Records.query.filter_by(userID=NowUser).order_by(Records.dateTime.desc()).first()
    record = Records.get_record(word_record)
    graph = name1[int(number)-1]
    if len(data1)!=1:
        for i in range(len(data1)):
            if i % 5 == 0:
                word = data1[i]
                x1 = int(float(data1[i + 1]))
                x2 = int(float(data1[i + 2]))
                w = int(float(data1[i + 3]))
                h = int(float(data1[i + 4]))
                save_wenzi.ss(word, x1, x2, w, h, h1data)
                no = len(Words.query.all())+1
                add_word(no, word, graph, record)
    path = basedir + "/static/photo/" + NowUser + "/"
    file_path = path + h3data[0:-1] + str(int(number)+1) + ".jpg"		#number是字符，加数字会出错,转换类型
    old_flie = path + h3data + ".jpg"
    new_file = path + h3data[0:-1] + name1[int(number)-1]
    old_xml = path + h3data + ".xml"
    new_xml = path + h3data[0:-1] + name1[int(number)-1][:-4] + ".xml"
    os.rename(old_flie, new_file)
    os.rename(old_xml, new_xml)
    if os.path.exists(file_path):
        data1 = findcountours(3, file_path)
        data = data1.flatten()
        path = os.path.join(os.getcwd(), file_path)
        img1 = Image.open(path)
        data2 = img1.size
        return render_template('index.html', var1=data, var2=data2[0], var3=data2[1],var4=img_length, UserName=NowUser,photoname=h3data[0:-1] + str(int(number)+1))
    else:
        merge = ""
        return render_template('index1.html', registSuceess='恭喜您注册成功', UserName=NowUser)