from datetime import datetime, timedelta
from django.shortcuts import render, redirect
from django.template import loader, RequestContext
from django.http import HttpResponse
from booktest.models import BookInfo


def login_required(view_func):
    '''登录判断装饰器'''

    # 定义闭包函数
    def wrapper(request, *view_args, **view_kwargs):
        # 判断用户是否登录
        if request.session.has_key('islogin'):
            # 用户已登录
            return view_func(request, *view_args, **view_kwargs)
        else:
            # 未登录，跳转登录页
            return redirect('/login')

    return wrapper


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


def login(request):
    '''显示登录页面'''
    # 先判断用户是否登录
    if request.session.has_key('islogin'):
        # 用户已经登录，跳转首页
        return redirect('/change_pwd')
    else:
        # 用户没有登录
        # 获取登录cookie username
        if 'username' in request.COOKIES:
            # 如果Cookie丽有username，取值，取空
            username = request.COOKIES['username']
        else:
            username = ''
        return render(request, 'booktest/login.html', {'username': username})


def login_check(request):
    # 登录校验视图
    # 1 获取提交的用户名和密码
    # POST和GET对应提交的方式,都是QueryDict类型的对象
    print(request.method)
    print(type(request.POST))  # <class 'django.http.request.QueryDict'>

    username = request.POST.get('username')
    password = request.POST.get('password')  # 有输出
    remember = request.POST.get('remember')

    # 获取验证码
    vcode1 = request.POST.get('vcode')
    vcode0 = request.session.get('verifycode')  # 前面session保存的验证码
    # 进行验证码校验
    if vcode1 != vcode0:
        # 验证码错误
        return redirect('/login')

    print(username, password)
    # 2 进行登录的校验。模拟 hu  666
    if username == 'hu' and password == '666':
        # 用户名密码正确，跳转首页
        # 用户名和密码正确的时候判断是否需要记住户名密码
        # response = redirect('/index')  # HttpResponse
        response = redirect('/change_pwd')  # 跳转到修改密码页面
        if remember == 'on':
            response.set_cookie('username', username, max_age=100)
            # response.set_cookie('username', username, expires=datetime.now() + timedelta(days=14))
            # 设置usename过期时间为1周 Set-Cookie: username=hu; expires=Thu, 31-Oct-2019 08:19:29 GMT; Max-Age=604800
        # 记住用户登录状态
        request.session['islogin'] = True  # 只要有这个值就说明登录

        # 记住用户的登录名
        request.session['username'] = username
        return response  # 设置好cookie后再应答
    else:
        # 密码错误跳转登录页面
        return redirect('/login')

    # 3 返回应答
    # return HttpResponse('OK login_check')


# /change_pwd
@login_required
def change_pwd(request):
    '''    显示修改密码页面    '''
    # 对用户登录进行判断
    # if not request.session.has_key('islogin'):
    #     return redirect('/login')

    return render(request, 'booktest/change_pwd.html')


# /change_pwd_action
@login_required
def change_pwd_action(request):
    '''模拟修改密码处理'''
    # 对用户登录进行判断
    if not request.session.has_key('islogin'):
        return redirect('/login')

    # 1 获取新密码
    pwd = request.POST.get('pwd')
    # 获取用户名
    username = request.session.get('username')
    # 2 实际开发：修改数据库中的内容
    # 3 返回一个应答
    return HttpResponse('%s修改密码为：%s' % (username, pwd))


from PIL import Image, ImageDraw, ImageFont
from django.utils.six import BytesIO


# 　/verify_code
def verify_code(request):
    # 引入随机函数模块
    import random
    # 定义变量，用于画面的背景色、宽、高
    bgcolor = (random.randrange(20, 100), random.randrange(
        20, 100), 255)
    width = 100
    height = 25
    # 创建画面对象
    im = Image.new('RGB', (width, height), bgcolor)
    # 创建画笔对象
    draw = ImageDraw.Draw(im)
    # 调用画笔的point()函数绘制噪点
    for i in range(0, 100):
        xy = (random.randrange(0, width), random.randrange(0, height))
        fill = (random.randrange(0, 255), 255, random.randrange(0, 255))
        draw.point(xy, fill=fill)  # 画笔的point方法
    # 定义验证码的备选值
    str1 = 'ABCD123EFGHIJK456LMNOPQRS789TUVWXYZ0'
    # 随机选取4个值作为验证码
    rand_str = ''
    for i in range(0, 4):
        # 随机选出四个字母作为验证码
        rand_str += str1[random.randrange(0, len(str1))]
    # 构造字体对象，ubuntu的字体路径为“/usr/share/fonts/truetype/freefont”
    # /usr/share/fonts/truetype/noto/   deepin字体路径
    font = ImageFont.truetype('NotoSans-Bold.ttf', 23)
    # 构造字体颜色
    fontcolor = (255, random.randrange(0, 255), random.randrange(0, 255))
    # 绘制4个字
    draw.text((5, 2), rand_str[0], font=font, fill=fontcolor)
    draw.text((25, 2), rand_str[1], font=font, fill=fontcolor)
    draw.text((50, 2), rand_str[2], font=font, fill=fontcolor)
    draw.text((75, 2), rand_str[3], font=font, fill=fontcolor)
    # 释放画笔
    del draw
    # 存入session，用于做进一步验证
    request.session['verifycode'] = rand_str
    # 内存文件操作
    buf = BytesIO()
    # 将图片保存在内存中，文件类型为png
    im.save(buf, 'png')
    # 将内存中的图片数据返回给客户端，MIME类型为图片png
    return HttpResponse(buf.getvalue(), 'image/png')
