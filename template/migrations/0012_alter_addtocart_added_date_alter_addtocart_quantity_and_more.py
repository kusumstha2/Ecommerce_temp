# Generated by Django 5.1.7 on 2025-03-27 07:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("template", "0011_remove_orderitem_order_remove_orderitem_product_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="addtocart",
            name="added_date",
            field=models.DateTimeField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name="addtocart",
            name="quantity",
            field=models.PositiveIntegerField(),
        ),
        migrations.AlterField(
            model_name="addtocart",
            name="total_price",
            field=models.DecimalField(
                decimal_places=2, default=0, editable=False, max_digits=10
            ),
        ),
    ]
