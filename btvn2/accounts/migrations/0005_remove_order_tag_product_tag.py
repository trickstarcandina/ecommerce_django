# Generated by Django 4.0.2 on 2022-02-28 16:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0004_tag_order_tag'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='order',
            name='tag',
        ),
        migrations.AddField(
            model_name='product',
            name='tag',
            field=models.ManyToManyField(to='accounts.Tag'),
        ),
    ]
