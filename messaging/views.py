from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from .models import Conversation, Message
from users.models import CustomUser
import random
from django.views.decorators.http import require_POST

@login_required
def conversation_list(request):
    """Show user's conversations"""
    conversations = request.user.conversations.all()
    # Get unread counts for each conversation
    conversation_data = []
    for conversation in conversations:
        other_user = conversation.participants.exclude(id=request.user.id).first()
        if other_user:
            unread_count = conversation.messages.filter(
                sender=other_user,
                is_read=False
            ).count()
            conversation_data.append({
                'conversation': conversation,
                'other_user': other_user,
                'unread_count': unread_count,
                'last_message': conversation.messages.last()
            })
    context = {
        'conversation_data': conversation_data,
    }
    return render(request, 'messaging/conversation_list.html', context)

@login_required
def conversation_detail(request, conversation_id):
    """Show conversation messages"""
    conversation = get_object_or_404(Conversation, id=conversation_id, participants=request.user)
    if request.method == 'POST':
        content = request.POST.get('content', '').strip()
        if content:
            # Create the message
            message = Message.objects.create(
                conversation=conversation,
                sender=request.user,
                content=content
            )
            # Auto-reply from the other participant (gig owner)
            other_user = conversation.participants.exclude(id=request.user.id).first()
            if other_user:
                auto_reply = generate_auto_reply(content, other_user)
                Message.objects.create(
                    conversation=conversation,
                    sender=other_user,
                    content=auto_reply
                )
            return redirect('messaging:conversation_detail', conversation_id=conversation_id)
    # Mark messages as read
    conversation.messages.filter(
        sender__in=conversation.participants.exclude(id=request.user.id)
    ).update(is_read=True)
    context = {
        'conversation': conversation,
        'messages': conversation.messages.all(),
        'other_user': conversation.participants.exclude(id=request.user.id).first(),
    }
    return render(request, 'messaging/conversation_detail.html', context)

@login_required
def start_conversation(request, user_id):
    """Start a new conversation with a user"""
    other_user = get_object_or_404(CustomUser, id=user_id)
    if other_user == request.user:
        return redirect('gigs:home')
    # Check if conversation already exists
    existing_conversation = Conversation.objects.filter(
        participants=request.user
    ).filter(
        participants=other_user
    ).first()
    if existing_conversation:
        return redirect('messaging:conversation_detail', conversation_id=existing_conversation.id)
    # Create new conversation
    conversation = Conversation.objects.create()
    conversation.participants.add(request.user, other_user)
    # Create initial welcome message from the gig owner
    welcome_message = generate_welcome_message(other_user)
    Message.objects.create(
        conversation=conversation,
        sender=other_user,
        content=welcome_message
    )
    return redirect('messaging:conversation_detail', conversation_id=conversation.id)

@require_POST
@login_required
def delete_conversation(request, conversation_id):
    conversation = get_object_or_404(Conversation, id=conversation_id, participants=request.user)
    conversation.delete()
    return redirect('messaging:conversation_list')

def generate_welcome_message(freelancer):
    """Generate a welcome message from the freelancer"""
    welcome_messages = [
        f"Hi! I'm {freelancer.get_full_name()}. Thanks for your interest in my services. How can I help you today?",
        f"Hello! I'm {freelancer.get_full_name()}. I'm excited to work with you. What project do you have in mind?",
        f"Welcome! I'm {freelancer.get_full_name()}. I'd love to discuss your project requirements. What are you looking for?",
        f"Hi there! I'm {freelancer.get_full_name()}. Ready to bring your ideas to life. What can I do for you?",
        f"Hello! I'm {freelancer.get_full_name()}. Let's discuss how I can help with your project. What do you need?"
    ]
    return random.choice(welcome_messages)

