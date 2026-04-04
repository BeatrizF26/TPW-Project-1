from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Chat, Message
from books.models import Book
from django.db.models import Q, Count

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

    return redirect('view_chat', chat_id=chat.id)

@login_required
def inbox(request):
    user_chats = Chat.objects.filter(
        Q(buyer=request.user) | Q(seller=request.user)
    ).annotate(
        msg_count=Count('messages')
    ).filter(
        msg_count__gt=0
    ).order_by('-created_at')

    return render(request, 'chat/inbox.html', {'chats': user_chats})

@login_required
def view_chat(request, chat_id):
    chat = get_object_or_404(Chat, id=chat_id)

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
            return redirect('view_chat', chat_id=chat.id)

    messages = chat.messages.all()

    chat.messages.filter(is_read=False).exclude(sender=request.user).update(is_read=True)

    return render(request, 'chat/view_chat.html', {
        'chat': chat,
        'chat_messages': messages
    })

@login_required
def delete_chat(request, chat_id):
    chat = get_object_or_404(Chat, id=chat_id)
    if request.user == chat.buyer or request.user == chat.seller:
        chat.delete()
    return redirect('inbox')