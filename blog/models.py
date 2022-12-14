from django.conf import settings  # Imports Django's loaded settings
from django.db import models
from django.urls import reverse
from django.contrib.auth import get_user_model


class Topic(models.Model):
    """
    Represents a topic to organize blog posts
    """
    # Name of topic (no duplicates) (required)
    name = models.CharField(
        max_length=255,
        null=False,
        blank=False,
        unique=True,
    )

    # Prepopulate with value in name (required)
    slug = models.SlugField(
        null=False,
        blank=False,
    )

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        kwargs = {'slug': self.slug}
        return reverse('topic-detail', kwargs=kwargs)


class PostManager(models.Manager):
    def get_queryset(self):
        queryset = super().get_queryset()  # Get the initial queryset
        return queryset.exclude(deleted=True)  # Exclude deleted records


class PostQuerySet(models.QuerySet):
    def published(self):
        return self.filter(status=self.model.PUBLISHED)

    def drafts(self):
        return self.filter(status=self.model.DRAFT)

    def get_authors(self):
        User = get_user_model()
        # Get the users who are authors of this queryset
        return User.objects.filter(blog_posts__in=self).distinct()


class Post(models.Model):
    """
    Represents a blog post
    """
    DRAFT = 'draft'
    PUBLISHED = 'published'

    STATUS_CHOICES = [
        (DRAFT, 'Draft'),
        (PUBLISHED, 'Published')
    ]

    # Post title (required)
    title = models.CharField(
        max_length=255,
        null=False,
        blank=False,
    )

    # Article's content
    content = models.TextField()

    # A user can create one or more blog posts, but a blog post can only have one author
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,  # The Django auth user model
        on_delete=models.PROTECT,  # Prevent posts from being deleted
        related_name='blog_posts',
        null=False,                # required
        blank=False,
    )

    # A timestamp which is automatically set only on create
    created = models.DateTimeField(auto_now_add=True)
    # A timestamp which updates each time the object is saved
    updated = models.DateTimeField(auto_now=True)

    # Blog is published or in draft. Default state = draft (required)
    status = models.CharField(
        max_length=10,
        choices=STATUS_CHOICES,
        default=DRAFT,
        null=False,
        blank=False,
        help_text='Set to "published" to make this post publicly visible',
    )

    # A timestamp at which blog went from draft to published
    published = models.DateTimeField(
        help_text='The date & time this article was published',
    )

    # Label used to form URL; Prepopulate with value in 'title' (required)
    slug = models.SlugField(
        null=False,
        blank=False,
        unique_for_date='published',
    )

    # Each post can have multiple topics
    topic = models.ManyToManyField(
        Topic,
        related_name='blog_posts',
    )

    # Marks deleted posts
    deleted = models.BooleanField()

    objects = PostQuerySet.as_manager()

    class Meta:
        ordering = ['-created']

    def __str__(self):
        return self.title

    def publish(self):
        """Publishes this post"""
        self.status = self.PUBLISHED
        self.published = timezone.now()  # The current datetime with timezone

    def get_absolute_url(self):
        if self.published:
            kwargs = {
                'year': self.published.year,
                'month': self.published.month,
                'day': self.published.day,
                'slug': self.slug
            }
        else:
            kwargs = {'pk': self.pk}

        return reverse('post-detail', kwargs=kwargs)


class Comment(models.Model):
    """
    Represents a comment on a blog post
    """
    # A relationship to the Post model. Set related_name='comments' on the field (required)
    post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE,  # Prevent posts from being deleted
        related_name='comments',
        null=False,                # required
        blank=False,
    )
    # The name of the person making the comment (required)
    name = models.CharField(
        max_length=50,
        null=False,
        blank=False,
    )
    # The email address for the commenter (required)
    email = models.CharField(
        max_length=100,
        null=False,
        blank=False,
    )
    # A field containing the actual comment. Optionally consider limiting the
    # amount of characters allowed so that users don't get carried away (required)
    text = models.TextField(
        max_length=500,
        null=False,
        blank=False,
    )
    # A boolean field which is intended for comment moderation. If true, the
    # comment will appear on the site, otherwise, it will be hidden
    approved = models.BooleanField(
        default=False,
    )
    # A timestamp which is automatically set only on create
    created = models.DateTimeField(auto_now_add=True)
    # A timestamp which updates each time the object is saved
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created']

    def __str__(self):
        return self.name


class Contest(models.Model):
    # The first name of the person submitting the photo (required)
    first_name = models.CharField(
        max_length=50,
        null=False,
        blank=False,
    )
    # The last name of the person submitting the photo (required)
    last_name = models.CharField(
        max_length=50,
        null=False,
        blank=False,
    )
    # The email address of the person submitting the photo (required)
    email = models.CharField(
        max_length=100,
        null=False,
        blank=False,
    )
    # The submitted photo (required)
    submission = models.ImageField(
        null=False,
        blank=False,
    )
    # The date submitted, generated on created
    submitted_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-submitted_date']

    def __str__(self):
        return f'{self.submitted_date}: {self.email}'
