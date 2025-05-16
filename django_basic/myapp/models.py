from django.db import models

class Area(models.Model):
    name = models.CharField('エリア名', max_length=100, unique=True)

    def __str__(self):
        return self.name

class Country(models.Model):
    area = models.ForeignKey(Area, verbose_name='エリア', on_delete=models.CASCADE)
    name = models.CharField('国名', max_length=100, unique=True)

    def __str__(self):
        return self.name

class Month(models.Model):
    name = models.CharField('月', max_length=10, unique=True)
    number = models.IntegerField('月番号', unique=True)

    def __str__(self):
        return self.name

class Tags(models.Model):
    name = models.CharField('タグ名', max_length=100, unique=True)

    def __str__(self):
        return self.name

class Spot(models.Model):
    country = models.ForeignKey(Country, verbose_name='国', on_delete=models.CASCADE)
    name = models.CharField('観光地名', max_length=200)
    information = models.TextField('詳細情報')
    best_season = models.ManyToManyField(Month, verbose_name='ベストシーズン', blank=True)
    photo = models.ImageField(upload_to='myapp/picture/', blank=True, null=True, verbose_name="イメージ")
    tag = models.ManyToManyField(Tags, verbose_name='タグ', blank=True)

    def __str__(self):
        return self.name

    def get_tag_ids(self):
        return list(self.tag.values_list('id', flat=True))

    def get_month_ids(self):
        return list(self.best_season.values_list('id', flat=True))

    class Meta:
        verbose_name = '観光スポット'
        verbose_name_plural = '観光スポット'
        unique_together = ('country', 'name')