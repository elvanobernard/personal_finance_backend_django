from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from finances_record import views

urlpatterns = [
    path('expense-categories/', views.ExpenseCategoryList.as_view()),
    path('income-categories/', views.IncomeCategoryList.as_view()),
    path('cash-accounts/', views.CashAccountList.as_view()),
    path('expenses/', views.ExpenseEntryList.as_view()),
    path('expenses/<int:pk>/', views.ExpenseEntryDetail.as_view()),
    path('incomes/', views.IncomeEntryList.as_view()),
    path('incomes/<int:pk>/', views.IncomeEntryDetail.as_view()),
    path('cash/', views.CashEntryList.as_view()),
    path('cash/<int:pk>/', views.CashEntryDetail.as_view()),
    path('balance-summary/', views.BalanceSummaryList.as_view()),
    # path('monthly-expense-summary/', views.MonthlyExpenseSummaryList.as_view()),
    path('monthly-expense-summary/<int:year>/<int:month>/', views.MonthlyExpenseSummaryList.as_view()),
    path('monthly-income-summary/<int:year>/<int:month>/', views.MonthlyIncomeSummaryList.as_view()),
    # path('monthly-income-summary/<int:year>/<int:month>/', views.MonthlyIncomeSummaryList.as_view()),
    path('payables/', views.PayableList.as_view()),
    path('payables/<int:pk>/', views.PayableDetail.as_view()),
    path('receivables/', views.ReceivableList.as_view()),
    path('receivables/<int:pk>/', views.ReceivableDetail.as_view()),
]

urlpatterns = format_suffix_patterns(urlpatterns)