"""
Account Views

API endpoints for:
- Business registration
- User login
- User profile management
"""
from rest_framework import status, generics, viewsets
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from .models import Business, CustomUser
from .serializers import (
    BusinessRegistrationSerializer,
    UserSerializer,
    LoginSerializer
)


class BusinessRegistrationView(generics.CreateAPIView):
    """
    API endpoint for business registration.
    
    POST /api/account/register/
    
    Accepts business details and creates:
    - A new Business
    - A new owner CustomUser
    - Returns JWT tokens for immediate login
    
    Permission: AllowAny (public endpoint)
    """
    
    queryset = Business.objects.all()
    serializer_class = BusinessRegistrationSerializer
    permission_classes = [AllowAny]
    
    def create(self, request, *args, **kwargs):
        """
        Handle business registration and return JWT tokens.
        """
        # Validate and save the business and owner
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        business = serializer.save()
        
        # Generate JWT tokens for the newly created owner
        owner = business.owner
        refresh = RefreshToken.for_user(owner)
        
        # Prepare response data
        response_data = {
            'message': 'Business registered successfully',
            'business': serializer.data,
            'tokens': {
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            },
            'user': UserSerializer(owner).data
        }
        
        return Response(response_data, status=status.HTTP_201_CREATED)


@api_view(['POST'])
@permission_classes([AllowAny])
def login_view(request):
    """
    API endpoint for user login.
    
    POST /api/account/login/
    
    Accepts:
        email: User's email address
        password: User's password
    
    Returns:
        - JWT access and refresh tokens
        - User profile information
    
    Permission: AllowAny (public endpoint)
    """
    serializer = LoginSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    
    email = serializer.validated_data['email']
    password = serializer.validated_data['password']
    
    # Authenticate user
    # Django's authenticate expects 'username', but our USERNAME_FIELD is 'email'
    user = authenticate(request, username=email, password=password)
    
    if user is None:
        return Response(
            {'detail': 'Invalid email or password.'},
            status=status.HTTP_401_UNAUTHORIZED
        )
    
    # Check if user's business is active
    if user.business and not user.business.is_active:
        return Response(
            {'detail': 'Your business account is inactive. Please contact support.'},
            status=status.HTTP_403_FORBIDDEN
        )
    
    # Generate JWT tokens
    refresh = RefreshToken.for_user(user)
    
    return Response({
        'message': 'Login successful',
        'tokens': {
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        },
        'user': UserSerializer(user).data
    }, status=status.HTTP_200_OK)


class UserProfileView(generics.RetrieveUpdateAPIView):
    """
    API endpoint for viewing and updating user profile.
    
    GET /api/account/profile/ - View current user's profile
    PUT/PATCH /api/account/profile/ - Update current user's profile
    
    Permission: IsAuthenticated
    """
    
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]
    
    def get_object(self):
        """
        Return the current authenticated user.
        """
        return self.request.user


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def business_details_view(request):
    """
    API endpoint to get details of the authenticated user's business.
    
    GET /api/account/business/
    
    Returns complete business information including industry details.
    
    Permission: IsAuthenticated
    """
    user = request.user
    
    if not user.business:
        return Response(
            {'detail': 'User is not associated with any business.'},
            status=status.HTTP_404_NOT_FOUND
        )
    
    business = user.business
    business_data = {
        'id': business.id,
        'store_name': business.store_name,
        'email': business.email,
        'phone': business.phone,
        'country': str(business.country.name),
        'country_code': business.country.code,
        'industry': {
            'id': business.industry.id,
            'name': business.industry.name,
            'description': business.industry.description
        },
        'is_active': business.is_active,
        'created_at': business.created_at,
        'owner': {
            'id': business.owner.id,
            'username': business.owner.username,
            'email': business.owner.email
        }
    }
    
    return Response(business_data, status=status.HTTP_200_OK)
