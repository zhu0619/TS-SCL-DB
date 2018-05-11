# from django.urls import path
from django.conf.urls import url
from django.views.generic.base import RedirectView

from django.conf import settings
from django.conf.urls import include
from django.contrib import admin

# from welcome.views import health
from welcome.views import index as welcome_index

from ts_scl_db.views import index,select_protein,detail_3,show_pmid_list,show_pub_tags,about,contact, download
# app_name = 'ts_scl_db'
favicon_view = RedirectView.as_view(url='/static/images/favicon.ico', permanent=True)

urlpatterns = [
    # url(r'^$', welcome_index),
    # url(r'^health$', health),
    # url(r'^admin/', include(admin.site.urls)),
    
    # path('', views.IndexView.as_view(), name='index'),
    # url(r'^$', index, name='index'),
    # url(r'',index, name='index'),
    url(r'', ts_scl_db.views.index),
    # path('', views.IndexView_2.as_view(), name='index_2'),
 #    path('<int:pk>/detail_2/', views.DetailView_2.as_view(), name='detail_2'),
 #    path('<int:pk>/', views.DetailView.as_view(), name='detail'),
 #    path('<int:pk>/results/', views.ResultsView.as_view(), name='results'),
 #    path('<int:question_id>/vote/', views.vote, name='vote'),
	# path('vote_2', views.vote_2, name='vote_2'),
	url(r'^select_protein', select_protein, name='select_protein'),
    # path('detail_3', views.detail_3, name='detail_3'),
    url(r'^triplet_details', detail_3, name='detail_3'),
	url(r'^show_pmid_list', show_pmid_list, name='show_pmid_list'),
	# path('show_pub_tags/<int:pk>/', views.PubtagView.as_view(), name='show_pub_tags'),
    url(r'^show_pub_tags/<int:pk>/', show_pub_tags, name='show_pub_tags'),
    # url(r'^scl_icon_bis\.ico$', RedirectView.as_view(url='/static/icon/scl_icon_bis.ico')),
    # url(r'^favicon\.ico$', favicon_view),
    url(r'^about', about, name='about'),
    url(r'^contact', contact, name='contact'),
    url(r'^download', download, name='download'),
    # url(r'^admin/', include(admin.site.urls)),
]


if settings.DEBUG:
    import debug_toolbar
    urlpatterns = [
        url(r'^__debug__/', include(debug_toolbar.urls)),
    ] + urlpatterns
