"""
Devices app models.

Hierarchy:  Category → Device → Node
"""
from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=120, unique=True)

    class Meta:
        verbose_name = "Category"
        verbose_name_plural = "Categories"
        ordering = ["name"]

    def __str__(self) -> str:
        return self.name


class Device(models.Model):
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="devices",
    )
    topic = models.ForeignKey(
        "education.Topic",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="devices",
    )
    name = models.CharField(max_length=200)
    short_desc = models.CharField(max_length=300, blank=True)
    description = models.TextField(blank=True)
    image = models.ImageField(upload_to="devices/", null=True, blank=True)
    model_file = models.FileField(upload_to="devices/models/", null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Device"
        verbose_name_plural = "Devices"
        ordering = ["-created_at"]

    def __str__(self) -> str:
        return self.name


class Node(models.Model):
    device = models.ForeignKey(
        Device,
        on_delete=models.CASCADE,
        related_name="nodes",
    )
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    icon = models.ImageField(upload_to="nodes/icons/", null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Node"
        verbose_name_plural = "Nodes"
        ordering = ["name"]

    def __str__(self) -> str:
        return f"{self.name} ({self.device.name})"
