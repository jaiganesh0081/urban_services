from django.db.models import Q
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView

from accounts.permissions import IsProvider,IsCustomer
from urban_services.paginate import paginate_data
from urban_services.utils import standard_message
from .models import Service
from .serializer import ProviderServiceSerializer, CategoryGroupSerializer
from .swagger_schema import providerserviceschema, listserviceschema


# Create your views here.

class ProviderServiceAPIView(APIView):
    permission_classes = [IsAuthenticated, IsProvider]

    @providerserviceschema
    def post(self, request):
        # print(f'requested data is {request.data}')
        serializer_class = ProviderServiceSerializer(data=request.data, context={"request": request})
        serializer_class.is_valid(raise_exception=True)
        serializer_class.save()
        return standard_message(message="Service has successfully saved", data=serializer_class.data,
                                status_code=status.HTTP_201_CREATED)


#
class ServiceListAPIView(APIView):
    permission_classes = [IsAuthenticated, IsCustomer]

    @listserviceschema
    def get(self, request):
        queryset = (
            Service.objects
            .select_related("category", "provider__user").prefetch_related("provider__availability")
            .filter(provider__user__is_active=True)
        )

        # -------- Filtering --------
        filters = {}

        category_id = request.query_params.get("category_id")
        search = request.query_params.get("search")
        min_rating = request.query_params.get("min_rating")
        min_fee = request.query_params.get("min_fee")
        max_fee = request.query_params.get("max_fee")

        if category_id:
            filters["category_id"] = category_id

        if min_fee:
            filters["base_fee__gte"] = min_fee

        if max_fee:
            filters["base_fee__lte"] = max_fee

        if min_rating:
            filters["provider__rating_avg__gte"] = min_rating

        queryset = queryset.filter(**filters)

        if search:
            queryset = queryset.filter(
                Q(title__icontains=search) |
                Q(description__icontains=search)
            )

        # -------- Group WITHOUT defaultdict --------
        grouped = {}  # normal dictionary

        for service in queryset:
            cat_id = service.category.id
            cat_name = service.category.name

            # If this category not created yet → create group
            if cat_id not in grouped:
                grouped[cat_id] = {
                    "category_id": cat_id,
                    "category_name": cat_name,
                    "services": []
                }

            # Add service to category group
            grouped[cat_id]["services"].append(service)
        print(f'before serializer the value is {grouped}')

        grouped_list = list(grouped.values())

        print(f'list of grouped data is {grouped_list}')

        serializer = CategoryGroupSerializer(grouped_list, many=True)

        paginated = paginate_data(request, serializer.data, key_name="services")

        return standard_message(
            message="Available Services",
            data=paginated,
            status_code=status.HTTP_200_OK
        )
