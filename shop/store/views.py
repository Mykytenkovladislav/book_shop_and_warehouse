from django.contrib.auth import authenticate, login, get_user_model
from django.contrib.auth.decorators import login_required
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

from store.models import Book, Order, OrderItem

User = get_user_model()


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


class BookListView(generic.ListView):
    queryset = Book.objects.all().order_by('title')
    template_name = 'index.html'
    paginate_by = 10


class BookDetailView(SuccessMessageMixin, generic.DetailView):
    model = Book
    template_name = 'store/book_details.html'


@login_required
def add_to_order(request, pk):
    book = get_object_or_404(Book, pk=pk)
    current_user = request.user
    order, created = Order.objects.get_or_create(status=2, user=current_user,
                                                 defaults={'user': current_user, 'comment': 'added automatically'})
    if OrderItem.objects.filter(book=book, order=order).exists():
        book_order_item = OrderItem.objects.get(book=book, order=order)
        book_order_item.quantity += 1
        book_order_item.save()
        messages.success(request, "Item already in cart! We added increased books quantity to +1")
        return redirect('index')
        #  TODO try both variants
        # return reverse_lazy('index')
    else:
        order_item = OrderItem.objects.create(order=order, book=book)
        messages.success(request, "Item added to the cart!")
        return redirect('index')
        #  TODO try both variants
        # return reverse_lazy('index')
