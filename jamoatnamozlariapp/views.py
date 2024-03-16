import logging
from django.shortcuts import get_object_or_404, render
from django.contrib.auth.decorators import user_passes_test
from .models import District, Masjid, Region, Subscription
from django.db.models import Count

def is_admin(user):
    return user.is_authenticated and user.is_staff


# Create your views here.

@user_passes_test(is_admin)
def region_statistics(request):
    regions = Region.objects.all()

    # Calculate unique subscriber count for each region
    region_stats = []
    for region in regions:
        subscriber_count = Subscription.objects.filter(masjid__district__region=region).values('user').distinct().count()
        region_stats.append(
            {"name": region.name_uz, "subscriber_count": subscriber_count}
        )

    # Sort region_stats based on subscriber_count (ascending by default)
    sort_order = request.GET.get("sort", "desc")
    region_stats = sorted(
        region_stats,
        key=lambda x: x["subscriber_count"],
        reverse=(sort_order == "desc"),
    )

    context = {"region_stats": region_stats}
    return render(request, "jamoatnamozlariapp/region_statistics.html", context)

@user_passes_test(is_admin)
def district_statistics(request):
    districts = District.objects.all()

    # Calculate unique subscriber count for each district
    district_stats = []
    for district in districts:
        subscriber_count = Subscription.objects.filter(masjid__district=district).values('user').distinct().count()
        district_stats.append(
            {"name": district.name_uz, "subscriber_count": subscriber_count}
        )

    # Sort district_stats based on subscriber_count (ascending by default)
    sort_order = request.GET.get("sort", "desc")
    district_stats = sorted(
        district_stats,
        key=lambda x: x["subscriber_count"],
        reverse=(sort_order == "desc"),
    )

    context = {"district_stats": district_stats}
    return render(request, "jamoatnamozlariapp/district_statistics.html", context)



@user_passes_test(is_admin)
def masjid_statistics(request):
    sort_order = request.GET.get("sort", "desc")

    order_field = (
        "-subscription_count" if sort_order == "desc" else "subscription_count"
    )
    masjid_stats = Masjid.objects.annotate(
        subscription_count=Count("subscription")
    ).order_by(order_field)

    return render(
        request,
        "jamoatnamozlariapp/masjid_statistics.html",
        {"masjid_stats": masjid_stats, "sort_order": sort_order},
    )


# views.py
# @user_passes_test(is_admin)
# def your_custom_view2(request):
#     return render(request, "jamoatnamozlariapp/statistic_menu.html")

@user_passes_test(is_admin)
def region_list_view(request):
    regions = Region.objects.all()
    return render(request, 'jamoatnamozlariapp/region_list.html', {'regions': regions})

@user_passes_test(is_admin)
def region_detail_view(request, pk):
    region = get_object_or_404(Region, pk=pk)
    districts_with_masjids = region.district_set.annotate(masjid_count=Count('masjid')).filter(masjid_count__gt=0)
    # Calculate the total number of masjids in the region
    masjid_count = sum(district.masjid_set.count() for district in districts_with_masjids)

    context = {
        'region': region,
        'districts': districts_with_masjids,
        'masjid_count': masjid_count,
    }

    return render(request, 'jamoatnamozlariapp/region_detail.html', context)

@user_passes_test(is_admin)
def masjids_in_district_statistics(request, district_id):
    sort_order = request.GET.get("sort", "desc")

    order_field = "-subscriber_count" if sort_order == "desc" else "subscriber_count"
    masjid_stats = Masjid.objects.filter(district_id=district_id).annotate(
        subscriber_count=Count('subscription')
    ).order_by(order_field)

    return render(
        request,
        "jamoatnamozlariapp/masjids_in_district_statistics.html",
        {"masjid_stats": masjid_stats, "sort_order": sort_order},
    )

@user_passes_test(is_admin)
def masjids_in_region_statistics(request, region_id):
    sort_order = request.GET.get("sort", "desc")

    order_field = "-subscriber_count" if sort_order == "desc" else "subscriber_count"
    masjid_stats = Masjid.objects.filter(district__region_id=region_id).annotate(
        subscriber_count=Count('subscription')
    ).order_by(order_field)

    return render(
        request,
        "jamoatnamozlariapp/masjids_in_region_statistics.html",
        {"masjid_stats": masjid_stats, "sort_order": sort_order},
    )


@user_passes_test(is_admin)
def districts_in_region_statistics(request, region_id):
    sort_order = request.GET.get("sort", "desc")

    order_field = "-subscriber_count" if sort_order == "desc" else "subscriber_count"
    district_stats = District.objects.filter(region_id=region_id).annotate(
        subscriber_count=Count('masjid__subscription__user', distinct=True)
    ).order_by(order_field)

    return render(
        request,
        "jamoatnamozlariapp/districts_in_region_statistics.html",
        {"district_stats": district_stats, "sort_order": sort_order},
    )