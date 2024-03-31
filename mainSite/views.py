from django.shortcuts import render

from vendor.models import Vendor
# for location query
from django.contrib.gis.geos import GEOSGeometry
from django.contrib.gis.measure import D  # ``D`` is a shortcut for ``Distance``
from django.contrib.gis.db.models.functions import Distance

def get_or_set_location(request):
    if 'lat' in request.session:
        lat = request.session['lat']
        lng = request.session['lng']
        return lng, lat
    elif 'lat' in request.GET:
        lat = request.GET.get('lat')
        lng = request.GET.get('lng')
        request.session['lat'] = lat
        request.session['lng'] = lng
    else:
        return None


def HomePageView(request):
    #print(request.GET)
    if get_or_set_location(request) is not None:
        # lat = request.GET.get('lat')
        # lng = request.GET.get('lng')
        # Distances will be calculated from this point, which does not have to be projected.
        pnt = GEOSGeometry("POINT(%s %s)" %(get_or_set_location(request)))
        vendors = Vendor.objects.filter(user_profile__location__distance_lte=(pnt,D(km=100))).\
                                        annotate(distance=Distance("user_profile__location", pnt)).order_by("distance")
        # THis is for to know from where to where 
        # how much is th edistance between the search points 
        for v in vendors:
            v.kms = round(v.distance.km, 1)
    else:
        vendors = Vendor.objects.filter(is_approved=True, user__is_active=True)[:8]
    
    context = {
        "vendors":vendors
    }
    return render(request, 'home.html', context)