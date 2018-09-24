from django.shortcuts import render, HttpResponseRedirect, HttpResponse, redirect, reverse, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, UpdateView, FormView, CreateView, TemplateView
from django.utils.decorators import method_decorator
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib import messages
from django.db.models import Q
from django.contrib.contenttypes.models import ContentType
from django.core.paginator import EmptyPage, Paginator, PageNotAnInteger


from products.models import Product,  Color, Size
from products.forms import VendorForm
from .models import Order, OrderItem, Vendor, Category
from .models import PaymentOrders
from site_settings.forms import PaymentForm
from inventory_manager.models import Order, OrderItem, Vendor
from inventory_manager.forms import OrderQuickForm, VendorQuickForm, WarehouseOrderForm, OrderItemForm

import datetime
import decimal


@method_decorator(staff_member_required, name='dispatch')
class WareHouseOrderPage(ListView):
    template_name = 'inventory_manager/index.html'
    model = Order
    paginate_by = 20

    def get_queryset(self):
        queryset = Order.objects.all()
        queryset = self.model.filter_data(self.request, queryset)
        return queryset

    def get_context_data(self, **kwargs):
        context = super(WareHouseOrderPage, self).get_context_data(**kwargs)
        search_name = self.request.GET.get('search_name', None)
        vendor_name = self.request.GET.getlist('vendor_name', None)
        date_start = self.request.GET.get('date_start', None)
        date_end = self.request.GET.get('date_end', None)
        vendors = Vendor.objects.filter(active=True)
        context.update(locals())
        return context


@staff_member_required
def create_new_warehouse_order(request):
    form = OrderQuickForm(request.POST or None,
                          initial = {'date_expired': datetime.datetime.now()}
                          )
    if form.is_valid():
        instance = form.save()
        return HttpResponseRedirect(reverse('inventory:warehouse_order_detail', kwargs={'dk': instance.id}))
    context = locals()
    return render(request, 'inventory_manager/create_order.html', context)


@staff_member_required
def quick_vendor_create(request):
    form = VendorQuickForm(request.POST or None)
    if form.is_valid():
        instance = form.save()
        return HttpResponse(
            '<script>opener.closePopup(window, "%s", "%s", "#id_vendor");</script>' % (instance.pk, instance))
    return render(request, 'dashboard/ajax_calls/popup_form.html', {"form": form})


@staff_member_required
def warehouse_order_detail(request, dk):
    instance = get_object_or_404(Order, id=dk)
    queryset = Product.my_query.get_site_queryset().active_warehouse().filter(vendor=instance.vendor)
    if 'search_name' in request.GET:
        queryset = queryset.filter(title__icontains=request.GET.get('search_name', None))
    products = queryset.filter(size=False)[:10]
    products_with_size = queryset.filter(size=True)
    form = WarehouseOrderForm(instance=instance)
    
    if 'add_products' in request.GET:
        ids = request.GET.getlist('ids', None)
        if ids:
            for id in ids:
                get_product = get_object_or_404(Product, id=id)
                OrderItem.add_to_order(request, product=get_product, order=instance)
            instance.save()
            return HttpResponseRedirect(reverse('inventory:warehouse_order_detail', kwargs={'dk': instance.id}))
                    
    if request.POST:
        form = WarehouseOrderForm(request.POST, instance=instance)
        if form.is_valid():
            form.save()
            messages.success(request, 'The order Edited!')
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    context = locals()
    return render(request, 'inventory_manager/order_detail.html', context)


@staff_member_required
def order_update_warehouse(request, pk):
    instance = get_object_or_404(Order, id=pk)
    instance.save()
    return HttpResponseRedirect(reverse('inventory:warehouse_order_detail'), kwargs={'dk': pk})


@staff_member_required
def edit_order_item(request, dk):
    instance = get_object_or_404(OrderItem, id=dk)
    page_title = f'Edit {instance.product.title}'
    back_url = reverse('inventory:warehouse_order_detail', kwargs={'dk':instance.order.id})
    old_qty = instance.qty
    form = OrderItemForm(request.POST or None, instance=instance)
    if form.is_valid():
        instance.remove_from_order(old_qty)
        new_qty = request.POST.get('qty')
        form.save()
        instance.quick_add_to_order(new_qty)
        return HttpResponseRedirect(reverse('inventory:warehouse_order_detail', kwargs={'dk': instance.order.id}))
    context = locals()
    return render(request, 'inventory_manager/form.html', context)


