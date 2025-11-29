import streamlit as st
import pandas as pd

st.set_page_config(page_title="JFFD DIY Meal Prep Calculator", layout="wide")

st.title("JFFD DIY Meal Prep Calculator 🐶")

st.markdown(
    """
This app uses **baked-in formulas** from your JFFD DIY sheet.

For each recipe (Chicken / Turkey / Beef):

- Column F (`Large x…`) is treated as the **7-day batch**
- That 7-day batch is correct for the **Dex + Indy daily ounces** in the original sheet
- We scale based on:
  - Your chosen **number of days**
  - Your current combined **Dexter + Indiana oz/day**
"""
)

# -------------------------------------------------------------------
# Embedded recipe data (extracted from your Excel)
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
            # Column F = "Large x1.75" 7-day batch
            {"name": "Chicken Thighs",     "base_7day_amount": 75.25,  "unit": "oz"},
            {"name": "Chicken Liver",      "base_7day_amount": 24.5,   "unit": "oz"},
            {"name": "Apple",              "base_7day_amount": 8.4,    "unit": "oz"},
            {"name": "Carrots",            "base_7day_amount": 14.0,   "unit": "oz"},
            {"name": "Kale",               "base_7day_amount": 14.0,   "unit": "oz"},
            {"name": "White Rice (Dry)",   "base_7day_amount": 19.25,  "unit": "oz"},
            {"name": "Brown Rice (Dry)",   "base_7day_amount": 11.2,   "unit": "oz"},
            {"name": "Sunflower Oil",      "base_7day_amount": 2.625,  "unit": "tsp"},
            {"name": "Omega",              "base_7day_amount": 0.875,  "unit": "tsp"},
            {"name": "Flaxseed Oil",       "base_7day_amount": 0.875,  "unit": "tsp"},
            {"name": "Nutrient",           "base_7day_amount": 13.125, "unit": "tbsp"},
        ],
    },
    "Turkey": {
        "base_daily_oz": 30.0,   # Dex 19 + Indy 11
        "dex_default": 19.0,
        "indy_default": 11.0,
        "base_days": 7.0,
        "ingredients": [
            # Column F = "Large x1.2" 7-day batch
            {"name": "Ground Turkey",      "base_7day_amount": 6.0,   "unit": "lbs"},
            {"name": "Turkey Liver",       "base_7day_amount": 3.0,   "unit": "oz"},
            {"name": "Whole Wheat Pasta",  "base_7day_amount": 48.0,  "unit": "oz"},  # from "Pasta" 48 oz
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
            # Column F = "Large x1.25" 7-day batch
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
    # If you later want Fish: add it here in the same format once column F is populated
}

# -------------------------------------------------------------------
# UI: tabs for each meal type
# -------------------------------------------------------------------

tabs = st.tabs(list(RECIPE_DATA.keys()))

for tab, meal_name in zip(tabs, RECIPE_DATA.keys()):
    with tab:
        recipe = RECIPE_DATA[meal_name]
        base_daily_oz = recipe["base_daily_oz"]
        dex_default = recipe["dex_default"]
        indy_default = recipe["indy_default"]
        base_days = recipe["base_days"]
        ingredients = recipe["ingredients"]

        st.header(f"{meal_name} Recipe")

        # -----------------------------
        # 1) Days selection
        # -----------------------------
        st.subheader("How many days of food do you want to prep?")

        col_days_select, col_days_custom = st.columns([2, 1])

        with col_days_select:
            days_choice = st.radio(
                "Choose a prep duration:",
                ("3 days (short trip)", "7 days (one week)", "Custom number of days"),
                key=f"days_choice_{meal_name}",
            )

        if days_choice.startswith("3"):
            days = 3
        elif days_choice.startswith("7"):
            days = 7
        else:
            with col_days_custom:
                days = st.number_input(
                    "Custom days:",
                    min_value=1,
                    value=7,
                    step=1,
                    key=f"custom_days_{meal_name}",
                )

        # -----------------------------
        # 2) Dexter & Indiana daily intake
        # -----------------------------
        st.subheader("Dexter & Indiana Daily Intake")

        st.markdown("Use the original sheet values, or change what they eat per day.")

        change_portions = st.checkbox(
            "Change what Dexter and Indiana eat per day?",
            value=False,
            key=f"change_portions_{meal_name}",
        )

        if change_portions:
            dex_daily = st.number_input(
                "Dexter daily food (oz)",
                min_value=0.0,
                value=float(dex_default),
                step=0.5,
                key=f"dex_daily_{meal_name}",
            )
            indy_daily = st.number_input(
                "Indiana daily food (oz)",
                min_value=0.0,
                value=float(indy_default),
                step=0.5,
                key=f"indy_daily_{meal_name}",
            )
        else:
            dex_daily = dex_default
            indy_daily = indy_default
            st.info(
                f"Using **original recipe defaults**: "
                f"Dexter = {dex_daily:.1f} oz, Indiana = {indy_daily:.1f} oz.\n\n"
                "Tick the checkbox above if you want to change them."
            )

        total_daily_oz = dex_daily + indy_daily

        st.markdown(
            f"""
**Daily total for both dogs:** `{total_daily_oz:.2f} oz`  
**Prep duration:** `{int(days)} day(s)`
"""
        )

        if total_daily_oz == 0:
            st.warning("Total daily intake is 0 oz — increase Dexter or Indiana’s daily ounces.")
            continue

        # -----------------------------
        # 3) Scaling calculations
        # -----------------------------
        # scale_factor = (your_daily / base_daily) * (your_days / base_days)
        scale_factor = (total_daily_oz / base_daily_oz) * (days / base_days)

        rows = []
        for ing in ingredients:
            name = ing["name"]
            base_7 = ing["base_7day_amount"]
            unit = ing["unit"]

            # Per-day in original recipe, for base_daily_oz
            base_per_day = base_7 / base_days

            # Per-day for your current dogs’ intake
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

        result_df = pd.DataFrame(rows)

        # -----------------------------
        # 4) Display results
        # -----------------------------
        st.subheader("Ingredient Requirements (scaled from column F 7-day batch)")

        st.dataframe(result_df, use_container_width=True)

        st.markdown(
            f"""
**Recipe base daily (Dex + Indy):** `{base_daily_oz:.2f} oz`  
**Your combined daily:** `{total_daily_oz:.2f} oz`  
**Scale factor vs original 7-day batch:** `{scale_factor:.3f}`
"""
        )

        st.caption(
            f"All amounts for **{meal_name}** are scaled from the original column F 7-day batch "
            "and the base Dex/Indy daily oz from your JFFD sheet."
        )
