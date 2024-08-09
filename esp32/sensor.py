import time
import network
import ujson
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

#这里需要根据自己的情况进行适当修改配置
homeassistant_device_name = "ESP32-04"
homeassistant_device_sensor_name = "1"
homeassistant_device_sensor_type = "Temp"
#下面的内容是固定格式，只需要替换对应数据就行
homeassistant_config_topic ="homeassistant/sensor/HA/HA-%s-%s/config"% (homeassistant_device_name, homeassistant_device_sensor_name)

homeassistant_config_content={

"unique_id":"HA-%s-%s"% (homeassistant_device_name,homeassistant_device_sensor_name),
"name":homeassistant_device_sensor_type,

"icon":"mdi:thermometer",

"state_topic":"HA-%s/%s/state" % (homeassistant_device_name, homeassistant_device_sensor_name),

"json_attributes_topic": "HA-%s/%s/attributes" % (homeassistant_device_name, homeassistant_device_sensor_name),

#＂unit＿of＿measurement＂：＂℃＂＃注意这个数据在ESP32中会导致发送失败，即℃符号导致发送失败，所以不要发这种数据

"device":{

"identifiers": homeassistant_device_name, "manufacturer": "gxy",

"model":"HA",

"name": homeassistant_device_name, "sw_version":"1.0"

} }

homeassistant_state_topic="HA-%s/%s/state"% (homeassistant_device_name, homeassistant_device_sensor_name)

homeassistant_state_content = 23
#这里是温度传感器的值，可以改为真正的数值（通过DS18B20采集）

def main():

#1.联网
    do_connect()

    # 2. 创建mqtt客户端#设备名字 mqtt的ip mqtt的port mqtt的用户名 mqtt的密码

    c = MQTTClient("esp32", "43.138.232.18", '1883', 'admin', 'guoxiangyang1.0', keepalive=60)  # 建立一个MQTT客户端

    c.set_callback(sub_cb)
    
    # 设置回调函数

    c.connect()

    # 建立连接

    c.subscribe(b"my_esp32")

    time.sleep(0.5)

    #发送自动配置MQTT服务的数据包

    send_content = ujson.dumps(homeassistant_config_content)

    c.publish(homeassistant_config_topic, send_content) # 告诉homeassistant服务器,有个新的设备实体要注册

    for i in range(10000):

        # c.check_msg

        time.sleep(0.5)

        c.publish(homeassistant_state_topic, "%d" % i)

        # 发送温度数据给HomeAssistant

        print("esp32...%d" % i)

        time.sleep(1)

if __name__ == "__main__":
    main()