import streamlit as st
import pandas as pd

st.set_page_config(page_title="JFFD DIY Meal Prep Calculator", layout="centered")

st.title("JFFD DIY Meal Prep Calculator 🐶")

st.markdown(
    """
This calculator uses **baked-in recipes** from your JFFD DIY sheet.

For each recipe (Chicken / Turkey / Beef):

- Column F (`Large x…`) is treated as the **7-day batch**
- That 7-day batch is calibrated to the original **Dex + Indy daily ounces**
- You can scale based on:
  - How many **days** you want to prep
  - How much **Dexter & Indiana eat per day now (oz)**

Main proteins are shown in **pounds**, other ingredients keep their original units.
"""
)

# -------------------------------------------------------------------
# Embedded recipe data (extracted from your Excel; no file needed)
# Column F = 7-day batch
# base_daily_oz = Dex + Indy from row 2 of each sheet
# -------------------------------------------------------------------

RECIPE_DATA = {
    "Chicken": {
        "base_daily_oz": 36.0,   # Dex 22 + Indy 14
        "dex_default": 22.0,
        "indy_default": 14.0,
        "base_days": 7.0,
        "ingredients": [
            # Chicken Thighs converted: 75.25 oz / 16 = 4.703125 lbs
            {"name": "Chicken Thighs",     "base_7day_amount": 4.703125, "unit": "lbs"},
            {"name": "Chicken Liver",      "base_7day_amount": 24.5,     "unit": "oz"},
            {"name": "Apple",              "base_7day_amount": 8.4,      "unit": "oz"},
            {"name": "Carrots",            "base_7day_amount": 14.0,     "unit": "oz"},
            {"name": "Kale",               "base_7day_amount": 14.0,     "unit": "oz"},
            {"name": "White Rice (Dry)",   "base_7day_amount": 19.25,    "unit": "oz"},
            {"name": "Brown Rice (Dry)",   "base_7day_amount": 11.2,     "unit": "oz"},
            {"name": "Sunflower Oil",      "base_7day_amount": 2.625,    "unit": "tsp"},
            {"name": "Omega",              "base_7day_amount": 0.875,    "unit": "tsp"},
            {"name": "Flaxseed Oil",       "base_7day_amount": 0.875,    "unit": "tsp"},
            {"name": "Nutrient",           "base_7day_amount": 13.125,   "unit": "tbsp"},
        ],
    },
    "Turkey": {
        "base_daily_oz": 30.0,   # Dex 19 + Indy 11
        "dex_default": 19.0,
        "indy_default": 11.0,
        "base_days": 7.0,
        "ingredients": [
            {"name": "Ground Turkey",      "base_7day_amount": 6.0,   "unit": "lbs"},
            {"name": "Turkey Liver",       "base_7day_amount": 3.0,   "unit": "oz"},
            {"name": "Whole Wheat Pasta",  "base_7day_amount": 48.0,  "unit": "oz"},
            {"name": "Carrots",            "base_7day_amount": 6.0,   "unit": "oz"},
            {"name": "Zucchini",           "base_7day_amount": 6.0,   "unit": "oz"},
            {"name": "Broccoli",           "base_7day_amount": 6.0,   "unit": "oz"},
            {"name": "Cranberries",        "base_7day_amount": 3.0,   "unit": "oz"},
            {"name": "Omega",              "base_7day_amount": 6.0,   "unit": "tsp"},
            {"name": "Nutrient",           "base_7day_amount": 3.0,   "unit": "tbsp"},
        ],
    },
    "Beef": {
        "base_daily_oz": 32.0,   # Dex 20 + Indy 12
        "dex_default": 20.0,
        "indy_default": 12.0,
        "base_days": 7.0,
        "ingredients": [
            {"name": "Ground Beef",        "base_7day_amount": 6.25,   "unit": "lbs"},
            {"name": "Beef Liver",         "base_7day_amount": 3.125,  "unit": "oz"},
            {"name": "Russet Potatoes",    "base_7day_amount": 71.25,  "unit": "oz"},
            {"name": "Sweet Potatoes",     "base_7day_amount": 37.5,   "unit": "oz"},
            {"name": "Carrots",            "base_7day_amount": 6.25,   "unit": "oz"},
            {"name": "Green Beans",        "base_7day_amount": 6.25,   "unit": "oz"},
            {"name": "Green Peas",         "base_7day_amount": 3.125,  "unit": "oz"},
            {"name": "Apple",              "base_7day_amount": 3.125,  "unit": "oz"},
            {"name": "Sunflower Oil",      "base_7day_amount": 4.6875, "unit": "oz"},
            {"name": "Omega",              "base_7day_amount": 1.25,   "unit": "tbsp"},
            {"name": "Nutrient",           "base_7day_amount": 3.75,   "unit": "tbsp"},
        ],
    },
}

# -------------------------------------------------------------------
# Recipe selector (centered layout)
# -------------------------------------------------------------------

