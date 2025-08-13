from rest_framework import serializers
from .models import KYCSubmission

class KYCSubmissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = KYCSubmission
        fields = ['document_type', 'document_file']

    def create(self, validated_data):
        user = self.context['request'].user
        # Overwrite or create a new submission
        kyc, created = KYCSubmission.objects.update_or_create(
            user=user,
            defaults={
                'document_type': validated_data['document_type'],
                'document_file': validated_data['document_file'],
                'status': 'pending'
            }
        )
        return kyc

class KYCStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = KYCSubmission
        fields = ['status', 'submitted_at', 'reviewed_at']
