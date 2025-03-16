from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from .forms import UserCreationForm
from django.contrib.auth import authenticate, login, logout
from .models import Ticket, TicketType, Department, Status, TicketPost
from django.contrib import messages
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .filters import TicketFilter
from .forms import TicketForm, TicketPostForm, TicketPostingForm, MyUserCreationForm
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from .utils import send_ticket_update_notification


@login_required
def index(request):
    sort_by = request.GET.get("sort", "updated")
    order = request.GET.get("order", "desc")
    if order == "desc":
        sort_by = f"-{sort_by}"

    tickets = Ticket.objects.all().order_by(sort_by)

    ticket_filter = TicketFilter(request.GET, queryset=tickets)
    filtered_tickets = ticket_filter.qs

    paginator = Paginator(filtered_tickets, 10)
    page_number = request.GET.get("page", 1)
    try:
        page_obj = paginator.page(page_number)
    except PageNotAnInteger:
        page_obj = paginator.page(1)
    except EmptyPage:
        page_obj = paginator.page(paginator.num_pages)

    departments = Department.objects.all()
    users = User.objects.filter(is_active=True)

    context = {
        "page_obj": page_obj,
        "ticket_filter": ticket_filter,
        "sort_by": request.GET.get("sort", "updated"),
        "order": request.GET.get("order", "desc"),
        "departments": departments,
        "users": users,
    }

    return render(request, "ticket/index.html", context)


@login_required
def create_ticket(request):
    if request.method == "POST":
        ticket_form = TicketForm(request.POST)
        post_form = TicketPostForm(request.POST, request.FILES)

        if ticket_form.is_valid() and post_form.is_valid():

            ticket = ticket_form.save(commit=False)
            ticket.created_by = request.user

            open_status = Status.objects.get(status="Open")
            ticket.status = open_status

            ticket.save()

            post = post_form.save(commit=False)
            post.ticket = ticket
            post.user = request.user
            post.save()

            return redirect("index")

    else:
        ticket_form = TicketForm()
        post_form = TicketPostForm()

    return render(
        request,
        "ticket/create_ticket.html",
        {"ticket_form": ticket_form, "post_form": post_form},
    )


@login_required
def view_ticket(request, pk):
    ticket = get_object_or_404(Ticket, id=pk)
    posts = ticket.posts.all().order_by("created")
    departments = Department.objects.all()
    statuses = Status.objects.all()
    is_following = request.user in ticket.followers.all()

    if request.method == "POST":
        form = TicketPostingForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.ticket = ticket
            post.user = request.user
            post.save()

            # Send email notifications
            # send_ticket_update_notification(
            #     ticket, post, exclude_user=request.user)

            return redirect("view_ticket", pk=ticket.id)
    else:
        form = TicketPostingForm()

    context = {
        "ticket": ticket,
        "posts": posts,
        "form": form,
        "departments": departments,
        "statuses": statuses,
        "is_following": is_following
    }
    return render(request, "ticket/view_ticket.html", context)


def loginuser(request):
    # if request.user.is_authenticated:
    #     return redirect('index')

    if request.method == 'POST':
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('index')
        else:
            messages.error(request, 'Username OR password does not exit')
    return render(request, 'ticket/login.html')


@login_required
def logoutuser(request):
    logout(request)
    return redirect('login')


def register(request):
    # if request.user.is_authenticated:
    #     return redirect('index')

    if request.method == 'POST':
        form = MyUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(
                request, "Registration successful! You are now logged in.")
            return redirect('index')
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = MyUserCreationForm()

    return render(request, 'ticket/register.html', {'form': form})


@login_required
def assign_ticket(request, pk):
    ticket = get_object_or_404(Ticket, id=pk)
    ticket.assigned = request.user
    ticket.save()
    return redirect("view_ticket", pk=ticket.id)


@login_required
def transfer_ticket(request, pk):
    ticket = get_object_or_404(Ticket, id=pk)

    if request.method == "POST":
        department_id = request.POST.get("department")
        new_department = get_object_or_404(Department, id=department_id)
        ticket.department = new_department
        ticket.save()
        messages.success(
            request, f"Ticket transferred to {new_department.department} successfully.")
        return redirect("view_ticket", pk=ticket.id)

    return redirect("view_ticket", pk=ticket.id)


