from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .serializers import TickerSearchSerializer
from drf_spectacular.utils import extend_schema, OpenApiParameter
from drf_spectacular.types import OpenApiTypes
from trade_registry.services.utils import save_tickers_to_session_pool
from trade_registry.services.service_utils import search_finnhub, search_alpha, search_yahoo
class TickerSearchAPIView(APIView):
    permission_classes = [IsAuthenticated]
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
            data = search_alpha(query)
        elif service == "yahoo":
            data = search_yahoo(query)
        elif service == "finnhub":
            data = search_finnhub(query)
        else:
            return Response({"error": "Service not supported"}, status=400)

        if data is None:
            return Response({"error": "External API failed"}, status=500)

        serializer = TickerSearchSerializer(data, many=True)
        request.session['has_searched'] = True 
        request.session.modified = True

        save_tickers_to_session_pool(request.session.session_key, serializer.data)
        return Response({"results": serializer.data})

