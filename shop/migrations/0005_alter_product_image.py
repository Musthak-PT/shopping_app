# Generated by Django 5.1a1 on 2024-06-27 17:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0004_alter_order_customer'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='image',
            field=models.ImageField(default=None, upload_to='gallery'),
            preserve_default=False,
        ),
    ]