st.subheader("1. Choose Recipe")

selected_recipe_name = st.selectbox(
    "Select which meal you are prepping:",
    list(RECIPE_DATA.keys()),
)

recipe = RECIPE_DATA[selected_recipe_name]
base_daily_oz = recipe["base_daily_oz"]
dex_default = recipe["dex_default"]
indy_default = recipe["indy_default"]
base_days = recipe["base_days"]
ingredients = recipe["ingredients"]

st.markdown(
    f"""
**Selected recipe:** `{selected_recipe_name}`  
**Original base daily (Dex + Indy):** `{base_daily_oz:.1f} oz/day`  
**Original 7-day batch:** column F (`Large x…`) from your JFFD sheet.
"""
)

# -------------------------------------------------------------------
# 2) How many days?
# -------------------------------------------------------------------

st.subheader("2. How many days of food do you want to prep?")

days_choice = st.radio(
    "Prep duration:",
    ("3 days (short trip)", "7 days (one week)", "Custom number of days"),
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

# -------------------------------------------------------------------
# 3) Dexter & Indiana daily intake
# -------------------------------------------------------------------

st.subheader("3. Dexter & Indiana's Daily Intake")

st.markdown("Use the original recipe values, or change what they eat now:")

change_portions = st.checkbox(
    "Change what Dexter and Indiana eat per day?",
    value=False,
)

if change_portions:
    dex_daily = st.number_input(
        "Dexter daily food (oz)",
        min_value=0.0,
        value=float(dex_default),
        step=0.5,
        key=f"dex_{selected_recipe_name}",
    )
    indy_daily = st.number_input(
        "Indiana daily food (oz)",
        min_value=0.0,
        value=float(indy_default),
        step=0.5,
        key=f"indy_{selected_recipe_name}",
    )
else:
    dex_daily = dex_default
    indy_daily = indy_default
    st.info(
        f"Using original **{selected_recipe_name}** defaults: "
        f"Dexter = {dex_daily:.1f} oz, Indiana = {indy_daily:.1f} oz.\n\n"
        "Tick the checkbox above if you want to change them."
    )

total_daily_oz = dex_daily + indy_daily

st.markdown(
    f"""
**Combined daily intake (Dex + Indy):** `{total_daily_oz:.2f} oz/day`  
**Prep duration:** `{int(days)} day(s)`
"""
)

if total_daily_oz == 0:
    st.warning("Total daily intake is 0 oz — increase Dexter or Indiana’s daily ounces.")
    st.stop()

# -------------------------------------------------------------------
# 4) Scale recipe
# -------------------------------------------------------------------

# scale_factor = (your_daily / base_daily) * (your_days / base_days)
scale_factor = (total_daily_oz / base_daily_oz) * (days / base_days)

rows = []
print_rows = []  # for print view

for ing in ingredients:
    name = ing["name"]
    base_7 = ing["base_7day_amount"]
    unit = ing["unit"]

    # Per-day in original recipe
    base_per_day = base_7 / base_days

    # Per-day for your current combined intake
    per_day_yours = base_per_day * (total_daily_oz / base_daily_oz)

    # Total for chosen period
    total_period = base_7 * scale_factor

    rows.append(
        {
            "Ingredient": name,
            "Per Day": f"{per_day_yours:.3f} {unit}".strip(),
            f"Total for {int(days)} days": f"{total_period:.3f} {unit}".strip(),
        }
    )

    print_rows.append(
        {
            "Ingredient": name,
            f"Total for {int(days)} days": f"{total_period:.3f} {unit}".strip(),
        }
    )

result_df = pd.DataFrame(rows)
print_df = pd.DataFrame(print_rows)

# -------------------------------------------------------------------
# 5) Display results – normal view
# -------------------------------------------------------------------

st.subheader("4. Ingredient Requirements (scaled from 7-day batch)")

st.dataframe(result_df, use_container_width=True)

st.markdown(
    f"""
**Base daily (original {selected_recipe_name} recipe):** `{base_daily_oz:.2f} oz/day`  
**Your combined daily:** `{total_daily_oz:.2f} oz/day`  
**Scale factor vs original 7-day batch:** `{scale_factor:.3f}`  
"""
)

# -------------------------------------------------------------------
# 6) Print-friendly view
# -------------------------------------------------------------------

st.subheader("5. Print-Friendly Summary")

show_print = st.checkbox("Show print-friendly summary (totals only)")

if show_print:
    st.markdown(
        f"**Print view for {selected_recipe_name} – Total for {int(days)} days**"
    )
    # use st.table for a simpler, print-ish look
    st.table(print_df)

if selected_recipe_name == "Chicken":
    st.caption(
        "Chicken Thighs 7-day batch was **75.25 oz**, converted here to "
        "`4.703 lb` so the protein is shown in pounds. All other ingredients "
        "retain their original units."
    )
else:
    st.caption(
        "All amounts are scaled from the original column-F 7-day batch for this recipe."
    )
