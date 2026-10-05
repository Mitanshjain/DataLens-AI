# ==========================================
# DATALENS AI - REGRESSION TEST DATASET
# ==========================================

import numpy as np
import pandas as pd


# ==========================================
# REPRODUCIBILITY
# ==========================================

np.random.seed(42)

n = 500


# ==========================================
# BASIC FEATURES
# ==========================================

employee_id = np.arange(
    1001,
    1001 + n
)

age = np.random.randint(
    21,
    60,
    n
)

experience_years = np.random.randint(
    0,
    30,
    n
)

education = np.random.choice(
    [
        "Bachelor",
        "Master",
        "PhD"
    ],
    size=n,
    p=[
        0.55,
        0.35,
        0.10
    ]
)

job_role = np.random.choice(
    [
        "Data Analyst",
        "Data Scientist",
        "ML Engineer",
        "Business Analyst"
    ],
    size=n
)

city = np.random.choice(
    [
        "Jaipur",
        "Delhi",
        "Mumbai",
        "Bengaluru",
        "Pune"
    ],
    size=n
)

performance_score = np.random.randint(
    1,
    6,
    n
)

projects_completed = np.random.randint(
    1,
    20,
    n
)


# ==========================================
# SALARY GENERATION
# ==========================================

salary = (
    25000
    + experience_years * 3500
    + performance_score * 5000
    + projects_completed * 800
)


# ==========================================
# EDUCATION EFFECT
# ==========================================

salary += np.where(
    education == "Master",
    12000,
    0
)

salary += np.where(
    education == "PhD",
    25000,
    0
)


# ==========================================
# JOB ROLE EFFECT
# ==========================================

salary += np.where(
    job_role == "Data Scientist",
    18000,
    0
)

salary += np.where(
    job_role == "ML Engineer",
    22000,
    0
)

salary += np.where(
    job_role == "Business Analyst",
    6000,
    0
)


# ==========================================
# RANDOM REAL-WORLD VARIATION
# ==========================================

salary = salary.astype(float)

salary += np.random.normal(
    0,
    10000,
    n
)

salary = np.round(
    salary,
    2
)


# ==========================================
# CREATE DATAFRAME
# ==========================================

df = pd.DataFrame(
    {
        "employee_id":
            employee_id,

        "age":
            age,

        "experience_years":
            experience_years,

        "education":
            education,

        "job_role":
            job_role,

        "city":
            city,

        "performance_score":
            performance_score,

        "projects_completed":
            projects_completed,

        "salary":
            salary
    }
)


# ==========================================
# ADD MISSING VALUES
# ==========================================

missing_age = np.random.choice(
    df.index,
    size=10,
    replace=False
)

missing_city = np.random.choice(
    df.index,
    size=8,
    replace=False
)

missing_education = np.random.choice(
    df.index,
    size=6,
    replace=False
)


df.loc[
    missing_age,
    "age"
] = np.nan

df.loc[
    missing_city,
    "city"
] = np.nan

df.loc[
    missing_education,
    "education"
] = np.nan


# ==========================================
# ADD SALARY OUTLIERS
# ==========================================

outlier_indexes = np.random.choice(
    df.index,
    size=3,
    replace=False
)

df.loc[
    outlier_indexes,
    "salary"
] *= 2.5


# ==========================================
# SAVE DATASET
# ==========================================

file_path = (
    "data/uploads/employee_salary.csv"
)

df.to_csv(
    file_path,
    index=False
)


# ==========================================
# DISPLAY SUMMARY
# ==========================================

print("\n================================")
print("REGRESSION DATASET GENERATED")
print("================================")

print(
    f"Rows: {df.shape[0]}"
)

print(
    f"Columns: {df.shape[1]}"
)

print(
    f"\nSaved to: {file_path}"
)

print(
    "\nMissing Values:"
)

print(
    df.isnull().sum()
)

print(
    "\nSalary Statistics:"
)

print(
    df["salary"].describe()
)