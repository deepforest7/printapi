from flask import Flask, request
import flask
import json
import random
import serial
#form icecream import ic

app = Flask(__name__)

from wsgiref.simple_server import make_server

# 只接受get方法访问
@app.route("/dibang", methods=["GET"])
def check():
    # 默认返回内容
    return_dict = {'return_code': '500', 'return_info': '处理失败', 'result': False}
    # 判断入参是否为空
    com = flask.request.values.get('com')
    bsp = flask.request.values.get('bsp')

    if com and bsp:
        # 对参数进行操作,并将结果返回
        return_dict['result'] = getdata(com, bsp)
        
        return json.dumps(return_dict, ensure_ascii=False)
    else:
        return json.dumps(return_dict, ensure_ascii=False)


# 功能函数
def getdata(com, bsp):  # 发送函数
    try:

        '''    connect serial'''
        try:
            '''    connect serial'''
            x = serial.Serial(com, bsp,timeout=0.3)  # 这是我的串口，测试连接成功，没毛病
        except Exception as e:
            print(e)
            return_dict['return_info'] = '串口链接超时'
            return 

        myinput = bytes([0x02,0x41,0x42,0x30,0x33,0x03])
        #print(myinput[2:5])
        x.write(myinput)

        data = x.read(14)
        datas =''.join(map(lambda x:('/x' if len(hex(x))>=4 else '/x0')+hex(x)[2:],data))#将数据转成十六进制的形式
        #datas =''.join(map(lambda x:('0x' if len(hex(x))>=4 else '0x0')+hex(x)[2:],data))#将数据转成十六进制的形式

        print(datas)
        #datas = '/x02/x41/x42/x2b/x30/x30/x30/x30/x30/x30/x30/x31/x38/x03'
        new_datas = datas.split("/x")#将字符串分割，拼接下标4和5部分的数据

        #拼接整数位
        nums = ''
        for num in new_datas[5:11]:
            ic(num)
            nums += str(bytes.fromhex(num), encoding='utf-8')


        ic(new_datas[12])
        nums = nums +'.' + str(bytes.fromhex(new_datas[11]), encoding='utf-8')
        ic(nums)
        nums = float(nums)
        ic(nums)
    except Exception as e:
        print(e)
    return nums
    # if nums :
   	#     return_dict['return_info'] = '处理成功'
    #     return_dict['return_code'] = '200'
    #     return nums


# 默认返回内容
return_dict = {'return_code': '500', 'return_info': '处理失败', 'r1': False, 'r2': False}


# 只接受get方法访问
@app.route("/dianziweilan", methods=["GET"])
def checkin():
    # 判断入参是否为空
    com = flask.request.values.get('com')
    bsp = flask.request.values.get('bsp')
    if com and bsp:
        # 对参数进行操作
        print(com, bsp)
        return_dict['return_code'] = '200'
        return_dict['return_info'] = '处理成功'
        return_dict['r1'], return_dict['r2'] = dianziweilan(com, bsp)
        return json.dumps(return_dict, ensure_ascii=False)

    else:
        return_dict['return_info'] = '参数为空'
        return json.dumps(return_dict, ensure_ascii=False)


# 获取电子围栏寄存器状态
def dianziweilan(com, bsp):
    r1 = False
    r2 = False

    try:
        try:
            '''    connect serial'''
            x = serial.Serial(com, bsp,timeout=0.3)  # 这是我的串口，测试连接成功，没毛病
        except Exception as e:
            print(e)
            return_dict['return_info'] = '串口链接超时'
        '''    connect dibang   握手'''
        myinput = bytes([0xFE, 0x02, 0x00, 0x00, 0x00, 0x04, 0x6D, 0xC6])
        x.write(myinput)

        '''    read from dianziweilan '''
        myout = x.read(6)  # 读取串口传过来的字节流，这里我根据文档只接收7个字节的数据

        if len(myout) < 6:
            return_dict['return_info'] = '串口未拿到返回值'

        datas = ''.join(map(lambda x: ('/x' if len(hex(x)) >= 4 else '/x0') + hex(x)[2:], myout))  # 将数据转成十六进制的形式

        new_datas = datas.split("/x")  # 将字符串分割，拼接下标4和5部分的数据

        '''     chuli '''
        status = new_datas[4]
        print(status)
        if status == '01':
            r1 = True
        if status == '03':
            r2 = True
            r1 = True
        if status == '02':
            r2 = True
    except Exception as e:
        print(e)

    # my_need = int(hex(int(need,16)),16)#将十六进制转化为十进制
    # my_need = my_need/10
    # print('weight',my_need)

    print(r1, r2)
    return r1, r2


if __name__ == "__main__":
    #server = make_server('', 5000, app)
    #server.serve_forever()
    app.run(host='0.0.0.0', port=5000, debug=True)
