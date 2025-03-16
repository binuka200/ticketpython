from rest_framework import serializers
from ticket.models import Ticket, TicketPost, Status, Department, TicketType
from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password
from rest_framework.validators import UniqueValidator


class RegisterSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
        required=True,
        validators=[UniqueValidator(queryset=User.objects.all())]
    )
    password = serializers.CharField(
        write_only=True,
        required=True,
        validators=[validate_password]
    )
    password2 = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ('username', 'password', 'password2', 'email')

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError(
                {"password": "Password fields didn't match."})
        return attrs

    def create(self, validated_data):
        user = User.objects.create(
            username=validated_data['username'],
            email=validated_data['email']
        )
        user.set_password(validated_data['password'])
        user.save()
        return user


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email']


class StatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = Status
        fields = ['id', 'status']


class DepartmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Department
        fields = ['id', 'department', 'desciption']


class TicketTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = TicketType
        fields = ['id', 'type', 'desciption']


class TicketPostSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    upload = serializers.FileField(
        required=False,
        allow_null=True,
        max_length=100,
        use_url=True,
        help_text='Upload file (PDF, DOC, DOCX, TXT, PNG, JPG, JPEG)'
    )

    class Meta:
        model = TicketPost
        fields = ['id', 'message', 'user', 'private',
                  'upload', 'created', 'updated']
        read_only_fields = ['user']

    def validate_upload(self, value):
        if value:
            ext = value.name.split('.')[-1].lower()
            allowed_extensions = ['pdf', 'doc',
                                  'docx', 'txt', 'png', 'jpg', 'jpeg']

            if ext not in allowed_extensions:
                raise serializers.ValidationError(
                    f"File type not supported. Allowed types: {', '.join(allowed_extensions)}"
                )

            # Check file size (limit to 5MB)
            if value.size > 5 * 1024 * 1024:  # 5MB in bytes
                raise serializers.ValidationError(
                    "File size too large. Maximum size is 5MB."
                )

        return value


class TicketSerializer(serializers.ModelSerializer):
    created_by = UserSerializer(read_only=True)
    assigned = UserSerializer(read_only=True)
    status = StatusSerializer(read_only=True)
    department = DepartmentSerializer()
    type = TicketTypeSerializer()
    posts = TicketPostSerializer(many=True, read_only=True)
    followers = UserSerializer(many=True, read_only=True)
    priority_display = serializers.CharField(
        source='get_priority_display', read_only=True)

    class Meta:
        model = Ticket
        fields = [
            'id', 'title', 'created_by', 'type', 'department',
            'status', 'priority', 'priority_display', 'assigned',
            'followers', 'sentiment', 'updated', 'created', 'posts'
        ]
        read_only_fields = ['created_by', 'assigned',
                            'status', 'sentiment', 'followers']


class TicketCreateSerializer(serializers.ModelSerializer):
    """Serializer for creating tickets with minimal required fields"""
    class Meta:
        model = Ticket
        fields = ['title', 'type', 'department', 'priority']

    def create(self, validated_data):
        user = self.context['request'].user

        open_status = Status.objects.get(status="Open")

        ticket = Ticket.objects.create(
            created_by=user,
            status=open_status,
            **validated_data
        )
        return ticket
