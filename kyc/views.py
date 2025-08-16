from rest_framework import generics, permissions, status
from rest_framework.response import Response
from .models import KYCSubmission
from .serializers import KYCSubmissionSerializer, AdminKYCActionSerializer


# ---------------------------
# User submits KYC
# ---------------------------
class SubmitKYCView(generics.CreateAPIView):
    """
    Allows an authenticated user to submit their KYC documents.
    """
    serializer_class = KYCSubmissionSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user, status='pending')


# ---------------------------
# User checks KYC status
# ---------------------------
class KYCStatusView(generics.RetrieveAPIView):
    serializer_class = KYCSubmissionSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return KYCSubmission.objects.get(user=self.request.user)


# ---------------------------
# Admin updates KYC (approve/reject)
# ---------------------------
class AdminKYCUpdateView(generics.UpdateAPIView):
    """
    Allows admin to approve or reject a KYC submission.
    """
    serializer_class = AdminKYCActionSerializer
    permission_classes = [permissions.IsAdminUser]
    queryset = KYCSubmission.objects.all()

    def update(self, request, *args, **kwargs):
        submission = self.get_object()
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        action = serializer.validated_data['action']
        reason = serializer.validated_data.get('reason', '')

        if action == 'approve':
            submission.approve()
            return Response(
                {"message": "KYC approved successfully", "status": submission.status},
                status=status.HTTP_200_OK
            )

        elif action == 'reject':
            if not reason:
                return Response(
                    {"error": "Reason is required for rejection"},
                    status=status.HTTP_400_BAD_REQUEST
                )
            submission.reject(reason)
            return Response(
                {"message": "KYC rejected", "status": submission.status, "reason": reason},
                status=status.HTTP_200_OK
            )

        return Response({"error": "Invalid action"}, status=status.HTTP_400_BAD_REQUEST)
