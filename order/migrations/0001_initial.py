# Generated by Django 5.0.7 on 2024-08-04 05:52

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('usersapp', '0002_improvepersonal'),
    ]

    operations = [
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('out_trade_num', models.UUIDField()),
                ('order_num', models.CharField(max_length=50)),
                ('trade_no', models.CharField(default='', max_length=120)),
                ('status', models.CharField(default='待支付', max_length=20)),
                ('payway', models.CharField(default='alipay', max_length=20)),
                ('address', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='usersapp.address')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='usersapp.userinfo')),
            ],
        ),
        migrations.CreateModel(
            name='OrderItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('goodsid', models.PositiveIntegerField()),
                ('sizeid', models.PositiveIntegerField()),
                ('count', models.PositiveIntegerField()),
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='order.order')),
            ],
        ),
    ]
