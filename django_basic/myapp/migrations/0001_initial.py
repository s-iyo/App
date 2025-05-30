# Generated by Django 5.2.1 on 2025-05-21 05:00

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Area',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, unique=True, verbose_name='エリア名')),
            ],
        ),
        migrations.CreateModel(
            name='Month',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=10, unique=True, verbose_name='月')),
                ('number', models.IntegerField(unique=True, verbose_name='月番号')),
            ],
        ),
        migrations.CreateModel(
            name='Tags',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, unique=True, verbose_name='タグ名')),
            ],
        ),
        migrations.CreateModel(
            name='Country',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, unique=True, verbose_name='国名')),
                ('area', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='myapp.area', verbose_name='エリア')),
            ],
        ),
        migrations.CreateModel(
            name='Spot',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200, verbose_name='観光地名')),
                ('information', models.TextField(verbose_name='詳細情報')),
                ('photo', models.ImageField(blank=True, null=True, upload_to='myapp/picture/', verbose_name='イメージ')),
                ('best_season', models.ManyToManyField(blank=True, to='myapp.month', verbose_name='ベストシーズン')),
                ('country', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='myapp.country', verbose_name='国')),
                ('tag', models.ManyToManyField(blank=True, to='myapp.tags', verbose_name='タグ')),
            ],
            options={
                'verbose_name': '観光スポット',
                'verbose_name_plural': '観光スポット',
                'unique_together': {('country', 'name')},
            },
        ),
        migrations.CreateModel(
            name='FavoriteSpot',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('added_at', models.DateTimeField(auto_now_add=True, verbose_name='追加日時')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='ユーザー')),
                ('spot', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='myapp.spot', verbose_name='観光スポット')),
            ],
            options={
                'verbose_name': 'お気に入りスポット',
                'verbose_name_plural': 'お気に入りスポット',
                'unique_together': {('user', 'spot')},
            },
        ),
    ]
