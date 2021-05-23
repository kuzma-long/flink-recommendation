# Generated by Django 2.2.1 on 2021-05-06 13:13

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ('shop', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='XinWei',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nums', models.IntegerField(default=0, verbose_name='次数')),
                ('date', models.DateTimeField(auto_now_add=True, verbose_name='时间')),
                ('case_item', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='shop.Case_item')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': '行为表',
                'verbose_name_plural': '行为表',
            },
        ),
        migrations.CreateModel(
            name='Dianji',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateTimeField(auto_now_add=True, verbose_name='时间')),
                ('case_item', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='shop.Case_item')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': '点击表',
                'verbose_name_plural': '点击表',
            },
        ),
    ]
