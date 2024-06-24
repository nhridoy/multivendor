from rest_framework.viewsets import ModelViewSet

from notice.models import Notice, NoticeType
from notice.serializers import NoticeSerializer, NoticeTypeSerializer


class NoticeTypeView(ModelViewSet):
    queryset = NoticeType.objects.all()
    serializer_class = NoticeTypeSerializer


class NoticeView(ModelViewSet):
    queryset = Notice.objects.select_related("type", "author")
    serializer_class = NoticeSerializer
