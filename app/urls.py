from django.urls import path
from  . import views 
from django.conf import settings
from django.conf.urls.static import static
from .views import verify_payment
from .views import search_and_export
urlpatterns = [
    path('', views.home, name='home'),
    path('application', views.application, name='application'),
    path('allNews', views.allNews, name='allNews'),
    path('login', views.login_func, name='login'),
    path('register', views.register, name='register'),
    path('contact', views.contact, name='contact'),
    path('submitcontact', views.submitcontact, name='submitcontact'),
    path('student', views.student, name='student'),
    path('token', views.token, name='token'),
    path('gentoken', views.gentoken, name='gentoken'),
    path('profile', views.profile, name='profile'),
    path('exam_slip', views.exam_slip, name='exam_slip'),
    path('test', views.test, name='test'),
    path('result', views.result, name='result'),
    path('payment', views.payment, name='payment'),
    path('course', views.course, name='course'),
    path('getSemester', views.getSemester, name='getSemester'),
    path('examcard', views.examcard, name='examcard'),
    path('getExamCard', views.getExamCard, name='getExamCard'), 
    path('verify-payment/<str:reference>/', verify_payment, name='verify_payment'),
    path('admin/search-export/', search_and_export, name='search_export'),
    path('admin/global-search/', views.global_search_export, name='global_search'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

