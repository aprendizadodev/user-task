from django.conf.urls import url
from apptask import views

urlpatterns = [
# Rotas user
url(r'^api/user$', views.user_list),
url(r'^api/user/(?P<pk>[0-9]+)$', views.user_detail),

# Rotas task
url(r'^api/task$', views.task_list),
url(r'^api/task/(?P<pk>[0-9]+)$', views.task_detail),
url(r'^api/tasks/state$', views.task_list_state),
url(r'^api/tasks_user/(?P<pk>[0-9]+)$', views.task_list_user)
]