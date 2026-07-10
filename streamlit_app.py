import streamlit as st
import pandas as pd

st.set_page_config(page_title="JFFD DIY Meal Prep Calculator", layout="centered")

# Initialize session state for app version
if "app_version" not in st.session_state:
    st.session_state.app_version = "original"

# Callback to switch app versions
def set_version(version_name):
    st.session_state.app_version = version_name

# -------------------------------------------------------------------
# Embedded recipe data (no Excel needed)
# base_7day_amount = base batch for base_days with base_daily_oz total intake
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
    "Fish": {
        # Calibrated so that this 7-day batch matches your real use:
        # Dexter = 11.75 oz/meal x2 = 23.5; Indiana = 7 oz/meal x2 = 14 → 37.5 oz/day
        "base_daily_oz": 37.5,
        "dex_default": 23.5,
        "indy_default": 14.0,
        "base_days": 7.0,
        "ingredients": [
            {"name": "Whitefish (Cod/Pollock/Haddock)", "base_7day_amount": 7.20, "unit": "lbs"},
            {"name": "Sweet Potatoes (with skin)",      "base_7day_amount": 4.96, "unit": "lbs"},
            {"name": "Russet Potatoes (with skin)",     "base_7day_amount": 4.96, "unit": "lbs"},
            {"name": "Green Beans",                     "base_7day_amount": 9.34, "unit": "oz"},
            {"name": "Broccoli",                        "base_7day_amount": 9.34, "unit": "oz"},
            {"name": "Sunflower Oil",                   "base_7day_amount": 6.23, "unit": "oz"},
            {"name": "Lemon Juice",                     "base_7day_amount": 3.11, "unit": "oz"},
            {"name": "Flaxseed (ground)",               "base_7day_amount": 2.33, "unit": "oz"},
            {"name": "Dried Seaweed (unseasoned Nori)", "base_7day_amount": 0.78, "unit": "oz"},
            {"name": "Fish & Sweet Potatoes DIY Nutrient Blend", "base_7day_amount": 3.11, "unit": "tbsp"},
        ],
    },
}

