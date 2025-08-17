from django.shortcuts import render
from .forms import UserRegistrationForm, UserProfileForm, PostForm, CommentForm
from django.shortcuts import render, redirect 
from django.contrib import messages 
from django.contrib.auth.decorators import login_required 
from django.contrib.auth import login, authenticate
from django.urls import reverse_lazy
from .models import Post, Comment
from django.views.generic import ListView,CreateView, UpdateView,DetailView,DeleteView 
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import get_object_or_404, redirect
def register_view(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Registration successful!")
            return redirect('login')
    else:
        form = UserRegistrationForm()
    return render(request, 'blog/register.html', {'form': form})

       
##profile 
@login_required
def profile_view(request):
    if request.method == 'POST':
        u_form = UserProfileForm(request.POST, instance=request.user)
        if u_form.is_valid():
            u_form.save()
            messages.success(request, "Your profile has been updated!")
            return redirect('profile')
    else:
        u_form = UserProfileForm(instance=request.user)

    return render(request, 'blog/profile.html', {'form': u_form})

class PostListView(ListView):
    model = Post 
    template_name = "blog/post_list.html"
    context_object_name = "posts"

class PostDetailView(DetailView):
    model = Post
    template_name = "blog/post_detail.html"

class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post 
    form_class = PostForm 
    template_name = "blog/post_form.html"

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):

    model = Post                 
    form_class = PostForm
    template_name = "blog/post_form.html"

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def test_func(self):
        post = self.get_object()
        return self.request.user == post.author

# Delete post
class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    template_name = "blog/post_confirm_delete.html"
    success_url = reverse_lazy('post-list')

    def test_func(self):
        post = self.get_object()
        return self.request.user == post.author
    

def add_comment(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.author = request.user
            comment.save()
            return redirect("post-detail", pk=post.id)
    else:
        form = CommentForm()
    return redirect("post-detail", pk=post.id)


class CommentUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Comment
    form_class = CommentForm
    template_name = "blog/comment_form.html"

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def test_func(self):
        comment = self.get_object()
        return self.request.user == comment.author


class CommentDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Comment
    template_name = "blog/comment_confirm_delete.html"

    def get_success_url(self):
        return self.object.post.get_absolute_url()  

    def test_func(self):
        comment = self.get_object()
        return self.request.user == comment.author