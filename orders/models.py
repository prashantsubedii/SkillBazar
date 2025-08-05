from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from users.models import CustomUser
from gigs.models import Gig


class Review(models.Model):
    """Review model for gig orders"""
    gig = models.ForeignKey(Gig, on_delete=models.CASCADE, related_name='reviews')
    reviewer = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='reviews_given')
    freelancer = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='reviews_received')
    rating = models.PositiveIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)],
        help_text='Rating from 1 to 5'
    )
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        unique_together = ['gig', 'reviewer']
        ordering = ['-created_at']
    
    def __str__(self):
        return f"Review by {self.reviewer.username} for {self.gig.title}"
    
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        # Update gig rating
        self.gig.update_rating()
        # Update freelancer rating
        self.freelancer.rating = Review.objects.filter(
            freelancer=self.freelancer
        ).aggregate(avg=models.Avg('rating'))['avg'] or 0
        self.freelancer.total_reviews = Review.objects.filter(
            freelancer=self.freelancer
        ).count()
        self.freelancer.save(update_fields=['rating', 'total_reviews']) 