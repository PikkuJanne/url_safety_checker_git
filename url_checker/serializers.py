from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from .models import URL

class URLSerializer(serializers.ModelSerializer):
    url = serializers.URLField(
        validators=[UniqueValidator(queryset=URL.objects.all())]
    )

    class Meta:
        model = URL
        fields = ['url', 'user', 'is_malicious', 'checked_date']

    def validate_url(self, value):
        return value


