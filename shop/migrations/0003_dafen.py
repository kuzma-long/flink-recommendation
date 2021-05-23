# Generated by Django 2.2.1 on 2021-05-10 07:52

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ('shop', '0002_dianji_xinwei'),
    ]

    operations = [
        migrations.CreateModel(
            name='DaFen',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fenshu', models.FloatField(default=0, verbose_name='分数')),
                ('date', models.DateTimeField(auto_now_add=True, verbose_name='时间')),
                ('case_item', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='shop.Case_item')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': '打分表',
                'verbose_name_plural': '打分表',
            },
        ),
    ]
