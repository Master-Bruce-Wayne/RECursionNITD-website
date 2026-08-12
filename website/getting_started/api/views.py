from rest_framework.generics import ListAPIView, RetrieveUpdateAPIView
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from getting_started.models import Topic, SubTopic, Level, UserProgress
from .serializers import LevelSerializer , SubTopicContentSerializer



class TopicListAPIView(ListAPIView):
    queryset = Level.objects.all()
    permission_classes = (IsAuthenticatedOrReadOnly,)
    serializer_class = LevelSerializer

    def get_queryset(self):
        level = self.request.query_params.get('level', None)
        return super().get_queryset()


class SubTopicRetrieveAPIView(RetrieveUpdateAPIView):
    queryset = SubTopic.objects.all()
    serializer_class = SubTopicContentSerializer
    permission_classes = (IsAuthenticatedOrReadOnly,)
    lookup_field = 'id'
    lookup_url_kwarg = 'subtopic_id'

    def get_queryset(self):
        return super().get_queryset()

class UserProgressAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        progress = UserProgress.objects.filter(user=request.user)
        completed_ids = progress.values_list('subtopic_id', flat=True)
        return Response({'completed_subtopics': list(completed_ids)}, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        subtopic_id = request.data.get('subtopic_id')
        if not subtopic_id:
            return Response({'error': 'subtopic_id is required'}, status=status.HTTP_400_BAD_REQUEST)
            
        progress, created = UserProgress.objects.get_or_create(user=request.user, subtopic_id=subtopic_id)
        if not created:
            progress.delete()
            return Response({'status': 'unmarked'}, status=status.HTTP_200_OK)
            
        return Response({'status': 'marked'}, status=status.HTTP_201_CREATED)