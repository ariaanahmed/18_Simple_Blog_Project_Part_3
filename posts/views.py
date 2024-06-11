from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from . import forms
from . import models
from django.contrib.auth.decorators import login_required
from django.views.generic import CreateView, UpdateView, DeleteView, DetailView
from django.utils.decorators import method_decorator


# add post using class based view: form, model, redirect, template
@method_decorator(login_required, name="dispatch")
class AddPostCreateView(CreateView):
    model = models.Post
    form_class = forms.PostForm
    template_name = "add_post.html"
    success_url = reverse_lazy("homepage")

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


# edit post: id, model, form, template
@method_decorator(login_required, name="dispatch")
class EditPostView(UpdateView):
    model = models.Post
    form_class = forms.PostForm
    template_name = "add_post.html"
    pk_url_kwarg = "id"
    success_url = reverse_lazy("profile")


# delete view
@method_decorator(login_required, name="dispatch")
class DeletePostView(DeleteView):
    model = models.Post
    template_name = "delete.html"
    pk_url_kwarg = "id"
    success_url = reverse_lazy("profile")


# details view
class DetailPostView(DetailView):
    model = models.Post
    pk_url_kwarg = "id"
    template_name = "post_details.html"

    def post(self, request, *args, **kwargs):
        comment_form = forms.CommentForm(data=self.request.POST)
        post = self.get_object()
        if comment_form.is_valid():
            new_comment = comment_form.save(commit=False)
            new_comment.post = post
            new_comment.save()
        return self.get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        post = self.object  # post model er object stored here
        comments = post.comments.all()
        comment_form = forms.CommentForm()

        context["comments"] = comments
        context["comment_form"] = comment_form
        return context
