from nle_library.httpHelp.NetWorkBusiness import *
import http.client
import json
import sys
import time 

headers = {'Content-Type':'application/json', 'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36'}
accessToken = None
try:
    connect = http.client.HTTPConnection('192.168.18.239:81')
    data = {'Account':'18306821670', 'Password':'123456789'}
    connect.request('POST', '/users/login', body=json.dumps(data), headers=headers)
    accessToken = json.loads(connect.getresponse().read().decode())['ResultObj']['AccessToken']
    print('AccessToken:'+accessToken)
    connect.close()
except Exception as e:
    print(e)
    accessToken = None
    sys.exit(1)

netWorkBusiness = NetWorkBusiness('192.168.18.239',81)
netWorkBusiness.setAccessToken(accessToken)
tempData = None

if __name__ == '__main__':
    while True:
        try:
            tempData = netWorkBusiness.getDeviceSensorHistoryDatas(147460, 'm_temp')
        except Exception as e:
            print(e)
        if(tempData):
            finallyData = tempData['ResultObj']['DataPoints'][0]
            print(
                {
                    'ApiTag:': finallyData['ApiTag'],
                    'Value:': finallyData['PointDTO'][0]['Value'],
                    'Time:':finallyData['PointDTO'][0]['RecordTime']
                }
            )
        time.sleep(2)
