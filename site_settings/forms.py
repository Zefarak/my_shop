from django import forms
from .models import PaymentOrders, PaymentMethod


class PaymentForm(forms.ModelForm):
    object_id = forms.IntegerField(widget=forms.HiddenInput())
    is_expense = forms.BooleanField(widget=forms.HiddenInput())
    date_expired = forms.DateTimeField(widget=forms.DateTimeInput(attrs={'type': 'date',}))

    class Meta:
        model = PaymentOrders
        fields = ['date_expired', 'value', 'title', 'payment_method', 'is_paid', 'content_type', 'object_id']
        exclude = ['date_created', ]

    def __init__(self, *args, **kwargs):
        super(PaymentForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'


class PaymentMethodForm(forms.ModelForm):

    class Meta:
        model = PaymentMethod
        fields = "__all__"

    def __init__(self, *args, **kwargs):
        super(PaymentMethodForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'