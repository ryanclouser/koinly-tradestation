#!/usr/bin/env python3
import csv
import arrow

class Transaction(object):
	id = None
	date = None
	type = None
	qty = None
	balance = None
	currency = None
	status = None

	side = None

	def __init__(self, row):
		self.id = row[0]
		self.date = arrow.get(row[1])
		self.type = row[2]
		self.qty = row[3]
		self.balance = row[4]
		self.currency = row[5]
		self.status = row[6]

		self.side = 'Buy' if float(self.qty) > 0 else 'Sell'

class Trade(object):
	executions = []
	commission = []
	interest = []
	debit = []
	credit = []
	withdrawal = []

	def __init__(self, t=None):
		self.executions = []
		self.commission = []
		self.interest = []
		self.debit = []
		self.credit = []
		self.withdrawal = []

		if t:
			self.update(t)

	def update(self, t):
		if self.interest or self.debit or self.credit or self.withdrawal:
			return False

		if self.executions or self.commission:
			prev = self.executions[0] if self.executions else self.commission[0]
			if abs((t.date - prev.date).total_seconds()) > 1:
				return False

		if t.type == 'Execution':
			self.executions.append(t)
		elif t.type == 'Trading commission':
			self.commission.append(t)
		elif t.type == 'Interest':
			self.interest.append(t)
		elif t.type == 'Debit':
			self.debit.append(t)
		elif t.type == 'Credit':
			self.credit.append(t)
		elif t.type == 'Withdrawal':
			self.withdrawal.append(t)
		else:
			raise Exception('Unknown transaction type %s' % (t.type))

		return True

def main():
	data = []
	trades = []

	with open('Transactions.csv') as f:
		reader = csv.reader(f, delimiter=',', quotechar='"')
		for row in reader:
			try:
				t = Transaction(row)
			except:
				continue
			if t.status == 'Succeeded':
				data.append(t)

	trade = Trade()
	for t in data:
		if not trade.update(t):
			trades.append(trade)
			trade = Trade(t)

	if trade not in trades:
		trades.append(trade)

	with open('trades.csv', 'w') as f:
		writer = csv.writer(f, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
		writer.writerow(['Koinly Date', 'Pair', 'Side', 'Amount', 'Total', 'Fee Amount', 'Fee Currency', 'Label'])

		for t in trades:
			for x in range(0, len(t.executions), 2):
				t1 = t.executions[x]
				t2 = t.executions[x + 1]

				if t.commission:
					row = [t1.date, t2.currency + '-' + t1.currency, t2.side, t2.qty, t1.qty, t.commission[0 if x == 0 else int(x / 2)].qty, t.commission[0 if x == 0 else int(x / 2)].currency, 'trade']
					writer.writerow(row)
				else:
					row = [t1.date, t2.currency + '-' + t1.currency, t2.side, t2.qty, t1.qty, '', '', 'trade']
					writer.writerow(row)

	with open('income.csv', 'w') as f:
		writer = csv.writer(f, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
		writer.writerow(['Koinly Date', 'Currency', 'Amount', 'Label', 'Description'])

		for t in trades:
			for i in t.interest:
				row = [i.date, i.currency, i.qty, 'reward', 'Interest']
				writer.writerow(row)
			for i in t.debit:
				row = [i.date, i.currency, i.qty, 'cost', 'Debit']
				writer.writerow(row)
			for i in t.credit:
				row = [i.date, i.currency, i.qty, 'fee refund', 'Credit']
				writer.writerow(row)
			for i in t.withdrawal:
				row = [i.date, i.currency, i.qty, 'withdrawal', 'Withdrawal']
				writer.writerow(row)


if __name__ == '__main__':
	main()