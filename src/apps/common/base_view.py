# from django.db import transaction
# from django.http.response import JsonResponse
# from rest_framework.views import APIView
#
# JSON_DUMPS_PARAMS = {
#     'ensure_ascii': False
# }
#
# class BaseView(APIView):
#     def dispatch(self, request, *args, **kwargs):
#         try:
#             with transaction.atomic:
#                 response = super().dispatch(request, *args, **kwargs)
#         except Exception as e:
#             return self._response
#
#     @staticmethod
#     def _response(request, *args, **kwargs):
#         return JsonResponse(
#             data=request.data
#         )