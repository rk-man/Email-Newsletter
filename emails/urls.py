from django.urls import path
from emails.views import subscribeUser, getSubscriptionConfirmed, loginAdmin, adminDashboard, getSingleContent, createContent, deleteContent,sendMailContent, getAllSubscribers, logoutAdmin

urlpatterns = [
    path("me/dashboard/subscribers/",getAllSubscribers,name = "all-subscribers"),
    path("", subscribeUser, name="subscribe-user"),
    path("confirm-subscription/<str:subscriber_id>/",
         getSubscriptionConfirmed, name="subscription-confirmed"),
    path("me/", loginAdmin, name="admin-login"),
    path("me/logout", logoutAdmin, name="admin-logout"),
    path("me/dashboard/", adminDashboard, name="admin-dashboard"),
    path("me/dashboard/<str:pk>/send-mail/", sendMailContent, name = "send-mail"),
    path("me/dashboard/<str:pk>/delete/", deleteContent, name = "delete-content"),
    path("me/dashboard/create/", createContent, name="create-content"),
    path("me/dashboard/<str:pk>/", getSingleContent, name="single-content"),
]
