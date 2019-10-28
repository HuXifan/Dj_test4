from booktest import views
from django.conf.urls import include, url

urlpatterns = [
    url(r'^index$', views.index),
    url(r'^index2$', views.index2),  # 模板加载顺序

    url(r'^temp_var$', views.temp_var),  # 模板变量
    url(r'^temp_tags$', views.temp_tags),  # 模板变量
    url(r'^temp_filter$', views.temp_filter),  # 模板过滤器

    url(r'^temp_inhertit$', views.temp_inhertit),  # 模板继承
    url(r'^html_escape$', views.html_escape),  # 模板继承
    url(r'^login$', views.login),  # 显示登录页面
    url(r'^login_check$', views.login_check),  # 登录校验
    url(r'^change_pwd$', views.change_pwd),  # 修改密码页面 显示
    # login_required(change_pwd)  先调用login_reqiured
    url(r'^change_pwd_action$', views.change_pwd_action),  # 修改密码处理
    url(r'^verify_code$', views.verify_code)  # 产生验证码图片

]
