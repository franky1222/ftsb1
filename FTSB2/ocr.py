import ctpn.demo_pb
import cv2
import numpy as np
from math import *

def sort_box(box):
    """
    对box进行排序
    """
    box = sorted(box, key=lambda x: sum([x[1], x[3], x[5], x[7]]))
    return box


def draw_boxes(img, boxes, scale):
    box_id = 0
    img = img.copy()
    text_recs = np.zeros((len(boxes), 8), np.int)
    for box in boxes:
        if np.linalg.norm(box[0] - box[1]) < 5 or np.linalg.norm(box[3] - box[0]) < 5:
            continue

        if box[8] >= 0.8:
            color = (255, 0, 0)  # red
        else:
            color = (0, 255, 0)  # green

        cv2.line(img, (int(box[0]), int(box[1])), (int(box[2]), int(box[3])), color, 2)
        cv2.line(img, (int(box[0]), int(box[1])), (int(box[4]), int(box[5])), color, 2)
        cv2.line(img, (int(box[6]), int(box[7])), (int(box[2]), int(box[3])), color, 2)
        cv2.line(img, (int(box[4]), int(box[5])), (int(box[6]), int(box[7])), color, 2)

        for i in range(8):
            text_recs[box_id, i] = box[i]

        box_id += 1

    img = cv2.resize(img, None, None, fx=1.0/scale, fy=1.0/scale, interpolation=cv2.INTER_LINEAR)
    return text_recs, img


def text_detect(img):
    scores, boxes, img, scale = ctpn.demo_pb.ctpn(img)
    text_recs, img_drawed = draw_boxes(img, boxes, scale)
    return text_recs, img_drawed, img, scale


