from rest_framework import viewsets

from .serializers import EntrySerializer
from .models import Entry

# Create your views here.
class EntryViewSet(viewsets.ModelViewSet):
    queryset = Entry.objects.all().order_by('name')
    serializer_class = EntrySerializer