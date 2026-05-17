from django.db import models


class Client(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(blank=True, default='')

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name


class Category(models.Model):
    title = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)

    class Meta:
        ordering = ['title']

    def __str__(self):
        return self.title


class DummyModel(models.Model):
    name = models.CharField(
        max_length=50,
        blank=True,
        null=True
    )
    description = models.CharField(
        max_length=50,
        blank=True,
        null=True
    )
    client = models.ForeignKey(
        Client,
        on_delete=models.CASCADE,
        related_name='items',
        blank=True,
        null=True
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        related_name='items',
        blank=True,
        null=True
    )

    def __str__(self):
        return str(self.name)