def generate_auto_reply(user_message, freelancer):
    """Generate an auto-reply based on the user's message content"""
    user_message_lower = user_message.lower()
    responses = {
        'price': [
            f"Thanks for asking about pricing! I offer competitive rates and can provide a detailed quote based on your specific requirements. What's your budget range?",
            f"I'd be happy to discuss pricing options with you. My rates are flexible and depend on the project scope. Could you share more details about your project?",
            f"Pricing varies based on project complexity and timeline. I can provide a custom quote once I understand your needs better. What's your timeline?",
            f"I offer transparent pricing with no hidden fees. Let me know your project details and I'll provide a fair quote. What's your budget?"
        ],
        'cost': [
            f"I offer competitive pricing that fits various budgets. Could you tell me more about your project so I can give you an accurate quote?",
            f"My rates are reasonable and I'm happy to work within your budget. What's the scope of your project?",
            f"I provide value for money with quality work. Let's discuss your requirements and I'll give you a fair price."
        ],
        'time': [
            f"Great question about timing! I typically deliver projects within the agreed timeframe. What's your deadline for this project?",
            f"I'm committed to meeting deadlines and keeping you updated throughout the process. When do you need this completed?",
            f"Timeline depends on project scope, but I always communicate clearly about delivery dates. What's your preferred timeline?",
            f"I work efficiently to meet your deadlines. How soon do you need this project completed?"
        ],
        'deadline': [
            f"I understand deadlines are important. I'll work efficiently to meet your timeline. When do you need this completed?",
            f"I'm committed to delivering on time. Let me know your deadline and I'll ensure we meet it.",
            f"Timely delivery is a priority for me. What's your target completion date?"
        ],
        'experience': [
            f"I have extensive experience in this field and have completed many successful projects. I'd be happy to share my portfolio with you.",
            f"With years of experience, I bring expertise and reliability to every project. Would you like to see some of my previous work?",
            f"I'm confident in my skills and experience. I can provide references and examples of my work if you'd like.",
            f"I've worked on various projects and have a proven track record. Would you like to see some examples of my work?"
        ],
        'portfolio': [
            f"I'd be happy to share my portfolio with you! I have examples of my best work that showcase my skills and style.",
            f"Absolutely! I can show you my portfolio with various projects I've completed. What type of work interests you most?",
            f"I have a comprehensive portfolio demonstrating my expertise. Would you like me to share specific examples relevant to your project?",
            f"My portfolio showcases my best work and demonstrates my capabilities. I'd love to share it with you!"
        ],
        'work': [
            f"I'd be happy to show you examples of my work. I have a portfolio that demonstrates my skills and style.",
            f"I can share my previous projects with you. What type of work are you most interested in seeing?",
            f"I have a collection of my best work that I can share. Would you like to see specific examples?"
        ],
        'start': [
            f"I'm ready to start working on your project! Let's discuss the details and get everything set up.",
            f"Perfect! I'm excited to begin. Let me know what specific requirements you have and I'll get started right away.",
            f"Great! I'm available to start immediately. What are the next steps you'd like to take?",
            f"I'm ready to get started on your project. Let's finalize the details and begin!"
        ],
        'begin': [
            f"I'm ready to begin working on your project. Let's discuss the requirements and get started.",
            f"Perfect! I'm excited to start. What specific details should we discuss first?",
            f"Great! Let's get started. What are the key requirements for your project?"
        ],
        'payment': [
            f"I accept various payment methods and can discuss payment terms that work for both of us. What's your preferred payment method?",
            f"Payment can be arranged through SkillBazar's secure system. I'm flexible with payment schedules. What works best for you?",
            f"I offer secure payment options and can work with your preferred payment method. Let's discuss the payment terms.",
            f"I'm flexible with payment arrangements. We can discuss terms that work for both of us."
        ],
        'pay': [
            f"I accept multiple payment methods for your convenience. What payment option works best for you?",
            f"Payment can be arranged securely through SkillBazar. I'm flexible with payment schedules.",
            f"I offer various payment options to make it easy for you. Let's discuss what works best."
        ],
        'quality': [
            f"I'm committed to delivering high-quality work that exceeds expectations. Quality is my top priority.",
            f"I take pride in my work and always strive for excellence. You can expect top-notch results.",
            f"Quality is non-negotiable for me. I ensure every project meets the highest standards."
        ],
        'revision': [
            f"I offer revisions to ensure you're completely satisfied with the final result. Your satisfaction is important to me.",
            f"I'm happy to make revisions until you're 100% satisfied. I want you to love the final product.",
            f"I provide revision rounds to make sure the work meets your exact requirements."
        ],
        'urgent': [
            f"I understand this is urgent. I'll prioritize your project and work efficiently to meet your timeline.",
            f"I can accommodate urgent projects. Let me know your deadline and I'll ensure timely delivery.",
            f"I'm available for urgent work and will work quickly to meet your needs."
        ],
        'quick': [
            f"I can work quickly to meet your timeline. Let me know your deadline and I'll ensure fast delivery.",
            f"I'm efficient and can complete projects quickly while maintaining quality. What's your timeline?",
            f"I can work fast to meet your needs. How soon do you need this completed?"
        ]
    }
    # Check for keywords in the user's message
    for keyword, reply_list in responses.items():
        if keyword in user_message_lower:
            return random.choice(reply_list)
    # Check for question words to provide more helpful responses
    question_words = ['what', 'how', 'when', 'where', 'why', 'can you', 'do you', 'will you']
    if any(word in user_message_lower for word in question_words):
        question_responses = [
            f"Great question! I'm {freelancer.get_full_name()} and I'd be happy to help. Could you provide more details about your project?",
            f"Thanks for asking! I'm {freelancer.get_full_name()}. Let me know more about your requirements so I can give you a detailed answer.",
            f"Good question! I'm {freelancer.get_full_name()}. I'd love to discuss your project in detail to provide the best answer."
        ]
        return random.choice(question_responses)
    # Default responses for general messages
    default_responses = [
        f"Thanks for your message! I'm {freelancer.get_full_name()} and I'm here to help with your project. Could you tell me more about what you need?",
        f"Hi! I appreciate your interest. I'm {freelancer.get_full_name()} and I'd love to discuss your project requirements in detail.",
        f"Hello! I'm {freelancer.get_full_name()}. I'm excited to work with you. What specific aspects of your project would you like to discuss?",
        f"Thanks for reaching out! I'm {freelancer.get_full_name()}. I'm ready to help bring your project to life. What are your main requirements?",
        f"Hi there! I'm {freelancer.get_full_name()}. I'm committed to delivering quality work. What can I help you with today?",
        f"Hello! I'm {freelancer.get_full_name()}. I'm here to help you with your project. What would you like to discuss?",
        f"Hi! I'm {freelancer.get_full_name()}. I'm excited to work with you. What project do you have in mind?",
        f"Thanks for contacting me! I'm {freelancer.get_full_name()}. I'd love to hear more about your project requirements."
    ]
    return random.choice(default_responses) 