@staff_member_required
def delete_order_item(request, dk):
    instance = get_object_or_404(OrderItem, id=dk)
    instance.delete()
    return HttpResponseRedirect(reverse('inventory:warehouse_order_detail', kwargs={'dk': instance.order.id}))


@staff_member_required
def order_payment_manager(request, pk):
    instance = get_object_or_404(Order, id=pk)
    payments = instance.payment_orders.all()
    vendor_payments = instance.vendor.payment_orders.all()
    form = PaymentForm(request.POST or None, 
                       initial={
                           'value': instance.get_remaining_value,
                           'title': 'Hello',
                           'object_id': instance.id,
                           'content_type': ContentType.objects.get_for_model(instance),
                           'is_expense': True,
                           
                       })
    if form.is_valid():
        form.save()
        instance.save()
    context = locals()
    return render(request, 'inventory_manager/order_manage_payments.html', context)

@staff_member_required
def order_payment_manager_add_or_remove(request, pk, dk, slug):
    instance = get_object_or_404(Order, id=pk)
    payment = get_object_or_404(PaymentOrders, id=dk)

    if slug == 'add':
        difference = instance.get_remaining_value
        if difference > 0 and payment.final_value >= difference:
            if payment.final_value == difference:
                payment.object_id = pk
                payment.content_type = ContentType.objects.get_for_model(instance)
                payment.save()
                instance.save()
            else:
                payment.final_value -= difference
                payment.save()
                new_check = payment
                new_check.pk = None
                new_check.object_id = pk
                new_check.content_type = ContentType.objects.get_for_model(instance)
                new_check.final_value = difference
                new_check.save()
                instance.save()
        return HttpResponseRedirect(reverse('inventory:order_payment_manager', kwargs={'pk': pk}))

    if slug == 'delete':
        payment.delete()
        instance.save()
        return HttpResponseRedirect(reverse('inventory:order_payment_manager', kwargs={'pk': pk}))

    if slug == 'paid':
        payment.is_paid = True
        payment.save()
        instance.save()
        return HttpResponseRedirect(reverse('inventory:order_payment_manager', kwargs={'pk': pk}))
    form = PaymentForm(request.POST or None, 
                       instance=payment,
                       initial = {
                           'object_id': payment.object_id,
                           'content_object': payment.content_object,
                           'is_expense': payment.is_expense,
                           'date_expired': payment.date_expired
                        }
                    )
    if form.is_valid():
        form.save()
        return HttpResponseRedirect(reverse('inventory:order_payment_manager', kwargs={'pk': pk}))
    instance.save()
    page_title = f'Edit {instance.title} payment'
    back_url = reverse('inventory:order_payment_manager', kwargs={'pk': pk})
    return render(request, 'inventory_manager/form.html', context=locals())


@method_decorator(staff_member_required, name='dispatch')
class VendorPageList(ListView):
    template_name = 'inventory_manager/vendor_list.html'
    model = Vendor
    paginate_by = 10

    def get_queryset(self):
        queryset = Vendor.objects.all()
        queryset = self.model.filter_data(self.request, queryset)
        return queryset

    def get_context_data(self, **kwargs):
        context = super(VendorPageList, self).get_context_data(**kwargs)
        search_name = self.request.GET.get('search_name', None)
        balance_name = self.request.GET.get('balance_name', None)
        context.update(locals())
        return context


@method_decorator(staff_member_required, name='dispatch')
class VendorPageDetail(UpdateView):
    template_name = 'inventory_manager/vendor_detail.html'
    form_class = VendorForm
    model = Vendor

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('inventory:vendor_list')


@method_decorator(staff_member_required, name='dispatch')
class VendorPageCreate(FormView):
    template_name = 'dashboard/page_create.html'
    form_class = VendorForm

    def get_context_data(self, **kwargs):
        context = super(VendorPageCreate, self).get_context_data(**kwargs)
        page_title, back_url = 'Create Vendor', reverse('inventory:vendor_create')
        context.update(locals())
        return context

    def form_valid(self, form):
        form.save()
        messages.success(self.request, 'New Vendor Added!')
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('inventory:vendor_list')


