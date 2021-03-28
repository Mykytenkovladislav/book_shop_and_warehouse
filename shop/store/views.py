from django.contrib.auth import authenticate, login, get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.core.mail import send_mail
from django.http import JsonResponse
from django.shortcuts import redirect, render, get_object_or_404
from django.template.loader import render_to_string
from django.urls import reverse_lazy
from django.views import generic

from store.forms import ContactForm, RegisterForm
from django.contrib import messages

User = get_user_model()


def index(request):
    return render(
        request,
        'index.html',
    )


class RegisterFormView(generic.FormView):
    template_name = 'registration/register.html'
    form_class = RegisterForm
    success_url = reverse_lazy("index")

    def form_valid(self, form):
        form.save()

        username = self.request.POST['username']
        password = self.request.POST['password1']

        user = authenticate(username=username, password=password)
        login(self.request, user)
        return super(RegisterFormView, self).form_valid(form)


def contact_form_ajax(request):
    data = dict()
    if request.method == "GET":
        form = ContactForm()
    else:
        form = ContactForm(request.POST)
        if form.is_valid():
            subject = form.cleaned_data['subject']
            from_email = form.cleaned_data['from_email']
            message = form.cleaned_data['message']
            send_mail(subject, message, from_email, ['admin@admin.com'])
            messages.add_message(request, messages.SUCCESS, 'Message sent')
            return redirect('index')
        else:
            data['form_is_valid'] = False
    context = {'form': form}
    data['html_form'] = render_to_string(
        template_name='include/contact_ajax.html',
        context=context,
        request=request
    )
    return JsonResponse(data)


class UpdateProfileView(LoginRequiredMixin, SuccessMessageMixin, generic.UpdateView):
    model = User
    fields = ['first_name', 'last_name', 'email']
    template_name = 'users/update_profile.html'
    success_url = reverse_lazy('index')
    success_message = 'Profile updated'

    def get_object(self, queryset=None):
        user = self.request.user
        return user
