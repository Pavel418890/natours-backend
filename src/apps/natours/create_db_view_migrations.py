from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("natours", "0001_initial"),
    ]

    operations = [
        migrations.RunSQL(
            """
            DROP VIEW IF EXISTS top_5_cheap_tours;
            CREATE OR REPLACE VIEW top_5_cheap_tours AS
            SELECT tours.id,
                   name,
                   price,
                   summary,
                   difficulty,
                   ROUND(AVG(tr.rating), 2) AS avg_rating
            FROM tours
                     JOIN tour_reviews tr ON tours.id = tr.tour_id
            GROUP BY tours.id, tours.name, price, summary, difficulty
            ORDER BY avg_rating DESC, price DESC
            LIMIT 5;
            """
        ),
        migrations.RunSQL(
            """
            DROP VIEW IF EXISTS report_2021;
            CREATE MATERIALIZED VIEW report_2021 AS
            (
            WITH tours_to_months(name, month) AS (
            SELECT name, to_char(sd.start_date, 'Month')
            FROM tours
            JOIN start_dates sd ON tours.id = sd.tour_id
            WHERE sd.start_date BETWEEN '2021-01-01 0:0' AND '2021-12-31 0:0'
            )
            SELECT tours_to_months.month,
                   COUNT(tours_to_months.month)    AS num_tours_starts,
                   ARRAY_AGG(tours_to_months.name) AS tours
            FROM tours_to_months
            GROUP BY month
            ORDER BY num_tours_starts DESC
            LIMIT 12
            );        
            """
        ),
        migrations.RunSQL(
            """
            DROP VIEW IF EXISTS report_2022;
            CREATE MATERIALIZED VIEW report_2022 AS (
            WITH tours_to_months(name, month) AS (
            SELECT name, to_char(sd.start_date, 'Month')
            FROM tours
            JOIN start_dates sd ON tours.id = sd.tour_id
            WHERE sd.start_date BETWEEN '2022-01-01 0:0' AND '2022-12-31 0:0'
            )
            SELECT tours_to_months.month,
                   COUNT(tours_to_months.month)    AS num_tours_starts,
                   ARRAY_AGG(tours_to_months.name) AS tours
            FROM tours_to_months
            GROUP BY month
            ORDER BY num_tours_starts DESC
            LIMIT 12
            );        
            """
        ),
        migrations.RunSQL(
            """
            CREATE MATERIALIZED VIEW tour_info AS (
                WITH tour 
            )
            """
        ),
    ]
