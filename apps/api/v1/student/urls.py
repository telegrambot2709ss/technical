from django.urls import path

from apps.api.v1.student import views

urlpatterns = [
    # With orm
    path('list/', views.StudentView.as_view(), name="student-list"),
    path('create/', views.StudentView.as_view(), name="student-create"),
    path('info/<int:pk>/', views.StudentView.as_view(), name="student-info"),
    path('update/<int:pk>/', views.StudentView.as_view(), name="student-update"),
    path('delete/<int:pk>/', views.StudentView.as_view(), name="student-delete"),

    # with sql
    path("paginate/list/", views.StudentListPaginationView.as_view(), name="student-list-paginate"),
]
