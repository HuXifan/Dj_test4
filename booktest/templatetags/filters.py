# 父文件夹的名称是固定的就是 templatetags 自定义过滤器 >> 过滤器的本质是Python的函数
from django.template import Library

# 创建Library的实例对象
register = Library()


# 使用register的filter方法装饰mod，是成为过滤器
@register.filter
def mod(num):
    # 判断num是否为偶数
    return num % 2 == 0


@register.filter
def mod_val(num, val):
    '''判断num能否被val整除'''
    return num % val == 0


'''
自定义过滤器函数，至少一个参数，最多两个
格式：模板变量｜过滤器：参数
'''
