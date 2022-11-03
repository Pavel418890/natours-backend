from apps.natours.models import TourStartDates


class TourStartDatesCRUD:
    def create_tour_start_dates(self, dates, tour):
        start_dates = [TourStartDates(date, tour) for date in dates]
        return TourStartDates.objects.bulk_create(start_dates)


natours_start_dates = TourStartDatesCRUD()
