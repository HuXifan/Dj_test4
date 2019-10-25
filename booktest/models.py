from django.db import models


# Create your models here
class BookInfo(models.Model):
    # 图书模型类
    # 对应写出来，不需要重新迁移
    btitle = models.CharField(max_length=20)
    bpub_date = models.DateField()
    bread = models.IntegerField(default=0)
    b_comment = models.IntegerField(default=0)
    isDelete = models.BooleanField(default=False)

    class Meta:
        db_table = 'bookinfo'  # 类属性>指定表名
