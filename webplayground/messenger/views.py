from django.shortcuts import render, get_object_or_404, redirect
from django.http import Http404, JsonResponse
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.views.generic import TemplateView
from django.views.generic.detail import DetailView
from .models import Thread, Message, User
from django.utils.timezone import now

# Create your views here.

# def format_timesince(time_since_created):
#     time_since_created_str = 'Hace '
    
#     years = time_since_created.days // 365
#     if years:
#         time_since_created_str += f"{years} {'años' if years > 1 else 'año'}, "
#     months = (time_since_created.days % 365) // 30
#     if months:
#         time_since_created_str += f"{months} {'meses' if months > 1 else 'mes'}, "
#     weeks = ((time_since_created.days % 365) % 30) // 7
#     if weeks:
#         time_since_created_str += f"{weeks} {'semanas' if weeks > 1 else 'semana'}, "
#     days = ((time_since_created.days % 365) % 30) % 7
#     if days:
#         time_since_created_str += f"{days} {'días' if days > 1 else 'día'}, "
#     hours, remainder = divmod(time_since_created.seconds, 3600)
#     if hours:
#         time_since_created_str += f"{hours} {'horas' if hours > 1 else 'hora'}, "
#     minutes, seconds = divmod(remainder, 60)
#     if minutes:
#         time_since_created_str += f"{minutes} {'minutos' if minutes > 1 else 'minuto'}, "

#     if len(time_since_created_str) > len('Hace '):
#         time_since_created_str = time_since_created_str[:-2]
#         last_comma_index = time_since_created_str.rfind(',')
#         if last_comma_index >= 0:
#             time_since_created_str = time_since_created_str[:last_comma_index] + ' y' + time_since_created_str[last_comma_index + 1:] ###
#     else:
#         time_since_created_str += 'unos segundos'

#     return time_since_created_str

# @method_decorator(login_required, name="dispatch")
# class ThreadList(TemplateView):
#     template_name = "messenger/thread_list.html"

#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         threads = self.request.user.threads.all()
#         threads_with_timesince = []
#         for thread in threads:
#             last_message = thread.messages.last()
#             if last_message:
#                 time_since_created = now() - last_message.created
#                 time_since_created_str = format_timesince(time_since_created)
#                 threads_with_timesince.append((thread, time_since_created_str))
#         context['threads_with_timesince'] = threads_with_timesince
#         return context

@method_decorator(login_required, name="dispatch")
class ThreadList(TemplateView):
    template_name = "messenger/thread_list.html"

@method_decorator(login_required, name="dispatch")
class ThreadDetail(DetailView):
    model = Thread

    def get_object(self):
        obj = super(ThreadDetail, self).get_object()
        if self.request.user not in obj.users.all():
            raise Http404()
        return obj

def add_message(request, pk):
    #print(request.GET)
    json_response = {'created': False}
    if request.user.is_authenticated:
        content = request.GET.get('content', None)
        if content:
            thread = get_object_or_404(Thread, pk=pk)
            message = Message.objects.create(user=request.user, content=content)
            thread.messages.add(message)
            json_response['created'] = True
            if len(thread.messages.all()):  # is 1
                json_response['changed'] = True
    else:
        raise Http404("User is not authenticated")
    return JsonResponse(json_response)

@login_required
def start_thread(request, username):
    user = get_object_or_404(User, username=username)
    thread = Thread.objects.find_or_create(user, request.user)
    return redirect(reverse_lazy('messenger:detail', args=[thread.pk]))
