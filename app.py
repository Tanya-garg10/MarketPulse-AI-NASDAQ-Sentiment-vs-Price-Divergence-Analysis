import pandas as pd
import numpy as np
import streamlit as st

st.set_page_config(page_title="MarketPulse AI", page_icon="📊", layout="wide")

# ─────────────────────────────────────────────────────────
# Load dataset directly from repo (no upload needed)
# ─────────────────────────────────────────────────────────
@st.cache_data
def load_data():
    df = pd.read_csv("NASDAQ_100_Data_From_2010.csv", sep="\t")
    df.columns = ["Date", "Open", "High", "Low", "Close", "Adj_Close", "Volume", "Name"]
    df["Date"] = pd.to_datetime(df["Date"], errors="coerce")
    for col in ["Open", "High", "Low", "Close", "Adj_Close", "Volume"]:
        df[col] = pd.to_numeric(df[col], errors="coerce")
    df = df.dropna().drop_duplicates(subset=["Date", "Name"])
    return df

df = load_data()

# ─────────────────────────────────────────────────────────
# Sidebar Filters
# ─────────────────────────────────────────────────────────
st.sidebar.title("🔧 Filters")
all_stocks = sorted(df["Name"].unique())
selected_stocks = st.sidebar.multiselect("Select Stocks", all_stocks, default=["AAPL", "TSLA", "AMZN", "NVDA", "MSFT"])

min_date = df["Date"].min().date()
max_date = df["Date"].max().date()
date_range = st.sidebar.date_input("Date Range", value=(min_date, max_date), min_value=min_date, max_value=max_date)

# ─────────────────────────────────────────────────────────
# Filter Data
# ─────────────────────────────────────────────────────────
if len(date_range) == 2:
    start_date, end_date = date_range
else:
    start_date, end_date = min_date, max_date

filtered = df[
    (df["Name"].isin(selected_stocks)) &
    (df["Date"] >= pd.Timestamp(start_date)) &
    (df["Date"] <= pd.Timestamp(end_date))
].copy()
filtered = filtered.sort_values(["Name", "Date"])

if filtered.empty:
    st.warning("No data for selected filters. Adjust sidebar options.")
    st.stop()

# ─────────────────────────────────────────────────────────
# Feature Engineering
# ─────────────────────────────────────────────────────────
filtered["Pct_Change"] = filtered.groupby("Name")["Close"].pct_change() * 100
filtered["MA_20"] = filtered.groupby("Name")["Close"].transform(lambda x: x.rolling(20).mean())
filtered["MA_50"] = filtered.groupby("Name")["Close"].transform(lambda x: x.rolling(50).mean())
filtered["Volatility_20"] = filtered.groupby("Name")["Pct_Change"].transform(lambda x: x.rolling(20).std())

# Mock Sentiment & Trend (reproducible)
rng = np.random.default_rng(42)
filtered["sentiment_score"] = rng.uniform(-1, 1, len(filtered))
filtered["trend_score"] = rng.uniform(0, 100, len(filtered))

# ─────────────────────────────────────────────────────────
# Header
# ─────────────────────────────────────────────────────────
st.title("📊 MarketPulse AI")
st.caption("NASDAQ 100 Insights — Detect mispriced stocks using sentiment vs price divergence")

# ─────────────────────────────────────────────────────────
# KPI Cards
# ─────────────────────────────────────────────────────────
latest = filtered.sort_values("Date").groupby("Name").tail(1)

col1, col2, col3, col4 = st.columns(4)
col1.metric("Stocks Selected", len(selected_stocks))
col2.metric("Total Records", f"{len(filtered):,}")
col3.metric("Date Range", f"{(end_date - start_date).days} days")
avg_vol = latest["Volatility_20"].mean()
col4.metric("Avg Volatility (20d)", f"{avg_vol:.2f}%" if pd.notna(avg_vol) else "N/A")

st.divider()

# ─────────────────────────────────────────────────────────
# 📈 Price Trend Chart
# ─────────────────────────────────────────────────────────
st.subheader("📈 Closing Price Trend")
price_pivot = filtered.pivot_table(index="Date", columns="Name", values="Close")
st.line_chart(price_pivot)

# ─────────────────────────────────────────────────────────
# 📊 Volume Comparison
# ─────────────────────────────────────────────────────────
st.subheader("📊 Average Daily Volume")
avg_volume = filtered.groupby("Name")["Volume"].mean().sort_values(ascending=False)
st.bar_chart(avg_volume)

