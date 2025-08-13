from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError
from django.utils import timezone
from .models import KYCSubmission
from .serializers import KYCSubmissionSerializer, KYCStatusSerializer


class SubmitKYCView(generics.CreateAPIView):
    serializer_class = KYCSubmissionSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        """
        Prevent re-submission if KYC is already approved.
        """
        existing_kyc = getattr(self.request.user, 'kyc_submission', None)
        if existing_kyc and existing_kyc.status == 'approved':
            raise ValidationError("Your KYC is already approved and cannot be changed.")
        serializer.save()


class KYCStatusView(generics.RetrieveAPIView):
    serializer_class = KYCStatusSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return KYCSubmission.objects.get(user=self.request.user)


class AdminKYCUpdateView(generics.UpdateAPIView):
    queryset = KYCSubmission.objects.all()
    serializer_class = KYCStatusSerializer
    permission_classes = [permissions.IsAdminUser]

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        new_status = request.data.get('status')

        if new_status not in dict(KYCSubmission.STATUS_CHOICES):
            return Response({"error": "Invalid status"}, status=status.HTTP_400_BAD_REQUEST)

        instance.status = new_status
        instance.reviewed_at = timezone.now()
        instance.save()

        # Mark user as verified if approved
        if new_status == 'approved':
            instance.user.is_kyc_verified = True
            instance.user.save()

        return Response({"status": instance.status})
