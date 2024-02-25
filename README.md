# EDGAR


- Can negative sentiment 10-k filings predict short term movements in share prices?
- Create a **package** to solve this

For each 10-k filing, count the number of words listed as 'Negative', 'Positive', 'Uncertain', etc..

Look for any correlations with short-term price movements.


#### BACKLOG:
- **Unit tests** - I think most unit tests a broken now, as they are left over from an earlier version of the system.

- **Un-merge quarterly reports** - I think I might have merged quarterly 10-Ks into one txt per year. This leaves us with fewer 'date' data points to analyze against stock prices.

- **Reorganize data directory** - Simplify data directory structure. Write script to create this structure from a fresh first-run.

- **Get yahoo data at similar resolution to 10-Ks** - might make sense to return quarterly trends over a longer period. Or maybe monthly. Also, make file output names more descriptive; including 'monthly' in the file name, for example.

**CLI** - package the project smartly into an intuitive CLI. 