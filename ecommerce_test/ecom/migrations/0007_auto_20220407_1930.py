# Generated by Django 3.0.5 on 2022-04-07 12:30

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ecom', '0006_auto_20220406_1917'),
    ]

    operations = [
        migrations.RenameField(
            model_name='book',
            old_name='book_image',
            new_name='product_image',
        ),
    ]
