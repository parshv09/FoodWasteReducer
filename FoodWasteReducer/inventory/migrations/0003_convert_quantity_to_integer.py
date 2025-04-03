from django.db import migrations,models

def convert_quantity(apps, schema_editor):
    FoodItem = apps.get_model('inventory', 'FoodItem')
    for item in FoodItem.objects.all():
        try:
            # Convert string quantity to integer
            item.quantity = int(''.join(filter(str.isdigit, item.quantity or '0')))
            item.save()
        except (ValueError, TypeError):
            item.quantity = 1
            item.save()

class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0002_alter_fooditem_expiry_date'),
    ]

    operations = [
        migrations.RunPython(convert_quantity),
        migrations.AlterField(
            model_name='fooditem',
            name='quantity',
            field=models.PositiveIntegerField(default=1),
        ),
    ]