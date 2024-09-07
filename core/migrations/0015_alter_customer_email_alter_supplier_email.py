# Generated by Django 5.1.1 on 2024-09-06 07:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0014_customer_user_ptransaction_user_stransaction_user_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customer',
            name='email',
            field=models.EmailField(blank=True, max_length=254, null=True),
        ),
        migrations.AlterField(
            model_name='supplier',
            name='email',
            field=models.EmailField(blank=True, max_length=254, null=True),
        ),
    ]
