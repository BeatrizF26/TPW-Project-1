from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Chat, Message
from books.models import Book
from django.db.models import Q, Count
from django.urls import reverse

@login_required
def start_conversation(request, book_id):
    book = get_object_or_404(Book, id=book_id)

    if book.seller == request.user:
        return redirect('book_list')

    chat, created = Chat.objects.get_or_create(
        seller=book.seller,
        buyer=request.user,
        defaults={'book': book}
    )

    return redirect(f"{reverse('view_chat', kwargs={'chat_id': chat.id})}?book_id={book.id}")

@login_required
def inbox(request):
    requested_mode = request.GET.get('mode')

    if request.user.is_buyer and request.user.is_seller:
        inbox_mode = requested_mode if requested_mode in {'buyer', 'seller'} else 'buyer'
    elif request.user.is_seller:
        inbox_mode = 'seller'
    else:
        inbox_mode = 'buyer'

    if inbox_mode == 'seller':
        role_filter = Q(seller=request.user)
    else:
        role_filter = Q(buyer=request.user)

    user_chats = Chat.objects.filter(
        role_filter
    ).annotate(
        msg_count=Count('messages')
    ).filter(
        msg_count__gt=0
    ).select_related('buyer', 'seller', 'seller__seller_profile').order_by('-created_at')

    return render(request, 'chat/inbox.html', {
        'chats': user_chats,
        'inbox_mode': inbox_mode,
        'show_mode_switch': request.user.is_buyer and request.user.is_seller,
    })

@login_required
def view_chat(request, chat_id):
    chat = get_object_or_404(
        Chat.objects.select_related('buyer', 'seller', 'seller__seller_profile'),
        id=chat_id
    )

    requested_book_id = request.GET.get('book_id')
    close_url = reverse('inbox')

    try:
        requested_book_id = int(requested_book_id) if requested_book_id else None
    except (TypeError, ValueError):
        requested_book_id = None

    if requested_book_id and chat.book_id == requested_book_id:
        close_url = reverse('book_detail', kwargs={'book_id': chat.book_id})

    if request.user != chat.buyer and request.user != chat.seller:
        return redirect('inbox')

    if request.method == 'POST':
        content = request.POST.get('content')
        if content:
            Message.objects.create(
                chat=chat,
                sender=request.user,
                content=content
            )
            redirect_url = reverse('view_chat', kwargs={'chat_id': chat.id})
            if chat.book_id:
                redirect_url = f"{redirect_url}?book_id={chat.book_id}"
            return redirect(redirect_url)

    messages = chat.messages.all()

    chat.messages.filter(is_read=False).exclude(sender=request.user).update(is_read=True)

    return render(request, 'chat/view_chat.html', {
        'chat': chat,
        'chat_messages': messages,
        'close_url': close_url,
    })

@login_required
def delete_chat(request, chat_id):
    chat = get_object_or_404(Chat, id=chat_id)
    if request.user == chat.buyer or request.user == chat.seller:
        chat.delete()
    return redirect('inbox')
