from django.conf.urls import url

from judge import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^index$', views.index, name='index'),
    url(r'^styles.css$', views.css, name='css'),
    url(r'^questions$', views.questions, name='questions'),
    url(r'^ranks', views.ranks, name='ranks'),
    url(r'^submit', views.submit, name='submit'),
    url(r'^logout', views.logout, name='logout'),
    url(r'^register', views.register, name='register'),
    url(r'^question$', views.questions, name='questions'),
    url(r'^questions/(?P<question>[A-Z]\.txt)$', views.display_question, name='display_question'),
    url(r'^submissions$', views.all_submissions, name='all_submissions'),

]
