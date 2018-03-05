# -*- coding: utf-8 -*-

# import os
# from skimage import color, data, filters
# from skimage.color import rgb2gray
# from skimage import io
# from PyInstaller.utils.hooks import collect_data_files, collect_submodules
#
# datas = collect_data_files("skimage.io.use_plugin")
# hiddenimports = collect_submodules('skimage.io._plugins')

######################################tesseract工具##########################################################
# 1、生成gif文件
# 2、转化为tif，是convert命令
# 3、tesseract douban.font.exp0.tif douban.font.exp0 batch.nochop makebox生成box文件，再使用jTe工具打开编辑调整
# 4、touch  执行改批处理前先要目录下创建font_properties文件，内容为font 0 0 0 0
# 5、tesseract  douban.font.exp0.tif douban.font.exp0 nobatch box.train
# 6、unicharset_extractor  douban.font.exp0.box
# 6、mftraining -F font_properties -U unicharset -O douban.unicharset douban.font.exp0.tr
# 7、cntraining  douban.font.exp0.tr
# 8、mv normproto douban.normproto
# mv inttemp douban.inttemp
# mv pffmtable douban.pffmtable
# mv shapetable douban.shapetable
# 9、combine_tessdata douban
############################################################################################################

from PIL import Image
import numpy as np
import copy
import os

import numpy
import os

WHITE = (0,0,0)
BLACK = (255,255,255)

cwddir = "/home/allen/downloadfiles/gittest/DoubanAuto/example"
imagdir = "/home/allen/downloadfiles/gittest/DoubanAuto/image"
trfimagedir = "/home/allen/downloadfiles/gittest/DoubanAuto/image/tfrimg-src"
trftifdir = "/home/allen/downloadfiles/gittest/DoubanAuto/image/tfrimg-tif"
rmnosietifdir = "/home/allen/downloadfiles/gittest/DoubanAuto/image/rmnosi-img-tif"


def batchConvertTif(trfimagedir):

    time = os.popen('date')
    print time.read()

    for path, dir, filename in os.walk(trfimagedir):
        for f in filename:
            status = os.popen('convert %s %s' % (path + '/' +f, path + '/' + f + '.tif'))
            print status.read()

def deal_each_img(path,filename,rsfname):

    if rsfname == '' or rsfname == None:
        rsfname = filename

    im = Image.open(path + '/' + filename)
    imb = copy.deepcopy(im)
    gray_img(im)
    interference_point(im, "11")
    remove_noise(im)
    if os.path.exists(rmnosietifdir) == 0:
        os.mkdir(rmnosietifdir)

    im.save(rmnosietifdir + '/' + rsfname)
    return rmnosietifdir + '/' + rsfname


def test_deal_img(path, filename, rsfname):

    im = Image.open(path+'/'+filename)
    imb = copy.deepcopy(im)
    # im.show()

    # im_gray = im.convert("L")
    gray_img(im)
    # im.show()
    # 转换成灰度图像
    # im_gray = imb.convert("L")
    # im_gray.show()
    # #
    # # 保存图像
    # im_gray.save(cwddir + "image_gray.jpg")

    interference_point(im, "11")
    # im.show()

    remove_noise(im)
    # im.show()
    if os.path.exists(trfimagedir) == 0:
        os.mkdir(trfimagedir)

    im.save(trfimagedir + '/' + rsfname)

    return trfimagedir + '/' + rsfname

# 灰度化并且二值化图片
def gray_img(_img):
    img1 = _img.load()

    print "after load()",   type(img1)
    print "jpg:",   type(_img)

    # print _img.shape
    print _img.size
    rows, cols = _img.size

    threshold = 23
    for i in range(rows):
        for j in range(cols):
            r, g, b = _img.getpixel((i, j))
            if r > threshold or g > threshold or b > threshold:
                img1[i, j] = (255, 255, 255)
            else:
                img1[i, j] = (0, 0, 0)


def int(t):
    r, g, b = t
    return r*256*256 + g*256 + b

