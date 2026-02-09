import os
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import TickerSearchSerializer
from drf_spectacular.utils import extend_schema, OpenApiParameter
from drf_spectacular.types import OpenApiTypes
from .utils import save_tickers_to_session_pool
import requests
import finnhub
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
            OpenApiParameter(
                name='service', 
                location=OpenApiParameter.PATH, # <--- Indispensable
                description='API provider to use for the search',
                required=True,
                type=OpenApiTypes.STR,
                enum=['alpha', 'yahoo', 'finnhub'] # Limita las opciones en la UI
            ),
        ],
        responses=TickerSearchSerializer(many=True),
    )
    def get(self, request, service):
        """
        Search for and return a list of financial assets (tickers).

        Uses the 'q' query parameter to perform a search against an external API 
        and returns the normalized results.

        :param request: The HTTP request object.
        :param service: The API service to use.
        :return: A JSON response containing the list of search matches.
        :rtype: rest_framework.response.Response
        """
        query = request.query_params.get('q', '')
        if not query:
            return Response({"results": []})
        
        if service == "alpha":
            data = self._search_alpha(query)
        elif service == "yahoo":
            data = self._search_yahoo(query)
        elif service == "finnhub":
            data = self._search_finnhub(query)
        else:
            return Response({"error": "Service not supported"}, status=400)

        if data is None:
            return Response({"error": "External API failed"}, status=500)

        serializer = TickerSearchSerializer(data, many=True)
        request.session['has_searched'] = True 
        request.session.modified = True

        save_tickers_to_session_pool(request.session.session_key, serializer.data)
        return Response({"results": serializer.data})
    def _search_alpha(self, query):
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
        return clean_matches
    def _search_yahoo(self, query):
        headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko)'
        }
        url = f"https://query1.finance.yahoo.com/v1/finance/search?q={query}"
        r = requests.get(url, headers=headers, timeout=5)
        data = r.json()        
        matches = data.get('quotes', [])
                
        clean_matches = []
        for item in matches:
            clean_matches.append({
                'symbol': item.get('symbol'),
                'name': item.get('shortname') or item.get('longname')
            })
        return clean_matches
    def _search_finnhub(self,query):
        api_key_var = os.environ.get('FINNHUB_API_KEY')
        finnhub_client = finnhub.Client(api_key=api_key_var)
        data = finnhub_client.symbol_lookup(query)
        matches = data.get('result', [])
        #Normalize keys before serializing.---
        clean_matches = []
        for item in matches:
            clean_matches.append({
                'symbol': item.get('symbol'),
                'name': item.get('description'),
            })
        return clean_matches
    
