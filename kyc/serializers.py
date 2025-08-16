from rest_framework import serializers
from .models import KYCSubmission

class KYCSubmissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = KYCSubmission
        fields = '__all__'
        read_only_fields = [
            'id', 'user', 'status', 'submitted_at', 'updated_at', 'rejection_reason'
        ]


class AdminKYCActionSerializer(serializers.Serializer):
    action = serializers.ChoiceField(choices=['approve', 'reject'])
    reason = serializers.CharField(required=False, allow_blank=True)

    def validate(self, attrs):
        if attrs['document_type'] in ['passport', 'driver_license'] and not attrs.get('document_back'):
            raise serializers.ValidationError("Back of document is required for this type.")
        return attrs

