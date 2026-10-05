# ==========================================
# DATALENS AI - CUSTOMER DATA GENERATOR
# ==========================================

import os
import random

import numpy as np
import pandas as pd


# ==========================================
# SETTINGS
# ==========================================

RANDOM_SEED = 42
TOTAL_CUSTOMERS = 500

random.seed(RANDOM_SEED)
np.random.seed(RANDOM_SEED)


# ==========================================
# POSSIBLE CATEGORIES
# ==========================================

cities = [
    "Jaipur",
    "Delhi",
    "Mumbai",
    "Bengaluru",
    "Pune"
]

subscription_types = [
    "Basic",
    "Standard",
    "Premium"
]


# ==========================================
# GENERATE CUSTOMER RECORDS
# ==========================================

records = []


for customer_id in range(
    1,
    TOTAL_CUSTOMERS + 1
):

    age = random.randint(
        18,
        65
    )

    city = random.choice(
        cities
    )

    income = random.randint(
        25000,
        180000
    )

    tenure_months = random.randint(
        1,
        72
    )

    monthly_spend = random.randint(
        500,
        10000
    )

    support_calls = random.randint(
        0,
        10
    )

    subscription_type = random.choice(
        subscription_types
    )


    # --------------------------------------
    # CREATE CHURN PROBABILITY
    # --------------------------------------

    churn_probability = 0.15


    # New customers may churn more
    if tenure_months < 12:
        churn_probability += 0.20


    # Frequent support calls may indicate
    # customer dissatisfaction
    if support_calls >= 6:
        churn_probability += 0.20


    # Higher monthly spend may increase
    # churn risk in this synthetic example
    if monthly_spend > 7500:
        churn_probability += 0.10


    # Premium customers get slightly
    # lower churn probability
    if subscription_type == "Premium":
        churn_probability -= 0.05


    churn_probability = max(
        0.05,
        min(0.80, churn_probability)
    )


    churned = (
        "Yes"
        if random.random() < churn_probability
        else "No"
    )


    records.append(
        {
            "customer_id": customer_id,
            "age": age,
            "city": city,
            "income": income,
            "tenure_months": tenure_months,
            "monthly_spend": monthly_spend,
            "support_calls": support_calls,
            "subscription_type": subscription_type,
            "churned": churned
        }
    )


# ==========================================
# CREATE DATAFRAME
# ==========================================

df = pd.DataFrame(
    records
)


# ==========================================
# ADD SOME MISSING VALUES
# ==========================================

missing_age_indices = np.random.choice(
    df.index,
    size=10,
    replace=False
)

df.loc[
    missing_age_indices,
    "age"
] = np.nan


missing_income_indices = np.random.choice(
    df.index,
    size=10,
    replace=False
)

df.loc[
    missing_income_indices,
    "income"
] = np.nan


missing_city_indices = np.random.choice(
    df.index,
    size=8,
    replace=False
)

df.loc[
    missing_city_indices,
    "city"
] = np.nan


# ==========================================
# ADD A FEW OUTLIERS
# ==========================================

outlier_indices = np.random.choice(
    df.index,
    size=3,
    replace=False
)

df.loc[
    outlier_indices,
    "income"
] = [
    750000,
    900000,
    1000000
]


# ==========================================
# SAVE DATASET
# ==========================================

output_folder = "data/uploads"

os.makedirs(
    output_folder,
    exist_ok=True
)

file_path = os.path.join(
    output_folder,
    "customer_churn.csv"
)

df.to_csv(
    file_path,
    index=False
)


# ==========================================
# DISPLAY SUMMARY
# ==========================================

print("\n================================")
print("CUSTOMER DATASET GENERATED")
print("================================")

print(
    f"File: {file_path}"
)

print(
    f"Rows: {df.shape[0]}"
)

print(
    f"Columns: {df.shape[1]}"
)

print("\nTarget Distribution:")

print(
    df["churned"].value_counts()
)

print("\nMissing Values:")

print(
    df.isnull().sum()
)

print(
    "\n✓ Dataset generated successfully."
)