from django import forms
from .models import FoodItem
from django.utils import timezone
from django.core.validators import RegexValidator  # Add this import

class FoodItemForm(forms.ModelForm):
    quantity = forms.CharField(
        validators=[RegexValidator(r'^[0-9]+$', 'Enter a valid number')]
    )
    
    class Meta:
        model = FoodItem
        fields = ['name', 'quantity', 'category', 'expiry_date']
        widgets = {
            'expiry_date': forms.DateInput(attrs={
                'type': 'date',
                'min': timezone.now().date().isoformat()
            }),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['expiry_date'].initial = timezone.now().date() + timezone.timedelta(days=7)