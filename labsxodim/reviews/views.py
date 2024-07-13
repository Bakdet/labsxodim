from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate
from django.contrib.auth.models import User,auth
from django.contrib import messages
from .forms import RegistrationForm, LoginForm
from django.contrib.auth.decorators import login_required
from .forms import ItemForm, ProfileForm, UserChangeForm, EditProfileForm, EditUserForm, SearchForm
from .models import Item, Profile
from django.urls import reverse_lazy

@login_required
def add_item(request):
    if request.method == 'POST':
        form = ItemForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('')
    else:
        form = ItemForm()
    return render(request, 'add_item.html', {'form': form})
def delete_view(request, pk):
    myobject = get_object_or_404(Item, pk=pk)
    myobject.delete()
    return redirect('')
def update_view(request, pk):
    item = get_object_or_404(Item, pk=pk)
    if request.method == 'POST':
        form = ItemForm(request.POST, instance=item)
        if form.is_valid():
            form.save()
            return redirect('')
    else:
        form = ItemForm(instance=item)
    return render(request, 'update.html', {'form': form})
def item_detail(request, pk):
    item = get_object_or_404(Item, pk=pk)

    last_viewed_items = request.session.get('last_viewed_items', [])
    if pk in last_viewed_items:
        last_viewed_items.remove(pk)
    last_viewed_items.insert(0, pk)
    if len(last_viewed_items) > 5:
        last_viewed_items.pop()
    request.session['last_viewed_items'] = last_viewed_items
    
    context = {
        'item': item,
    }
    return render(request, 'item_detail.html', context)

from django.db.models import Q
def item_list(request):
    search_query = request.GET.get('search')
    items = Item.objects.all()

    if search_query:
        items = items.filter(Q(name__icontains=search_query))
    items = Item.objects.all()
    context = {
        'items': items
    }

    return render(request, 'home.html',  context)

def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('')
    else:
        form = RegistrationForm()

    context = {'form': form}
    return render(request, 'register.html', context)
def logout_user(request):
	auth.logout(request)
	return redirect('') 

def user_login(request):
	if request.method == 'POST':
		username =request.POST['username']
		password = request.POST['password']
		user = auth.authenticate(username=username, password=password)
		if user is not None:
			auth.login(request, user)
			return redirect('')
		else:
			messages.info(request, 'Invalid Username or Password')
			return redirect('login')
	else:
		return render(request, 'login.html')

@login_required
def profile(request):
    user = request.user
    return render(request, 'profile.html', {'user': user})


@login_required
def edit_profile(request):
    user = request.user
    try:
        profile = user.profile
    except Profile.DoesNotExist:
        profile = Profile.objects.create(user=user)
    if request.method == 'POST':
        user_form = EditUserForm(request.POST, instance=user)
        profile_form = EditProfileForm(request.POST, request.FILES, instance=profile)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, ('Your profile was successfully updated!'))
            return redirect('profile')
        else:
            messages.error(request, ('Please correct the error below.'))
    else:
        user_form = EditUserForm(instance=user)
        profile_form = EditProfileForm(instance=profile)
    return render(request, 'edit_profile.html', {'user_form': user_form, 'profile_form': profile_form})

from django.views.generic import ListView, UpdateView, DeleteView
from .forms import UserAdminForm

from django.contrib.auth.mixins import UserPassesTestMixin
class UserAdminListView(UserPassesTestMixin, ListView):
    model = User
    template_name = 'user_list.html'
    context_object_name = 'users'
    def test_func(self):
        return self.request.user.is_staff

class UserAdminUpdateView(UserPassesTestMixin, UpdateView):
    model = Profile
    form_class = EditProfileForm
    template_name = 'user_edit.html'
    success_url = reverse_lazy('user_list')
    
    def test_func(self):
        return self.request.user.is_staff
    
    def get_object(self, queryset=None):
        user_pk = self.kwargs.get('pk')
        profile = get_object_or_404(Profile, user__pk=user_pk)
        return profile
from django.http import Http404

class UserAdminDeleteView(UserPassesTestMixin, DeleteView):
    model = User
    success_url = reverse_lazy('user_list')
    template_name = 'delete_profile.html'
    pk_url_kwarg = 'pk'
    def test_func(self):
        return self.request.user.is_staff


from django.contrib.auth.decorators import user_passes_test
from .models import ItemRequest
@login_required
def create_item_request(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        price = request.POST.get('price')
        description = request.POST.get('description')
        picture = request.FILES.get('picture')
        item_request = ItemRequest.objects.create(
            user=request.user,
            name=name,
            price=price,
            description=description,
            picture=picture
        )
        messages.success(request, 'Item request submitted successfully!')
        return redirect('item_request_list')
    return render(request, 'create_item_request.html')


@user_passes_test(lambda u: u.is_staff)
def approve_item_request(request, item_request_id):
    item_request = ItemRequest.objects.get(id=item_request_id)
    item_request.status = 'approved'
    item_request.save()
    item = Item.objects.create(
        name=item_request.name,
        price=item_request.price,
        picture=item_request.picture,
        description=item_request.description
    )
    item_request.item = item
    item_request.save()
    messages.success(request, 'Item request approved successfully!')
    return redirect('item_request_list')

@user_passes_test(lambda u: u.is_staff)
def reject_item_request(request, item_request_id):
    item_request = ItemRequest.objects.get(id=item_request_id)
    item_request.status = 'rejected'
    item_request.save()
    messages.success(request, 'Item request rejected successfully!')
    return redirect('item_request_list')

@login_required
def item_request_list(request):
    if request.user.is_staff:
        item_requests = ItemRequest.objects.all()
    else:
        item_requests = ItemRequest.objects.filter(user=request.user)
    return render(request, 'item_request_list.html', {'item_requests': item_requests})


def last_viewed_items(request):
	last_viewed = request.session.get('last_viewed_items', [])[:5] # Get last viewed items from session, limiting to 5
	items = [] # Create an empty list to hold the items
	for item_id in last_viewed:
		item = get_object_or_404(Item, pk=item_id) # Retrieve each item from the database
		items.append(item) # Add the item to the list
	return render(request, '', {'items': items})
from django.contrib.auth.signals import user_logged_in

def reset_last_viewed_items(sender, user, request, **kwargs):
    if 'last_viewed_items' in request.session:
        del request.session['last_viewed_items']

user_logged_in.connect(reset_last_viewed_items)
from django.db.models import Q
from django.views.generic import ListView, View


def item_search(request):
    query = request.GET.get('search_query')
    min_price = request.GET.get('min_price')
    max_price = request.GET.get('max_price')
    if query:
        items = Item.search(query, min_price=min_price, max_price=max_price)
    else:
        items = Item.objects.none()
    context = {'items': items, 'query': query, 'min_price': min_price, 'max_price': max_price}
    return render(request, 'item_search.html', context)