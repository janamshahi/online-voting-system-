from django.urls import path
from . import views

urlpatterns = [
    path("register/", views.register, name="register"),
    path("elections/<int:election_id>/", views.election_detail, name="election_detail"),
    path("elections/<int:election_id>/vote/", views.cast_vote, name="cast_vote"),
    path("elections/<int:election_id>/results/", views.results, name="results"),
    
    path(
    "forgot-password/",
    views.forgot_password,
    name="forgot_password",
),
]
