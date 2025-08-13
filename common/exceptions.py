from rest_framework.exceptions import APIException
from rest_framework import status

class InvalidReferralCode(APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = 'The referral code provided is invalid.'
    default_code = 'invalid_referral'

class InsufficientBalance(APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = 'Insufficient balance to complete the transaction.'
    default_code = 'insufficient_balance'

class KycNotApproved(APIException):
    status_code = status.HTTP_403_FORBIDDEN
    default_detail = 'You must complete and have your KYC approved before performing this action.'
    default_code = 'kyc_not_approved'
