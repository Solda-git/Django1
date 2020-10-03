from django import forms

from kworders.models import Order, OrderItem
from main.models import Product


class FormControlMixin:
    ## to be optimized!!! extract Mixin from this form and from other project forms
    ## and insert in different project folder
    def __init__(self, *args, **kwargs):
        super ().__init__ (*args, **kwargs)
        for field_name, field in self.fields.items ():
            field.widget.attrs['class'] = f'form-control {field_name}'
            field.help_text = ''

class  OrderForm (FormControlMixin, forms.ModelForm):
    class  Meta:
        model = Order
        exclude = ('user', 'is_active', 'status')


class  OrderItemForm (FormControlMixin, forms.ModelForm):
    price = forms.CharField(label='цена', required=False)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs);
        self.fields["product"].queryset = Product.get_items()

    class  Meta:
        model = OrderItem
        fields = ('__all__')
        #exclude = ()
