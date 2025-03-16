import django_filters
from django.contrib.auth.models import User
from django import forms
from .models import Ticket, Status, Department, TicketType


def get_select_widget():
    return forms.Select(attrs={'class': 'form-select'})


class TicketFilter(django_filters.FilterSet):
    title = django_filters.CharFilter(
        lookup_expr='icontains',
        label='Title',
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Search by title...'
        })
    )

    status = django_filters.ModelChoiceFilter(
        queryset=Status.objects.all(),
        empty_label="All Statuses",
        label='Status'
    )

    priority = django_filters.ChoiceFilter(
        choices=Ticket.TicketPriority.choices,
        empty_label="All Priorities",
        label='Priority'
    )

    department = django_filters.ModelChoiceFilter(
        queryset=Department.objects.all(),
        empty_label="All Departments",
        label='Department'
    )

    type = django_filters.ModelChoiceFilter(
        queryset=TicketType.objects.all(),
        empty_label="All Types",
        label='Type'
    )

    created_by = django_filters.ModelChoiceFilter(
        queryset=User.objects.all(),
        empty_label="All Creators",
        label='Created By'
    )

    assigned = django_filters.ModelChoiceFilter(
        queryset=User.objects.all(),
        empty_label="All Assignees",
        label='Assigned To'
    )

    sentiment = django_filters.ChoiceFilter(
        choices=[
            ('Positive', 'Positive'),
            ('Negative', 'Negative'),
            ('Neutral', 'Neutral'),
        ],
        empty_label="All Sentiments",
        label='Sentiment'
    )

    order_by = django_filters.OrderingFilter(
        fields=(
            ("id", "ID"),
            ("title", "Title"),
            ("priority", "Priority"),
            ("department__department", "Department"),
            ("status__status", "Status"),
            ("assigned__username", "Assigned User"),
            ("updated", "Last Updated"),
        ),
        field_labels={
            "id": "ID",
            "title": "Title",
            "priority": "Priority",
            "department__department": "Department",
            "status__status": "Status",
            "assigned__username": "Assigned User",
            "updated": "Last Updated",
        },
        label="Sort by"
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.form.fields.values():
            if isinstance(field.widget, forms.Select):
                field.widget.attrs.update({'class': 'form-select'})

    class Meta:
        model = Ticket
        fields = ["title", "status", "priority", "department",
                  "type", "created_by", "assigned", "sentiment"]
