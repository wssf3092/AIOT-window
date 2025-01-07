from paho.mqtt import client as mqtt
import uuid
import requests
import os
from datetime import datetime

# API和风天气, 这里调试过了，api每日有使用限制，不需要重复调试
API_KEY = "b6e0be06cab03e87ce3cb6324f90027c"

DATA = dict()
def get_forecast():
    response = requests.get('https://devapi.qweather.com/v7/minutely/5m?location=102.42,25.02&key=3a4aa2839f7746c2a502d5e603202d2a' )
    if response.status_code == 200:
        data = response.json()
        forecast = []
        for item in data['minutely']:
            if float(item['precip']) >= 0.3:
                forecast.append({
                    "precip": item['precip'],
                    "time": item['fxTime']
                })
        summary = data['summary']
        return forecast,summary
    else:
        return None

def get_preci():
    fore, suma = get_forecast()
    print(fore)
    print(suma)



#mqtt部分
def on_connect(client, userdata, flags, rc):
    """
    一旦连接成功, 回调此方法
    rc的值表示成功与否：
        0:连接成功
        1:连接被拒绝-协议版本不正确
        2:连接被拒绝-客户端标识符无效
        3:连接被拒绝-服务器不可用
        4:连接被拒绝-用户名或密码不正确
        5:连接被拒绝-未经授权
        6-255:当前未使用。
    """
    rc_status = ["连接成功", "协议版本不正确", "客户端标识符无效", "服务器不可用", "用户名或密码不正确", "未经授权"]
    print("connect：", rc_status[rc])


def mqtt_connect():
    """连接MQTT服务器"""

    mqttClient = mqtt.Client(mqtt.CallbackAPIVersion.VERSION1, str(uuid.uuid4()))
    mqttClient.on_connect = on_connect  # 返回连接状态的回调函数
    mqttClient.on_message = on_message
    MQTTHOST = "127.0.0.1"  # MQTT服务器地址
    MQTTPORT = 1883  # MQTT端口
#   mqttClient.username_pw_set("username", "password")  # MQTT服务器账号密码, 无密码时注释即可
    mqttClient.connect(MQTTHOST, MQTTPORT, 60)
    mqttClient.loop_start()  # 启用线程连接

    return mqttClient


def mqtt_publish():
    """发布主题为'mqtt/demo',内容为'Demo text',服务质量为2"""
    mqttClient = mqtt_connect()

    text = "Demo text"
    mqttClient.publish('window/control', text, 2)
    mqttClient.loop_stop()

def on_message(client, userdata, msg):
    """一旦订阅到消息, 回调此方法"""
    print("主题:"+msg.topic+" 消息:"+str(msg.payload.decode('gb2312')))
    DATA[msg.topic] = str(msg.payload.decode('gb2312'))


def on_subscribe():
    """订阅主题：mqtt/demo"""
    mqttClient = mqtt_connect()
    mqttClient.subscribe("window/tem", 2)

#web部分


if __name__ == '__main__':
    # mqttClient = mqtt_connect()
    # mqtt_publish()
    # on_subscribe()
    # mqttClient.loop_forever()
