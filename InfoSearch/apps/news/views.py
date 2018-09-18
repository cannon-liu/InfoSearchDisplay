import json
from django.shortcuts import render
from django.views.generic.base import View
from elasticsearch_dsl.connections import connections
from apps.news.models import NewsType
from django.http import HttpResponse

# Create your views here.
class SearchSuggest(View):
    def get(self, request):
        key_words = request.GET.get("s", "")
        re_data = []
        if key_words:
            s = NewsType.search()
            s.suggest('my_suggest', key_words, completion={
                "field":"suggest",
                "fuzzy":{
                    "fuzziness": 2
                },
                "size": 10
            })
            suggestions = s.execute_suggest()
            for match in suggestions.my_suggest[0].options:
                source = match._source
                re_data.append(source["title"])

        return HttpResponse(json.dumps(re_data), content_type='application/json')



