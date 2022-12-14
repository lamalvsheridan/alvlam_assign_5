from django.db.models import Count

from . import models


def base_context(request):
    topics_aside = models.Topic.objects.annotate(Count('blog_posts')).order_by('-blog_posts__count')[:10]

    authors = models.Post.objects.published().get_authors().order_by('first_name')

    return {
        'topics_aside': topics_aside,
        'authors': authors
    }
