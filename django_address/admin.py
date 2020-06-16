from django.contrib import admin

from django_address.models import Address, Country, District, Locality, Region, Street


@admin.register(Country)
class CountryAdmin(admin.ModelAdmin):
    search_fields = ("name", "code")


@admin.register(Region)
class RegionAdmin(admin.ModelAdmin):
    search_fields = ("name", "code")


@admin.register(District)
class DistrictAdmin(admin.ModelAdmin):
    search_fields = ("name", "code")


@admin.register(Locality)
class LocalityAdmin(admin.ModelAdmin):
    search_fields = ("name", "postal_code")
    prepopulated_fields = {"slug": ("name",)}


@admin.register(Street)
class StreetAdmin(admin.ModelAdmin):
    list_display = ("name", "locality")
    search_fields = ("name",)


@admin.register(Address)
class AddressAdmin(admin.ModelAdmin):
    search_fields = ("route", "formatted_address")
    list_filter = ["locality"]
