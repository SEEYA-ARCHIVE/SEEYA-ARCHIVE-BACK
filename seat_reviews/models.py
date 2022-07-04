from django.db import models


class Review(models.Model):
    user = models.ForeignKey('accounts.User',
                             related_name='user_reviews',
                             on_delete=models.SET_NULL, null=True)
    seat_area = models.ForeignKey('concert_halls.SeatArea',
                                  related_name='seat_area_reviews',
                                  on_delete=models.SET_NULL, null=True)
    artist = models.CharField(max_length=128, blank=True, null=True)
    seat_row = models.CharField(max_length=128, blank=True, null=True)
    seat_num = models.CharField(max_length=128, blank=True, null=True)
    reviews = models.TextField(blank=True, null=True)
    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)
    like_users = models.ManyToManyField('accounts.User',
                                        related_name='like_reviews',
                                        blank=True, null=True)

    def __str__(self):
        return 'review_{}'.format(self.id)


class ReviewImage(models.Model):
    review = models.ForeignKey('seat_reviews.Review',
                               related_name='images',
                               on_delete=models.CASCADE)
    image = models.ImageField()

    def __str__(self):
        return 'review_{} image{}'.format(self.review.pk, self.id)


class Comment(models.Model):
    user = models.ForeignKey('accounts.User',
                             related_name='users',
                             on_delete=models.CASCADE)
    review = models.ForeignKey('seat_reviews.Review',
                               related_name='comments',
                               on_delete=models.CASCADE)
    comment = models.CharField(max_length=1024)
    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return 'id:{} comment:{}..'.format(self.id, self.comment[:15])