def dumpRotateImage(img, degree, pt1, pt2, pt3, pt4):
    height, width = img.shape[:2]
    heightNew = int(width * fabs(sin(radians(degree))) + height * fabs(cos(radians(degree))))
    widthNew = int(height * fabs(sin(radians(degree))) + width * fabs(cos(radians(degree))))
    matRotation = cv2.getRotationMatrix2D((width // 2, height // 2), degree, 1)
    matRotation[0, 2] += (widthNew - width) // 2
    matRotation[1, 2] += (heightNew - height) // 2
    imgRotation = cv2.warpAffine(img, matRotation, (widthNew, heightNew), borderValue=(255, 255, 255))
    pt1 = list(pt1)
    pt3 = list(pt3)

    [[pt1[0]], [pt1[1]]] = np.dot(matRotation, np.array([[pt1[0]], [pt1[1]], [1]]))
    [[pt3[0]], [pt3[1]]] = np.dot(matRotation, np.array([[pt3[0]], [pt3[1]], [1]]))
    ydim, xdim = imgRotation.shape[:2]
    imgOut = imgRotation[max(1, int(pt1[1])) : min(ydim - 1, int(pt3[1])), max(1, int(pt1[0])) : min(xdim - 1, int(pt3[0]))]

    return imgOut


def process_img(img,text_recs,scale):
    result_loc=[]
    xDim, yDim = img.shape[1], img.shape[0]
    heigh=int(yDim/scale)
    wide=int(xDim/scale)
    # print("the size:" + str(wide) + " " + str(heigh))
    for index, rec in enumerate(text_recs):
        pt1 = (max(1, rec[0]), max(1, rec[1]))
        pt2 = (rec[2], rec[3])
        pt3 = (min(rec[6], xDim - 2), min(yDim - 2, rec[7]))
        pt4 = (rec[4], rec[5])

        degree = degrees(atan2(pt2[1] - pt1[1], pt2[0] - pt1[0]))  # 图像倾斜角度
        if abs(degree)<15:
            partImg = dumpRotateImage(img, degree, pt1, pt2, pt3, pt4)
            if partImg.shape[0] < 25 or partImg.shape[1] < 25 or partImg.shape[0] > partImg.shape[1]:  # 过滤异常图片
                continue
            loc_list=get_letter_list(partImg, scale)
            for loc in loc_list:
                start, end=loc
                x1=pt1[0]+start-2
                y1=pt3[1]+2
                x2=pt1[0]+end-2
                y2=pt1[1]+2
                x1,y1=transform_xy(x1,y1,yDim,scale)
                x2,y2=transform_xy(x2,y2,yDim,scale)
                x1,x2,y1,y2=float(x1/heigh),float(x2/heigh),float(y1/wide),float (y2/wide)
                result_loc.append((y1,x1,y2,x2))
                # result_loc.append((x1,y1,x2,y2))
    print("result_loc:")
    print(result_loc)
    return result_loc


# def transform_xy(x,y,h,scale):
    # return int(max(0,h-y)/scale),int(x/scale)
def transform_xy(x,y,h,scale):
    return int(max(0,h-y)/scale),int(x/scale)

def model(img, adjust=False):
    """
    @img: 图片
    @adjust: 是否调整文字识别结果
    """
    obj = cv2.imread(".\\image\\22.jpg")
    text_recs, img_framed, img, scale = text_detect(img)#获取每列文字
    text_recs = sort_box(text_recs)#从右至左排序文字列
    all_recs = process_img(img,text_recs,scale)#分割文字
    return all_recs


def getHProjection(image, scale):
    hProjection = np.zeros(image.shape, np.uint8)

    # 图像高与宽

    (h, w) = image.shape

    # 长度与图像高度一致的数组

    h_ = [0] * h

    # 循环统计每一行白色像素的个数

    for y in range(h):

        for x in range(w):

            if image[y, x] == 255:
                h_[y] += 1
    # print(h_)
    # 绘制水平投影图像

    for y in range(h):

        for x in range(h_[y]):
            hProjection[y, x] = 255

    # cv2.imshow('hProjection2',hProjection)

    return h_


def getVProjection(image):
    vProjection = np.zeros(image.shape, np.uint8);

    # 图像高与宽

    (h, w) = image.shape

    # 长度与图像宽度一致的数组

    w_ = [0] * w

    # 循环统计每一列白色像素的个数

    for x in range(w):

        for y in range(h):

            if image[y, x] == 255:
                w_[x] += 1

    # 绘制垂直平投影图像
    # print(w_)
    for x in range(w):

        for y in range(h - w_[x], h):
            vProjection[y, x] = 255

    # cv2.imshow('vProjection',vProjection)

    return w_


def get_letter_list(img, scale):
    # 读入原始图像

    # origineImage = cv2.imread('./origin/999.jpg')
    origineImage = img
    # 图像灰度化

    # image = cv2.imread('test.jpg',0)

    image = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # cv2.imshow('gray',image)

    # 将图片二值化

    retval, img = cv2.threshold(image, 127, 255, cv2.THRESH_BINARY_INV)

    # cv2.imshow('binary',img)

    Position = []
    min_font_size = img.shape[0] / 4 * 3

    W = getVProjection(img)

    Wstart = 0

    Wend = 0

    W_Start = 0

    W_End = 0

    for j in range(len(W)):

        if W[j] > 0 and Wstart == 0:
            W_Start = j

            Wstart = 1

            Wend = 0

        if W[j] <= 0 and Wstart == 1:

            if j - W_Start >= min_font_size:
                W_End = j

                Wstart = 0

                Wend = 1

        if W[j] >= 0 and Wstart == 1 and j == len(W) - 1:
            W_End = j

            Wstart = 0

            Wend = 1

        if W[j] >= img.shape[0] - 1:
            break

        if Wend == 1:
            Position.append([W_Start, W_End])

            Wend = 0

    # 根据确定的位置分割字符

    for m in range(len(Position)):
        width = Position[m][1] - Position[m][0]
        height = img.shape[0]
        if width != height:
            # pass
            # if width > height:
            # Position[m][1] -= int((width-height)/2)
            # Position[m][3] += int((width-height)/2)
            if width < height:
                Position[m][0] -= int((height - width) / 2)
                Position[m][1] += int((height - width) / 2)
        cv2.rectangle(origineImage, (Position[m][0], 0), (Position[m][1], img.shape[0]), (0, 229, 238), 1)

    # for i in range(len(Position)):
    # Position[i][0] = int(Position[i][0]/scale)
    # Position[i][1] = int(Position[i][1]/scale)

    print(Position)

    # cv2.imshow('image0',origineImage)

    # cv2.waitKey(0)
    return Position