import time
import network
from umqttsimple import MQTTClient


def do_connect():
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    if not wlan.isconnected():
        print('connecting to network...')
        wlan.connect('FAST_4136', 'GXY.20040705.0')
        i = 1
        while not wlan.isconnected():
            print("正在链接...{}".format(i))
            i += 1
            time.sleep(1)
    print('network config:', wlan.ifconfig())


def sub_cb(topic, msg): # 回调函数，收到服务器消息后会调用这个函数
    print(topic, msg)

if __name__ == "__main__":
    # 1. 联网
    do_connect()
    # 2. 创建mqt
    c = MQTTClient("esp32", "43.138.232.18", '1883', 'admin', 'guoxiangyang1.0', keepalive=60)  # 建立一个MQTT客户端
    c.set_callback(sub_cb)  # 设置回调函数
    c.connect()  # 建立连接
    c.subscribe("my_esp32")  # 监控ledctl这个通道，接收控制命令
    for i in range(100):
        c.check_msg()
        time.sleep(1)
        c.publish('hello','esp32111..%d'%i)
        print('esp32111..%d'%i)
        time.sleep(0.5)
