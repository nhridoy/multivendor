from rest_framework import generics, permissions, response, views, viewsets

from options.models import City, Country, Language, Province
from options.serializers import (
    CityCreateSerializer,
    CitySerializer,
    CountryCreateSerializer,
    CountrySerializer,
    LanguageCreateSerializer,
    LanguageSerializer,
    ProvinceCreateSerializer,
    ProvinceSerializer,
)
from utils.extensions.permissions import IsAdmin


class OptionsListView(views.APIView):
    """
    API endpoint to retrieve a list of interests, optionally filtered by language.
    """

    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request, *args, **kwargs):

        country_queryset = Country.objects.all()
        countries = CountrySerializer(country_queryset, many=True)

        province_queryset = Province.objects.all().prefetch_related("cities")
        provinces = ProvinceSerializer(province_queryset, many=True)

        language_queryset = Language.objects.all()
        languages = LanguageSerializer(language_queryset, many=True)

        return response.Response(
            {
                "countries": countries.data,
                "provinces": provinces.data,
                "languages": languages.data,
            }
        )



class LanguageView(viewsets.ModelViewSet):
    permission_classes = (IsAdmin,)
    queryset = Language.objects.all()
    serializer_class = LanguageCreateSerializer



class ProvinceView(viewsets.ModelViewSet):
    permission_classes = (IsAdmin,)
    queryset = Province.objects.all()
    serializer_class = ProvinceCreateSerializer


class CityView(viewsets.ModelViewSet):
    permission_classes = (IsAdmin,)
    queryset = City.objects.all().select_related("province")
    serializer_class = CityCreateSerializer


class CountryView(viewsets.ModelViewSet):
    permission_classes = (IsAdmin,)
    queryset = Country.objects.all()
    serializer_class = CountryCreateSerializer
