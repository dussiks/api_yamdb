from rest_framework import serializers


class GenreField(serializers.SlugRelatedField):
    def to_representation(self, value):
        fields = {
            'name': value.name,
            'slug': value.slug
        }
        return fields


class CategoryField(serializers.SlugRelatedField):
    def to_representation(self, value):
        fields = {
            'name': value.name,
            'slug': value.slug
        }
        return fields
