from django.db import models
from django.utils.text import slugify


class BaseStatusModel(models.Model):
    STATUS_CHOICES = [
        ("pending", "Pending"),
        ("approved", "Approved"),
        ("rejected", "Rejected"),
        ("expired", "Expired"),
    ]
    status = models.CharField(max_length=255, choices=STATUS_CHOICES, default="pending")

    class Meta:
        abstract = True


class BaseVisibilityModel(models.Model):
    VISIBILITY_CHOICES = [
        ("public", "Public"),
        ("private", "Private"),
    ]
    visibility = models.CharField(
        max_length=255, choices=VISIBILITY_CHOICES, default="public"
    )

    class Meta:
        abstract = True


class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class HasSlugModel(models.Model):
    slug = models.SlugField(max_length=255, unique=True, blank=True)

    class Meta:
        abstract = True

    def slug_key(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.slug_key())[
                :250
            ]  # Limit base slug to 250 for appending numbers
            unique_slug = base_slug
            counter = 1

            while (
                self.__class__.objects.filter(slug=unique_slug)
                .exclude(pk=self.pk)
                .exists()
            ):
                unique_slug = f"{base_slug}-{counter}"
                counter += 1

            self.slug = unique_slug

        super().save(*args, **kwargs)
