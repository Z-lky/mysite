from django.shortcuts import render
from django.views import View


# Create your views here.
class TrendView(View):
    def get(self, request):
        return render(request, 'trends/trendIndex.html')