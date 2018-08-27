from django.views.generic import ListView
from django.shortcuts import render, get_object_or_404
from django.utils.decorators import method_decorator
from django.contrib.admin.views.decorators import staff_member_required
from transcations.models import *


def transcations_homepage(request):
    bills = BillCategory.my_query.get_queryset().is_active()
    payrolls = Person.my_query.get_queryset().is_active()
    expenses = GenericExpenseCategory.objects.filter(active=True)
    context = locals()
    return render(request, 'report/transcations/homepage.html', context)


@method_decorator(staff_member_required, name='dispatch')
class BillsReportView(ListView):
    model = Bill
    template_name = 'report/transcations/page_list.html'
    paginate_by = 100

    def get_queryset(self):
        date_start, date_end, date_range, months_list = estimate_date_start_end_and_months(self.request)
        queryset = Bill.objects.filter(date_expired__range=[date_start, date_end])
        queryset = Bill.filters_data(self.request, queryset)
        return queryset

    def get_context_data(self, **kwargs):
        context = super(BillsReportView, self).get_context_data(**kwargs)
        page__title, currency = 'Bils', CURRENCY
        date_start, date_end, date_range, months_list = estimate_date_start_end_and_months(self.request)
        search_name, bill_name, paid_name = [self.request.GET.get('search_name'),
                                             self.request.GET.getlist('bill_name'),
                                             self.request.GET.get('paid_name')
                                            ]
        bills = BillCategory.my_query.get_queryset().is_active()
        payments_orders = PaymentOrders.objects.filter(object_id__in=self.object_list.values('id'),
                                                       content_type=ContentType.objects.get_for_model(self.object_list.model)
                                                       )
        analysis_per_bill = self.object_list.values('category__title').annotate(value=Sum('final_value'),
                                                                                paid_value_=Sum('paid_value'),
                                                                                remaining=Sum(F('final_value')-F('paid_value'))
                                                                                ).order_by('value')
        context.update(locals())
        return context


@method_decorator(staff_member_required, name='dispatch')
class PayrollReportView(ListView):
    model = Payroll
    template_name = 'report/transcations/payroll.html'
    paginate_by = 50

    def get_queryset(self):
        date_start, date_end, date_range, months_list = estimate_date_start_end_and_months(self.request)
        queryset = Payroll.objects.filter(date_expired__range=[date_start, date_end])
        return queryset

    def get_context_data(self, **kwargs):
        context = super(PayrollReportView, self).get_context_data(**kwargs)
        date_start, date_end, date_range, months_list = estimate_date_start_end_and_months(self.request)
        search_name, bill_name, paid_name = [self.request.GET.get('search_name'),
                                             self.request.GET.getlist('bill_name'),
                                             self.request.GET.get('paid_name')
                                            ]
        persons = Person.my_query.get_queryset().is_active()
        occupations = Occupation.my_query.get_queryset().is_active()
        context.update(locals())
        return context


@method_decorator(staff_member_required, name='dispatch')
class GenericExpenseView(ListView):
    model = GenericExpense
    template_name = 'report/transcations/generic_expenses.html'
    paginate_by = 100

    def get_queryset(self):
        date_start, date_end, date_range, months_list = estimate_date_start_end_and_months(self.request)
        queryset = self.model.objects.filter(date_expired__range=[date_start, date_end])
        return queryset

    def get_context_data(self, **kwargs):
        context = super(GenericExpense, self).get_context_data(**kwargs)
        date_start, date_end, date_range, months_list = estimate_date_start_end_and_months(self.request)
        search_name, bill_name, paid_name = [self.request.GET.get('search_name'),
                                             self.request.GET.getlist('bill_name'),
                                             self.request.GET.get('paid_name')
                                            ]

        context.update(locals())

