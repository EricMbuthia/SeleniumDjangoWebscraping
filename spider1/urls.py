from django.urls import path, include
from . import views
app_name = "spider1"
urlpatterns = [
path('', views.home, name='home'),
path('home', views.home,name = "home"),
path("create_db_notice/", views.create_db_notice, name="create_db_notice"),
path("inv_rec/", views.inv_rec, name="inv_rec"),
path("inv_rec_detail/<int:pk>", views.inv_rec_detail, name="inv_rec_detail"),
path("undone_recs_detail/<int:ll>/", views.undone_recs_detail, name = "undone_recs_detail"),
path ("inv_rec_update/", views.inv_rec_update, name = "inv_rec_update"),
path ("write_notices_to_file/", views.write_notices_to_file, name = "write_notices_to_file"),
path ("handle_undone_notices/<int:ref_id>", views.handle_undone_notices, name = "handle_undone_notices"),


]




