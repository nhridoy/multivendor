from django.db import transaction
from rest_framework import serializers
from rest_framework.serializers import ModelSerializer

from forum.models import Forum, ForumComment, ForumImage, Tag
from options.models import City, Province


class TagSerializer(ModelSerializer):
    class Meta:
        model = Tag
        fields = (
            "id",
            "tag_name",
        )


class TagCreateSerializer(ModelSerializer):
    class Meta:
        model = Tag
        fields = ("id", "tag_name_en", "tag_name_ko")


class ForumCommentsSerializer(serializers.ModelSerializer):
    replies = serializers.SerializerMethodField(read_only=True)
    author = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = ForumComment
        fields = (
            "id",
            "author",
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
            # "author": {"read_only": True},
        }

    def get_replies(self, obj):
        # Get all replies for the current comment
        replies = obj.replies.all()
        return ForumCommentsSerializer(
            replies, many=True, context={"request": self.context.get("request")}
        ).data

    def get_author(self, obj):
        request = self.context.get("request")
        return {
            "id": obj.author.id,
            "username": obj.author.username,
            "full_name": obj.author.user_information.full_name,
            "profile_picture": (
                request.build_absolute_uri(
                    obj.author.user_information.profile_picture.url
                )
                if obj.author.user_information.profile_picture
                else None
            ),
        }

    def validate_parent_comment(self, value):
        if value:
            forum_slug = self.context.get("view").kwargs.get("slug")
            if value.forum.slug != forum_slug:
                raise serializers.ValidationError("Must belong to the same forum.")

        return value


class ForumImageSerializer(ModelSerializer):
    class Meta:
        model = ForumImage
        fields = ("image",)


class ForumListSerializer(ModelSerializer):
    province = serializers.CharField(source="province.province_name")
    city = serializers.CharField(source="city.city_name")
    tags = TagSerializer(many=True, read_only=True)
    author = serializers.SerializerMethodField(read_only=True)
    is_liked = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Forum
        fields = [
            "id",
            "slug",
            "title",
            "content",
            "province",
            "city",
            "tags",
            "total_like",
            "total_comment",
            "created_at",
            "updated_at",
            "author",
            "is_liked",
        ]

    def get_is_liked(self, obj):
        user_likes = self.context.get("user_likes", set())
        return obj.id in user_likes

    def get_author(self, obj):
        request = self.context.get("request")
        return {
            "id": obj.author.id,
            "username": obj.author.username,
            "full_name": obj.author.user_information.full_name,
            "profile_picture": (
                request.build_absolute_uri(
                    obj.author.user_information.profile_picture.url
                )
                if obj.author.user_information.profile_picture
                else None
            ),
        }


class ForumDetailSerializer(ModelSerializer):
    forum_images = ForumImageSerializer(many=True, read_only=True, source="images")
    tags = TagSerializer(many=True, read_only=True)
    province = serializers.CharField(source="province.province_name", read_only=True)
    city = serializers.CharField(source="city.city_name", read_only=True)
    author = serializers.SerializerMethodField(read_only=True)
    forum_comments = ForumCommentsSerializer(many=True, read_only=True)

    province_id = serializers.PrimaryKeyRelatedField(
        queryset=Province.objects.all(), write_only=True
    )
    city_id = serializers.PrimaryKeyRelatedField(
        queryset=City.objects.all(), write_only=True
    )
    tag_id = serializers.PrimaryKeyRelatedField(
        many=True, queryset=Tag.objects.all(), write_only=True, required=True
    )
    images = serializers.ListField(
        child=serializers.ImageField(allow_empty_file=False, use_url=False),
        write_only=True,
    )

    class Meta:
        model = Forum
        fields = (
            "id",
            "slug",
            "title",
            "content",
            "province",
            "province_id",
            "city",
            "city_id",
            "tags",
            "tag_id",
            "forum_images",
            "total_like",
            "total_comment",
            "created_at",
            "updated_at",
            "images",
            "author",
            "forum_comments",
        )
        read_only_fields = ("author", "slug", "total_like", "total_comment")

    def get_author(self, obj):
        request = self.context.get("request")
        return {
            "id": obj.author.id,
            "username": obj.author.username,
            "full_name": obj.author.user_information.full_name,
            "profile_picture": (
                request.build_absolute_uri(
                    obj.author.user_information.profile_picture.url
                )
                if obj.author.user_information.profile_picture
                else None
            ),
        }

    @staticmethod
    def validate_tag_id(obj):
        if obj is None or len(obj) == 0:
            raise serializers.ValidationError("This field is required.")
        return obj

    @transaction.atomic
    def create(self, validated_data):
        images = validated_data.pop("images", None)
        tags_ids = validated_data.pop("tag_id", [])
        province = validated_data.pop("province_id")
        city = validated_data.pop("city_id")

        forum = Forum.objects.create(**validated_data, province=province, city=city)
        images_obj = [
            ForumImage(forum=forum, image=image_data) for image_data in images
        ]
        ForumImage.objects.bulk_create(images_obj)

        forum.tags.set(tags_ids)  # Use set() to assign the tags
        return forum

    def update(self, instance, validated_data):
        tags = validated_data.pop("tags", None)
        province = validated_data.pop("province_id", None)
        city = validated_data.pop("city_id", None)
        instance = super().update(instance, validated_data)
        if tags is not None:
            instance.tags.set(tags)  # Use set() to update the tags
        if province is not None:
            instance.province = province
        if city is not None:
            instance.city = city
        return instance
