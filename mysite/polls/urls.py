from . import views
from django.urls import path

"""pk is used as it is framework config for classbased view.
If not use and use custom name need to change it. 
In view as pk_url_kwarg ='question_id'.
Then framework can map it.
"""

app_name = "polls"
urlpatterns = [
    path('', views.IndexView.as_view(), name = "index"),
    path("<int:pk>/", views.DetailView.as_view(), name = "detail"), 
    path("<int:pk>/results/", views.ResultView.as_view(), name = "results"),
    path("<int:question_id>/vote/", views.vote, name = "vote"),
]
