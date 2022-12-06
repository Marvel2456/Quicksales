from django.forms import ModelForm, ValidationError
from django import forms
from django.contrib.auth.forms import UserCreationForm
from account.models import CustomUser
from . models import *

class UserCreateForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = (
            'username', 'password1', 'password2', 'is_admin', 'is_sub_admin', 'is_work_staff'
            )

class UserForm(ModelForm):
    class Meta:
        model = CustomUser
        fields = ('first_name', 'last_name', 'phone_number', 'address')

class ProductForm(ModelForm):
    class Meta:
       model = Product
       fields = ('product_name', 'category', 'brand', 'unit', 'batch_no')
       
       widgets = {
           'category': forms.Select(attrs={'class':'form-select', 'placeholder':'Category', 'required':True, 'title':'Select Category'})
       }

    def clean(self):
        super(ProductForm, self).clean()

        product_name = self.cleaned_data.get('product_name')
        for product in Product.objects.all():
            if product.product_name == product_name:
                self._errors['product_name'] = self.error_class([
                'The product you tried to create already exists'])

        return self.cleaned_data   

class EditProductForm(ModelForm):
    class Meta:
        model = Product
        fields = ('product_name', 'category', 'brand', 'unit', 'batch_no',)

class CategoryForm(ModelForm):
    class Meta:
        model = Category
        fields = ('category_name',)

    def clean(self):
        super(CategoryForm, self).clean()

        category_name = self.cleaned_data.get('category_name')

        for category in Category.objects.all():
            if category.category_name == category_name:
                self._errors['category_name'] = self.error_class([
                'The category you tried to create already exists'])

        return self.cleaned_data   

class EditCategoryForm(ModelForm):
    class Meta:
        model = Category
        fields = ('category_name',)

class CreateInventoryForm(ModelForm):
    class Meta:
        model = Inventory
        fields = ('product', 'quantity', 'cost_price', 'sale_price', 'reorder_level')

    def clean(self):
        super(CreateInventoryForm, self).clean()

        product = self.cleaned_data.get('product')

        for inventory in Inventory.objects.all():
            if inventory.product.product_name == product.product_name:
                self._errors['product'] = self.error_class([
                'The inventory you tried to create already exists'])

        return self.cleaned_data   

class RestockForm(ModelForm):
    class Meta:
        model = Inventory
        fields = ('quantity_restocked', 'sale_price', 'cost_price')

class EditInventoryForm(ModelForm):
    class Meta:
        model = Inventory
        fields = ('reorder_level',)

class CreateTicketForm(ModelForm):
    class Meta:
        model = ErrorTicket
        fields = ('title', 'description')
        exclude = ['staff']

class UpdateTicketForm(ModelForm):
    class Meta:
        model = ErrorTicket
        fields = ('status',)

        widgets = {
            'status': forms.Select(attrs={'class':'form-select', 'placeholder':'status', 'required':True})
        }

class PaymentForm(ModelForm):
    class Meta:
        model = Sale
        fields = ('method',)


