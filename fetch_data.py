"""Fetch end-of-day prices and recent headlines for the Market Desk page.
Writes data/prices.json. Runs on GitHub Actions; personal reference use only."""
import json, datetime as dt, urllib.parse, urllib.request
import xml.etree.ElementTree as ET
import yfinance as yf

# (display name, NSE ticker without .NS). Edit freely.
SECTORS = {
    "IT": [("TCS", "TCS"), ("Infosys", "INFY"), ("HCL Tech", "HCLTECH")],
    "Banks and financials": [("HDFC Bank", "HDFCBANK"), ("ICICI Bank", "ICICIBANK"), ("SBI", "SBIN")],
    "Oil producers": [("ONGC", "ONGC"), ("Oil India", "OIL")],
    "Oil marketing, paints, aviation": [("BPCL", "BPCL"), ("IOC", "IOC"), ("Asian Paints", "ASIANPAINT"), ("IndiGo", "INDIGO")],
    "Metals": [("Tata Steel", "TATASTEEL"), ("Hindalco", "HINDALCO"), ("Vedanta", "VEDL")],
    "Pharma exporters": [("Sun Pharma", "SUNPHARMA"), ("Dr Reddy's", "DRREDDY"), ("Cipla", "CIPLA")],
    "Autos": [("Maruti", "MARUTI"), ("M&M", "M&M"), ("Bajaj Auto", "BAJAJ-AUTO")],
    "Power and utilities": [("Tata Power", "TATAPOWER"), ("NTPC", "NTPC"), ("Power Grid", "POWERGRID")],
}


def headlines(name, n=3):
    q = urllib.parse.quote(f"{name} share NSE")
    url = f"https://news.google.com/rss/search?q={q}&hl=en-IN&gl=IN&ceid=IN:en"
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
        root = ET.fromstring(urllib.request.urlopen(req, timeout=20).read())
        out = []
        for it in root.iter("item"):
            out.append({"t": it.findtext("title", ""), "l": it.findtext("link", "")})
            if len(out) == n:
                break
        return out
    except Exception as e:
        print("news failed", name, e)
        return []


def targets(tk):
    """Analyst consensus as aggregated by Yahoo Finance. May be missing or stale."""
    try:
        i = tk.info
        mean = i.get("targetMeanPrice")
        if not mean:
            return None
        return {
            "mean": round(float(mean), 2),
            "high": i.get("targetHighPrice"),
            "low": i.get("targetLowPrice"),
            "n": i.get("numberOfAnalystOpinions"),
            "rating": i.get("recommendationKey"),
        }
    except Exception as e:
        print("targets failed", e)
        return None


def main():
    data = {"updated": dt.datetime.now(dt.timezone.utc).isoformat(), "sectors": [], "stocks": {}}
    for sector, items in SECTORS.items():
        keys = []
        for name, sym in items:
            try:
                tk = yf.Ticker(sym + ".NS")
                h = tk.history(period="1y")
                if len(h) < 30:
                    raise ValueError("not enough data")
                c = h["Close"]
                data["stocks"][sym] = {
                    "name": name,
                    "price": round(float(c.iloc[-1]), 2),
                    "prev": round(float(c.iloc[-2]), 2),
                    "hi": round(float(h["High"].max()), 2),
                    "lo": round(float(h["Low"].min()), 2),
                    "move": round(float(c.pct_change().tail(60).std() * 100), 2),
                    "target": targets(tk),
                    "news": headlines(name),
                }
                keys.append(sym)
            except Exception as e:
                print("skip", sym, e)
        data["sectors"].append({"name": sector, "stocks": keys})
    with open("data/prices.json", "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=1)


if __name__ == "__main__":
    main()
