from ..models import TourStartDates

from apps.common.utils import Singleton


class TourStartDatesCrud(metaclass=Singleton):
    start_date_manager = TourStartDates.objects

    def create_tour_start_dates(self, dates, tour):
        start_dates = [TourStartDates(date, tour) for date in dates]
        self.start_date_manager.bulk_create(start_dates)