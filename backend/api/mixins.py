from django.db.models import Q
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework.serializers import ModelSerializer
from rest_framework.status import (
    HTTP_201_CREATED, HTTP_204_NO_CONTENT,
    HTTP_400_BAD_REQUEST
)
from django.conf import settings


class AddedDeleteViewMixin:

    additional_serializer: ModelSerializer

    def _add_del_obj(self, obj_id, m2m_model, query):
        obj = get_object_or_404(self.queryset, id=obj_id)
        serializer = self.additional_serializer(obj)
        m2m_obj = m2m_model.objects.filter(query & Q(user=self.request.user))

        if (self.request.method in settings.GET_POST_METHODS) and not m2m_obj:
            m2m_model(None, obj.id, self.request.user.id).save()
            return Response(serializer.data, status=HTTP_201_CREATED)

        if (self.request.method in settings.DEL_METHODS) and m2m_obj:
            m2m_obj[0].delete()
            return Response(status=HTTP_204_NO_CONTENT)

        return Response(status=HTTP_400_BAD_REQUEST)
