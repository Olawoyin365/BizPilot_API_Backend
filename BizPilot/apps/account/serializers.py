"""
Account Serializers

Handles serialization for:
- Business registration
- User authentication
- User profile
"""
from rest_framework import serializers
from django.contrib.auth.password_validation import validate_password
from django.db import transaction
from .models import Business, CustomUser
from apps.industry.serializers import IndustrySerializer


class BusinessRegistrationSerializer(serializers.ModelSerializer):
    """
    Serializer for business registration.
    
    Handles the complete business onboarding process:
    1. Validates business information
    2. Validates user credentials
    3. Creates business and owner user in a single transaction
    4. Returns JWT tokens for immediate login
    
    Input fields:
        - store_name: Business name
        - email: Business/owner email (also used for login)
        - phone: Business phone
        - country: Business country
        - industry: Industry ID
        - username: Owner username
        - password: Owner password
        - password2: Password confirmation
    """
    
    # User fields (not part of Business model)
    username = serializers.CharField(
        write_only=True,
        required=True,
        help_text="Username for the business owner account"
    )
    password = serializers.CharField(
        write_only=True,
        required=True,
        validators=[validate_password],
        style={'input_type': 'password'},
        help_text="Password (min 8 characters)"
    )
    password2 = serializers.CharField(
        write_only=True,
        required=True,
        style={'input_type': 'password'},
        help_text="Confirm password"
    )
    
    # Read-only fields for response
    industry_details = IndustrySerializer(source='industry', read_only=True)
    
    class Meta:
        model = Business
        fields = [
            'id', 'store_name', 'email', 'phone', 'country', 
            'industry', 'industry_details', 'username', 'password', 
            'password2', 'created_at'
        ]
        read_only_fields = ['id', 'created_at']
        extra_kwargs = {
            'industry': {'write_only': True}  # Don't return ID, return details instead
        }
    
    def validate(self, attrs):
        """
        Validate the registration data.
        
        Checks:
        - Passwords match
        - Email is not already registered
        - Username is not already taken
        """
        # Check passwords match
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({
                "password": "Password fields didn't match."
            })
        
        # Check if email is already registered
        if CustomUser.objects.filter(email=attrs['email'].lower()).exists():
            raise serializers.ValidationError({
                "email": "A user with this email already exists."
            })
        
        # Check if username is taken
        if CustomUser.objects.filter(username=attrs['username']).exists():
            raise serializers.ValidationError({
                "username": "This username is already taken."
            })
        
        return attrs
    
    @transaction.atomic
    def create(self, validated_data):
        """
        Create business and owner user in a single atomic transaction.
        
        This ensures that if either creation fails, neither is created
        (maintains data integrity).
        
        Steps:
        1. Extract user-specific fields
        2. Create the Business
        3. Create the owner CustomUser
        4. Link user to business
        5. Update business with owner reference
        
        Returns:
            Business: The created business instance (with owner attached)
        """
        # Extract user fields from validated data
        username = validated_data.pop('username')
        password = validated_data.pop('password')
        validated_data.pop('password2')  # Remove password2, we don't need it
        
        # Create the business (without owner initially)
        business = Business.objects.create(**validated_data)
        
        # Create the owner user
        owner = CustomUser.objects.create_user(
            username=username,
            email=validated_data['email'],
            password=password,
            phone=validated_data['phone'],
            business=business,
            is_business_owner=True,
            is_staff_member=False
        )
        
        # Link the owner back to the business
        business.owner = owner
        business.save()
        
        return business


class UserSerializer(serializers.ModelSerializer):
    """
    Serializer for user profile information.
    
    Used for:
    - Displaying user details
    - Updating user profile
    """
    
    business_name = serializers.CharField(source='business.store_name', read_only=True)
    industry_name = serializers.CharField(source='business.industry.name', read_only=True)
    
    class Meta:
        model = CustomUser
        fields = [
            'id', 'username', 'email', 'phone', 'first_name', 
            'last_name', 'is_business_owner', 'is_staff_member',
            'business_name', 'industry_name', 'date_joined'
        ]
        read_only_fields = [
            'id', 'email', 'is_business_owner', 'is_staff_member', 
            'business_name', 'industry_name', 'date_joined'
        ]


class LoginSerializer(serializers.Serializer):
    """
    Serializer for user login.
    
    Accepts email and password, returns JWT tokens on successful authentication.
    """
    
    email = serializers.EmailField(required=True)
    password = serializers.CharField(
        required=True,
        style={'input_type': 'password'},
        write_only=True
    )
    
    def validate(self, attrs):
        """
        Validate email format (additional validation happens in view).
        """
        attrs['email'] = attrs['email'].lower()
        return attrs
