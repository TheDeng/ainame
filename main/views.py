from django.shortcuts import render
from django.http import FileResponse
from itertools import combinations, permutations
import requests
import uuid
import os
import json
from django.conf import settings
file_root=settings.MEDIA_ROOT
# Create your views here.
def home(request):
	return render(request,'home.html')

def result(request):
	return render(request,'result.html')

def genname(request):
	#根据是否是post请求进行分类处理
	if request.method=='POST':
		key1=request.POST.get('keyword1',None)
		key2=request.POST.get('keyword2',None)
		key3=request.POST.get('keyword3',None)
		key4=request.POST.get('keyword4',None)
		keylist=list()
		keylist.append(key1)
		keylist.append(key2)
		keylist.append(key3)
		keylist.append(key4)
		filename=str(uuid.uuid4())+'.doc'
		file_path=os.path.join(file_root,filename)
		file=open(file_path,'w')
		result=getNameList(keylist)
		statement='共有'+str(len(result))+'个名字'+'\n'
		file.write(statement)
		for i,name  in enumerate(result,1):
			file.write(str(i)+':'+'['+name+']'+'\n')
		quantity=len(result);

		content = list()
		for i, r in enumerate(result, 1):
			c = str(i) + '. [ ' + r+' ]'
			content.append(c)


		return render(request,'result.html',{'filename':filename,'quantity':quantity,'content':content})


def download(request,filename):

	file=open(os.path.join(file_root,filename),'rb')
	response =FileResponse(file) 
	response['Content-Type']='application/octet-stream'
	response['Content-Disposition']='attachment;filename="result.txt"'
	return response 


def getNameList(keylist):
	temp=list()
	for key in keylist:
		if key !=None and key!='':
			temp.append(key)
	re=list()
	#print (len(temp))
	for i in range(2,len(temp)+1):
		r=list(permutations(temp,i))
		# print(r)
		for item in r:
			s=''
			for j in range(0,i):
				s=s+item[j]

			re.append(s)
	result=list(set(re))
	result.sort(key=re.index)
	return result

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
        return True
    else:
        return False
		