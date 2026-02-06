import os
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import TickerSearchSerializer
from drf_spectacular.utils import extend_schema, OpenApiParameter
import requests

class TickerSearchAPIView(APIView):
    """
    Endpoint to search for assets in real time.
    
    Connects to Alpha Vantage API and gets matches
    based on the ticker or the name.
    """
    @extend_schema(
        parameters=[
            OpenApiParameter(
                name='q', 
                description='Search text (ticker or asset name)', 
                required=True, 
                type=str
            ),
        ],
        responses=TickerSearchSerializer(many=True),
    )
    def get(self, request):
        """
        Search for and return a list of financial assets (tickers).

        Uses the 'q' query parameter to perform a search against an external API 
        and returns the normalized results.

        :param request: The HTTP request object.
        :return: A JSON response containing the list of search matches.
        :rtype: rest_framework.response.Response
        """
        query = request.query_params.get('q', '')
        if not query:
            return Response({"results": []})
        api_key = os.environ.get('ALPHA_VANTAGE_API_KEY')
        url = f'https://www.alphavantage.co/query?function=SYMBOL_SEARCH&keywords={query}&apikey={api_key}'
        r = requests.get(url)
        data = r.json()
        matches = data.get('bestMatches', [])
        #Normalize keys before serializing.---
        clean_matches = []
        for item in matches:
            clean_matches.append({
                'symbol': item.get('1. symbol'),
                'name': item.get('2. name'),
                'market': item.get('4. region')
            })
        serializer = TickerSearchSerializer(clean_matches, many=True)
        return Response({"results": serializer.data})