from django.db import IntegrityError
from rest_framework import generics, viewsets, status, filters
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
from rest_framework.response import Response
from rest_framework.decorators import action

from library.utils import recommend_books
from .models import Author, Book, Favorite
from .serializers import AuthorSerializer, BookSerializer, FavoriteSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import AllowAny
from django.contrib.auth.models import User
from rest_framework.decorators import api_view, permission_classes
from django.contrib.auth import authenticate


class AuthorViewSet(viewsets.ModelViewSet):
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]


class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    filterset_fields = ['title', 'author__name']
    search_fields = ['title', 'authors__name']  # Specify fields for searching
    filter_backends = [filters.SearchFilter]


class FavoriteViewSet(viewsets.ModelViewSet):
    queryset = Favorite.objects.all()
    serializer_class = FavoriteSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Favorite.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        # Automatically assign the current user
        serializer.save(user=self.request.user)

    def create(self, request, *args, **kwargs):
        # Check if the user already has a favorite
        if Favorite.objects.filter(user=request.user).count() >= 20:
            return Response({'detail': 'You can only have up to 20 favorite.'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            # Perform the create operation
            response = super().create(request, *args, **kwargs)

            # Generate recommendations based on the new favorite
            recommendations = recommend_books(request.user)

            # Serialize the recommendations
            book_serializer = BookSerializer(recommendations, many=True)

            # Add recommendations to the response data
            response.data['recommendations'] = book_serializer.data

            return response

        except IntegrityError:
            return Response({'detail': 'This book is already your favorite.'}, status=status.HTTP_400_BAD_REQUEST)


class RegisterView(generics.CreateAPIView):
    permission_classes = [AllowAny]

    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        if User.objects.filter(username=username).exists():
            return Response({'error': 'Username already exists'}, status=status.HTTP_400_BAD_REQUEST)

        User.objects.create_user(username=username, password=password)
        return Response({'success': 'User registered successfully'}, status=status.HTTP_201_CREATED)


@api_view(['POST'])
@permission_classes([AllowAny])
def login_view(request):
    username = request.data.get('username')
    password = request.data.get('password')

    user = authenticate(username=username, password=password)

    if user is not None:
        refresh = RefreshToken.for_user(user)
        return Response({
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        })
    else:
        return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)
