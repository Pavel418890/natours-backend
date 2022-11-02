from django.contrib.postgres.fields import ArrayField
from django.db import models
from django.db.models import F, Window, Avg, Max, Min, Count
from django.db.models.functions import Round


class Report(models.Manager):
    def get_top5_cheapest_tours(self):
        return GetTop5CheapTours.objects.all().values()

    def get_group_statistics_by_difficulty(self):
        return self.model.objects.prefetch_related(
            'reviews'
        ).values(
            'difficulty'
        ).annotate(
            avg_price=Round(Avg('price'), 2),
            max_price=Max('price'),
            min_price=Min('price'),
            num_reviews=Count('reviews__id'),
            avg_rating=Round(Avg('reviews__rating'), 2)
        )

    def get_year_report(self, year_report_model):
        return ReportRunner(year_report_model).run()


class GetTop5CheapTours(models.Model):
    """
    Возвращает топ-5 туров по среднему показателю рейтинга и минимально цене
    """
    name = models.CharField(max_length=200)
    difficulty = models.CharField(max_length=20)
    price = models.DecimalField(max_digits=7, decimal_places=2)
    summary = models.CharField(max_length=255, null=True)
    avg_rating = models.DecimalField(max_digits=2, decimal_places=1)

    def save(self, *args, **kwargs):
        raise NotImplemented(
            'This model is tied to a view, it cannot be saved.')

    class Meta:
        db_table = 'top_5_cheap_tours'
        managed = False


class YearReport(models.Model):
    month = models.CharField(
        verbose_name='Month name',
        max_length=9,
        primary_key=True
    )
    num_tours_starts = models.PositiveSmallIntegerField(
        verbose_name='Tours quantity per months',
    )
    tours = ArrayField(
        models.TextField(),
        verbose_name='Tour names with particular month'
    )

    class Meta:
        managed = False
        abstract = True


class R2021(YearReport):
    class Meta:
        managed = False
        db_table = 'report_2021'


class R2022(YearReport):
    class Meta:
        managed = False
        db_table = 'report_2022'


class ReportRunner:
    def __init__(self, report: YearReport):
        self._report = report

    def run(self):
        return self._report.objects.all().values()