from autoslug import AutoSlugField
from django.core.exceptions import ValidationError
from django.db import models
from tinymce.models import HTMLField

from core.models import BaseModel
from utils.helper import content_file_path

# Create your models here.


class ArticleCategory(BaseModel):
    name = models.CharField(max_length=100, blank=True)
    icon = models.ImageField(upload_to=content_file_path)
    description = models.TextField()

    class Meta:
        verbose_name_plural = "Article Categories"

    def __str__(self):
        return self.name


class Article(BaseModel):
    slug = AutoSlugField(populate_from="title", unique=True)
    title = models.CharField(max_length=100)
    square_thumbnail = models.ImageField(upload_to=content_file_path)
    landscape_thumbnail = models.ImageField(
        upload_to=content_file_path, blank=True, null=True
    )
    short_content = models.TextField()
    content = HTMLField()
    category = models.ForeignKey(
        ArticleCategory,
        on_delete=models.PROTECT,
        related_name="article_category",
    )
    author = models.ForeignKey(
        "authentications.User",
        on_delete=models.PROTECT,
        related_name="article_author",
    )
    total_like = models.PositiveIntegerField(default=0, editable=False)
    total_comment = models.PositiveIntegerField(default=0, editable=False)

    def __str__(self):
        return self.title


class ArticleComment(BaseModel):
    content = models.TextField()
    image = models.ImageField(upload_to=content_file_path, blank=True, null=True)
    article = models.ForeignKey(
        Article, on_delete=models.CASCADE, related_name="article_comments"
    )
    parent_comment = models.ForeignKey(
        "self",
        on_delete=models.CASCADE,
        related_name="replies",
        null=True,
        blank=True,
    )
    author = models.ForeignKey(
        "authentications.User",
        on_delete=models.PROTECT,
        related_name="comments",
    )

    def clean(self):
        errors = {}
        # Ensure that the parent comment belongs to the same article
        if self.parent_comment and self.parent_comment.article_id != self.article_id:
            errors.setdefault("parent_comment", []).append(
                "Parent comment must belong to the same article."
            )

        if errors:
            raise ValidationError(errors)

    def get_replies(self):
        return ArticleComment.objects.filter(comment=self)

    def __str__(self):
        return f"Comment by {self.author} on {self.article}"


class ArticleLike(BaseModel):
    article = models.ForeignKey(
        Article, on_delete=models.CASCADE, related_name="article_like"
    )
    author = models.ForeignKey(
        "authentications.User",
        on_delete=models.PROTECT,
        related_name="article_like_author",
    )

    class Meta:
        unique_together = (("article", "author"),)

    def __str__(self):
        return f"{self.author} like {self.article}"
