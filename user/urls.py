from django.urls import path

from . import views

urlpatterns = [
    # ex: /house/
    path('', views.index, name='index'),
    path('update/', views.user_update, name='user_update'),
    path('password/', views.change_password, name='change_password'),
    path('comments/', views.comments, name='comments'),
    path('delete_comment/<int:id>', views.delete_comment, name='delete_comment'),
    path('addhouse/', views.addhouse, name='addhouse'),
    path('edithouse/<int:id>', views.edithouse, name='edithouse'),
    path('deletehouse/<int:id>', views.deletehouse, name='deletehouse'),
    path('houses/', views.houses, name='houses'),
    path('houseaddimage/<int:id>', views.houseaddimage, name='houseaddimage'),

    # ex: /home/5/
    # path('<int:question_id>/', views.detail, name='detail'),
    # ex: /home/5/results/
    # path('<int:question_id>/results/', views.results, name='results'),
    # ex: /home/5/vote/
    # path('<int:question_id>/vote/', views.vote, name='vote'),
]
