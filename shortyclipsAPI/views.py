from django.contrib.auth import authenticate
from django.shortcuts import render

# Create your views here.
from django.views.decorators.csrf import csrf_exempt
from rest_framework import generics, status
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view, permission_classes
from rest_framework.generics import CreateAPIView
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly, BasePermission
from rest_framework.response import Response
from rest_framework.status import HTTP_400_BAD_REQUEST, HTTP_404_NOT_FOUND, HTTP_200_OK
from rest_framework.views import APIView
from rest_framework import filters



from shortyclipsAPI.models import Clip, Like, ClipUser
from shortyclipsAPI.serializers import ClipSerializer, UserSerializer


class ClipList(generics.ListAPIView):
    filter_class = Clip
    filter_backends = [filters.SearchFilter]
    search_fields = ['title','user__username','tags']
    queryset = Clip.objects.all().order_by('-created')
    serializer_class = ClipSerializer


@permission_classes((IsAuthenticatedOrReadOnly,))
class ClipDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Clip.objects.all()
    serializer_class = ClipSerializer


@permission_classes([IsAuthenticated])
class ClipCreate(CreateAPIView):
    queryset = Clip.objects.all()
    serializer_class = ClipSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


@permission_classes(IsAuthenticated)
@csrf_exempt
@api_view(['POST', 'DELETE'])
def postLike(request, pk):
    user = request.user
    try:
        clip = Clip.objects.get(pk=pk)
    except Clip.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    if not user:
        return Response({'error': 'Invalid Credentials'},
                        status=HTTP_404_NOT_FOUND)
    if request.method == 'POST':
        Like.objects.create(user=user, clip=clip)
        return Response(status.HTTP_201_CREATED)
    if request.method == 'DELETE':
        try:
            Like.objects.get(user=user, clip=clip).delete()
            return Response(status.HTTP_200_OK)
        except Like.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)


@permission_classes({IsAuthenticated})
class UserInfo(generics.RetrieveUpdateDestroyAPIView):
    queryset = ClipUser.objects.all()
    serializer_class = UserSerializer


@csrf_exempt
@permission_classes((IsAuthenticatedOrReadOnly))
@api_view(["GET"])
def getUserFavorite(request):
    user = request.user
    if not user:
        return Response({'error': 'Invalid Credentials'},
                        status=HTTP_404_NOT_FOUND)
    likes = Like.objects.filter(user=user)
    clips = []
    for like in likes:
        clips.append(like.clip)
    serializer = ClipSerializer(clips, many=True)
    return Response({'clips': serializer.data})
    # return Response({'error': 'Error returning clips'},
    #                 status=HTTP_404_NOT_FOUND)


@csrf_exempt
@api_view(["POST"])
def login(request):
    username = request.data.get("username")
    password = request.data.get("password")

    if username is None or password is None:
        return Response({'error': 'Please provide both username and password'},
                        status=HTTP_400_BAD_REQUEST)
    user = authenticate(username=username, password=password)
    if not user:
        return Response({'error': 'Invalid Credentials'},
                        status=HTTP_404_NOT_FOUND)
    token, _ = Token.objects.get_or_create(user=user)
    return Response({'token': token.key},
                    status=HTTP_200_OK)


class UserCreate(APIView):

    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            if user:
                if user:
                    token = Token.objects.get(user=user)
                    json = serializer.data
                    json['token'] = token.key
                    json['password'] = 'valid'
                    return Response(json, status=status.HTTP_201_CREATED)

            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


SAFE_METHODS = ['GET', 'HEAD', 'OPTIONS']


class IsAuthenticatedOrReadOnly(BasePermission):
    """
    The request is authenticated as a user, or is a read-only request.
    """

    def has_permission(self, request, view):
        if (request.method in SAFE_METHODS or
                request.user and
                request.user.is_authenticated()):
            return True
        return False
