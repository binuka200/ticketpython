from rest_framework import generics, status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.shortcuts import get_object_or_404
from ticket.models import Ticket, TicketPost, Status, Department, TicketType
from .serializers import (
    TicketSerializer, TicketCreateSerializer, TicketPostSerializer,
    StatusSerializer, DepartmentSerializer, TicketTypeSerializer,
    RegisterSerializer, UserSerializer
)
from ticket.utils import send_ticket_update_notification
from rest_framework_simplejwt.views import TokenObtainPairView
from django.contrib.auth.models import User
from drf_spectacular.utils import extend_schema, OpenApiParameter, OpenApiExample


class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = RegisterSerializer


class UserDetailView(generics.RetrieveAPIView):
    queryset = User.objects.all()
    permission_classes = (IsAuthenticated,)
    serializer_class = UserSerializer

    def get_object(self):
        return self.request.user


class TicketViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = Ticket.objects.all()

    def get_serializer_class(self):
        if self.action == 'create':
            return TicketCreateSerializer
        return TicketSerializer

    def perform_create(self, serializer):
        serializer.save()

    @extend_schema(
        description="Assign the ticket to the current user",
        responses={200: None}
    )
    @action(detail=True, methods=['post'])
    def assign_to_me(self, request, pk=None):
        """Assign the ticket to the current user"""
        ticket = self.get_object()
        ticket.assigned = request.user
        ticket.save()
        return Response({'status': 'Ticket assigned successfully'})

    @extend_schema(
        description="Change the status of a ticket",
        parameters=[
            OpenApiParameter(
                name="status",
                type=int,
                location=OpenApiParameter.QUERY,
                description="ID of the new status"
            )
        ],
        responses={200: None}
    )
    @action(detail=True, methods=['post'])
    def change_status(self, request, pk=None):
        """Change the ticket status"""
        ticket = self.get_object()
        status_id = request.data.get('status')
        if not status_id:
            return Response(
                {'error': 'Status ID is required'},
                status=status.HTTP_400_BAD_REQUEST
            )

        new_status = get_object_or_404(Status, id=status_id)
        ticket.status = new_status
        ticket.save()
        return Response({'status': f'Ticket status changed to {new_status.status}'})

    @extend_schema(
        description="Transfer ticket to another department",
        parameters=[
            OpenApiParameter(
                name="department",
                type=int,
                location=OpenApiParameter.QUERY,
                description="ID of the new department"
            )
        ],
        responses={200: None}
    )
    @action(detail=True, methods=['post'])
    def transfer_department(self, request, pk=None):
        """Transfer ticket to another department"""
        ticket = self.get_object()
        department_id = request.data.get('department')
        if not department_id:
            return Response(
                {'error': 'Department ID is required'},
                status=status.HTTP_400_BAD_REQUEST
            )

        new_department = get_object_or_404(Department, id=department_id)
        ticket.department = new_department
        ticket.save()
        return Response({'status': f'Ticket transferred to {new_department.department}'})

    @extend_schema(
        description="Toggle following status for the current user",
        responses={200: None}
    )
    @action(detail=True, methods=['post'])
    def toggle_follow(self, request, pk=None):
        """Toggle following status for the current user"""
        ticket = self.get_object()
        user = request.user

        if user in ticket.followers.all():
            ticket.followers.remove(user)
            action = 'unfollowed'
        else:
            ticket.followers.add(user)
            action = 'followed'

        return Response({'status': f'Successfully {action} the ticket'})

    @extend_schema(
        description="Add a new post/comment to the ticket",
        responses={201: TicketPostSerializer},
        request={
            'multipart/form-data': TicketPostSerializer
        },
        examples=[
            OpenApiExample(
                'Basic Example',
                value={
                    'message': 'This is a response to the ticket',
                    'private': False,
                    'upload': None
                },
                request_only=True,
            ),
        ]
    )
    @action(detail=True, methods=['post'])
    def add_post(self, request, pk=None):
        """Add a new post/comment to the ticket with optional file attachment"""
        ticket = self.get_object()

        # Handle file upload
        serializer = TicketPostSerializer(
            data=request.data,
            context={'request': request}  # Required for file URL generation
        )

        if serializer.is_valid():
            post = serializer.save(
                ticket=ticket,
                user=request.user
            )

            # Send email notifications
            send_ticket_update_notification(
                ticket, post, exclude_user=request.user)

            return Response(
                TicketPostSerializer(post, context={'request': request}).data,
                status=status.HTTP_201_CREATED
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class StatusViewSet(viewsets.ReadOnlyModelViewSet):

    permission_classes = [IsAuthenticated]
    queryset = Status.objects.all()
    serializer_class = StatusSerializer


class DepartmentViewSet(viewsets.ReadOnlyModelViewSet):

    permission_classes = [IsAuthenticated]
    queryset = Department.objects.all()
    serializer_class = DepartmentSerializer


class TicketTypeViewSet(viewsets.ReadOnlyModelViewSet):

    permission_classes = [IsAuthenticated]
    queryset = TicketType.objects.all()
    serializer_class = TicketTypeSerializer
