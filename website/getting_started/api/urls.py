from django.urls import path
from user_profile.views import activate
from .views import (
    TopicListAPIView,
    SubTopicRetrieveAPIView,
    UserProgressAPIView,
)

app_name = 'getting_started_api'

urlpatterns = [
    path('contents/', TopicListAPIView.as_view(), name='getting_started'),
    path('progress/', UserProgressAPIView.as_view(), name='user_progress'),
    path('<int:subtopic_id>/', SubTopicRetrieveAPIView.as_view(), name='subtopic_detail'),
]
