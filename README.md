TradeStation Crypto Transaction Parser for [Koinly.io](https://koinly.io/?via=6BCBDC5B)
===

**TradeStation Crypto is shutting down and all crypto must be sold or withdrawn!**

[Koinly](https://koinly.io/?via=6BCBDC5B) does not support importing the `Transactions.csv` from TradeStation. They do support the `Tax.csv` file but it misses some transactions and does not include interest.

Requirements
---

1. Python 3
1. arrow

Usage
---

1. `pip3 install arrow`
1. Download your `Transactions.csv` from TradeStation (set your start date to before the account was opened)
1. Run `python3 tradestation.py`
1. Import `trades.csv` and `income.csv` into [Koinly](https://koinly.io/?via=6BCBDC5B)

Caveats
---

- The parser does not handle incoming crypto deposits. It should be easy to add but I have no example data.

Disclaimer
---

- I do _not_ guarentee the accuracy of the output CSV data and there could be bugs. Speak to a tax professional before filing!

License
---

MIT