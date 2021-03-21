# Generated by Django 3.1.7 on 2021-03-21 16:11

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('storehouse', '0003_auto_20210321_1553'),
    ]

    operations = [
        migrations.AddField(
            model_name='bookinstance',
            name='order_item',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='storehouse.orderitem'),
        ),
        migrations.AlterField(
            model_name='bookinstance',
            name='order',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='storehouse.order'),
        ),
    ]
