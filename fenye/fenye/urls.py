"""fenye URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.core.paginator import Paginator,Page,PageNotAnInteger,EmptyPage
from  django.shortcuts import HttpResponse,render
data = []
for i in range(999):        #创建数据
    data.append(i)


class PageInfo(object):
    def __init__(self,current_page,per_page):       #参数设置当前页，每页显示多少调数据
        self.current_page = current_page
        self.per_page = per_page

    def start(self):
        return (self.current_page - 1) * self.per_page
    def end(self):
        return self.current_page * self.per_page




def custom(request):
    current_page = request.GET.get('page')      #获取用户请求的第几页
    current_page = int(current_page)
    #每页显示多少数据个数
    per_page = 10
    #1 0:10
    #2 10:20
    #3 20:30
    #得到第一页
    page_info=PageInfo(current_page,10)

    all_page,div = divmod(len(data),10)

    #all_page,得到整数
    #div，取余数

    if div > 0:     #如果div 余数大于0，表示8页+div条数据，实际应该是9页数据
        all_page += 1   #所以最后总共页数需要+1

    pager_str=""
    if current_page >5 and current_page < all_page:            #翻页动态显示，以当前页为中心，只显示10调
        page_start= current_page - 5
        page_end =  current_page + 5
        if page_end > all_page:                 #当结束页大于总共页，则结束页的值为总共页
            page_end = all_page

    elif current_page <= 5:
        page_start = 1              #假如当前页小于5，显示前10页，
        page_end = 11
    elif current_page == all_page:
        page_start = current_page - 10
        page_end = current_page


    for i in range(page_start,page_end):
        temp = '<a  class="btn btn-default" href="/custom/?page=%d" role="button">%d</a>' %(i,i)

        pager_str += temp

    if current_page >5 and current_page <= all_page:
        temp1='<a  class="btn btn-default" href="/custom/?page=1" role="button">1</a>'
        pager_str = temp1 + pager_str
        temp2 = '<a  class="btn btn-default" href="/custom/?page=%d" role="button">%d</a>' %(all_page,all_page)
        pager_str = pager_str + temp2

    user_list = []
    for i in range(page_info.start(),page_info.end()):      #获取对应的数据放入列表
        user_list.append(i)
    return render(request,"custom.html",{'user_list':user_list,'pager_str':pager_str})



urlpatterns = [
    path('admin/', admin.site.urls),
    path('custom/', custom),
]
