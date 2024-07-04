from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Trader, Company, Buy, Sell
from .serializers import TraderSerializer, CompanySerializer, BuySerializer, SellSerializer


@api_view(['GET'])
def all_data(request):
    traders = Trader.objects.order_by('-total_value')
    companies = Company.objects.all()
    buys = Buy.objects.all()
    sells = Sell.objects.all()

    traders_serializer = TraderSerializer(traders, many=True).data
    companies_serializer = CompanySerializer(companies, many=True).data
    buys_serializer = BuySerializer(buys, many=True).data
    sells_serializer = SellSerializer(sells, many=True).data

    data = {
        'traders': traders_serializer,
        'companies': companies_serializer,
        'buys': buys_serializer,
        'sells': sells_serializer,
    }

    return Response(data)
