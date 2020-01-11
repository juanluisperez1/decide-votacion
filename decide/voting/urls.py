from django.urls import path, re_path
from . import views

#Imported re_path class in order to allow django old url syntax
urlpatterns = [
    path('', views.VotingView.as_view(), name='voting'),
    path('<int:voting_id>/', views.VotingUpdate.as_view(), name='voting'),
    path('user/', views.VotingsPerUser.as_view(), name='votingsPerUser'),
    re_path(r'^politicalparty/$', views.PoliticalPartyList.as_view(), name='get_post_politicalparty'),
    re_path(r'^politicalparty/(?P<pk>\d+)/$',views.PoliticalPartyDetail.as_view(), name='get_delete_update_politicalparty'),

]
