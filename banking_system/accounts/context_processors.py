from .models import  District


def menu_links(request):
    links=District.objects.all()
    print (dict (links=links))
    return dict(links=links)
