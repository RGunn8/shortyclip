from django.contrib.auth.hashers import make_password
from rest_framework.validators import UniqueValidator
from rest_framework import serializers
import json
import six

from shortyclipsAPI.models import ClipUser, Clip, Like, Category, SearchItem


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('id', 'name')


class ClipSerializer(serializers.ModelSerializer):
    user = serializers.SlugRelatedField(many=False, read_only=True, slug_field="username")
    # categoryName = serializers.SlugRelatedField(many=False, slug_field='name',required=False,queryset=Category.objects.all())
    category = serializers.PrimaryKeyRelatedField(queryset=Category.objects.all(), required=False)
    likes = serializers.SerializerMethodField()
    currentUserLikes = serializers.SerializerMethodField('get_currentUserLike')

    class Meta:
        model = Clip
        fields = (
            'id', 'title', 'duration', 'likes', 'clipURL', 'tags', 'user', 'created', 'currentUserLikes', 'category',
        )

    def get_likes(self, obj):
        return obj.like_set.count()

    def get_currentUserLike(self, obj):
        request = getattr(self.context, 'request', None)
        if request and hasattr(request, "user"):
            user = request.user
            count = Like.objects.filter(user=user, clip=obj).count()
            if count > 0:
                return True
        return False


class SearchItemSerializer(serializers.ModelSerializer):
    searchItem = serializers.CharField(max_length=150, allow_blank=False,allow_null=False)
    # created = serializers.DateTimeField(input_formats="%d-%m-%Y")

    class Meta:
        model = SearchItem
        fields = (
            'searchItem','createdAt'
        )


class UserSerializer(serializers.ModelSerializer):
    username = serializers.CharField(validators=[UniqueValidator(queryset=ClipUser.objects.all())])
    password = serializers.CharField(min_length=4, write_only=True)
    clips = ClipSerializer(source='clip_set', read_only=True, many=True,allow_null=True)

    def create(self, validated_data):
        user = ClipUser.objects.create(
            username=validated_data['username']
        )
        user.set_password(validated_data['password'])
        user.save()

        return user

    def update(self, instance, validated_data):
        if 'user' in validated_data:
            instance.user.password = make_password(
                validated_data.get('user').get('password', instance.user.password)
            )
            instance.user.save()

    class Meta:
        model = ClipUser
        fields = (
            'id', 'username', 'password', 'clips'
        )
