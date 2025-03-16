from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login/", views.loginuser, name="login"),
    path("logout/", views.logoutuser, name="logout"),
    path("register/", views.register, name="register"),
    path("my-tickets/", views.my_tickets, name="my_tickets"),
    path("create-ticket/", views.create_ticket, name="create_ticket"),
    path("view-ticket/<str:pk>/", views.view_ticket, name="view_ticket"),
    path("transfer-ticket/<str:pk>/",
         views.transfer_ticket, name="transfer_ticket"),
    path("assign-ticket/<str:pk>/", views.assign_ticket, name="assign_ticket"),
    path("change-status/<str:pk>/", views.change_status, name="change_status"),
    path("follow-ticket/<str:pk>/", views.follow_ticket, name="follow_ticket"),
    path("quick-transfer/<str:pk>/", views.quick_transfer_ticket,
         name="quick_transfer_ticket"),
    path("quick-assign/<str:pk>/", views.quick_assign_ticket,
         name="quick_assign_ticket"),
    path("quick-assign/<str:pk>/<str:user_id>/",
         views.quick_assign_ticket, name="quick_assign_ticket"),
]
