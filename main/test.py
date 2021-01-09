import requests
import json

def validate(markword):
    url='http://api.tmkoo.com/search.php'
    payload={'keyword':markword,'apiKey':'A_YV7B47ha','apiPassword':'SpQExUEXMH','pageSize':'0','pageNo':'1','searchType':'1'}
    r=requests.get(url,payload)
    json_response=r.content.decode()
    dict_json=json.loads(json_response)
    print(type(dict_json))
    print(dict_json)
    namelist=list()
    for cell in dict_json["results"]:
        name=cell["tmName"]
        namelist.append(name)

    print(namelist)
    if markword in namelist:
        print(True)
    else:
        print(False)

if __name__ == '__main__':
    validate('小甜')