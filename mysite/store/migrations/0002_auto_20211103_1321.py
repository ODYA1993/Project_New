# Generated by Django 3.2 on 2021-11-03 10:21

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='product',
            name='stock',
        ),
        migrations.AlterField(
            model_name='cart',
            name='final_price',
            field=models.DecimalField(decimal_places=0, default=0, max_digits=9, verbose_name='Общая цена'),
        ),
        migrations.AlterField(
            model_name='cartproduct',
            name='user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='store.customer', verbose_name='Покупатель'),
        ),
        migrations.AlterField(
            model_name='product',
            name='price',
            field=models.DecimalField(decimal_places=0, default=0, max_digits=10, verbose_name='Цена'),
        ),
    ]
