from django.shortcuts import render
from django.http import HttpResponse

from django.utils.dateformat import format
from django.utils.translation import gettext as _

import markdown2
import re

from salsalive_viz.models import Events

# ------------
# Error 404
# ------------
def custom_404(request, exception):
    """
    Vue personnalisée pour les erreurs 404
    """
    return render(request, '404.html', status=404)

def test_404(request):
    response = render(request, '404.html')
    response.status_code = 404
    return response



def extract_images(text):
    # ![Soirée Salsa au Moulin de la Bièvre](/images/230/2025-11-21-soiree-salsa-la-espina-moulin-bievre-hay-roses.avif)
    
    # [[image2022-03-26-soiree-salsa-la-espina-avara-fresnes-hay-les-roses.jpg]]
    # [[image2022-03-26-soiree-salsa-la-espina-avara-fresnes-hay-les-roses.jpg|Le flyer de la soirée dansante]]
    # [[salsalive2017-09-15-luna-y-su-banda-moulin-de-la-bievre.jpg|L'orchestre Luna y su Banda]]
    # [[salsalive2017-09-15-david-garlitz-gissel-ortiz.jpg|David Garlitz et Gissel Ortiz]]
    filtred_images=[]

    pattern = r'!\[(.*?)\]\((.*?)\)'
    matches  = re.findall(pattern, text)
    for alt, url in matches:
        url = url.replace('/images/600/', '/images/230/')
        filtred_images.append({ 'alt': alt, 'url': url })

    return filtred_images

def escape_slug(slug):
    slug = slug.lower()
    slug = slug.replace(' ', '-').replace('#', '').replace("'", '-')
    slug = slug.replace('à', 'a')
    slug = slug.replace('é', 'e').replace('ê', 'e').replace('è', 'e')
    slug = slug.replace('ï', 'i')
    slug = slug.replace('û', 'u')
    slug = slug.replace('ÿ', 'y')
    slug = slug.replace('ô', 'o')
    return slug

# ------------
# Home page
# ------------
def index(request):
    current_path = request.get_full_path()
    #return HttpResponse(f"Le chemin actuel est : {current_path}")

    if current_path == '/':  # index page
        sql_where = 'orchestra_id in (10, 18)'
        sql_limit = 'LIMIT 8'
    elif current_path == '/soirees-salsa-live':  # Soirées Live
        sql_where = 'orchestra_id in (10, 18) OR location_id IN (22, 31, 89, 291, 411, 412, 413)'
        sql_limit = ''
    elif current_path == '/atelier-orchestre-salsa-la-espina':  # La Espina
        sql_where = 'orchestra_id = 10'
        sql_limit = ''
    elif current_path == '/soirees-salsa-moulin-bievre-hay-les-roses':  # Soirées au Moulin de la Bièvre
        sql_where = 'location_id = 31'
        sql_limit = ''
    elif current_path == '/soirees-salsa-avara-hay-les-roses-fresnes':  # Soirées à l'Avara    
        sql_where = 'location_id = 89'
        sql_limit = ''
    elif current_path == '/soirees-salsa-cubaneando-clamart':  # Soirées à Clamart
        sql_where = 'location_id in (291, 411, 412, 413)'
        sql_limit = ''
    elif current_path == '/concerts-salsa-au-parc-montsouris-a-paris': # après-midi au parc Montsouris
        sql_where = 'location_id = 22'
        sql_limit = ''
    else:
        #return HttpResponse(f"Le chemin actuel est : {current_path}")
        return HttpResponse(f"Error")  # TODO Page 404

    # request on page
    rows = Events.objects.raw(f"SELECT id, header, title, description, nav FROM page WHERE path='{current_path}'")    
    for row in rows:
       page_title = row.title
       page_description = row.description
       page_nav = row.nav
       page_header = row.header

    # request on events
    events = []
    rows = Events.objects.raw(f"""
        SELECT
            events.id, events.title, events.title1, events.title2, events.text,
            events.startdate, events.starttime, events.enddate, events.endtime, 
            locations.id AS location_id, locations.title AS location_name, locations.postalcode AS location_postalcode, locations.city AS location_city
        FROM events
        LEFT OUTER JOIN locations
            ON locations.id = events.location_id
        WHERE {sql_where}
        ORDER BY startdate DESC
        {sql_limit}
        """)    
    for row in rows:
        events.append({
            'id': row.id,
            'title': row.title,
            'title1': row.title1,
            'title2': row.title2,
            'start': {
                'date': row.startdate,
                'time': row.starttime,
            },
            'end': {
                'date': row.enddate,
                'time': row.endtime,
            },
            'location': {
                'id':row.location_id,
                'name':row.location_name,
                'postalcode': row.location_postalcode,
                'city': row.location_city,
            },
            'images': extract_images(row.text),
            'slug': escape_slug(row.title),
        })
    
    return render(
        request,
        'index.html',
        {
            'page': {
                'title': page_title,
                'description': page_description,
                'active': page_nav,
                'header': page_header,
            },
            'events': events
        }
    )