def show_original_version():
    col_hdr, col_btn = st.columns([3, 1])
    with col_hdr:
        st.title("JFFD DIY Meal Prep Calculator 🐶")
    with col_btn:
        st.write("")
        st.write("")
        st.button("✨ Try Clean Version", on_click=set_version, args=("clean",))

    st.markdown(
        """
This calculator uses **baked-in recipes** from your JFFD DIY sheet.

For each recipe (Chicken / Turkey / Beef / Fish):

- The baked-in amounts are a **7-day batch**
- Each batch is calibrated to the original **Dex + Indy daily ounces**
- You can scale based on:
  - How many **days** you want to prep
  - How much **Dexter & Indiana eat per day now (oz)**

Main proteins are shown in **pounds**, other ingredients keep their original units.
"""
    )

    # -------------------------------------------------------------------
    # Recipe selector (centered layout)
    # -------------------------------------------------------------------

    st.subheader("1. Choose Recipe")

    selected_recipe_name = st.selectbox(
        "Select which meal you are prepping:",
        list(RECIPE_DATA.keys()),
        key="orig_recipe_select"
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
**Original 7-day batch:** values baked in from your DIY sheet / calibration.
"""
    )

    # -------------------------------------------------------------------
    # 2) How many days?
    # -------------------------------------------------------------------

    st.subheader("2. How many days of food do you want to prep?")

    days_choice = st.radio(
        "Prep duration:",
        ("3 days (short trip)", "7 days (one week)", "Custom number of days"),
        key="orig_days_choice"
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
            key="orig_custom_days"
        )

    if days is None:
        st.warning("Please enter a valid number of days.")
        st.stop()

    # -------------------------------------------------------------------
    # 3) Dexter & Indiana daily intake
    # -------------------------------------------------------------------

    st.subheader("3. Dexter & Indiana's Daily Intake")

    st.markdown("Use the original recipe values, or change what they eat now:")

    change_portions = st.checkbox(
        "Change what Dexter and Indiana eat per day?",
        value=False,
        key="orig_change_portions"
    )

    if change_portions:
        dex_daily = st.number_input(
            "Dexter daily food (oz)",
            min_value=0.0,
            value=float(dex_default),
            step=0.5,
            key=f"orig_dex_{selected_recipe_name}",
        )
        indy_daily = st.number_input(
            "Indiana daily food (oz)",
            min_value=0.0,
            value=float(indy_default),
            step=0.5,
            key=f"orig_indy_{selected_recipe_name}",
        )
    else:
        dex_daily = dex_default
        indy_daily = indy_default
        st.info(
            f"Using original **{selected_recipe_name}** defaults: "
            f"Dexter = {dex_daily:.1f} oz, Indiana = {indy_daily:.1f} oz.\n\n"
            "Tick the checkbox above if you want to change them."
        )

    if dex_daily is None or indy_daily is None:
        st.warning("Please enter valid food portions.")
        st.stop()

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
    print_rows = []

    for ing in ingredients:
        name = ing["name"]
        base_7 = ing["base_7day_amount"]
        unit = ing["unit"]

        # Per-day in original recipe for that recipe's base_daily_oz
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

    st.dataframe(result_df, width="content")

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

    show_print = st.checkbox("Show print-friendly summary (totals only)", key="orig_show_print")

    if show_print:
        st.markdown(
            f"**Print view for {selected_recipe_name} – Total for {int(days)} days**"
        )
        st.table(print_df)

    if selected_recipe_name == "Chicken":
        st.caption(
            "Chicken Thighs 7-day batch was **75.25 oz**, converted here to "
            "`4.703 lb` so the protein is shown in pounds. All other ingredients "
            "retain their original units."
        )
    elif selected_recipe_name == "Fish":
        st.caption(
            "Fish recipe is calibrated so that a 7-day batch uses **7.2 lb of fish** "
            "and matches Dexter at 11.75 oz/meal (twice daily) and Indiana at 7 oz/meal "
            "(twice daily), for a total of 37.5 oz/day."
        )
    else:
        st.caption(
            "All amounts are scaled from the original 7-day batch values for this recipe."
        )


def show_clean_version():
    # Style Header & Switch Button in Columns
    col_hdr, col_btn = st.columns([3, 1])
    with col_hdr:
        st.markdown("<h1 style='margin-bottom: 0px;'>JFFD DIY Meal Prep Calculator 🐶</h1>", unsafe_allow_html=True)
        st.markdown("<p style='font-size: 1.15rem; color: #556b2f; margin-top: 0px; font-weight: 400;'>Clean & Modern Version</p>", unsafe_allow_html=True)
    with col_btn:
        st.write("")
        st.button("🔙 Original Version", on_click=set_version, args=("original",))

    # Custom CSS for styling
    st.markdown(
        """
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;500;600;700&display=swap');
        
        /* Apply Outfit font and larger base text size */
        html, body, [data-testid="stAppViewContainer"], [class*="css"] {
            font-family: 'Outfit', sans-serif !important;
            font-size: 19px !important;
        }
        
        /* Titles and Headers */
        h1 {
            font-size: 2.8rem !important;
            font-weight: 700 !important;
            color: #2e5a32 !important; /* Forest Green */
        }
        
        /* Custom Cards for UI Sections */
        .clean-section {
            background-color: #f7f9f6;
            border-radius: 12px;
            padding: 20px;
            border-left: 6px solid #4a7c59;
            margin-top: 25px;
            margin-bottom: 15px;
            box-shadow: 0 4px 12px rgba(0, 0, 0, 0.04);
        }
        
        .clean-section-title {
            font-size: 1.3rem;
            font-weight: 600;
            color: #2e5a32;
        }
        
        /* Metric styling */
        .metric-container {
            display: flex;
            justify-content: space-around;
            background-color: #edf2ed;
            border-radius: 10px;
            padding: 15px;
            margin-top: 20px;
            margin-bottom: 25px;
            border: 1px solid #c8dcd0;
        }
        
        .metric-box {
            text-align: center;
        }
        
        .metric-val {
            font-size: 2rem;
            font-weight: 700;
            color: #2e5a32;
        }
        
        .metric-lbl {
            font-size: 0.95rem;
            color: #555555;
            text-transform: uppercase;
            letter-spacing: 0.5px;
            margin-top: 4px;
        }
        
        /* Bigger Font for inputs and checkboxes */
        .stRadio label, .stSelectbox label, .stNumberInput label {
            font-size: 1.15rem !important;
            font-weight: 500 !important;
            color: #333333 !important;
        }
        
        /* Custom caption styling */
        .custom-caption {
            font-size: 0.95rem !important;
            color: #565656 !important;
            line-height: 1.5;
            background-color: #fcfcfc;
            border: 1px solid #eef2ef;
            border-radius: 8px;
            padding: 15px;
            margin-top: 20px;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )

    # 1) Choose Recipe and Dog Selection
    st.markdown(
        """
        <div class='clean-section'>
            <div class='clean-section-title'>📋 Step 1: Recipe & Dog Selection</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    col_rec, col_dog = st.columns([1, 1])

    with col_rec:
        selected_recipe_name = st.selectbox(
            "Select recipe to prep:",
            list(RECIPE_DATA.keys()),
            key="clean_recipe_select"
        )
        recipe = RECIPE_DATA[selected_recipe_name]
        base_daily_oz = recipe["base_daily_oz"]
        dex_default = recipe["dex_default"]
        indy_default = recipe["indy_default"]
        base_days = recipe["base_days"]
        ingredients = recipe["ingredients"]

    with col_dog:
        dog_choice = st.radio(
            "Prepare food for:",
            ("Both Dogs (Dexter & Indiana)", "Dexter Only", "Indiana Only"),
            key="clean_dog_choice"
        )

    # 2) Daily portions (Only showing relevant inputs)
    st.markdown(
        """
        <div class='clean-section'>
            <div class='clean-section-title'>⚖️ Step 2: Daily Portions & Prep Duration</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    col_port, col_days = st.columns([1, 1])

    with col_port:
        if dog_choice == "Both Dogs (Dexter & Indiana)":
            dex_daily = st.number_input(
                "Dexter daily food (oz):",
                min_value=0.0,
                value=float(dex_default),
                step=0.5,
                key=f"clean_dex_{selected_recipe_name}"
            )
            indy_daily = st.number_input(
                "Indiana daily food (oz):",
                min_value=0.0,
                value=float(indy_default),
                step=0.5,
                key=f"clean_indy_{selected_recipe_name}"
            )
            if dex_daily is None or indy_daily is None:
                st.warning("Please enter valid food portions.")
                st.stop()
            total_daily_oz = dex_daily + indy_daily
        elif dog_choice == "Dexter Only":
            dex_daily = st.number_input(
                "Dexter daily food (oz):",
                min_value=0.0,
                value=float(dex_default),
                step=0.5,
                key=f"clean_dex_only_{selected_recipe_name}"
            )
            if dex_daily is None:
                st.warning("Please enter a valid daily food portion.")
                st.stop()
            indy_daily = 0.0
            total_daily_oz = dex_daily
            st.info("🐶 Preparing food for Dexter only. Indiana is excluded.")
        else: # Indiana Only
            indy_daily = st.number_input(
                "Indiana daily food (oz):",
                min_value=0.0,
                value=float(indy_default),
                step=0.5,
                key=f"clean_indy_only_{selected_recipe_name}"
            )
            if indy_daily is None:
                st.warning("Please enter a valid daily food portion.")
                st.stop()
            dex_daily = 0.0
            total_daily_oz = indy_daily
            st.info("🐶 Preparing food for Indiana only. Dexter is excluded.")

    with col_days:
        days_choice = st.radio(
            "Prep duration (days):",
            ("3 days (short trip)", "7 days (one week)", "Custom number of days"),
            key="clean_days_choice"
        )
        if days_choice.startswith("3"):
            days = 3
        elif days_choice.startswith("7"):
            days = 7
        else:
            days = st.number_input(
                "Enter custom days:",
                min_value=1,
                value=7,
                step=1,
                key="clean_custom_days"
            )
        if days is None:
            st.warning("Please enter a valid number of days.")
            st.stop()

    if total_daily_oz == 0:
        st.warning("⚠️ Total daily intake is 0 oz — please increase the daily ounces.")
        st.stop()

    # Calculate scale factor
    scale_factor = (total_daily_oz / base_daily_oz) * (days / base_days)

    # 3) Display Metrics Summary
    st.markdown(
        f"""
        <div class="metric-container">
            <div class="metric-box">
                <div class="metric-val">{total_daily_oz:.1f} oz</div>
                <div class="metric-lbl">Daily Intake</div>
            </div>
            <div class="metric-box">
                <div class="metric-val">{int(days)}</div>
                <div class="metric-lbl">Prep Days</div>
            </div>
            <div class="metric-box">
                <div class="metric-val">{scale_factor:.3f}x</div>
                <div class="metric-lbl">Scale Factor</div>
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

    # Calculate rows
    rows = []
    print_rows = []

    for ing in ingredients:
        name = ing["name"]
        base_7 = ing["base_7day_amount"]
        unit = ing["unit"]

        # Per-day in original recipe for that recipe's base_daily_oz
        base_per_day = base_7 / base_days

        # Per-day for your current combined intake
        per_day_yours = base_per_day * (total_daily_oz / base_daily_oz)

        # Total for chosen period
        total_period = base_7 * scale_factor

        rows.append(
            {
                "Ingredient": name,
                "Per Day": f"{per_day_yours:.3f} {unit}",
                f"Total for {int(days)} days": f"{total_period:.3f} {unit}",
            }
        )

        print_rows.append(
            {
                "Ingredient": name,
                f"Total for {int(days)} days": f"{total_period:.3f} {unit}",
            }
        )

    result_df = pd.DataFrame(rows)
    print_df = pd.DataFrame(print_rows)

    # 4) Ingredients requirements table
    st.markdown(
        """
        <div class='clean-section'>
            <div class='clean-section-title'>🛒 Step 3: Ingredient Requirements</div>
        </div>
        """,
        unsafe_allow_html=True,
    )
    
    st.dataframe(result_df, width="content")

    # 5) Print friendly view
    st.markdown(
        """
        <div class='clean-section'>
            <div class='clean-section-title'>🖨️ Step 4: Print Summary</div>
        </div>
        """,
        unsafe_allow_html=True,
    )
    
    show_print = st.checkbox("Show print-friendly summary (totals only)", key="clean_show_print")
    if show_print:
        st.markdown(f"**Print view for {selected_recipe_name} – Total for {int(days)} days ({dog_choice})**")
        st.table(print_df)

    # Recipe-specific calibration captions
    if selected_recipe_name == "Chicken":
        st.markdown(
            """
            <div class="custom-caption">
                💡 <b>Recipe Info:</b> Chicken Thighs 7-day batch was <b>75.25 oz</b>, 
                converted here to <b>4.703 lb</b> so the protein is shown in pounds. 
                All other ingredients retain their original units.
            </div>
            """,
            unsafe_allow_html=True
        )
    elif selected_recipe_name == "Fish":
        st.markdown(
            """
            <div class="custom-caption">
                💡 <b>Recipe Info:</b> Fish recipe is calibrated so that a 7-day batch uses <b>7.2 lb of fish</b> 
                and matches Dexter at 11.75 oz/meal (twice daily) and Indiana at 7 oz/meal (twice daily), 
                for a total of 37.5 oz/day.
            </div>
            """,
            unsafe_allow_html=True
        )
    else:
        st.markdown(
            """
            <div class="custom-caption">
                💡 <b>Recipe Info:</b> All amounts are scaled from the original 7-day batch values for this recipe.
            </div>
            """,
            unsafe_allow_html=True
        )


# Render version based on session state
if st.session_state.app_version == "clean":
    show_clean_version()
else:
    show_original_version()
