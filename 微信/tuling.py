
import requests
def getresponse(_info):
    apiurl = 'http://www.tuling123.com/openapi/api'
    data = {
        'key':'9d5b1c331e8c4fe68a8243f9587f753e',
        'info':_info,
        'userid':'snall'
    }
    r = requests.post(apiurl,data).json()
    return r

print(getresponse("666"))
