from django.db.models import Max, Q
from django.shortcuts import render, redirect
from django.urls import reverse
from django.utils import timezone
from .models import User, Message
# the line below just should not exist.
from django.views.decorators.csrf import csrf_exempt
import hashlib


user_manager = getattr(User, 'objects')


def get_current_user(request):
    user_id = request.session.get("user_id")
    if user_id is None:
        return None
    return user_manager.filter(user_id=user_id).first()


def auth_context(request):
    current_user = get_current_user(request)
    return {
        "current_user": current_user,
        "logged_in": current_user is not None,
    }


def _build_admin_conversation_threads():
    users_by_id = {user.user_id: user for user in User.objects.all()}
    threads = {}

    for message in Message.objects.select_related("user").order_by("-pub_date", "-msg_id"):
        sender = users_by_id.get(message.user_id)
        recipient = users_by_id.get(message.recipient)
        if sender is None or recipient is None:
            continue

        participant_ids = tuple(sorted((sender.user_id, recipient.user_id)))
        thread = threads.get(participant_ids)
        if thread is None:
            thread = {
                "participant_a": users_by_id[participant_ids[0]],
                "participant_b": users_by_id[participant_ids[1]],
                "message_count": 0,
                "latest_message": message,
            }
            threads[participant_ids] = thread

        thread["message_count"] += 1
        if message.pub_date >= thread["latest_message"].pub_date:
            thread["latest_message"] = message

    conversation_threads = sorted(
        threads.values(),
        key=lambda thread: thread["latest_message"].pub_date,
        reverse=True,
    )
    for thread in conversation_threads:
        thread["url"] = reverse(
            "admin_conversation",
            args=[thread["participant_a"].user_id, thread["participant_b"].user_id],
        )

    return conversation_threads


def index(request):
    if get_current_user(request):
        return redirect("conversations")

    return render(request, "messenger/index.html", auth_context(request))


def messages(request, user_id):
    return redirect("conversation", user_id=user_id)

def login(request):
    current_user = get_current_user(request)
    if current_user:
        return redirect("conversations")

    error = None
    if request.method == "POST":
        name = request.POST.get("name", "")
        password = request.POST.get("password", "")
        # hashed_password = hashlib.sha256(password.encode()).hexdigest()
        user = user_manager.filter(name=name, password=password).first()
        # user = user_manager.filter(name=name, password=hashed_password).first()

        if user is not None:
            request.session["user_id"] = user.user_id
            request.session["user_name"] = user.name
            return redirect("conversations")

        error = "Invalid credentials"

    context = auth_context(request)
    context["error"] = error
    return render(request, 'messenger/login.html', context)

# FIX: the line below just should not exist.
@csrf_exempt
def register(request):
    current_user = get_current_user(request)
    if current_user:
        return redirect("conversations")

    if request.method == "POST":
        name = request.POST["name"]
        password = request.POST["password"]


        isadmin = request.POST["isadmin"]=="true"


        # hashed_password = hashlib.sha256(password.encode()).hexdigest()

        next_id = (User.objects.aggregate(Max("user_id"))["user_id__max"] or 0) + 1

        User.objects.create(
            user_id=next_id,
            name=name,
            password=password,
            # password=hashed_password,
            isadmin=isadmin,
        )
        return redirect("login")

    context = auth_context(request)
    context["users"] = User.objects.all()
    return render(request, "messenger/register.html", context)

def conversations(request):
    current_user = get_current_user(request)
    if current_user is None:
        return redirect("login")

    context = auth_context(request)
    context["users"] = User.objects.exclude(user_id=current_user.user_id)
    context["conversations"] = []
    context["active_conversation"] = None
    context["allow_message_form"] = True

    if current_user.isadmin:
        context["conversation_threads"] = _build_admin_conversation_threads()

    return render(request, 'messenger/conversations.html', context)

def logout(request):
    request.session.flush()
    return redirect("index")


def conversation(request, user_id):
    current_user = get_current_user(request)
    if current_user is None:
        return redirect("login")

    # FIX: if current_user.user_id != user_id:
    #          return redirect("conversations")
    recipient = User.objects.filter(user_id=user_id).first()
    if recipient is None:
        return redirect("conversations")

    if request.method == "POST":
        message_text = request.POST.get("message", "").strip()
        if message_text:
            next_msg_id = (Message.objects.aggregate(Max("msg_id"))["msg_id__max"] or 0) + 1
            Message.objects.create(
                user=current_user,
                recipient=recipient.user_id,
                msg_id=next_msg_id,
                message=message_text,
                pub_date=timezone.now(),
            )
            return redirect("conversation", user_id=user_id)

    messages = Message.objects.filter(
        Q(user=current_user, recipient=recipient.user_id) |
        Q(user=recipient, recipient=current_user.user_id)
    ).order_by("-pub_date")[:10]
    messages = list(reversed(messages))

    context = auth_context(request)
    context["recipient"] = recipient
    context["messages"] = messages
    context["conversation_title"] = f"Yapping with {recipient.name}"
    context["back_url"] = reverse("conversations")
    context["back_label"] = "Back to conversations"
    context["allow_message_form"] = True
    return render(request, 'messenger/conversation.html', context)


def admin_conversation(request, user_a_id, user_b_id):
    current_user = get_current_user(request)
    if current_user is None:
        return redirect("login")

    if not current_user.isadmin:
        return redirect("conversations")

    user_a = User.objects.filter(user_id=user_a_id).first()
    user_b = User.objects.filter(user_id=user_b_id).first()
    if user_a is None or user_b is None:
        return redirect("conversations")

    messages = Message.objects.filter(
        Q(user=user_a, recipient=user_b.user_id) |
        Q(user=user_b, recipient=user_a.user_id)
    ).select_related("user").order_by("pub_date", "msg_id")

    context = auth_context(request)
    context["participants"] = [user_a, user_b]
    context["conversation_title"] = f"Conversation: {user_a.name} and {user_b.name}"
    context["messages"] = messages
    context["back_url"] = reverse("conversations")
    context["back_label"] = "Back to admin conversations"
    context["allow_message_form"] = False
    return render(request, 'messenger/conversation.html', context)


def obscure_very_secret_admin_page(request):
    return render(request, 'messenger/obscure_very_secret_admin_page.html', auth_context(request))
