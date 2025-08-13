# Transaction status choices
TX_STATUS_PENDING = 'pending'
TX_STATUS_COMPLETED = 'completed'
TX_STATUS_FAILED = 'failed'

TRANSACTION_STATUS_CHOICES = [
    (TX_STATUS_PENDING, 'Pending'),
    (TX_STATUS_COMPLETED, 'Completed'),
    (TX_STATUS_FAILED, 'Failed'),
]

# Transaction types
TX_TYPE_DEPOSIT = 'deposit'
TX_TYPE_WITHDRAWAL = 'withdrawal'
TX_TYPE_BONUS = 'bonus'

TRANSACTION_TYPE_CHOICES = [
    (TX_TYPE_DEPOSIT, 'Deposit'),
    (TX_TYPE_WITHDRAWAL, 'Withdrawal'),
    (TX_TYPE_BONUS, 'Bonus'),
]

# KYC status choices
KYC_PENDING = 'pending'
KYC_APPROVED = 'approved'
KYC_REJECTED = 'rejected'

KYC_STATUS_CHOICES = [
    (KYC_PENDING, 'Pending'),
    (KYC_APPROVED, 'Approved'),
    (KYC_REJECTED, 'Rejected'),
]
