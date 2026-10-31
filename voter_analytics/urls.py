from django.urls import path
from django.conf.urls.static import static
from django.conf import settings
from .views import VoterListView, VoterDetailView, VoterGraphsView

urlpatterns = [
    # map the URL (empty string) to the view
    path('', VoterListView.as_view(), name='voters'),
    path('voter/<int:pk>', VoterDetailView.as_view(), name='voter'),
    path('graphs', VoterGraphsView.as_view(), name='graphs'),
]
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
