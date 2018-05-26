from django.db import models
from jsonfield import JSONField


# Create your models here.

class FaceCharacteristic(models.Model):
    id = models.AutoField(primary_key=True)
    # union_id = models.CharField(max_length=100)  # 用户唯一ID
    characteristic_value = JSONField()  # 脸部特征值
