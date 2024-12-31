from django.urls import path
from . import views
from django.contrib.auth.views import LoginView, LogoutView
from .forms import UserLoginForm

app_name = "polls"
urlpatterns = [
    path("", views.index, name="home"),
    #path('/accounts/login/', LoginView.as_view(authentication_form=UserLoginForm), name="login"),
    path('login/', LoginView.as_view(template_name='login.html'), name='login'),
    #path('login/', views.custom_login, name='custom_login'),  # this is not working .
    # path('logout/', LogoutView.as_view(next_page='/'), name='logout'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('bookyourride/', views.bookyourride,name='bookyourride'),
    path('register/', views.registerView, name="register_url"),
    path("driverdetail/", views.driverdertail, name="driverdetail"),
    path("create/", views.create_driver_detail, name="create_driver_detail"),
    path('add/', views.person_create_view, name='person_add'),
    path('<int:pk>/', views.person_update_view, name='person_change'),
    path('ajax/load-cities/', views.load_cities, name='ajax_load_cities'), # AJAX
    path('success/', views.success, name='success'),
    path('travelonewayinput/', views.travelonewayinput, name='travelonewayinput'),
    path('cardetailview/', views.cardetailview, name='cardetailview'),
    path('book/', views.book_car_view, name='book_car'),
    path('booksuccess/', views.booking_success, name='booking_success'),
    path('hotels/', views.hotelsview, name='hotels'),

    # path("<int:question_id>/", views.detail, name="detail"),
    # path("<int:question_id>/result", views.result, name="result"),
    # path("<int:question_id>/vote/", views.vote, name="vote"),
    # path("", views.IndexView.as_view(), name="index"),
    # path("<int:pk>/", views.DetailView.as_view(), name="detail"),
    # path("<int:pk>/results/", views.ResultsView.as_view(), name="results"),
    # path("<int:question_id>/vote/", views.vote, name="vote"),
]