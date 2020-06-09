from .serializers import EntrySerializer, UserSerializer
from .models import Entry, User
from .helpers import post_entry
from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

# Create your views here.


class EntryDetail(APIView):
    """
    Retrieve, update or delete a entry instance.
    """

    def get_object(self, pk):
        try:
            return Entry.objects.get(pk=pk)
        except Entry.DoesNotExist:
            raise Http404

    def post(self, request, format=None):
        processed_entry = post_entry(request.data.dict())
        serializer = EntrySerializer(data=processed_entry)
        if serializer.is_valid():
            serializer.save()
            parent_user = User.objects.get(pk=serializer.data['user'])

            if serializer.data['completed'] == True:
                updated_user = parent_user.leveling_up(serializer.data['xp'])
                serializer = UserSerializer(parent_user, data=updated_user)
                if serializer.is_valid():
                    serializer.save()
                    return Response(serializer.data, status=status.HTTP_201_CREATED)
            else:
                serializer = UserSerializer(parent_user)
                return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, pk, format=None):
        entry = self.get_object(pk)
        completion = entry.completed
        processed_data = entry.update_self(request.data.dict())
        entry_serializer = EntrySerializer(entry, data=processed_data)
        if entry_serializer.is_valid():
            entry_serializer.save()
            parent_user = User.objects.get(pk=entry_serializer.data['user'])

            if (entry_serializer.data['completed'] == True) and (completion == False):
                updated_user = parent_user.leveling_up(entry_serializer.data['xp'])
                user_serializer = UserSerializer(parent_user, data=updated_user)
                if user_serializer.is_valid():
                    user_serializer.save()
                    return Response(user_serializer.data, status=status.HTTP_200_OK)

            elif (entry_serializer.data['completed'] == False) and (completion == True):
                updated_user = parent_user.leveling_down(entry_serializer.data['xp'])
                user_serializer = UserSerializer(parent_user, data=updated_user)
                if user_serializer.is_valid():
                    user_serializer.save()
                    return Response(user_serializer.data, status=status.HTTP_200_OK)

            else:
                user_serializer = UserSerializer(parent_user)
                return Response(user_serializer.data, status=status.HTTP_200_OK)

        return Response(entry_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        entry = self.get_object(pk)
        entry.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class UserDetail(APIView):

    def get_object(self, pk):
        try:
            return User.objects.get(pk=pk)
        except User.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        user = self.get_object(pk)
        serializer = UserSerializer(user)
        return Response(serializer.data)

    def patch(self, request, pk, format=None):
        user = self.get_object(pk)
        updated_user = user.leveling_up(int(request.data['xp']))
        serializer = UserSerializer(user, data=updated_user)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        user = self.get_object(pk)
        user.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
