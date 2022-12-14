from django.contrib import admin
from django.urls import path,include
from admin_app import views

urlpatterns = [
    path('admin_login/', views.admin_login, name="admin_login"),
    path('admin_logout/', views.admin_logout, name="admin_logout"),
    path('admin_home', views.admin_home, name="admin_home"),
    path('admin_view_users', views.admin_view_users, name="admin_view_users"),
    path('block/<int:id>',views.block, name='block'),
    path('unblock/<int:id>',views.unblock, name='unblock'),
    path('category_add',views.category_add, name='category_add'),
    path('export_to_pdf',views.export_to_pdf, name='export_to_pdf'),
    path('add_product',views.add_product,name='add_product'),
    path('update/<int:id>',views.updaterow, name='update'),
    path('list_product',views.list_product,name='list_product'),
    path('<int:id>',views.deleterow, name='delete'),
    path('admin_order_management/',views.admin_order_management,name='admin_order_management'),
    path('admin_cancel_order/<int:id>',views.admin_cancel_order, name='admin_cancel_order'), 
    path('admin_order_detailed_view/<int:id>',views.admin_order_detailed_view, name='admin_order_detailed_view'),
    path('filter_order/<str:status>',views.filter_order,name='filter_order'),
    path('coupan_management/', views.coupan_management, name="coupan_management"),
    path('category_offer_management/', views.category_offer_management, name="category_offer_management"),
    path('export_to_excel',views.export_to_excel, name='export_to_excel'),
    # path('sales',views.sales, name='sales'),
    # path('monthly_sales',views.monthly_sales, name='monthly_sales'),
    # path('export_to_excel1',views.export_to_excel1, name='export_to_excel1'),
    # path('export_to_pdf1',views.export_to_pdf1, name='export_to_pdf1'),
    path('view_categories',views.view_categories, name='view_categories'),
    path('delete_category/<int:id>',views.delete_category, name='delete_category'),
    path('product_offer_management/', views.product_offer_management, name="product_offer_management"),
    path('view_offers',views.view_offers, name='view_offers'),
    path('delete_category_offer/<int:id>',views.delete_category_offer, name='delete_category_offer'),
    path('delete_product_offer/<int:id>',views.delete_product_offer, name='delete_product_offer'),
    path('delete_coupan_offer/<int:id>',views.delete_coupan_offer, name='delete_coupan_offer'),
    path('view_coupan',views.view_coupan, name='view_coupan'),
    path('sales',views.sales_report_date, name='sales'),
]