from django.contrib import admin
from django.urls import path
from pdf_app import views

urlpatterns = [
    path("admin/", admin.site.urls),                        # Django admin interface
    path("", views.home, name="home"),
    path("upload_pdf/", views.upload_pdf, name="upload_pdf"),
    path("successful_upload/", views.successful_upload, name="successful_upload"),
    path("ask_question/", views.ask_question, name="ask_question"),
    path("insufficient_quota/", views.insufficient_quota, name="insufficient_quota"),
    path("rate_limit_exceeded/", views.rate_limit_exceeded, name="rate_limit_exceeded"),]


