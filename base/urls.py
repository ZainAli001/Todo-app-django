from django.contrib import admin
from django.urls import path,include
from base.views import TaskList,TaskDetail,TaskCreate,TaskUpdate,TaskDelete,CustomeLoginView,RegisterPage
from django.contrib.auth.views import LogoutView


urlpatterns = [

    path('',TaskList.as_view(),name="tasks" ),
    # path('task/<int:pk>/',TaskDetail.as_view(),name="task" ),
    path('task-create/',TaskCreate.as_view(),name="task-create" ),
    path('task-update/<int:pk>/',TaskUpdate.as_view(),name="task-update" ),
    path('task-delete/<int:pk>/',TaskDelete.as_view(),name="task-delete" ),
    
    path('login/', CustomeLoginView.as_view(),name="login" ),
    path('logout/',LogoutView.as_view(next_page='login'),name="logout" ),
    path('register/',RegisterPage.as_view(),name="register" ),
]