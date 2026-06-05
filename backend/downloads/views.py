from rest_framework import viewsets, permissions
from .models import DownloadHistory


class DownloadHistoryViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = None
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return DownloadHistory.objects.filter(user=self.request.user).order_by('-created_at')

    def get_serializer_class(self):
        from .serializers import DownloadHistorySerializer
        return DownloadHistorySerializer
