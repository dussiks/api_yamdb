from rest_framework import serializers

from .models import CustomUser, Category, Genre, Title, Review, Comment
from . import permissions


MODERATOR_METHODS = ('PATCH', 'DELETE')


class CodeGenerationSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)


class EmailConfirmationSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)
    confirmation_code = serializers.CharField(required=True)


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = (
            'first_name', 'last_name', 'username', 'bio', 'email', 'role',
        )


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        fields = ('name', 'slug')
        lookup_field = 'slug'

        model = Category


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ('name', 'slug')
        model = Genre


class GenreField(serializers.SlugRelatedField):
    def to_representation(self, value):
        return GenreSerializer(value).data


class CategoryField(serializers.SlugRelatedField):
    def to_representation(self, value):
        return CategorySerializer(value).data


class TitleSerializer(serializers.ModelSerializer):
    genre = GenreField(
        many=True,
        slug_field='slug',
        queryset=Genre.objects.all()
    )
    category = CategoryField(
        slug_field='slug',
        queryset=Category.objects.all()
    )
    rating = serializers.IntegerField(read_only=True, required=False)

    class Meta:
        fields = '__all__'
        model = Title


class ReviewSerializer(serializers.ModelSerializer):
    title = serializers.SlugRelatedField(
        many=False, read_only=True, slug_field='description'
    )
    author = serializers.SlugRelatedField(read_only=True,
                                          slug_field='username')

    def create(self, data):
        name = self.context['view'].kwargs.get('title_id')
        author = self.context['request'].user
        message = 'Рецензия уже существует.'
        if Review.objects.filter(title=name, author=author).exists():
            raise serializers.ValidationError(message)
        return Review.objects.create(**data)

    class Meta:
        fields = '__all__'
        model = Review


class CommentSerializer(serializers.ModelSerializer):
    text = serializers.CharField()
    author = serializers.ReadOnlyField(source='author.username')

    class Meta:
        fields = ('id', 'text', 'author', 'pub_date')
        model = Comment
