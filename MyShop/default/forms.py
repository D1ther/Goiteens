from django import forms
from .models import User, Product, Comment

class RegisterForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    password_confirm = forms.CharField(widget=forms.PasswordInput)
    
    class Meta:
        model = User
        fields = ['username', 'email']
    
    def clean(self):
        cleaned_data = super().clean()
        if cleaned_data.get('password') != cleaned_data.get('password_confirm'):
            raise forms.ValidationError('Паролі не збігаються!')
        return cleaned_data
    
class AddProduct(forms.Form):
    name = forms.CharField(max_length=255)
    description = forms.CharField(widget=forms.Textarea)
    price = forms.DecimalField(max_digits=10, decimal_places=2)
    stock = forms.IntegerField(min_value=0)
    rating = forms.FloatField(min_value=0.0, max_value=5.0)

    class Meta:
        model = Product
        fields = ['name', 'description', 'price', 'stock', 'rating']

    def clean(self):
        return super().clean()
    
class AddComment(forms.Form):
    content = forms.CharField(widget=forms.Textarea, label='Коментар')

    class Meta:
        model = Comment
        fields = ['content']
    
