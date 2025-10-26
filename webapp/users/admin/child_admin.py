from django.contrib import admin
from unfold.admin import ModelAdmin

from users.models import Child


@admin.register(Child)
class ChildAdmin(ModelAdmin):
  list_display = (
    "parent",
    "name",
    "birth_year",
    "gender",
  )
  list_filter = (
    "gender",
    "created_at",
  )
  search_fields = (
    "parent__email",
    "parent__username",
    "name",
  )
  readonly_fields = (
    "parent",
    "created_at",
    "updated_at",
  )
  ordering = ("-created_at",)

  fields = (
    "parent",
    "name",
    "birth_year",
    "gender",
    "created_at",
    "updated_at",
  )

  actions = ()
