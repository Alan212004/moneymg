# Generated by Django 5.1 on 2024-08-31 09:37

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0006_alter_product_category_remove_product_prd_type_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='inventorytransaction',
            name='product',
        ),
        migrations.RemoveField(
            model_name='product',
            name='supplier',
        ),
        migrations.DeleteModel(
            name='InventoryItem',
        ),
        migrations.DeleteModel(
            name='InventoryTransaction',
        ),
        migrations.DeleteModel(
            name='Product',
        ),
    ]
