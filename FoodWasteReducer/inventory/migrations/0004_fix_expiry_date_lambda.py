from django.db import migrations,models
from django.utils import timezone

def default_expiry_date():
    return timezone.now().date() + timezone.timedelta(days=7)

def forwards_func(apps, schema_editor):
    FoodItem = apps.get_model('inventory', 'FoodItem')
    for item in FoodItem.objects.all():
        if not item.expiry_date:
            item.expiry_date = default_expiry_date()
            item.save()

class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0003_convert_quantity_to_integer'),
    ]

    operations = [
        migrations.RunPython(forwards_func),
        migrations.AlterField(
            model_name='fooditem',
            name='expiry_date',
            field=models.DateField(default=default_expiry_date),
        ),
    ]