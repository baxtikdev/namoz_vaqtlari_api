from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as usrmadmin
from django.contrib.auth.models import Group

from .models import (
    User,
    Region,
    District,
    Masjid,
    Subscription,
    CustomUser,
    CustomMessage
)

admin.site.unregister(Group)


@admin.action(description="Faol qilish")
def make_published(modeladmin, request, queryset):
    queryset.update(is_active=True)


@admin.action(description="Nofaol qilish")
def make_unpublished(modeladmin, request, queryset):
    queryset.update(is_active=False)


# class ChangeMasjidTimeAdminInline(admin.TabularInline):
#     model = ChangeMasjidTimeSchedule
#     extra = 2


# class ChangeRegionTimeAdminInline(admin.TabularInline):
#     model = ChangeRegionTimeSchedule
#     extra = 2


class MasjidInline(admin.StackedInline):
    model = Masjid
    extra = 1


class SubscriptionInline(admin.TabularInline):
    model = Subscription
    extra = 0


class DistrictInline(admin.TabularInline):
    model = District
    extra = 1


class CustomUserAdmin(usrmadmin):
    model = CustomUser
    fieldsets = (
        (
            None,
            {
                "fields": (
                    "username",
                    "password",
                    "region",
                    "district",
                    "masjid",
                    "admin_type",
                )
            },
        ),
        ("Personal info", {"fields": ("first_name", "last_name", "email")}),
        (
            "Permissions",
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                ),
            },
        ),
        ("Important dates", {"fields": ("last_login", "date_joined")}),
    )

    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": (
                    "username",
                    "password1",
                    "password2",
                    "region",
                    "district",
                    "masjid",
                    "admin_type",
                    "is_staff",
                    "groups",
                ),
            },
        ),
    )


@admin.register(Masjid)
class MasjidAdmin(admin.ModelAdmin):
    list_display = ["name_uz", "name_cyrl", "name_ru", "district", "longitude", "latitude", "is_active"]
    search_fields = ["name_uz", "name_cyrl", "name_ru"]
    list_filter = ["district__region", "district"]
    list_select_related = ['"district__region", "district"']


class DistrictAdmin(admin.ModelAdmin):
    list_display = ["name_uz", "name_cyrl", "name_ru", "region", "is_active"]
    search_fields = ["name_uz", "name_cyrl", "name_ru"]
    list_filter = ["region"]

    actions = [make_published, make_unpublished]

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "district":
            # Filter choices based on the assigned region for custom admins
            if not request.user.is_superuser and request.user.admin_type == "region":
                kwargs["queryset"] = Region.objects.filter(region=request.user.region)
        return super().formfield_for_foreignkey(db_field, request, **kwargs)

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        elif request.user.admin_type == "region":
            return qs.filter(region__pk=request.user.region.pk)
        elif request.user.admin_type == "district":
            return qs.filter(region__pk=request.user.district.region.pk)

    inlines = [MasjidInline]


class RegionAdmin(admin.ModelAdmin):
    list_display = ["name_uz", "name_cyrl", "name_ru", "is_active"]
    search_fields = ["name_uz", "name_cyrl", "name_ru"]


class SubscriptionAdmin(admin.ModelAdmin):
    list_display = ["user", "masjid"]
    search_fields = [
        "user__full_name",
        "masjid__name_uz",
        "masjid__name_cyrl",
        "masjid__name_ru",
    ]


class AdminModelAdmin(admin.ModelAdmin):
    list_display = ["full_name", "user_id"]


class CustomMessageAdmin(admin.ModelAdmin):
    search_fields = ["message_uz", "message_cyrl"]


class UserAdmin(admin.ModelAdmin):
    list_display = [
        "full_name",
        "user_id",
    ]
    search_fields = ["full_name", "user_id"]
    list_filter = [
        "lang",
    ]
    inlines = [SubscriptionInline]


