'''
打印word pdf excel

'''
import win32print
import win32api

import base64
def base64Encode(img_path):
    '''
    图片64编码
    :param img_path:
    :return:
    '''
    try:
        image = open(img_path, 'rb')  # open binary file in read mode
        image_read = image.read()
        image_64_encode = base64.encodestring(image_read)
        print(image_64_encode)
        return image_64_encode
    except Exception as e:
        print(e)

def base64Decode(base64code,img):
    '''
    图片解码
    :param base64code:
    :param img: 图片保存路径
    :return: 图片保存路径
    '''
    try:
        image_64_decode = base64.decodestring(base64code)
        image_result = open(img, 'wb')  # create a writable image and write the decoding result
        image_result.write(image_64_decode)
        return img
    except Exception as e:
        print(e)

def callprint(img):
    '''
    调用打印机打印图片
    :param img_path:
    :return:
    '''
    try:
        fn = img
        win32api.ShellExecute(0,\
                              'print',\
                              fn,\
                              win32print.GetDefaultPrinterW(),\
                              ".",
                              0)
    except Exception as e:
        print(e)


if __name__ == '__main__':

    img_path = 'C:\\Users\\DeepForest\\Pictures\\微信图片_20210319111956.jpg'
    base64code = base64Encode(img_path)
    img = 'C:\\Users\\DeepForest\\Pictures\\0210319111956.jpg'
    img = base64Decode(base64code,img)
    callprint(img)