# AK Smart Market Desk

A small personal reference page for Indian stocks. It shows end-of-day prices, typical price ranges, 52-week high and low, an analyst consensus target and recent headlines, grouped by sector. A GitHub Action refreshes the data twice every weekday.

**For personal reference and education only. Not investment advice, a recommendation or a price target. The owner is not a SEBI-registered adviser or research analyst.**

## How it works

| File | Purpose |
|---|---|
| `index.html` | The page. It reads `data/prices.json` and draws each sector and stock. |
| `fetch_data.py` | Gets prices, 52-week high and low, analyst consensus and headlines, then writes `data/prices.json`. |
| `.github/workflows/update.yml` | Runs the script at 9:00 am and 4:00 pm IST on weekdays and commits the new data. |
| `data/prices.json` | The latest data. Overwritten by the workflow. |

## Set up

1. Upload all files to a GitHub repository, keeping the folder names exactly as they are.
2. Open **Settings → Pages**, choose the `main` branch and the root folder, and save.
3. Open **Actions → Update market data → Run workflow** once to create the first data.
4. Open your Pages link. If the page says there is no data, check the workflow log in the Actions tab.

## Change the stock list

Edit the `SECTORS` list at the top of `fetch_data.py`. Each entry is a display name and the NSE ticker without `.NS`, for example `("Tata Power", "TATAPOWER")`. Commit the change and run the workflow again.

## What the numbers mean

- **Typical day range and week range:** the price plus or minus the stock's recent daily move (the standard deviation of daily changes over the last 60 trading days). The week range uses that move times about 2.2. It shows how far the stock has usually moved, not where it will go. News or results can push a stock well outside it.
- **52-week low and high:** the lowest and highest prices in the past year.
- **Analyst consensus:** the average, low and high target and the rating as summarised by Yahoo Finance. Targets are usually 12-month views, can be stale or missing, and are often revised or wrong.
- **Headlines:** the top three Google News search results for each stock, linked to the original publisher. Some may be old or off-topic.

## Limits

- Data comes from unofficial sources (`yfinance`, Google News RSS) that can be delayed, wrong, rate-limited or stop working without notice. Check the exchange or your broker before acting.
- Prices are end-of-day. This is not a live quote page.
- GitHub scheduled workflows can start several minutes late, and GitHub may pause them in repositories with no activity for 60 days.
- The page does not include option premiums or your positions.

## Privacy

A GitHub Pages site is public to anyone with the link, even when the repository is private. The page includes a `noindex` tag so search engines should not list it. Do not store personal details, positions or notes in this repository.

## Disclaimer

Not affiliated with or endorsed by NSE, BSE, Google, Yahoo or any company named here. All names belong to their owners. Stocks and options can lose money, and you may lose your entire investment. Check the terms of each data source before sharing the page publicly or using it commercially.
