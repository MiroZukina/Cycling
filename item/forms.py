from django import forms
from .models import Item

INPUT_CLASSES = 'w-full py-4 px-6 rounded-xl border'

class NewItemForm(forms.ModelForm):
    class Meta:
        model = Item
        fields = ('category', 'name', 'description', 'price', 'image_url',)
        widgets = {
            'category': forms.Select(attrs={
                'class': INPUT_CLASSES
            }),
            'name': forms.TextInput(attrs={
                'class': INPUT_CLASSES
            }),
            'description': forms.Textarea(attrs={
                'class': INPUT_CLASSES
            }),
            'price': forms.TextInput(attrs={
                'class': INPUT_CLASSES
            }),
            'image': forms.FileInput(attrs={
                'class': INPUT_CLASSES
            })
        }


class EditItemForm(forms.ModelForm):
    class Meta:
        model = Item
        fields = ('name', 'description', 'price', 'image_url', 'is_sold')
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'INPUT_CLASSES'
            }),
            'description': forms.Textarea(attrs={
                'class': 'INPUT_CLASSES'
            }),
            'price': forms.TextInput(attrs={
                'class': 'INPUT_CLASSES'
            }),
        }
    
    # Adding a custom method to render the image_url field with class
    def __init__(self, *args, **kwargs):
        super(EditItemForm, self).__init__(*args, **kwargs)
        self.fields['image_url'].widget.attrs['class'] = 'INPUT_CLASSES'