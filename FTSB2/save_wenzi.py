import cv2
import os
import sys
import time
sys.path.append('../')
basedir = os.path.abspath(os.path.dirname(__file__))


def mkdir(path):
    # 引入模块
    import os
    # 去除首位空格
    path = path.strip()
    # 去除尾部 \ 符号
    path = path.rstrip("\\")
    # 判断路径是否存在
    # 存在     True
    # 不存在   False
    isExists = os.path.exists(path)
    # 判断结果
    if not isExists:
        # 如果不存在则创建目录
         # 创建目录操作函数
        os.makedirs(path)
        return True
    else:
        # 如果目录存在则不创建，并提示目录已存在
        return False


def ss(data, s1,  s2, s3, s4, file_path):
    # 定义要创建的目录
    i = 0
    path = basedir + "/static/photo/"+file_path
    image = cv2.imread(path)
    img = image[s2:s4, s1:s3]
    # mkpath = "D:\\FTZSB\\"+data
    mkpath = path[0:-5] + "文字/" +  data
    # 调用函数
    mkdir(mkpath)
    srtrr = (int(time.time() * 1000))
    file_mkpath = mkpath + "/"
    # file_paths=file_mkpath +str(srtrr) + '.jpg'
    file_paths=file_mkpath + data + '.jpg'
    # cv2.imshow("11",img)
    # cv2.waitKey()
    #cv2.imwrite(file_paths,img)
    flag = os.path.exists(file_paths)
    while flag:
        i = i + 1
        file_paths = file_mkpath + data + "(" + str(i) + ').jpg'
        flag = os.path.exists(file_paths)
    cv2.imencode('.jpg', img)[1].tofile(file_paths)

