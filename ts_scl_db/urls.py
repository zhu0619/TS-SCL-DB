from django.urls import path
from django.conf.urls import url
from django.views.generic.base import RedirectView
from . import views


app_name = 'ts_scl_db'
favicon_view = RedirectView.as_view(url='/static/images/favicon.ico', permanent=True)

urlpatterns = [
    # path('', views.IndexView.as_view(), name='index'),
    path('', views.index, name='index'),
    # path('', views.IndexView_2.as_view(), name='index_2'),
    path('<int:pk>/detail_2/', views.DetailView_2.as_view(), name='detail_2'),
    path('<int:pk>/', views.DetailView.as_view(), name='detail'),
    path('<int:pk>/results/', views.ResultsView.as_view(), name='results'),
    path('<int:question_id>/vote/', views.vote, name='vote'),
	path('vote_2', views.vote_2, name='vote_2'),
	path('select_protein', views.select_protein, name='select_protein'),
    # path('detail_3', views.detail_3, name='detail_3'),
    path('triplet_details', views.detail_3, name='detail_3'),
	path('show_pmid_list', views.show_pmid_list, name='show_pmid_list'),
	# path('show_pub_tags/<int:pk>/', views.PubtagView.as_view(), name='show_pub_tags'),
    path('show_pub_tags/<int:pk>/', views.show_pub_tags, name='show_pub_tags'),
    # url(r'^scl_icon_bis\.ico$', RedirectView.as_view(url='/static/icon/scl_icon_bis.ico')),
    url(r'^favicon\.ico$', favicon_view),
    path('about',views.about, name='about'),
    path('contact', views.contact, name='contact'),
    path('download', views.download, name='download')
]
