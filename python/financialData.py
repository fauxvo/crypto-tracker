class FinancialData:
    def __init__(
            self, previous_balance, current_balance, previous_rate, current_rate, previous_perc, current_perc,
            previous_balance_change, current_balance_change):
        self.previous_balance = previous_balance
        self.current_balance = current_balance
        self.previous_rate = previous_rate
        self.current_rate = current_rate
        self.previous_perc = previous_perc
        self.current_perc = current_perc
        self.previous_balance_change = previous_balance_change
        self.current_balance_change = current_balance_change