class MintaqaAdmin(admin.ModelAdmin):
    list_display = ["name_uz", "name_cyrl", "name_ru", "viloyat", "mintaqa_id"]
    search_fields = ["name_uz", "name_cyrl", "name_ru", "viloyat"]
    list_filter = ["viloyat"]


class ChangeDistrictTimeScheduleAdmin(admin.ModelAdmin):
    search_fields = ["district__name_uz", "district__name_cyrl", "district__name_ru"]
    exclude = ['is_notify']


class NamozVaqtiAdmin(admin.ModelAdmin):
    list_display = [
        "mintaqa",
        "milodiy_oy",
        "milodiy_kun",
        "xijriy_oy",
        "xijriy_kun",
        "vaqtlari",
    ]
    autocomplete_fields = ["mintaqa"]
    search_fields = ["mintaqa__name_uz", "mintaqa__name_cyrl", "mintaqa__name_ru"]
    list_filter = ["mintaqa__viloyat"]


class MasjidJadvallarAdmin(admin.ModelAdmin):
    list_display = ["date", "masjid", "bomdod", "peshin", "asr", "shom", "hufton"]
    search_fields = ["masjid__name_uz", "masjid__name_cyrl", "masjid__name_ru"]
    list_filter = [
        "masjid__district__region",
        "masjid__district",
    ]

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "masjid":
            # Filter choices based on the assigned region for custom admins
            if not request.user.is_superuser and request.user.admin_type == "region":
                kwargs["queryset"] = Masjid.objects.filter(district__region=request.user.region)
            if not request.user.is_superuser and request.user.admin_type == "district":
                kwargs["queryset"] = Masjid.objects.filter(district=request.user.district)
            if not request.user.is_superuser and request.user.admin_type == "masjid":
                kwargs["queryset"] = Masjid.objects.filter(pk=request.user.masjid.pk)
        return super().formfield_for_foreignkey(db_field, request, **kwargs)

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        elif request.user.admin_type == "region":
            return qs.filter(masjid__district__region__pk=request.user.region.pk)
        elif request.user.admin_type == "district":
            return qs.filter(masjid__district__pk=request.user.district.pk)
        elif request.user.admin_type == "masjid":
            return qs.filter(masjid=request.user.masjid)


class DistrictJadvallarAdmin(admin.ModelAdmin):
    list_display = ["date", "district", "bomdod", "peshin", "asr", "shom", "hufton"]
    search_fields = ["district__name_uz", "district__name_cyrl", "district__name_ru"]
    list_filter = [
        "district__region",
        "district",
    ]

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "district":
            # Filter choices based on the assigned region for custom admins
            if not request.user.is_superuser and request.user.admin_type == "region":
                kwargs["queryset"] = District.objects.filter(region=request.user.region)
            if not request.user.is_superuser and request.user.admin_type == "district":
                kwargs["queryset"] = District.objects.filter(pk=request.user.district.pk)
        return super().formfield_for_foreignkey(db_field, request, **kwargs)

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        elif request.user.admin_type == "region":
            return qs.filter(district__region__pk=request.user.region.pk)
        elif request.user.admin_type == "district":
            return qs.filter(district__pk=request.user.district.pk)


class RegionJadvallarAdmin(admin.ModelAdmin):
    list_display = ["date", "region", "bomdod", "peshin", "asr", "shom", "hufton"]
    search_fields = ["region__name_uz", "region__name_cyrl", "region__name_ru"]
    list_filter = [
        "region",
    ]

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "region":
            # Filter choices based on the assigned region for custom admins
            if not request.user.is_superuser and request.user.admin_type == "region":
                kwargs["queryset"] = Region.objects.filter(pk=request.user.region.pk)
        return super().formfield_for_foreignkey(db_field, request, **kwargs)

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        elif request.user.admin_type == "region":
            return qs.filter(region__pk=request.user.region.pk)


admin.site.register(User, UserAdmin)
admin.site.register(CustomMessage, CustomMessageAdmin)
admin.site.register(Region, RegionAdmin)
admin.site.register(District, DistrictAdmin)
admin.site.register(CustomUser, CustomUserAdmin)
