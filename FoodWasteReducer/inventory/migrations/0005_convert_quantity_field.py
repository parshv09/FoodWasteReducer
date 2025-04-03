from django.db import migrations,models

def convert_quantity_values(apps, schema_editor):
    FoodItem = apps.get_model('inventory', 'FoodItem')
    for item in FoodItem.objects.all():
        try:
            # Convert string to integer, default to 1 if invalid
            item.quantity = int(float(item.quantity)) if item.quantity else 1
            item.save()
        except (ValueError, TypeError):
            item.quantity = 1
            item.save()

class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0004_fix_expiry_date_lambda'),
    ]

    operations = [
        migrations.RunPython(convert_quantity_values),
        migrations.AlterField(
            model_name='fooditem',
            name='quantity',
            field=models.PositiveIntegerField(default=1),
        ),
    ]