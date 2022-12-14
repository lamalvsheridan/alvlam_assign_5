from django.shortcuts import render
from django.db.models import Count

from django.contrib import messages

from django.views.generic.base import TemplateView
from django.views.generic import DetailView, CreateView, FormView, ListView
from django.urls import reverse_lazy

from . import forms, models


class HomeView(TemplateView):
    template_name = 'blog/home.html'

    def get_context_data(self, **kwargs):
        # Get the parent context
        context = super().get_context_data(**kwargs)

        latest_posts = models.Post.objects.published().order_by('-published')[:3]

        # Update the context with our context variables
        context.update({'latest_posts': latest_posts})

        return context


class AboutView(TemplateView):
    template_name = 'blog/about.html'

def terms_and_conditions(request):
   return render(request, 'blog/terms_and_conditions.html')


class PostListView(ListView):
    model = models.Post
    context_object_name = 'posts'
    queryset = models.Post.objects.published()  # Customized queryset


class PostDetailView(DetailView):
    model = models.Post

    def get_queryset(self):
        queryset = super().get_queryset().published()

        # If this is a `pk` lookup, use default queryset
        if 'pk' in self.kwargs:
            return queryset

        # Otherwise, filter on the published date
        return queryset.filter(
            published__year=self.kwargs['year'],
            published__month=self.kwargs['month'],
            published__day=self.kwargs['day'],
        )

    def get_context_data(self, **kwargs):
        # Get the parent context
        context = super().get_context_data(**kwargs)

        post_topics = super().get_object().topic.all()

        context.update({
            'post_topics': post_topics
        })

        return context


class TopicListView(ListView):
    model = models.Topic
    context_object_name = 'topics'


class TopicDetailView(DetailView):
    model = models.Topic

    def get_context_data(self, **kwargs):
        # Get the parent context
        context = super().get_context_data(**kwargs)

        blog_posts = super().get_object().blog_posts.all()

        context.update({
            'blog_posts': blog_posts
        })

        return context


class ContestView(CreateView):
    model = models.Contest

    template_name = 'blog/contest_form.html'
    success_url = reverse_lazy('home')

    fields = [
        'first_name',
        'last_name',
        'email',
        'submission',
    ]

    def form_valid(self, form):
        # Create a "success" message
        messages.add_message(
            self.request,
            messages.SUCCESS,
            'Thank you for submitting your entry to the Photo Contest!'
        )
        # Continue with default behaviour
        return super().form_valid(form)
