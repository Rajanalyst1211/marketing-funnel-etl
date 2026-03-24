import pandas as pd
from faker import Faker
import random
import uuid
import os
from datetime import datetime

fake = Faker()
random.seed(42)
Faker.seed(42)

RAW_DIR = "data/raw"
os.makedirs(RAW_DIR, exist_ok=True)

CHANNELS   = ["Google Ads", "Meta Ads", "Email", "Organic", "Referral"]
INDUSTRIES = ["SaaS", "Retail", "Finance", "Healthcare", "E-commerce"]
STAGES     = ["Lead", "MQL", "SQL", "Opportunity", "Customer"]
STAGE_WEIGHTS = [40, 25, 15, 12, 8]   # realistic funnel drop-off


def generate_leads(n=5000):
    """
    Generate raw leads data simulating a B2B marketing funnel.
    Each lead has a source channel, industry, funnel stage, and revenue.
    """
    leads = []
    for _ in range(n):
        stage = random.choices(STAGES, weights=STAGE_WEIGHTS, k=1)[0]
        # Only customers have revenue — others are $0
        revenue = round(random.uniform(500, 50000), 2) if stage == "Customer" else 0.0

        leads.append({
            "lead_id"       : str(uuid.uuid4()),
            "created_date"  : fake.date_between(start_date="-2y", end_date="today"),
            "source_channel": random.choice(CHANNELS),
            "industry"      : random.choice(INDUSTRIES),
            "region"        : fake.state(),
            "stage"         : stage,
            "revenue"       : revenue,
            "sales_rep"     : fake.name(),
            "company_name"  : fake.company()
        })

    df = pd.DataFrame(leads)
    df["created_date"] = pd.to_datetime(df["created_date"])
    return df
def generate_campaign_spend():
    """
    Generate monthly marketing spend per channel.
    Used to calculate cost-per-lead and ROI later.
    """
    records = []
    months = pd.date_range(start="2023-01-01", end="2024-12-31", freq="MS")

    for month in months:
        for channel in CHANNELS:
            records.append({
                "month"     : month.strftime("%Y-%m"),
                "channel"   : channel,
                "spend_usd" : round(random.uniform(1000, 20000), 2)
            })

    return pd.DataFrame(records)
def main():
    print("Generating leads data...")
    leads_df = generate_leads(n=5000)
    leads_df.to_csv(f"{RAW_DIR}/leads.csv", index=False)
    print(f"  Saved {len(leads_df)} rows → data/raw/leads.csv")

    print("Generating campaign spend data...")
    spend_df = generate_campaign_spend()
    spend_df.to_csv(f"{RAW_DIR}/campaign_spend.csv", index=False)
    print(f"  Saved {len(spend_df)} rows → data/raw/campaign_spend.csv")

    print("\nSample leads data:")
    print(leads_df.head(3).to_string())

    print("\nStage distribution:")
    print(leads_df["stage"].value_counts())

    print("\nDone! Check data/raw/ folder.")

if __name__ == "__main__":
    main()