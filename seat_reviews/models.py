from django.db import models
from django.contrib.postgres.fields import ArrayField
from sorl.thumbnail import get_thumbnail
from django.utils.html import format_html


def get_seat_image_path(self, filename):
    return '{}'.format(filename)


class Post(models.Model):
    # user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    concert_hall = models.ForeignKey("concert_halls.ConcertHall", on_delete=models.SET_NULL, null=True)
    images = ArrayField(models.ImageField(upload_to=get_seat_image_path))
    review = models.TextField(blank=True, null=True)
    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)


class AdminPost(models.Model):
    concert_hall = models.CharField(max_length=128, blank=True, null=True, default="올림픽홀")
    source_url = models.URLField()
    image1 = models.ImageField(upload_to=get_seat_image_path, blank=True, null=True)
    image2 = models.ImageField(upload_to=get_seat_image_path, blank=True, null=True)
    image3 = models.ImageField(upload_to=get_seat_image_path, blank=True, null=True)
    image4 = models.ImageField(upload_to=get_seat_image_path, blank=True, null=True)
    image5 = models.ImageField(upload_to=get_seat_image_path, blank=True, null=True)
    text = models.TextField(blank=True, null=True)
    floor = models.CharField(max_length=128, blank=True, null=True)
    area = models.CharField(max_length=128, blank=True, null=True)
    seat_row = models.CharField(max_length=128, blank=True, null=True)
    seat_num = models.CharField(max_length=128, blank=True, null=True)
    date = models.CharField(max_length=128, blank=True, null=True)

    def __str__(self):
        return self.source_url

    @property
    def image_previews(self):
        _img_tag = ''
        if self.image1:
            _image1 = get_thumbnail(self.image1, '100x100', quality=100)
            _img_tag += '<img src="{}" width="{}" height="{}">'.format(_image1.url, _image1.width, _image1.height)
        if self.image2:
            _image2 = get_thumbnail(self.image2, '100x100', quality=100)
            _img_tag += '<img src="{}" width="{}" height="{}">'.format(_image2.url, _image2.width, _image2.height)
        if self.image3:
            _image3 = get_thumbnail(self.image3, '100x100', quality=100)
            _img_tag += '<img src="{}" width="{}" height="{}">'.format(_image3.url, _image3.width, _image3.height)
        if self.image4:
            _image4 = get_thumbnail(self.image4, '100x100', quality=100)
            _img_tag += '<img src="{}" width="{}" height="{}">'.format(_image4.url, _image4.width, _image4.height)
        if self.image5:
            _image5 = get_thumbnail(self.image5, '100x100', quality=100)
            _img_tag += '<img src="{}" width="{}" height="{}">'.format(_image5.url, _image5.width, _image5.height)
        return format_html(_img_tag)

    @property
    def href_url(self):
        return format_html('<a href={}>twitter link</a>'.format(self.source_url))

    def save(self, *args, **kwargs):
        if self.id is None:
            temp_image = self.image1
            self.image1 = None
            super().save(*args, **kwargs)
            self.image1 = temp_image
        super().save(*args, **kwargs)