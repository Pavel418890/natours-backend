from rest_framework.generics import get_object_or_404


class MultipleFieldLookupMixin:
    """
    Позволяет во View использовать несколько полей для поиска модели в БД
    """
    def get_object(self):
        queryset = self.get_queryset()
        queryset = self.filter_queryset(queryset)
        _lookup_fields = {
            field: self.kwargs[field]
            for field in self.lookup_fields
            if self.kwargs.get(field, None)
        }
        obj = get_object_or_404(queryset, **_lookup_fields)
        self.check_object_permissions(self.request, obj)
        return obj
