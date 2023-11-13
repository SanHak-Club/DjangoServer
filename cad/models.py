from django.db import models


# Create your models here.
class Cad(models.Model):
    _id = models.CharField(primary_key=True, max_length=100)
    author = models.CharField(max_length=100)
    mainCategory = models.CharField(max_length=255)
    subCategory = models.CharField(max_length=255)
    title = models.CharField(max_length=255)
    index = models.TextField()
    s3Url = models.TextField()
    createdAt = models.DateTimeField()
    _class = models.CharField(max_length=255)
    tfidf = models.TextField(default="")
    CadLabel = models.CharField(max_length=255, default="")  # 추가된 필드

    class Meta:
        db_table = "cad"