def event(request, id, slug):
    event = {}
    rows = Events.objects.raw(f"""
        SELECT 
            events.id, events.title, events.title1, events.title2, events.description, events.text, events.link,
            startdate, starttime, enddate, endtime, datePublished AS published_date,
            locations.id AS location_id, locations.title AS location_name, locations.address AS location_address, locations.postalcode AS location_postalcode, locations.city AS location_city, locations.link AS location_link,
            orchestras.id  AS orchestra_id, orchestras.title AS orchestra_name
        FROM events
        LEFT OUTER JOIN locations ON
            events.location_id = locations.id
        LEFT OUTER JOIN orchestras ON
            events.orchestra_id = orchestras.id
        WHERE events.id= {id}
        """)    
    for row in rows:

        # alt devient un texte descriptif de l'image
        pattern = r'!\[(.*?)\]\((.*?)\)'
        matches  = re.findall(pattern, row.text)
        for alt, url in matches:
            link_old = f'![{alt}]({url})'
            link_new = link_old + f'  \n_{alt}_  \n' 
            row.text = row.text.replace(link_old, link_new)

        page_title = row.title
        page_description = row.description
        event = {
            'id': row.id,
            'start': {
                'date': row.startdate,
                'time': row.starttime,
            },
            'end': {
                'date': row.enddate,
                'time': row.endtime,
            },
            'published_date': row.published_date,
            'title': row.title,
            'title1': row.title1,
            'title2': row.title2,
            'description': row.description,
            'slug': escape_slug(row.title),
            'text': markdown2.markdown(row.text),
            'link': row.link,
            'location': {
                'id':row.location_id,
                'name':row.location_name,
                'address': row.location_address,
                'postalcode': row.location_postalcode,
                'city': row.location_city,
                'link': row.location_link,
            },
            'orchestra': {
                'id': row.orchestra_id,
                'name': row.orchestra_name,
            }
        }

    return render(
        request,
        'event.html',
        {
            'page': {
                'title': page_title,
                'description': page_description,
                'active': None,
                'header': None,
            },
            'event': event
        }
    )

# -----------------------
# https://salsalive.net
# -----------------------
def get_host(request):
    scheme = request.scheme  # https://
    host = request.get_host()  # salsalive.net
    return f"{scheme}://{host}"  # https://salsalive.net

    
# ------------
# Robots.txt
# ------------
def robots_txt(request):
    robots_content = f'''
    User-agent: * 
    Allow: /
    
    Sitemap: { get_host(request) }/sitemap.xml
    '''
    return HttpResponse(robots_content, content_type="text/plain")


# ------------
# Sitemap
# ------------
def sitemap(request):
    host = get_host(request)
    xml_data = ''

    # request on articles
    rows = Events.objects.raw("""
        SELECT 
            id, events.title, startdate, is_seo_optimized
        FROM events
        WHERE 
            orchestra_id IN (10,18) OR location_id IN (31, 89, 291, 411, 412, 413)
        """)

    xml_data += '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" xmlns:xhtml="http://www.w3.org/1999/xhtml">\n'

    for row in rows:
        #return HttpResponse( type(slug).__name__ )
    
        xml_data += '<url>\n'
        xml_data += f'  <loc>{host}/{row.id}/{escape_slug(row.title)}</loc>\n'
        xml_data += f'  <lastmod>{row.startdate}</lastmod>\n'
        xml_data += f'  <changefreq>weekly</changefreq>\n'
        #xml_data += f'<priority>{priority}</priority>\n'
        #xml_data += f'  <xhtml:link rel="alternate" hreflang="fr" href="{host}/{row.id}/{slug}" />\n'
        xml_data += '</url>\n'

    xml_data += '</urlset>\n'

    # Retourner la réponse HTTP avec le type MIME correct
    response = HttpResponse(xml_data, content_type="application/xml")
    response['Content-Disposition'] = 'inline; filename="sitemap.xml"'
    return response

