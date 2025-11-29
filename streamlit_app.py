import streamlit as st
import pandas as pd

st.set_page_config(page_title="Beef Meal Prep Calculator", layout="centered")

st.title("Beef Meal Prep Calculator 🥩🐶")

st.markdown(
    """
This calculator uses the **7-day batch in column F (Large x1.25)** from your sheet.

Assumptions baked in:

- Column F is a **7-day batch**.
- That batch is correct when **Dex + Indiana eat 32 oz/day total**.
- We scale **up or down** based on:
  - Your dogs' combined daily ounces, and
  - How many days you want to prep.
"""
)

# ============================
# CONSTANTS FROM YOUR RECIPE
# ============================

BASE_DAILY_OZ = 32.0   # Dex + Indy total / day in the original sheet
BASE_DAYS = 7.0        # Column F is a 7-day batch

# These are column F (Large x1.25) values + units from the Excel sheet.
# We treat the numbers as "units" in the listed unit (lb, oz, tbsp).
INGREDIENTS = [
    {"ingredient": "Ground Beef",       "base_7day_amount": 6.25,   "unit": "lbs"},
    {"ingredient": "Beef Liver",       "base_7day_amount": 3.125,  "unit": "oz"},
    {"ingredient": "Russet Potatoes",  "base_7day_amount": 71.25,  "unit": "oz"},
    {"ingredient": "Sweet Potatoes",   "base_7day_amount": 37.5,   "unit": "oz"},
    {"ingredient": "Carrots",          "base_7day_amount": 6.25,   "unit": "oz"},
    {"ingredient": "Green Beans",      "base_7day_amount": 6.25,   "unit": "oz"},
    {"ingredient": "Green Peas",       "base_7day_amount": 3.125,  "unit": "oz"},
    {"ingredient": "Apple",            "base_7day_amount": 3.125,  "unit": "oz"},
    {"ingredient": "Sunflower Oil",    "base_7day_amount": 4.6875, "unit": "oz"},
    {"ingredient": "Omega",            "base_7day_amount": 1.25,   "unit": "tbsp"},
    {"ingredient": "Nutrient",         "base_7day_amount": 3.75,   "unit": "tbsp"},
]

ingredient_df = pd.DataFrame(INGREDIENTS)

# ============================
# 1) DAYS SELECTION PROMPTS
# ============================

st.subheader("How many days of food do you want to prep?")

days_choice = st.radio(
    "Choose a prep duration:",
    (
        "3 days (short trip)",
        "7 days (one week)",
        "Custom number of days",
    ),
)

if days_choice.startswith("3"):
    days = 3
elif days_choice.startswith("7"):
    days = 7
else:
    days = st.number_input(
        "Enter custom number of days:",
        min_value=1,
        value=7,
        step=1,
    )

# ============================
# 2) DEX / INDIANA DAILY INTAKE
# ============================

st.subheader("Dexter & Indiana's Daily Intake")

st.markdown(
    "You can keep their usual portions, or change what they eat per day."
)

change_portions = st.checkbox(
    "Change what Dexter and Indiana eat per day?",
    value=False,
)

if change_portions:
    dex_daily = st.number_input("Dexter daily food (oz)", min_value=0.0, value=20.0, step=0.5)
    indy_daily = st.number_input("Indiana daily food (oz)", min_value=0.0, value=12.0, step=0.5)
else:
    # Defaults – tweak to whatever you normally feed.
    dex_daily = 20.0
    indy_daily = 12.0
    st.info(
        f"Using default daily portions: Dexter = {dex_daily} oz, "
        f"Indiana = {indy_daily} oz. Tick the checkbox above if you want to change them."
    )

total_daily_oz = dex_daily + indy_daily

st.markdown(
    f"""
**Daily total for both dogs:** `{total_daily_oz:.2f} oz`  
**Prep duration:** `{int(days)} day(s)`
"""
)

if total_daily_oz == 0:
    st.warning("Total daily intake is 0 oz — increase Dexter or Indiana’s daily ounces to get calculations.")
    st.stop()

# ============================
# 3) SCALE RECIPE
# ============================

# Scale from original scenario: 32 oz/day, 7 days
# scale_factor = (your_daily / 32) * (your_days / 7)
scale_factor = (total_daily_oz / BASE_DAILY_OZ) * (days / BASE_DAYS)

calc_df = ingredient_df.copy()

# Per-day amount in the original recipe (for 32 oz/day)
calc_df["Base_Per_Day"] = calc_df["base_7day_amount"] / BASE_DAYS

# Per-day amount for your dogs (same units as column F)
calc_df["Per_Day_Amount"] = calc_df["Base_Per_Day"] * (total_daily_oz / BASE_DAILY_OZ)

# Total over your chosen prep period
calc_df["Total_For_Period"] = calc_df["base_7day_amount"] * scale_factor

# ============================
# 4) DISPLAY RESULTS
# ============================

st.subheader("Ingredient Requirements (same units as column F)")

display_df = pd.DataFrame({
    "Ingredient": calc_df["ingredient"],
    "Per Day": [
        f"{amt:.3f} {unit}"
        for amt, unit in zip(calc_df["Per_Day_Amount"], calc_df["unit"])
    ],
    f"Total for {int(days)} days": [
        f"{amt:.3f} {unit}"
        for amt, unit in zip(calc_df["Total_For_Period"], calc_df["unit"])
    ],
})

st.dataframe(display_df, use_container_width=True)

st.markdown(
    f"""
### Batch Summary
- **Combined daily intake used for scaling:** `{total_daily_oz:.2f} oz/day`
- **Prep duration:** `{int(days)} day(s)`
- **Scale factor vs original 7-day / 32 oz batch:** `{scale_factor:.3f}`
"""
)

st.caption(
    "All amounts are scaled from the original 7-day batch in column F, "
    "which is calibrated for 32 oz/day total between Dexter and Indiana."
)
