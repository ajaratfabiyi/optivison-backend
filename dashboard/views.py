# dashboard/views.py
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.db.models import Sum

from users.models import User
from transactions.models import Transaction
from withdrawals.models import WithdrawalRequest
from .serializers import UserStatsSerializer


class UserStatsView(APIView):
    """
    Returns overall statistics for the authenticated user:
    - Current balance
    - Total earnings
    - Total withdrawn
    - Number of referrals
    """
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user

        # Total earnings = all deposits + bonuses
        total_earnings = Transaction.objects.filter(
            user=user,
            tx_type__in=['deposit', 'bonus'],
            status='completed'
        ).aggregate(total=Sum('amount'))['total'] or 0

        # Total withdrawn = all completed withdrawals
        total_withdrawn = WithdrawalRequest.objects.filter(
            user=user,
            status='paid'
        ).aggregate(total=Sum('amount'))['total'] or 0

        # Balance = earnings - withdrawn
        balance = total_earnings - total_withdrawn

        # Referrals count
        referrals_count = User.objects.filter(referred_by=user).count()

        data = {
            "balance": balance,
            "total_earnings": total_earnings,
            "total_withdrawn": total_withdrawn,
            "referrals_count": referrals_count
        }

        return Response(UserStatsSerializer(data).data)


class DownlineStatsView(APIView):
    """ Returns total and active referrals """
    permission_classes = [IsAuthenticated]

    def get(self, request):
        total_referrals = User.objects.filter(referred_by=request.user).count()
        active_referrals = User.objects.filter(
            referred_by=request.user, is_active=True
        ).count()
        return Response({
            "total_referrals": total_referrals,
            "active_referrals": active_referrals
        })


class EarningsStatsView(APIView):
    """ Returns total earnings for authenticated user """
    permission_classes = [IsAuthenticated]

    def get(self, request):
        total_earnings = Transaction.objects.filter(
            user=request.user,
            tx_type__in=['deposit', 'bonus'],
            status='completed'
        ).aggregate(total=Sum('amount'))['total'] or 0

        return Response({"total_earnings": total_earnings})


class ReferralTreeView(APIView):
    """ Returns first-level referral tree """
    permission_classes = [IsAuthenticated]

    def get(self, request):
        referrals = User.objects.filter(referred_by=request.user).values(
            'id', 'username', 'email', 'date_joined'
        )
        return Response({"referral_tree": list(referrals)})


class DashboardOverviewView(APIView):
    """
    Returns a consolidated dashboard overview for the authenticated user.
    Includes:
    - Balance
    - Total earnings
    - Total withdrawn
    - Total referrals
    - Active referrals
    - Referral tree (first level)
    """
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user

        total_earnings = Transaction.objects.filter(
            user=user,
            tx_type__in=['deposit', 'bonus'],
            status='completed'
        ).aggregate(total=Sum('amount'))['total'] or 0

        total_withdrawn = WithdrawalRequest.objects.filter(
            user=user,
            status='paid'
        ).aggregate(total=Sum('amount'))['total'] or 0

        balance = total_earnings - total_withdrawn

        total_referrals = User.objects.filter(referred_by=user).count()
        active_referrals = User.objects.filter(
            referred_by=user, is_active=True
        ).count()

        referrals_list = list(User.objects.filter(referred_by=user).values(
            'id', 'username', 'email', 'date_joined'
        ))

        return Response({
            "balance": balance,
            "total_earnings": total_earnings,
            "total_withdrawn": total_withdrawn,
            "total_referrals": total_referrals,
            "active_referrals": active_referrals,
            "referral_tree": referrals_list
        })