# 点降噪
def interference_point(_img,img_name, x = 0, y = 0):

    img = _img.load()
    """
    9邻域框,以当前点为中心的田字框,黑点个数
    :param x:
    :param y:
    :return:
    """
    # filename =  './out_img/' + img_name.split('.')[0] + '-interferencePoint.jpg'
    # todo 判断图片的长宽度下限

    cur_pixel = img[x, y]# 当前像素点的值
    height, width = _img.size
    for y in range(0, width - 1):
      for x in range(0, height - 1):
        if y == 0:  # 第一行
            if x == 0:  # 左上顶点,4邻域
                # 中心点旁边3个点
                sum = int(cur_pixel) \
                      + int(img[x, y + 1]) \
                      + int(img[x + 1, y]) \
                      + int(img[x + 1, y + 1])
                if sum <= 2 * 245:
                  img[x, y] = 0
            elif x == height - 1:  # 右上顶点
                sum = int(cur_pixel) \
                      + int(img[x, y + 1]) \
                      + int(img[x - 1, y]) \
                      + int(img[x - 1, y + 1])
                if sum <= 2 * 245:
                  img[x, y] = 0
            else:  # 最上非顶点,6邻域
                sum = int(img[x - 1, y]) \
                      + int(img[x - 1, y + 1]) \
                      + int(cur_pixel) \
                      + int(img[x, y + 1]) \
                      + int(img[x + 1, y]) \
                      + int(img[x + 1, y + 1])
                if sum <= 3 * 245:
                  img[x, y] = 0
        elif y == width - 1:  # 最下面一行
            if x == 0:  # 左下顶点
                # 中心点旁边3个点
                sum = int(cur_pixel) \
                      + int(img[x + 1, y]) \
                      + int(img[x + 1, y - 1]) \
                      + int(img[x, y - 1])
                if sum <= 2 * 245:
                  img[x, y] = 0
            elif x == height - 1:  # 右下顶点
                sum = int(cur_pixel) \
                      + int(img[x, y - 1]) \
                      + int(img[x - 1, y]) \
                      + int(img[x - 1, y - 1])
                if sum <= 2 * 245:
                  img[x, y] = 0
            else:  # 最下非顶点,6邻域
                sum = int(cur_pixel) \
                      + int(img[x - 1, y]) \
                      + int(img[x + 1, y]) \
                      + int(img[x, y - 1]) \
                      + int(img[x - 1, y - 1]) \
                      + int(img[x + 1, y - 1])
                if sum <= 3 * 245:
                  img[x, y] = 0
        else:  # y不在边界
            if x == 0:  # 左边非顶点
                sum = int(img[x, y - 1]) \
                      + int(cur_pixel) \
                      + int(img[x, y + 1]) \
                      + int(img[x + 1, y - 1]) \
                      + int(img[x + 1, y]) \
                      + int(img[x + 1, y + 1])
                if sum <= 3 * 245:
                  img[x, y] = 0
            elif x == height - 1:  # 右边非顶点
                sum = int(img[x, y - 1]) \
                      + int(cur_pixel) \
                      + int(img[x, y + 1]) \
                      + int(img[x - 1, y - 1]) \
                      + int(img[x - 1, y]) \
                      + int(img[x - 1, y + 1])
                if sum <= 3 * 245:
                  img[x, y] = 0
            else:  # 具备9领域条件的
                sum = int(img[x - 1, y - 1]) \
                      + int(img[x - 1, y]) \
                      + int(img[x - 1, y + 1]) \
                      + int(img[x, y - 1]) \
                      + int(cur_pixel) \
                      + int(img[x, y + 1]) \
                      + int(img[x + 1, y - 1]) \
                      + int(img[x + 1, y]) \
                      + int(img[x + 1, y + 1])
                if sum <= 4 * 245:
                  img[x, y] = 0
    # cv2.imwrite(filename,img)
    return img


def remove_noise(_img, window=1):
    """ 中值滤波移除噪点
        """
    img = _img.load()
    if window == 1:
        # 十字窗口
        window_x = [1, 0, 0, -1, 0]
        window_y = [0, 1, 0, 0, -1]
    elif window == 2:
        # 3*3矩形窗口
        window_x = [-1, 0, 1, -1, 0, 1, 1, -1, 0]
        window_y = [-1, -1, -1, 1, 1, 1, 0, 0, 0]

    width, height = _img.size

    for i in xrange(width):
        for j in xrange(height):
            box = []
            black_count, white_count = 0, 0
            for k in xrange(len(window_x)):
                d_x = i + window_x[k]
                d_y = j + window_y[k]
                try:
                    d_point = img[d_x, d_y]
                    if d_point == BLACK:
                        box.append(1)
                    else:
                        box.append(0)
                except IndexError:
                    img[i, j] = WHITE
                    continue

            box.sort()
            if len(box) == len(window_x):
                mid = box[len(box) / 2]
                if mid == 1:
                    img[i, j] = BLACK
                else:
                    img[i, j] = WHITE

#按照阀值设置灰度
def dealImg(self):
    width, heith = self.img.size
    threshold = 21
    for i in range(0, width):
        for j in range(0, heith):
            p = self.frame[i, j]
            r, g, b = p
            if r > threshold or g > threshold or b > threshold:
                self.frame[i, j] = WHITE
            else:
                self.frame[i, j] = BLACK

def batch_trasf(path1 ):

    index = 0
    for path, dirs, files in os.walk(path1):
        for file in files:
                index = index + 1
                print file, path
                ## 处理每一个文件
                test_deal_img(path, file, "%s.jpg" % str(index))





def batch_trfimg_convert():
    #批量转化样本图片
    batch_trasf(imagdir)
    #辅助程序，转化tif
    batchConvertTif(trfimagedir)

# if __name__ == "__main__":
#
#     group_id = ""
#     group_url = doubanurl.DOUBAN_GROUP + group_id
#     topiclist = doubanutil.get_topics()
#     count = 100
#     while count > 0:
#       for tp in topiclist:
#         topic_url = tp
#         print "the processing topics url is :[%s]" % tp
#         comment_topic_url = topic_url + "/add_comment#last"
#         comment_str = "up" + "%d" % random.randint(100, 500)
#         comment_dict = comment.make_comment_dict_fake(topic_url, comment_str)
#         img = doubanutil
#
#         random_sleep = random.randint(1, 5)
#         time.sleep(random_sleep)
#         count = count - 1
#
#     print " the  autoComment is finished "
