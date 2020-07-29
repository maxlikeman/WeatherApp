from django.conf.urls import url
from . import views

urlpatterns = [
    url('^$', views.news_today, name='newsToday'),
    url(r'^archives/(\d{4}-\d{2}-\d{2})/$', views.past_days_news, name='pastNews')
]
