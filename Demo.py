import requests
import json
import threading
import time

class DataThread(threading.Thread):
    def __init__(self, name, headers):
        super().__init__(name=name)
        self.headers = headers
    def run(self):
        while True:
            tempData = get_Data("m_temp", self.headers)
            print("传感器数据："+tempData)
            time.sleep(2)

session = requests.Session()
headers = None

def get_Token():
    headers = {"Content-Type": "application/json"}
    data = {"Account":"18306821670","Password":"123456789"} 
    response = session.post("http://192.168.18.239:81/Users/Login",headers=headers,data=json.dumps(data))
    token = response.json()["ResultObj"]["AccessToken"]
    headers["AccessToken"] = token
    return headers

def get_Data(apiTag,headers):
    response = session.get("http://192.168.18.239:81/devices/147461/datas?apitags="+apiTag, headers=headers)
    try:
        data = response.json()["ResultObj"]["DataPoints"][0]["PointDTO"][0]["Value"]
    except Exception as e:
        print(e)
    return data

def Turn(deviceId,apiTag,result):
    session.post("http://192.168.18.239:81/Cmds"+"?deviceId="+deviceId+"&apiTag="+apiTag,headers=headers,data=result)

if __name__ == '__main__':
    headers= get_Token()
    Turn("147461", "m_fan", "1")
    data_thread = DataThread("datathread", headers)
    data_thread.start()