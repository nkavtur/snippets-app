# Create your views here.
from django.http import JsonResponse, HttpResponse
from django.shortcuts import get_object_or_404
from rest_framework.status import HTTP_201_CREATED, HTTP_400_BAD_REQUEST, HTTP_200_OK, HTTP_204_NO_CONTENT
from rest_framework.views import APIView

from snippets.models import Snippet
from snippets.serializers import SnippetSerializer


class SnippetList(APIView):
    """
    List all code snippets, or create a new snippet.
    """

    def get(self, request, format=None):
        snippets = Snippet.objects.all()
        serializer = SnippetSerializer(snippets, many=True)
        return JsonResponse(serializer.data, safe=False)

    def post(self, request, format=None):
        serializer = SnippetSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=HTTP_201_CREATED)
        return JsonResponse(serializer.errors, status=HTTP_400_BAD_REQUEST)


class SnippetDetail(APIView):
    """
    Retrieve, update or delete a code snippet.
    """

    def get(request, pk, format=None):
        snippet = get_object_or_404(Snippet, pk=pk)
        serializer = SnippetSerializer(snippet)
        return JsonResponse(serializer.data, safe=False)

    def put(request, pk, format=None):
        snippet = get_object_or_404(Snippet, pk=pk)
        serializer = SnippetSerializer(snippet, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=HTTP_200_OK)

    def post(request, pk, format=None):
        snippet = get_object_or_404(Snippet, pk=pk)
        snippet.delete()
        return HttpResponse(status=HTTP_204_NO_CONTENT)
