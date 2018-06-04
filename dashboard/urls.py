from django.contrib import admin
from django.urls import path, include, re_path
from .views import *
from .view_sells import *
from .views_ajax import *

app_name = 'dashboard'

urlpatterns = [
    path('', DashBoard.as_view(), name='home'),

    path('products/', ProductsList.as_view(), name='products'),
    path('products/create/', ProductCreate.as_view(), name='product_create'),
    path('products/<int:pk>/', view=product_detail, name='product_detail'),
    path('products/add-images/<int:dk>/', ProductAddMultipleImages.as_view(), name='product_add_images'),
    path('products/delete-images/<int:pk>/', view=delete_product_image, name='delete_image'),
    path('products/add-sizes/<int:dk>/', view=product_add_sizechart, name='product_add_sizes'),
    path('products/add-sizes/create/<int:dk>/<int:pk>/', view=create_new_sizechart, name='create_product_sizechart'),
    path('products/add-related-products/<int:pk>/', RelatedProductsView.as_view(), name='product_related_view'),

    # popup and ajax calls
    # path('products/popup/create-brand/', view=createBrandPopup, name='brand_popup'),
    # path('products/popup/create-category/', view=createCategoryPopup, name='category_popup'),
    # path('products/popup/get_brand_id/', view=get_brand_id, name='get_brand_id'),
    # path('products/popup/create-color/', view=create_color_popup, name='color_popup'),


    path('category/', CategoryPage.as_view(), name='categories'),
    path('categories-site/', CategorySitePage.as_view(), name='categories_site'),
    path('brands/', BrandPage.as_view(), name='brands'),
    path('colors/', ColorPage.as_view(), name='colors'),
    path('sizes/', SizePage.as_view(), name='sizes'),

    # popup and ajax calls
    path('products/popup/create-brand/', view=createBrandPopup, name='brand_popup'),
    path('products/popup/create-category/', view=createCategoryPopup, name='category_popup'),
    path('products/popup/get_brand_id/', view=get_brand_id, name='get_brand_id'),
    path('products/popup/create-color/', view=create_color_popup, name='color_popup'),

    path('category/', CategoryPage.as_view(), name='categories'),
    path('categories-site/', CategorySitePage.as_view(), name='categories_site'),
    path('brands/', BrandPage.as_view(), name='brands'),
    path('colors/', ColorPage.as_view(), name='colors'),
    path('sizes/', SizePage.as_view(), name='sizes'),

    #  create urls
    path('category/create/', CategoryCreate.as_view(), name='category_create'),
    path('brands/create/', BrandsCreate.as_view(), name='brands_create'),
    path('colors/create/', ColorCreate.as_view(), name='color_create'),
    path('sizes/create/', SizeCreate.as_view(), name='size_create'),
    path('category/site/create/', CategorySiteCreate.as_view(), name='category_site_create'),

    #  delete urls
    path('category/delete/<int:pk>/', view=delete_category, name='delete_category'),
    path('brands/delete/<int:pk>/', view=delete_brand, name='delete_brand'),
    path('color/delete/<int:pk>/', view=delete_color, name='delete_color'),

    # edit url
    path('category/detail/<int:pk>/', CategoryDetail.as_view(), name='category_detail'),
    path('category/site/<int:pk>/', CategorySiteEdit.as_view(), name='edit_category_site'),
    path('brands/edit/<int:pk>', view=brandEditPage, name='edit_brand'),
    path('size/edit/<int:pk>', SizeEditPage.as_view(), name='edit_size'),
    path('color/edit/<int:pk>/', ColorEditPage.as_view(), name='edit_color'),


    # redirects
    path('product/copy/<int:pk>/', view=create_copy_item, name='copy_product'),

    path('site-settings', view=create_copy_item, name='site_view'),

    path('warehouse/home/', view=create_copy_item, name='warehouse_home'),

    # order section
    path('eshop-orders/', EshopOrdersPage.as_view(), name='eshop_orders_page'),
    path('eshop-orders/create/', view=create_eshop_order, name='eshop_order_create'),
    path('eshop-orders/edit/<int:pk>/', view=eshop_order_edit, name='eshop_order_edit'),
    path('eshop-orders/add-or-edit/<int:dk>/<int:pk>/<int:qty>/', view=add_edit_order_item, name='add_or_create'),
    path('eshop-orders/edit-order-item/<int:dk>/', view=edit_order_item, name='edit_order_item'),
    path('eshop-orders/delete-order-item/<int:dk>/', view=delete_order_item, name='delete_order_item'),
    path('eshop-orders/print/<int:pk>/', view=print_invoice, name='print_invoice'),

    path('warehouse/order/shipping/', ShippingPage.as_view(), name='shipping_view'),
    path('warehouse/order/shipping/detail/<int:pk>/', ShippingEditPage.as_view(), name='shipping_edit_view'),
    path('warehouse/order/shipping/delete/<int:pk>/', view=delete_shipping, name='shipping_delete_view'),
    path('warehouse/order/shipping/create/', ShippingCreatePage.as_view(), name='shipping_create_view'),

    path('warehouse/order/payment-method/', PaymentMethodPage.as_view(), name='payment_view'),
    path('warehouse/order/payment-method/detail/<int:pk>/', PaymentMethodEditPage.as_view(), name='payment_edit_view'),
    path('warehouse/order/payment-method/delete/<int:pk>/', view=delete_payment_method, name='payment_delete_view'),
    path('warehouse/order/payment-method/create/', PaymentMethodCreatePage.as_view(), name='payment_create_view'),

    path('eshop-order/fast-change-status/', view=order_choices, name='order_choices'),


    # ajax calls
    #  ajax calls
    path('category/ajax/create/', view=category_create, name='ajax_create_category'),
    path('category/ajax/get_category_id', view=get_category_id, name="ajax_category_id"),
]

