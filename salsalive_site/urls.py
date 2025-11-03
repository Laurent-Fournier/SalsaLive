from django.contrib import admin
from django.urls import path
from django.conf.urls import handler404

from salsalive_viz import views, views_compta, views_media

handler404 = 'salsalive_viz.views.custom_404'

urlpatterns = [
    path('robots.txt', views.robots_txt, name='robots_txt'),
    path('sitemap.xml', views.sitemap, name='sitemap'),     
    path('admin/', admin.site.urls),

    path('', views.index),
    path('soirees-salsa-live', views.index),
    path('soirees-salsa-moulin-bievre-hay-les-roses', views.index),
    path('soirees-salsa-avara-hay-les-roses-fresnes', views.index),
    path('soirees-salsa-cubaneando-clamart', views.index),
    path('concerts-salsa-au-parc-montsouris-a-paris', views.index),
    path('atelier-orchestre-salsa-la-espina', views.index),
    path('compta', views_compta.index),
    path('compta/all', views_compta.all),
    path('<int:id>/<slug:slug>', views.event),
    
    # Images
    path('images/<int:size>/<str:image_name>', views_media.sized_image),
    path('images/<str:image_name>', views_media.image),
    
    # test erreur 404
    path('test-404/', views.test_404),    
]
