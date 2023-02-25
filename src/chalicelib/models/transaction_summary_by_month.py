import calendar

from .transaction_summary import TransactionSummary


class TransactionSummaryByMonth(TransactionSummary):
    month: int

    def get_month_name(self):
        return calendar.month_name[self.month]
