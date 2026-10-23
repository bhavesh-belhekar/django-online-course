
from django.contrib import admin
from django.urls import path
from onlinecourse import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path(
        'submit/<int:question_id>/',
        views.submit,
        name='submit'
    ),
    path(
        'exam/<int:course_id>/result/',
        views.show_exam_result,
        name='show_exam_result'
    ),
]
