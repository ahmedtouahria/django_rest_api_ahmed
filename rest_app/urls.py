from django.urls import path
from . import views
urlpatterns = [
 
    path("rest/fbv",views.mixins_list.as_view()),
    path("rest/fbv/<int:pk>",views.mixins_pk.as_view()),
    #path("rest/fbv/<int:pk>",views.FBV_pk),
    

]