@login_required
def change_status(request, pk):
    ticket = get_object_or_404(Ticket, id=pk)

    if request.method == "POST":
        status_id = request.POST.get("status")
        new_status = get_object_or_404(Status, id=status_id)
        ticket.status = new_status
        ticket.save()
        messages.success(
            request, f"Ticket status changed to {new_status.status} successfully.")
        return redirect("view_ticket", pk=ticket.id)

    return redirect("view_ticket", pk=ticket.id)


@login_required
def quick_transfer_ticket(request, pk):
    ticket = get_object_or_404(Ticket, pk=pk)
    if request.method == 'POST':
        department_id = request.POST.get('department')
        if department_id:
            department = get_object_or_404(Department, pk=department_id)
            ticket.department = department
            ticket.save()
            messages.success(
                request, f'Ticket #{ticket.id} transferred to {department.department}')
    return redirect('index')


@login_required
def quick_assign_ticket(request, pk, user_id=None):
    ticket = get_object_or_404(Ticket, pk=pk)
    if request.method == 'POST':
        if user_id:
            user = get_object_or_404(User, pk=user_id)
        else:
            user = request.user
        ticket.assigned = user
        ticket.save()
        messages.success(
            request, f'Ticket #{ticket.id} assigned to {user.username}')
    return redirect('index')


@login_required
def deleteTicket(request, pk):
    ticket = get_object_or_404(Ticket, id=pk)
    if request.method == "POST":
        ticket.delete()
        messages.success(request, "Ticket deleted successfully")
        return redirect("index")
    return render(request, "ticket/delete_ticket.html", {"ticket": ticket})


@login_required
def updateTicket(request, pk):
    ticket = get_object_or_404(Ticket, id=pk)
    if request.method == "POST":
        form = TicketForm(request.POST, instance=ticket)
        if form.is_valid():
            form.save()
            messages.success(request, "Ticket updated successfully")
            return redirect("view_ticket", id=ticket.id)
    else:
        form = TicketForm(instance=ticket)
    return render(request, "ticket/update_ticket.html", {"form": form, "ticket": ticket})


@login_required
def deletePost(request, pk):
    post = get_object_or_404(TicketPost, id=pk)
    ticket_id = post.ticket.id
    if request.method == "POST":
        post.delete()
        messages.success(request, "Post deleted successfully")
        return redirect("view_ticket", id=ticket_id)
    return render(request, "ticket/delete_post.html", {"post": post})


@login_required
def updatePost(request, pk):
    post = get_object_or_404(TicketPost, id=pk)
    if request.method == "POST":
        form = TicketPostingForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            form.save()
            messages.success(request, "Post updated successfully")
            return redirect("view_ticket", id=post.ticket.id)
    else:
        form = TicketPostingForm(instance=post)
    return render(request, "ticket/update_post.html", {"form": form, "post": post})


@login_required
def follow_ticket(request, pk):
    ticket = get_object_or_404(Ticket, id=pk)
    if request.user in ticket.followers.all():
        ticket.followers.remove(request.user)
        messages.success(request, "You have unfollowed this ticket.")
    else:
        ticket.followers.add(request.user)
        messages.success(request, "You are now following this ticket.")
    return redirect("view_ticket", pk=ticket.id)


@login_required
def my_tickets(request):

    filter_type = request.GET.get('filter', 'created')

    sort_by = request.GET.get("sort", "updated")
    order = request.GET.get("order", "desc")
    if order == "desc":
        sort_by = f"-{sort_by}"

    if filter_type == 'created':
        tickets = Ticket.objects.filter(created_by=request.user)
    elif filter_type == 'assigned':
        tickets = Ticket.objects.filter(assigned=request.user)
    elif filter_type == 'followed':
        tickets = request.user.followed_tickets.all()
    else:
        tickets = Ticket.objects.filter(created_by=request.user)

    tickets = tickets.order_by(sort_by)

    paginator = Paginator(tickets, 10)
    page_number = request.GET.get("page", 1)
    try:
        page_obj = paginator.page(page_number)
    except PageNotAnInteger:
        page_obj = paginator.page(1)
    except EmptyPage:
        page_obj = paginator.page(paginator.num_pages)

    context = {
        "page_obj": page_obj,
        "sort_by": request.GET.get("sort", "updated"),
        "order": request.GET.get("order", "desc"),
        "filter_type": filter_type,
        "created_count": Ticket.objects.filter(created_by=request.user).count(),
        "assigned_count": Ticket.objects.filter(assigned=request.user).count(),
        "followed_count": request.user.followed_tickets.count(),
    }

    return render(request, "ticket/my_tickets.html", context)
