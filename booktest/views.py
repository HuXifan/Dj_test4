from django.shortcuts import render
from django.template import loader, RequestContext
from django.http import HttpResponse
from booktest.models import BookInfo


def my_render(request, template_path, context={}):
    # 1 加载模板上下文，获取一个模板对象
    temp = loader.get_template(template_path)
    # 2 定义模板上下文，给模板文件传数据
    context = RequestContext(request, context)  # 字典就是要给模板文件穿的数据
    # 3 模板渲染，产生一个替换后的html内容
    res_html = temp.render(context)
    return HttpResponse(res_html)


# /index
def index(request):
    # 1 加载模板上下文，获取一个模板对象
    # temp = loader.get_template('booktest/index.html')
    # # 2 定义模板上下文，给模板文件传数据
    # context = RequestContext(request, {})  # 字典就是要给模板文件穿的数据
    # # 3 模板渲染，产生一个替换后的html内容
    # res_html = temp.render(context)
    # return HttpResponse(res_html)
    return render(request, 'booktest/index.html')


def index2(request):
    # 模板文件的加载顺序
    return render(request, 'booktest/index2.html')


# /temp_var
def temp_var(request):
    #  模板变量
    my_dict = {'title': '字典键值'}
    my_list = [1, 2, 3]
    book = BookInfo.objects.get(id=1)
    context = {'my_dict': my_dict, 'my_list': my_list, 'book': book}

    return render(request, 'booktest/temp_var.html', context)


# /temp_tags
def temp_tags(request):
    # 模板标签
    # 通过模型类从数据库丽查
    # 1 查找所有图书信息
    books = BookInfo.objects.all()
    # 传给页面去展示
    return render(request, 'booktest/temp_tags.html', {'books': books})


def temp_filter(request):
    # 模板标签
    # 通过模型类从数据库丽查
    # 1 查找所有图书信息
    books = BookInfo.objects.all()
    # 传给页面去展示
    return render(request, 'booktest/temp_filter.html', {'books': books})


def temp_inhertit(request):
    '''模板继承'''
    return render(request, 'booktest/child.html')


def html_escape(request):
    '''html转义'''
    return render(request, 'booktest/html_escape.html', {'content': '<h1>hello</h1>'})