# ─────────────────────────────────────────────────────────
# 🔥 Volatility Heatmap (table style)
# ─────────────────────────────────────────────────────────
st.subheader("🔥 Monthly Volatility")
filtered["YearMonth"] = filtered["Date"].dt.to_period("M").astype(str)
vol_table = filtered.groupby(["Name", "YearMonth"])["Pct_Change"].std().reset_index()
vol_pivot = vol_table.pivot(index="Name", columns="YearMonth", values="Pct_Change")
st.dataframe(vol_pivot.style.background_gradient(cmap="YlOrRd", axis=1), use_container_width=True)

# ─────────────────────────────────────────────────────────
# 🏆 Mispriced Stocks (Sentiment vs Price Divergence)
# ─────────────────────────────────────────────────────────
st.subheader("🏆 Mispriced Stocks — Sentiment vs Price Divergence")

agg_df = filtered.groupby("Name").agg(
    avg_sentiment=("sentiment_score", "mean"),
    avg_pct_change=("Pct_Change", "mean"),
    avg_trend=("trend_score", "mean"),
    avg_volatility=("Volatility_20", "mean"),
    avg_close=("Close", "mean"),
).reset_index()

max_val = agg_df["avg_pct_change"].abs().max()
if max_val and max_val > 0:
    agg_df["norm_price"] = agg_df["avg_pct_change"] / max_val
else:
    agg_df["norm_price"] = 0

agg_df["divergence"] = abs(agg_df["avg_sentiment"] - agg_df["norm_price"])
agg_df = agg_df.sort_values("divergence", ascending=False)

col_left, col_right = st.columns(2)
with col_left:
    st.markdown("**Divergence Table**")
    st.dataframe(
        agg_df[["Name", "avg_sentiment", "norm_price", "divergence", "avg_close"]].style.format({
            "avg_sentiment": "{:.4f}",
            "norm_price": "{:.4f}",
            "divergence": "{:.4f}",
            "avg_close": "${:.2f}",
        }),
        use_container_width=True,
    )
with col_right:
    st.markdown("**Sentiment vs Normalized Price**")
    chart_data = agg_df.set_index("Name")[["avg_sentiment", "norm_price"]]
    st.bar_chart(chart_data)

# ─────────────────────────────────────────────────────────
# 📉 Moving Averages
# ─────────────────────────────────────────────────────────
st.subheader("📉 Moving Averages (20 & 50 day)")
ma_stock = st.selectbox("Pick a stock for MA chart", selected_stocks)
ma_data = filtered[filtered["Name"] == ma_stock][["Date", "Close", "MA_20", "MA_50"]].set_index("Date")
st.line_chart(ma_data)

# ─────────────────────────────────────────────────────────
# 🧠 Auto-Generated Insights
# ─────────────────────────────────────────────────────────
st.subheader("🧠 Auto-Generated Insights")

# Best & worst performer
best = agg_df.iloc[-1] if len(agg_df) else None  # lowest divergence = fairly priced
worst = agg_df.iloc[0] if len(agg_df) else None  # highest divergence = mispriced

insights = []

if worst is not None:
    insights.append(f"⚠️ **{worst['Name']}** has the highest sentiment-price divergence ({worst['divergence']:.4f}), suggesting potential mispricing.")
if best is not None:
    insights.append(f"✅ **{best['Name']}** is the most fairly priced stock with divergence of {best['divergence']:.4f}.")

# Highest volatility
most_volatile = agg_df.sort_values("avg_volatility", ascending=False).iloc[0]
insights.append(f"🔥 **{most_volatile['Name']}** is the most volatile (avg 20-day volatility: {most_volatile['avg_volatility']:.2f}%).")

# Highest avg close
priciest = agg_df.sort_values("avg_close", ascending=False).iloc[0]
insights.append(f"💰 **{priciest['Name']}** has the highest average closing price at ${priciest['avg_close']:.2f}.")

# Volume insight
top_vol_stock = filtered.groupby("Name")["Volume"].mean().idxmax()
top_vol_val = filtered.groupby("Name")["Volume"].mean().max()
insights.append(f"📊 **{top_vol_stock}** leads in average daily trading volume ({top_vol_val:,.0f} shares).")

for insight in insights:
    st.markdown(insight)

# ─────────────────────────────────────────────────────────
# 📋 Raw Data Explorer
# ─────────────────────────────────────────────────────────
with st.expander("📋 View Raw Data"):
    st.dataframe(filtered.drop(columns=["YearMonth"], errors="ignore"), use_container_width=True)
    st.download_button(
        "Download Filtered CSV",
        filtered.drop(columns=["YearMonth"], errors="ignore").to_csv(index=False),
        file_name="filtered_nasdaq.csv",
        mime="text/csv",
    )
