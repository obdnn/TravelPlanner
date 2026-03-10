import requests
from rest_framework import serializers
from .models import Project, Place

class PlaceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Place
        fields = ['id', 'external_id', 'notes', 'is_visited']

    def validate_external_id(self, value):
        api_url = f"https://api.artic.edu/api/v1/artworks/{value}"
        try:
            response = requests.get(api_url, timeout=5)
            if response.status_code != 200:
                raise serializers.ValidationError(f"Place with ID {value} not found in Art Institute API.")
        except requests.RequestException:
            raise serializers.ValidationError("Art Institute API is currently unavailable.")
        return value


class ProjectSerializer(serializers.ModelSerializer):
    places = PlaceSerializer(many=True, required=False)
    is_completed = serializers.BooleanField(read_only=True)

    class Meta:
        model = Project
        fields = ['id', 'name', 'description', 'start_date', 'places', 'is_completed']


    def validate_places(self, value):
        if len(value) > 10:
            raise serializers.ValidationError("A project cannot have more than 10 places.")
        if self.instance is None and len(value) < 1:
            raise serializers.ValidationError("A project must have at least 1 place.")
        return value

    def create(self, validated_data):
        places_data = validated_data.pop('places', [])
        project = Project.objects.create(**validated_data)

        for place_data in places_data:
            Place.objects.create(project=project, **place_data)

        return project