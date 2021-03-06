"""
Required by django
"""
from django.urls import path
from .views import (
    home_view,
    # all_character_view,
    # character_view,
    dice_view,
    best_dice_view,
)

app_name = 'dice'
urlpatterns = [
    path('', home_view, name='home'),
    # path('characters', all_character_view, name='characters'),
    # path('<int:idenitifer>/', character_view, name='character'),
    path('dice', dice_view, name='dice'),
    path('best_dice', best_dice_view, name='best_dice',)

]
# from .views import (product_create_view,
#                     product_detail_view,
#                     product_delete_view,
#                     product_list_view,
#                     product_update_view)

# app_name = 'products'
# urlpatterns = [
#     path('', product_list_view, name='product-list'),
#     path('create/', product_create_view, name='product-list'),
#     path('<int:id>/', product_detail_view, name='product-detail'),
#     path('<int:id>/update/', product_update_view, name='product-update'),
#     path('<int:id>/delete/', product_delete_view, name='product-delete'),
# ]
