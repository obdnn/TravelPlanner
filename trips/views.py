from rest_framework import viewsets, status
from rest_framework.response import Response
from .models import Project, Place
from .serializers import ProjectSerializer, PlaceSerializer

class ProjectViewSet(viewsets.ModelViewSet):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance.places.filter(is_visited=True).exists():
            return Response(
                {"error": "Cannot delete project with visited places."},
                status=status.HTTP_400_BAD_REQUEST
            )
        return super().destroy(request, *args, **kwargs)

class PlaceViewSet(viewsets.ModelViewSet):
    queryset = Place.objects.all()
    serializer_class = PlaceSerializer

    def get_queryset(self):

        queryset = Place.objects.all()
        project_id = self.request.query_params.get('project')
        if project_id:
            queryset = queryset.filter(project_id=project_id)
        return queryset