@method_decorator(staff_member_required, name='dispatch')
class WarehousePaymentPage(ListView):
    model = PaymentOrders
    template_name = 'inventory_manager/payment_list.html'

    def get_queryset(self):
        queryset = PaymentOrders.objects.all()
        return queryset

    def get_context_data(self, **kwargs):
        context = super(WarehousePaymentPage, self).get_context_data(**kwargs)
        search_name = self.request.GET.get('search_name', None)
        paid_name = self.request.GET.get('paid_name', None)
        vendor_name = self.request.GET.getlist('vendor_name', None)
        date_start = self.request.GET.get('date_start', None)
        date_end = self.request.GET.get('date_end', None)
        vendors  = Vendor.objects.filter(active=True)
        context.update(locals())
        return context


@staff_member_required
def warehouse_order_paid(request, pk):
    instance = get_object_or_404(Order, id=pk)
    instance.is_paid = True
    instance.save()
    messages.success(request, 'The order %s is paid.')
    return HttpResponseRedirect(reverse('inventory:payment_list'))


@staff_member_required
def warehouser_order_paid_detail(request, pk):
    instance = get_object_or_404(Order, id=pk)
    vendor = instance.vendor
    create = True
    form = PaymentForm(request.POST or None, initial={'value': instance.get_remaining_value,
                                                      'content_type': ContentType.objects.get_for_model(instance),
                                                      'payment_type': instance.payment_method,
                                                      'title': '%s' % instance.code,
                                                      'date_expired': instance.date_created,
                                                      'object_id': pk,
                                                      'is_expense': True,
                                                      'is_paid':True,
                                                      })
    if request.POST:
        if form.is_valid():
            form.save()
            messages.success(request, 'The payment added!')
            return HttpResponseRedirect(reverse('inventory:ware_order_paid_detail', kwargs={'pk': pk}))
    context = locals()
    return render(request, 'inventory_manager/payment_details.html', context)


@staff_member_required
def warehouse_check_order_convert(request, dk, pk):
    instance = get_object_or_404(PaymentOrders, id=pk)
    order = get_object_or_404(Order, id=dk)
    if instance.value <= order.total_price:
        instance.object_id = dk
        instance.content_type = ContentType.objects.get_for_model(order)
        instance.is_paid = True
        instance.save()
    else:
        new_payment_order = PaymentOrders.objects.create(content_type=ContentType.objects.get_for_model(order),
                                                         object_id=dk,
                                                         title='%s' % order.code,
                                                         date_expired=instance.date_expired,
                                                         payment_type=instance.payment_type,
                                                         bank=instance.bank,
                                                         value=order.total_price,
                                                         is_expense=True,
                                                         is_paid=True
                                                         )
        instance.value -= order.total_price
        instance.save()
    messages.success(request, 'The check order is converted')
    return HttpResponseRedirect(reverse('inventory:ware_order_paid_detail', kwargs={'pk': dk}))


@staff_member_required
def warehouse_order_paid_delete(request, pk):
    instance = get_object_or_404(PaymentOrders, id=pk)
    instance.delete()
    messages.warning(request, 'The payment deleted!')
    return HttpResponseRedirect(reverse('inventory:ware_order_paid_detail', kwargs={'pk': instance.object_id}))


@staff_member_required
def warehouse_edit_paid_order(request, dk, pk):
    instance = get_object_or_404(Order, id=dk)
    payorder = get_object_or_404(PaymentOrders, id=pk)
    form = PaymentForm(request.POST or None,
                       instance=payorder,
                       initial={'is_expense': True
                                })
    create = False
    if request.POST:
        if form.is_valid():
            form.save()
            messages.success(request, 'The paid order is edited')
            return HttpResponseRedirect(reverse('inventory:ware_order_paid_detail',
                                                kwargs={'pk': instance.id}
                                                )
                                        )
    context = locals()
    return render(request, 'inventory_manager/form_edit_payment_order.html', context)


