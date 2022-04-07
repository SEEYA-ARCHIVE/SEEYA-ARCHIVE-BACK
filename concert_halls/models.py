from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator


class ConcertHall(models.Model):
    name = models.CharField(max_length=512)
    address = models.CharField(max_length=1024)
    lat = models.FloatField()
    lng = models.FloatField()

    def __str__(self):
        return self.name


class Floor(models.Model):
    concert_hall = models.ForeignKey("concert_halls.ConcertHall", related_name='floors', on_delete=models.CASCADE)
    floor = models.PositiveSmallIntegerField(validators=[MinValueValidator(1), MaxValueValidator(10)])

    def __str__(self):
        return self.floor


class Seat(models.Model):
    floor = models.ForeignKey("concert_halls.Floor", related_name="seats", on_delete=models.CASCADE)
    area = models.CharField(max_length=128)
    seat_row = models.CharField(max_length=128, blank=True, null=True)
    seat_num = models.CharField(max_length=128, blank=True, null=True)

    def __str__(self):
        return self.area + "구역 " + self.seat_row + "열 " + self.seat_num + "번"