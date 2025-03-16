from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from django import forms
from .models import Ticket, TicketPost
from django.contrib.auth.models import User

# from .models import User


class MyUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

    def __init__(self, *args, **kwargs):
        super(MyUserCreationForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs.update(
                {'class': 'form-control', 'placeholder': field.label})


class TicketForm(forms.ModelForm):
    class Meta:
        model = Ticket
        fields = ["title", "type", "department", "priority"]
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter ticket title',
                'autocomplete': 'off'
            }),
            'type': forms.Select(attrs={
                'class': 'form-select',
            }),
            'department': forms.Select(attrs={
                'class': 'form-select',
            }),
            'priority': forms.Select(attrs={
                'class': 'form-select',
            })
        }
        labels = {
            'title': 'Ticket Title',
            'type': 'Ticket Type',
            'department': 'Department',
            'priority': 'Priority Level'
        }
        help_texts = {
            'title': 'Provide a clear and concise title for the ticket',
            'priority': 'Select the urgency level of this ticket'
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name in ['type', 'department', 'priority']:
            self.fields[field_name].empty_label = f"Select {self.fields[field_name].label}"


class TicketPostForm(forms.ModelForm):
    class Meta:
        model = TicketPost
        fields = ["message", "upload"]
        widgets = {
            'message': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Describe your issue or request in detail...',
                'rows': 5,
                'style': 'resize: vertical;'
            }),
            'upload': forms.ClearableFileInput(attrs={
                'class': 'form-control',
                'accept': '.pdf,.doc,.docx,.txt,.png,.jpg,.jpeg'
            })
        }
        labels = {
            'message': 'Description',
            'upload': 'Attachments'
        }
        help_texts = {
            'message': 'Please provide all relevant details to help us understand your request',
            'upload': 'Accepted files: PDF, DOC, DOCX, TXT, PNG, JPG, JPEG'
        }


class TicketPostingForm(forms.ModelForm):
    class Meta:
        model = TicketPost
        fields = ["message", "upload", "private"]
        widgets = {
            "message": forms.Textarea(attrs={
                "class": "form-control",
                "rows": 3,
                "placeholder": "Type your response here..."
            }),
            "upload": forms.ClearableFileInput(attrs={
                "class": "form-control",
                'accept': '.pdf,.doc,.docx,.txt,.png,.jpg,.jpeg'
            }),
            "private": forms.CheckboxInput(attrs={
                "class": "form-check-input"
            }),
        }
        help_texts = {
            'upload': 'Accepted files: PDF, DOC, DOCX, TXT, PNG, JPG, JPEG',
            'private': 'Check this box to make this response visible only to staff members'
        }
