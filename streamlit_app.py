import streamlit as st
import pandas as pd

st.set_page_config(page_title="JFFD DIY Meal Prep Calculator", layout="centered")

# -------------------------------------------------------------------
# Persistent State Initialization
# -------------------------------------------------------------------
if "app_version" not in st.session_state:
    st.session_state.app_version = "original"

# Initialize default portion sizes for Dexter and Indiana
if "dex_portions" not in st.session_state:
    st.session_state.dex_portions = {
        "Chicken": 22.0,
        "Turkey": 19.0,
        "Beef": 20.0,
        "Fish": 23.5
    }
if "indy_portions" not in st.session_state:
    st.session_state.indy_portions = {
        "Chicken": 14.0,
        "Turkey": 11.0,
        "Beef": 12.0,
        "Fish": 14.0
    }

# Callback to switch app versions
def set_version(version_name):
    st.session_state.app_version = version_name

# -------------------------------------------------------------------
# Embedded Recipe Data
# -------------------------------------------------------------------
RECIPE_DATA = {
    "Chicken": {
        "base_daily_oz": 36.0,   # Dex 22 + Indy 14
        "dex_default": 22.0,
        "indy_default": 14.0,
        "base_days": 7.0,
        "ingredients": [
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
        "base_daily_oz": 37.5,   # Dex 23.5 + Indy 14
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

# -------------------------------------------------------------------
# ORIGINAL VERSION SCREEN
# -------------------------------------------------------------------
def show_original_version():
    col_hdr, col_btn = st.columns([3, 1])
    with col_hdr:
        st.title("JFFD DIY Meal Prep Calculator 🐶")
    with col_btn:
        st.write("")
        st.write("")
        st.button("✨ Try Mobile App UI", on_click=set_version, args=("clean",))

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

    st.subheader("1. Choose Recipe")

    selected_recipe_name = st.selectbox(
        "Select which meal you are prepping:",
        list(RECIPE_DATA.keys()),
        key="orig_recipe_select"
    )

    recipe = RECIPE_DATA[selected_recipe_name]
    base_daily_oz = recipe["base_daily_oz"]
    
    # Read portions from session state or default config
    dex_default = st.session_state.dex_portions.get(selected_recipe_name, recipe["dex_default"])
    indy_default = st.session_state.indy_portions.get(selected_recipe_name, recipe["indy_default"])
    base_days = recipe["base_days"]
    ingredients = recipe["ingredients"]

    st.markdown(
        f"""
**Selected recipe:** `{selected_recipe_name}`  
**Original base daily (Dex + Indy):** `{base_daily_oz:.1f} oz/day`  
**Original 7-day batch:** values baked in from your DIY sheet / calibration.
"""
    )

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

    st.subheader("3. Dexter & Indiana's Daily Intake")
    st.markdown("Use the default portions, or change what they eat now:")

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
            f"Using active defaults: Dexter = {dex_daily:.1f} oz, Indiana = {indy_daily:.1f} oz.\n\n"
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

    # Scale factor
    scale_factor = (total_daily_oz / base_daily_oz) * (days / base_days)

    rows = []
    print_rows = []

    for ing in ingredients:
        name = ing["name"]
        base_7 = ing["base_7day_amount"]
        unit = ing["unit"]

        base_per_day = base_7 / base_days
        per_day_yours = base_per_day * (total_daily_oz / base_daily_oz)
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

    st.subheader("4. Ingredient Requirements (scaled from 7-day batch)")
    st.dataframe(result_df, use_container_width=True)

    st.markdown(
        f"""
**Base daily (original {selected_recipe_name} recipe):** `{base_daily_oz:.2f} oz/day`  
**Your combined daily:** `{total_daily_oz:.2f} oz/day`  
**Scale factor vs original 7-day batch:** `{scale_factor:.3f}`  
"""
    )

    st.subheader("5. Print-Friendly Summary")
    show_print = st.checkbox("Show print-friendly summary (totals only)", key="orig_show_print")

    if show_print:
        st.markdown(f"**Print view for {selected_recipe_name} – Total for {int(days)} days**")
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
        st.caption("All amounts are scaled from the original 7-day batch values for this recipe.")

# -------------------------------------------------------------------
# MOBILE-FIRST CLEAN VERSION SCREEN
# -------------------------------------------------------------------
def show_clean_version():
    # Inject mobile app styling & Outfit Font
    st.markdown(
        """
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;500;600;700&display=swap');
        
        /* Mobile-First Frame Emulator for Desktop */
        @media (min-width: 600px) {
            .main .block-container {
                max-width: 440px !important;
                padding: 40px 24px 30px 24px !important;
                border: 12px solid #2e3033 !important; /* Phone Bezel */
                border-radius: 40px !important;
                box-shadow: 0 20px 40px rgba(0,0,0,0.15) !important;
                background-color: #ffffff !important;
                margin-top: 30px !important;
                margin-bottom: 30px !important;
                position: relative;
            }
            
            /* Notch Simulator */
            .main .block-container::before {
                content: "";
                position: absolute;
                top: 0;
                left: 50%;
                transform: translateX(-50%);
                width: 140px;
                height: 20px;
                background-color: #2e3033;
                border-bottom-left-radius: 12px;
                border-bottom-right-radius: 12px;
                z-index: 999;
            }
        }
        
        /* Apply fonts globally */
        html, body, [data-testid="stAppViewContainer"], [class*="css"] {
            font-family: 'Outfit', sans-serif !important;
            font-size: 18px !important;
        }
        
        /* Headers and Text */
        .app-title {
            font-size: 1.8rem !important;
            font-weight: 700 !important;
            color: #1e3f20 !important; /* Dark Green */
            margin-bottom: 4px !important;
            text-align: center;
        }
        
        .app-subtitle {
            font-size: 0.95rem !important;
            color: #556b2f !important;
            margin-top: 0px !important;
            margin-bottom: 20px !important;
            text-align: center;
            font-weight: 400;
        }
        
        /* Custom Mobile Cards */
        .mobile-card {
            background-color: #f8faf7;
            border-radius: 16px;
            padding: 16px;
            border: 1px solid #e6ede8;
            margin-bottom: 16px;
            box-shadow: 0 4px 10px rgba(0,0,0,0.02);
        }
        
        .card-header {
            font-size: 1.15rem;
            font-weight: 600;
            color: #1e3f20;
            margin-bottom: 12px;
            border-bottom: 1px solid #e1e9e3;
            padding-bottom: 6px;
        }
        
        /* Large Highlighted Metrics */
        .mobile-metrics {
            display: flex;
            justify-content: space-between;
            background-color: #edf2ed;
            border-radius: 14px;
            padding: 14px;
            margin-top: 15px;
            margin-bottom: 15px;
            border: 1px solid #d4ded4;
        }
        
        .metric-item {
            text-align: center;
            flex: 1;
        }
        
        .metric-val {
            font-size: 1.55rem;
            font-weight: 700;
            color: #1e3f20;
        }
        
        .metric-lbl {
            font-size: 0.8rem;
            color: #666666;
            text-transform: uppercase;
            letter-spacing: 0.5px;
            margin-top: 3px;
        }

        /* Ingredient Plate styling */
        .ingredient-plate {
            background-color: #edf2ed;
            border-radius: 12px;
            padding: 12px 16px;
            border-left: 5px solid #4a7c59;
            margin-bottom: 10px;
            display: flex;
            justify-content: space-between;
            align-items: center;
            box-shadow: 0 2px 6px rgba(0,0,0,0.02);
            border-top: 1px solid #e1e9e3;
            border-right: 1px solid #e1e9e3;
            border-bottom: 1px solid #e1e9e3;
        }
        
        .plate-name {
            font-weight: 600;
            color: #1e3f20;
            font-size: 1.05rem;
        }
        
        .plate-subtext {
            font-size: 0.85rem;
            color: #555555;
            margin-top: 2px;
        }
        
        .plate-val {
            font-size: 1.3rem;
            font-weight: 700;
            color: #1e3f20;
            text-align: right;
        }
        
        /* Bigger Font for inputs and checkboxes */
        .stRadio label, .stSelectbox label, .stNumberInput label {
            font-size: 1.15rem !important;
            font-weight: 500 !important;
            color: #333333 !important;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )

    # App Header
    st.markdown("<div class='app-title'>DIMeal App 🐾</div>", unsafe_allow_html=True)
    st.markdown("<div class='app-subtitle'>JFFD DIY Meal Prep Companion</div>", unsafe_allow_html=True)

    # Version toggle button inside the container
    col_btn = st.columns([1])[0]
    col_btn.button("🔙 Switch to Original Calculator", on_click=set_version, args=("original",), use_container_width=True)
    st.write("")

    # Mobile Tab Navigation
    tab_calc, tab_recipes, tab_dogs, tab_guide = st.tabs([
        "⚖️ Calculator",
        "📚 Recipes",
        "🐶 Profiles",
        "🍳 Prep Guide"
    ])

    # --------------------------------------------------------
    # TAB 1: CALCULATOR
    # --------------------------------------------------------
    with tab_calc:
        # Recipe Selection
        st.markdown("<div class='mobile-card'><div class='card-header'>Recipe & Dog Selection</div>", unsafe_allow_html=True)
        selected_recipe_name = st.selectbox(
            "Select recipe to prepare:",
            list(RECIPE_DATA.keys()),
            key="clean_recipe_select"
        )
        recipe = RECIPE_DATA[selected_recipe_name]
        base_daily_oz = recipe["base_daily_oz"]
        base_days = recipe["base_days"]
        ingredients = recipe["ingredients"]

        # Dog Selection
        dog_choice = st.radio(
            "Prepare food for:",
            ("Both Dogs (Dexter & Indiana)", "Dexter Only", "Indiana Only"),
            key="clean_dog_choice"
        )
        st.markdown("</div>", unsafe_allow_html=True)

        # Portions & Duration
        st.markdown("<div class='mobile-card'><div class='card-header'>Portions & Duration</div>", unsafe_allow_html=True)
        
        # Load defaults dynamically from session state
        dex_default = st.session_state.dex_portions.get(selected_recipe_name, recipe["dex_default"])
        indy_default = st.session_state.indy_portions.get(selected_recipe_name, recipe["indy_default"])

        if dog_choice == "Both Dogs (Dexter & Indiana)":
            dex_daily = st.number_input(
                "Dexter portion (oz/day):",
                min_value=0.0,
                value=float(dex_default),
                step=0.5,
                key=f"clean_dex_{selected_recipe_name}"
            )
            indy_daily = st.number_input(
                "Indiana portion (oz/day):",
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
                "Dexter portion (oz/day):",
                min_value=0.0,
                value=float(dex_default),
                step=0.5,
                key=f"clean_dex_only_{selected_recipe_name}"
            )
            if dex_daily is None:
                st.warning("Please enter a valid portion size.")
                st.stop()
            indy_daily = 0.0
            total_daily_oz = dex_daily
        else: # Indiana Only
            indy_daily = st.number_input(
                "Indiana portion (oz/day):",
                min_value=0.0,
                value=float(indy_default),
                step=0.5,
                key=f"clean_indy_only_{selected_recipe_name}"
            )
            if indy_daily is None:
                st.warning("Please enter a valid portion size.")
                st.stop()
            dex_daily = 0.0
            total_daily_oz = indy_daily

        # Quick Portion Actions (Zero / Reset Shortcuts)
        st.markdown("<p style='font-size: 0.9rem; color: #555555; margin-bottom: 6px; font-weight: 600;'>Quick Actions:</p>", unsafe_allow_html=True)
        col_z1, col_z2, col_z3 = st.columns(3)
        with col_z1:
            if st.button("Zero Dex 🚫", key=f"zero_dex_btn_{selected_recipe_name}", use_container_width=True):
                st.session_state[f"clean_dex_{selected_recipe_name}"] = 0.0
                st.session_state[f"clean_dex_only_{selected_recipe_name}"] = 0.0
                st.rerun()
        with col_z2:
            if st.button("Zero Indy 🚫", key=f"zero_indy_btn_{selected_recipe_name}", use_container_width=True):
                st.session_state[f"clean_indy_{selected_recipe_name}"] = 0.0
                st.session_state[f"clean_indy_only_{selected_recipe_name}"] = 0.0
                st.rerun()
        with col_z3:
            if st.button("Reset 🔄", key=f"reset_defaults_btn_{selected_recipe_name}", use_container_width=True):
                st.session_state[f"clean_dex_{selected_recipe_name}"] = float(dex_default)
                st.session_state[f"clean_indy_{selected_recipe_name}"] = float(indy_default)
                st.session_state[f"clean_dex_only_{selected_recipe_name}"] = float(dex_default)
                st.session_state[f"clean_indy_only_{selected_recipe_name}"] = float(indy_default)
                st.rerun()

        # Days Choice
        days_choice = st.radio(
            "Prep duration (days):",
            ("3 days (trip)", "7 days (week)", "Custom days"),
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
            
        st.markdown("</div>", unsafe_allow_html=True)

        if total_daily_oz == 0:
            st.warning("Total daily intake cannot be 0 oz.")
            st.stop()

        # Calculate scale factor
        scale_factor = (total_daily_oz / base_daily_oz) * (days / base_days)

        # Display Mobile Metrics (Intake, Days, Scale Plates)
        st.markdown(
            f"""
            <div class="mobile-metrics">
                <div class="metric-item">
                    <div class="metric-val">{total_daily_oz:.1f} oz</div>
                    <div class="metric-lbl">Daily Intake</div>
                </div>
                <div class="metric-item">
                    <div class="metric-val">{int(days)}</div>
                    <div class="metric-lbl">Days</div>
                </div>
                <div class="metric-item">
                    <div class="metric-val">{scale_factor:.2f}x</div>
                    <div class="metric-lbl">Scale</div>
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

        # Ingredients requirements custom plates rendering
        st.markdown("<div class='mobile-card'><div class='card-header'>🛒 Scaled Ingredients</div>", unsafe_allow_html=True)
        
        print_rows = []
        for ing in ingredients:
            name = ing["name"]
            base_7 = ing["base_7day_amount"]
            unit = ing["unit"]

            base_per_day = base_7 / base_days
            per_day_yours = base_per_day * (total_daily_oz / base_daily_oz)
            total_period = base_7 * scale_factor

            # Render custom UI plates matching the metric theme
            st.markdown(
                f"""
                <div class="ingredient-plate">
                    <div>
                        <div class="plate-name">{name}</div>
                        <div class="plate-subtext">Daily: {per_day_yours:.2f} {unit}</div>
                    </div>
                    <div class="plate-val">
                        {total_period:.2f} {unit}
                    </div>
                </div>
                """,
                unsafe_allow_html=True
            )
            
            print_rows.append({
                "Ingredient": name,
                f"Total ({int(days)}d)": f"{total_period:.2f} {unit}"
            })

        print_df = pd.DataFrame(print_rows)
        st.markdown("</div>", unsafe_allow_html=True)

        # Recipe description captions
        if selected_recipe_name == "Chicken":
            st.caption("Chicken Thighs are shown in lbs (converted from original 75.25 oz). Other items keep original units.")
        elif selected_recipe_name == "Fish":
            st.caption("Fish recipe is calibrated so that a 7-day batch uses 7.2 lbs of fish (calibrated for Dex 23.5 oz and Indy 14 oz daily).")

        # Print Friendly Checkbox
        show_print = st.checkbox("Show print-friendly summary", key="clean_show_print")
        if show_print:
            st.markdown(f"**Print view – Total for {int(days)} days ({dog_choice})**")
            st.table(print_df)

    # --------------------------------------------------------
    # TAB 2: RECIPES LIBRARY
    # --------------------------------------------------------
    with tab_recipes:
        st.markdown("### JFFD Recipes Info")
        for r_name, r_info in RECIPE_DATA.items():
            with st.expander(f"📚 {r_name} Recipe"):
                st.write(f"**Original Base Intake (Dex + Indy):** {r_info['base_daily_oz']} oz/day")
                st.write(f"**Calibrated 7-day batch ingredients:**")
                for ing in r_info["ingredients"]:
                    st.write(f"- {ing['name']}: **{ing['base_7day_amount']:.3f} {ing['unit']}**")

    # --------------------------------------------------------
    # TAB 3: DOGS PROFILE
    # --------------------------------------------------------
    with tab_dogs:
        st.markdown("### Dog Profiles 🐶")
        st.write("Customize default daily food portions (oz) for Dexter and Indiana. Changes update the calculator defaults dynamically.")

        # Dexter Card
        st.markdown("<div class='mobile-card'><div class='card-header'>Dexter Portions (oz)</div>", unsafe_allow_html=True)
        for r_name in RECIPE_DATA.keys():
            st.session_state.dex_portions[r_name] = st.number_input(
                f"{r_name} default daily portion:",
                min_value=0.0,
                value=float(st.session_state.dex_portions[r_name]),
                step=0.5,
                key=f"profile_dex_{r_name}"
            )
        st.markdown("</div>", unsafe_allow_html=True)

        # Indiana Card
        st.markdown("<div class='mobile-card'><div class='card-header'>Indiana Portions (oz)</div>", unsafe_allow_html=True)
        for r_name in RECIPE_DATA.keys():
            st.session_state.indy_portions[r_name] = st.number_input(
                f"{r_name} default daily portion:",
                min_value=0.0,
                value=float(st.session_state.indy_portions[r_name]),
                step=0.5,
                key=f"profile_indy_{r_name}"
            )
        st.markdown("</div>", unsafe_allow_html=True)

    # --------------------------------------------------------
    # TAB 4: PREP GUIDE
    # --------------------------------------------------------
    with tab_guide:
        st.markdown("### Meal Prep Checklist 🍳")
        st.write("Keep track of your JFFD DIY batch cooking steps:")

        st.checkbox("🛒 1. Shop for ingredients (proteins, veggies, starch, oils, nutrients)", key="ch_shop")
        st.checkbox("🍗 2. Weigh & cook protein (e.g. Ground Turkey, Chicken Thighs)", key="ch_cook")
        st.checkbox("🍚 3. Steam/boil carbohydrates (Rice, Sweet Potatoes, or Pasta)", key="ch_carbs")
        st.checkbox("🥦 4. Puree or steam vegetables (Carrots, Broccoli, Zucchini, etc.)", key="ch_veggies")
        st.checkbox("🥣 5. Mix all cooked ingredients, oils, and nutrients thoroughly in a large bowl", key="ch_mix")
        st.checkbox("📦 6. Portion out daily/weekly amounts into containers and freeze", key="ch_freeze")

        st.info("💡 **Nutrient Blend Tip:** Always make sure foods are cool before adding JFFD DIY Nutrient Blend to preserve vitamins.")

# -------------------------------------------------------------------
# ROUTING
# -------------------------------------------------------------------
if st.session_state.app_version == "clean":
    show_clean_version()
else:
    show_original_version()
