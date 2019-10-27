from booktest import views
from django.conf.urls import include, url

urlpatterns = [
    url(r'^index$', views.index),
    url(r'^index2$', views.index2),  # 模板加载顺序

    url(r'^temp_var$', views.temp_var),  # 模板变量
    url(r'^temp_tags$', views.temp_tags),  # 模板变量
    url(r'^temp_filter$', views.temp_filter),  # 模板过滤器

    url(r'^temp_inhertit$', views.temp_inhertit),  # 模板继承

]
