from rest_framework import generics, parsers

from apps.common.permissions import IsAdmin, IsLeadGuide, IsGuide
from apps.natours.models.tour import Tour
from apps.natours.models.tour_image import TourImage
from ..serializers.tour_image import TourImageSerializer


class TourImageAPIView(generics.CreateAPIView, generics.RetrieveDestroyAPIView):
    permission_classes = (IsLeadGuide, IsGuide, IsAdmin)
    queryset = TourImage.objects.all()
    serializer_class = TourImageSerializer
    parser_classes = [parsers.MultiPartParser, parsers.FormParser]

    def perform_create(self, serializer):
        tour = generics.get_object_or_404(Tour, pk=self.kwargs['pk'])
        serializer.save(tour=tour)