@method_decorator(staff_member_required, name='dispatch')
class WarehousePaymentOrderCreate(CreateView):
    template_name = 'inventory_manager/form.html'
    model = PaymentOrders
    form_class = PaymentForm

    def get_initial(self):
        initial = super(WarehousePaymentOrderCreate, self).get_initial()
        instance = get_object_or_404(Vendor, id=self.kwargs['pk'])
        initial['object_id'] = instance.id
        initial['content_type'] = ContentType.objects.get_for_model(instance)
        initial['date_expired'] = datetime.datetime.now()
        initial['title'] = '%s' % instance.title
        initial['is_expense'] = True
        initial['value'] = instance.balance
        initial['is_check'] = True
        return initial

    def get_context_data(self, **kwargs):
        context = super(WarehousePaymentOrderCreate, self).get_context_data(**kwargs)
        page_title = 'Create Check'
        back_url = reverse('inventory:vendor_list')
        context.update(locals())
        return context

    def form_valid(self, form):
        if form.is_valid():
            form.save()
            instance = get_object_or_404(Vendor, id=self.kwargs['pk'])
            instance.save()
            messages.success(self.request, 'The check created!')
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('inventory:vendor_list')


@staff_member_required
def edit_check_order(request, pk):
    instance = get_object_or_404(PaymentOrders, id=pk)
    form = PaymentForm(request.POST or None, instance=instance, initial={'is_expense': True})
    if form.is_valid():
        form.save()
        messages.success(request, 'The Check order is edited')
        return HttpResponseRedirect(reverse('inventory:vendor_detail', kwargs={'pk': instance.object_id }))
    print(form.errors)
    page_title = 'Edit %s' % instance.title
    context = locals()
    return render(request, 'dash_ware/form.html', context)


    def get_success_url(self):
        instance = get_object_or_404(PaymentOrders, id=self.kwargs['pk'])
        return reverse('inventory:vendor_detail', kwargs={'pk': instance.object_id })


@staff_member_required
def delete_check_order(request, pk):
    instance = get_object_or_404(PaymentOrders, id=pk)
    instance.delete()
    messages.warning(request, 'The Payment Order deleted!')
    return HttpResponseRedirect(reverse('inventory:vendor_detail', kwargs={'pk': instance.object_id}))


@staff_member_required
def check_order_paid(request, pk):
    instance = get_object_or_404(PaymentOrders, id=pk)
    instance.is_paid = True
    instance.save()
    messages.success(request, 'The order is paid.')
    return HttpResponseRedirect(reverse('inventory:vendor_detail', kwargs={'pk': instance.object_id}))


@method_decorator(staff_member_required, name='dispatch')
class CheckOrdersView(ListView):
    template_name = 'inventory_manager/checkOrders.html'
    model = PaymentOrders
    paginate_by = 100

    def get_queryset(self):
        queryset = PaymentOrders.objects.all()
        return queryset

    def get_context_data(self, **kwargs):
        context = super(CheckOrdersView, self).get_context_data(**kwargs)
        vendors = Vendor.objects.filter(active=True)
        vendor_name, search_name, check_name = [self.request.GET.getlist('vendor_name', None),
                                                self.request.GET.get('search_name', None),
                                                self.request.GET.get('check_name', None)
                                                ]
        context.update(locals())
        return context


@method_decorator(staff_member_required, name='dispatch')
class CheckOrderUpdateView(UpdateView):
    model = PaymentOrders
    template_name = 'inventory_manager/form.html'
    form_class = PaymentForm
    success_url = reverse_lazy('inventory:check_orders')

    def get_initial(self):
        initial = super(CheckOrderUpdateView, self).get_initial()
        instance = get_object_or_404(PaymentOrders, id=self.kwargs['pk'])
        initial['object_id'] = instance.id
        initial['content_type'] = instance.content_type
        initial['is_expense'] = instance.is_expense
        return initial

    def get_context_data(self, **kwargs):
        context = super(CheckOrderUpdateView, self).get_context_data(**kwargs)
        back_url = self.success_url
        page_title = 'Edit Payment'
        context.update(locals())
        return context

    def form_valid(self, form):
        form.save()
        messages.success(self.request, 'The Payment is edited')
        return super().form_valid(form)