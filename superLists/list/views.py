import json

from django.shortcuts import render,render_to_response
from django.http import HttpResponse
from django import template
import os
from  .flight_data import test_data


register = template.Library()
# Create your views here.
def index(request):
    return render(request,'index.html',{
# 'new_item_text': request.POST.get('item_text', ''),
})
def Search_route(request):
    if request.method=='POST':
        print (request.POST.get('next'))
        src=request.POST.get('src_city')
        des=request.POST.get('des_city')
        # route_data = master_file(src,des)
        data={}
        lvl_0_data,lvl_1_data = test_data.path_data()

        #print(os.getcwd())
        # result = search_routes(src,des,lvl_1_data, lvl_0_data)
        print(lvl_0_data)
        res_1 = json.dumps(lvl_0_data,indent=4,sort_keys=True)
        res_1 += '\r\n'+json.dumps(lvl_0_data,indent=4,sort_keys=True)
        # print(result)
        return HttpResponse(res_1)


def search_routes(src, des, lvl_1_data, lvl_0_data):
    db0 = lvl_0_data
    db1 = lvl_1_data
    result = []

    for source in db0['src']:
        if source == src:
            for dest in db0['src'][source]:
                if dest == des:
                    result[src+'-'+des].append(db0['src'][source][dest])

    st = src+'_'+des
    if st in db1:
        result[src+'-'+des] .append(db1[st])

    return result