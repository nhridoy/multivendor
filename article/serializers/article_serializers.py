from rest_framework import serializers

from article.models import Article, ArticleCategory, ArticleComment
from authentications.serializers import UserSerializer


class ArticleCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = ArticleCategory
        fields = ("id", "icon", "name")


class ArticleCategoryCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = ArticleCategory
        fields = ("id", "icon", "name_en", "name_ko")


class ArticleCommentsSerializer(serializers.ModelSerializer):
    replies = serializers.SerializerMethodField(read_only=True)
    user = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = ArticleComment
        fields = (
            "id",
            "user",
            "content",
            "image",
            "created_at",
            "replies",
            "parent_comment",
        )
        # write_only_fields = ("article", "parent_comment",)
        extra_kwargs = {
            # "article": {"write_only": True},
            "parent_comment": {"write_only": True},
            # "user": {"read_only": True},
        }

    def get_replies(self, obj):
        # Get all replies for the current comment
        replies = obj.replies.all()
        return ArticleCommentsSerializer(
            replies, many=True, context={"request": self.context.get("request")}
        ).data

    def get_user(self, obj):
        request = self.context.get("request")
        return {
            "id": obj.user.id,
            "full_name": obj.user.user_information.full_name,
            "profile_picture": (
                request.build_absolute_uri(
                    obj.user.user_information.profile_picture.url
                )
                if obj.user.user_information.profile_picture
                else None
            ),
        }

    def validate_parent_comment(self, value):
        if value:
            article_slug = self.context.get("view").kwargs.get("slug")
            if value.article.slug != article_slug:
                raise serializers.ValidationError("Must belong to the same article.")

        return value


class ArticleListSerializer(serializers.ModelSerializer):
    user = serializers.SerializerMethodField(read_only=True)
    category = ArticleCategorySerializer(read_only=True)
    is_liked = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Article
        fields = [
            "id",
            "slug",
            "title",
            "short_content",
            "category",
            "user",
            "total_like",
            "total_comment",
            "thumbnail",
            "created_at",
            "updated_at",
            "is_liked",
        ]

    def get_user(self, obj):
        request = self.context.get("request")
        return {
            "id": obj.user.id,
            "full_name": obj.user.user_information.full_name,
            "profile_picture": (
                request.build_absolute_uri(
                    obj.user.user_information.profile_picture.url
                )
                if obj.user.user_information.profile_picture
                else None
            ),
        }

    def get_is_liked(self, obj):
        user_likes = self.context.get("user_likes", set())
        return obj.id in user_likes


class ArticleDetailSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    article_comments = ArticleCommentsSerializer(many=True, read_only=True)

    class Meta:
        model = Article
        fields = (
            "id",
            "slug",
            "category",
            "user",
            "title",
            "thumbnail",
            "short_content",
            "content",
            "total_like",
            "total_comment",
            "created_at",
            "updated_at",
            "article_comments",
        )
