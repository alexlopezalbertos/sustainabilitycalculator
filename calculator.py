import streamlit as st
import pandas as pd
import io

# ======================================================= 0. Page config and Title =======================================================================
st.set_page_config(
    page_title="Sustainability Calculator",
    page_icon="icon.png",
    initial_sidebar_state="expanded",
)

# Create a placeholder for the dynamic title
title_placeholder = st.empty()

# Static default title
default_title = "Sustainability Calculator"

st.header("Initiative Master Data", divider="red")
# Inputs
# ================================================================== 1. BASE DATA ====================================================================================
st.subheader("1️⃣ Base Data")
c1, c2, c3 = st.columns(3)
with c1:
    cm = st.selectbox("Select CM", (
        "BlueSun", "Carpenter", "Colep", "Dr Schumacher", "Expac", "Farmol Berlingo",
        "Farmol CN & Colep", "Farmol Comun Nuovo", "Hayco China", "Hayco DR", "Kompak",
        "McBride Italy", "McBride Poland", "McBride Spain", "PTG", "Zobele"
    ), index=None, help=":blue[[SL/MPD]] Introduce the CM name")
with c2:
    initiative_name = st.text_input("Initiative Name", help=":blue[[SL/SIEL]] Introduce the CM name")
with c3:
    fpc = st.text_input("FPC number example", help=":blue[[MPD]] For the current execution, provide an example of any released FPC.")

initiative_description = st.text_input("Describe the initiative in one sentence", help=":blue[[SL/SIEL]]")

# Update the title with the initiative name if present
if initiative_name:
    title_placeholder.title(f"♻️ Sustainability Calculator :blue[{initiative_name}]")
else:
    title_placeholder.title(default_title)

# ================================================================== 2. VOLUMES ====================================================================================
st.subheader("2️⃣ Volumes")
c1, c2 = st.columns(2)
with c1:
    yearly_volume = st.number_input("Total yearly volume (MSU)", step=0.01, format="%f", help=":blue[[SL]] Introduce the total forecasted yearly volume in MSU")
with c2:
    st.write('')

c1, c2 = st.columns(2)
with c1:
    su_factor_c = st.number_input(":blue[**Current**] Case SU factor", step=0.001, format="%.3f", help=":blue[[MPD]] Can be found in [CDB](https://rdc.internal.pg.com/)")
    items_case_c = st.number_input(":blue[**Current**] Items/Case", step=1, format="%d", help=":blue[[MPD]] Can be found in [CDB](https://rdc.internal.pg.com/)")
with c2:
    su_factor_n = st.number_input(":red[**New**] Case SU factor", step=0.001, format="%.3f", help=":blue[[MPD]] Can be found in [CDB](https://rdc.internal.pg.com/)")
    items_case_n = st.number_input(":red[**New**] Items/Case", step=1, format="%d", help=":blue[[MPD]] Can be found in [CDB](https://rdc.internal.pg.com/)")

cases_total_c = (yearly_volume / su_factor_c) * 1000 if su_factor_c else 0
cases_total_n = (yearly_volume / su_factor_n) * 1000 if su_factor_n else 0
items_total_c = cases_total_c * items_case_c
items_total_n = cases_total_n * items_case_n

# ================================================================== 3. TRANSPORTATION ====================================================================================
st.subheader("3️⃣ Transportation")
transport_modes = st.multiselect("Select all transportation modes", ["🚚 Road", "🚢 Sea"], help=":blue[[SL/SIEL]] Introduce all transportation modes that apply")

if "🚢 Sea" in transport_modes:
    c1, c2 = st.columns(2)
    with c1:
        cases_sea_c = st.number_input(":blue[**Current**] number of Cases/Container", step=1, format="%d", help=":blue[[MPD]] Introduce the current number of cases/container")
    with c2:
        cases_sea_n = st.number_input(":red[**New**] number of Cases/Container", step=1, format="%d", help=":blue[[MPD]] Introduce the new number of cases/container")

if "🚚 Road" in transport_modes:
    pallet_factors = {"B1": 66, "B2": 33, "C1": 52, "C2": 26}
    cases_per_truck_current_eu = cases_per_truck_current_uk = 0
    cases_per_truck_new_eu = cases_per_truck_new_uk = 0

    # EU Pallets
    c1, c2, c3, c4 = st.columns(4)
    with c1:
        pallet_type_eu_c = st.selectbox(":blue[**Current**] EU pallet type", ["B1", "B2", "N/A"], index=None, help=":blue[[MPD]]")
    with c2:
        if pallet_type_eu_c == "B1":
            cases_b1_c = st.number_input(":blue[**Current**] Cases/Pallet B1", step=1, format="%d", help=":blue[[MPD]]")
            cases_per_truck_current_eu = cases_b1_c * pallet_factors["B1"]
        elif pallet_type_eu_c == "B2":
            cases_b2_c = st.number_input(":blue[**Current**] Cases/Pallet B2", step=1, format="%d", help=":blue[[MPD]]")
            cases_per_truck_current_eu = cases_b2_c * pallet_factors["B2"]

    with c3:
        pallet_type_eu_n = st.selectbox(":red[**New**] EU pallet type", ["B1", "B2", "N/A"], index=None, help=":blue[[MPD]]")
    with c4:
        if pallet_type_eu_n == "B1":
            cases_b1_n = st.number_input(":red[**New**] Cases/Pallet B1", step=1, format="%d", help=":blue[[MPD]]")
            cases_per_truck_new_eu = cases_b1_n * pallet_factors["B1"]
        elif pallet_type_eu_n == "B2":
            cases_b2_n = st.number_input(":red[**New**] Cases/Pallet B2", step=1, format="%d", help=":blue[[MPD]]")
            cases_per_truck_new_eu = cases_b2_n * pallet_factors["B2"]

    # UK Pallets
    c5, c6, c7, c8 = st.columns(4)
    with c5:
        pallet_type_uk_c = st.selectbox(":blue[**Current**] UK pallet type", ["C1", "C2", "N/A"], index=None, help=":blue[[MPD]]")
    with c6:
        if pallet_type_uk_c == "C1":
            cases_c1_c = st.number_input(":blue[**Current**] Cases/Pallet C1", step=1, format="%d", help=":blue[[MPD]]")
            cases_per_truck_current_uk = cases_c1_c * pallet_factors["C1"]
        elif pallet_type_uk_c == "C2":
            cases_c2_c = st.number_input(":blue[**Current**] Cases/Pallet C2", step=1, format="%d", help=":blue[[MPD]]")
            cases_per_truck_current_uk = cases_c2_c * pallet_factors["C2"]

    with c7:
        pallet_type_uk_n = st.selectbox(":red[**New**] UK pallet type", ["C1", "C2", "N/A"], index=None, help=":blue[[MPD]]")
    with c8:
        if pallet_type_uk_n == "C1":
            cases_c1_n = st.number_input(":red[**New**] Cases/Pallet C1", step=1, format="%d", help=":blue[[MPD]]")
            cases_per_truck_new_uk = cases_c1_n * pallet_factors["C1"]
        elif pallet_type_uk_n == "C2":
            cases_c2_n = st.number_input(":red[**New**] Cases/Pallet C2", step=1, format="%d", help=":blue[[MPD]]")
            cases_per_truck_new_uk = cases_c2_n * pallet_factors["C2"]

# ================================================================== 4. WEIGHT DATA ====================================================================================
st.subheader("4️⃣ Weight")
c1, c2 = st.columns(2)
with c1:
    case_weight_c = st.number_input(":blue[**Current**] Case Weight [kg]", help=":blue[[MPD]] Weight of the current CUP. FPP Weights and Dimensions section in Enovia")
with c2:
    case_weight_n = st.number_input(":red[**New**] Case Weight [kg]", help=":blue[[MPD]] Weight of the new CUP. FPP Weights and Dimensions section in Enovia")

try:
    truck_eu_weight_c = case_weight_c * cases_per_truck_current_eu
    truck_eu_weight_n = case_weight_n * cases_per_truck_new_eu
    truck_uk_weight_c = case_weight_c * cases_per_truck_current_uk
    truck_uk_weight_n = case_weight_n * cases_per_truck_new_uk
except:  # You can specify a more specific exception if desire
    st.write("")


# ================================================================== 5. MATERIAL ====================================================================================
try:
    st.subheader("5️⃣ Material Data")
    material_types = st.multiselect("Select all types of material included in your CUP that have suffered a change in weight",
                                    ["Corrugate (Case)", "Carton", "Paper", "Plastic", "Glass", "Metal", "Other"], help=":blue[[MPD]]")
    material_data = {}

    c1, c2 = st.columns(2)
    with c1:
        if "Corrugate (Case)" in material_types:
            kg_corrugate_c = st.number_input(":blue[**Current**] corrugate kg/case", format="%.3f", help=":blue[[MPD]] FPP -> Bill of Materials -> EBOM W&D tab")
        if "Carton" in material_types:
            kg_carton_c = st.number_input(":blue[**Current**] carton kg/case", format="%.3f", help=":blue[[MPD]] FPP -> Bill of Materials -> EBOM W&D tab")
        if "Paper" in material_types:
            kg_paper_c = st.number_input(":blue[**Current**] paper kg/case", format="%.3f", help=":blue[[MPD]] FPP -> Bill of Materials -> EBOM W&D tab")
        if "Plastic" in material_types:
            kg_plastic_c = st.number_input(":blue[**Current**] plastic kg/case", format="%.3f", help=":blue[[MPD]] FPP -> Bill of Materials -> EBOM W&D tab")
        if "Glass" in material_types:
            kg_glass_c = st.number_input(":blue[**Current**] glass kg/case", format="%.3f", help=":blue[[MPD]] FPP -> Bill of Materials -> EBOM W&D tab")
        if "Metal" in material_types:
            kg_metal_c = st.number_input(":blue[**Current**] metal kg/case", format="%.3f", help=":blue[[MPD]] FPP -> Bill of Materials -> EBOM W&D tab")
        if "Other" in material_types:
            kg_other_c = st.number_input(":blue[**Current**] other kg/case", format="%.3f", help=":blue[[MPD]] FPP -> Bill of Materials -> EBOM W&D tab")
    with c2:
        if "Corrugate (Case)" in material_types:
            kg_corrugate_n = st.number_input(":red[**New**] corrugate kg/case", format="%.3f", help=":blue[[MPD]] FPP -> Bill of Materials -> EBOM W&D tab")
            material_data["Corrugate (Case)"] = (cases_total_c * kg_corrugate_c,
                                                cases_total_n * kg_corrugate_n)
        if "Carton" in material_types:
            kg_carton_n = st.number_input(":red[**New**] carton kg/case", format="%.3f", help=":blue[[MPD]] FPP -> Bill of Materials -> EBOM W&D tab")
            material_data["Carton"] = (cases_total_c * kg_carton_c, cases_total_n * kg_carton_n)
        if "Paper" in material_types:
            kg_paper_n = st.number_input(":red[**New**] paper kg/case", format="%.3f", help=":blue[[MPD]] FPP -> Bill of Materials -> EBOM W&D tab")
            material_data["Paper"] = (cases_total_c * kg_paper_c, cases_total_n * kg_paper_n)
        if "Plastic" in material_types:
            kg_plastic_n = st.number_input(":red[**New**] plastic kg/case", format="%.3f", help=":blue[[MPD]] FPP -> Bill of Materials -> EBOM W&D tab")
            material_data["Plastic"] = (cases_total_c * kg_plastic_c, cases_total_n * kg_plastic_n)
        if "Glass" in material_types:
            kg_glass_n = st.number_input(":red[**New**] glass kg/case", format="%.3f", help=":blue[[MPD]] FPP -> Bill of Materials -> EBOM W&D tab")
            material_data["Glass"] = (cases_total_c * kg_glass_c, cases_total_n * kg_glass_n)
        if "Metal" in material_types:
            kg_metal_n = st.number_input(":red[**New**] metal kg/case", format="%.3f", help=":blue[[MPD]] FPP -> Bill of Materials -> EBOM W&D tab")
            material_data["Metal"] = (cases_total_c * kg_metal_c, cases_total_n * kg_metal_n)
        if "Other" in material_types:
            kg_other_n = st.number_input(":red[**New**] other kg/case", format="%.3f", help=":blue[[MPD]] FPP -> Bill of Materials -> EBOM W&D tab")
            material_data["Other"] = (cases_total_c * kg_other_c, cases_total_n * kg_other_n)
except:
    st.info("Please fill in all inputs above before continuing")

# ======================= 6. MATERIAL SAVINGS TABLE ========================
on = st.toggle("Show Material Savings")

if on:
    try:
        if material_data:
            st.subheader("📊 Material Savings Summary")

            def highlight_savings_cells(val):
                if isinstance(val, (int, float)):
                    if val > 0:
                        return "background-color: #d4edda"  # light green
                    elif val < 0:
                        return "background-color: #f8d7da"  # light red
                return ""

            # Collect all materials into one dataframe
            rows = []
            for material, (current_kg, new_kg) in material_data.items():
                current_t = current_kg / 1000
                new_t = new_kg / 1000
                saving_pct = ((current_kg - new_kg) / current_kg * 100) if current_kg else 0

                rows.append({
                    "Material": material,
                    "Current [t]": round(current_t, 2),
                    "New [t]": round(new_t, 2),
                    "Saving": round(saving_pct, 2)
                })

            df_all = pd.DataFrame(rows)

            styled_df = df_all.style.applymap(
                highlight_savings_cells,
                subset=["Saving"]
            ).format({
                "Current [t]": "{:.2f}",
                "New [t]": "{:.2f}",
                "Saving": "{:.2f}%"
            })

            st.dataframe(styled_df, use_container_width=True, hide_index=True)
    except Exception as e:
        st.info(f"{e}Please fill in all inputs above before continuing")


# ================================================================== TRUCK CO2 EMISSIONS ====================================================================================

st.header("CO2 Emissions", divider="red")
 
if "🚚 Road" in transport_modes:
    with st.container(border=True):
        st.subheader("🚚 Road")
        try:
            locations = [
                "London", "Skelmersdale", "DHL Nordic Klippan", "PRL Dublin", "Sochaczew", "Hopi",
                "Euskirchen", "Crailsheim", "Amiens", "Mechelen", "Luis Simoes Mato", "Pomezia",
                "Mataro", "Stckhse Liscate", "Luis Simoes Cabanillas",
                "Unilog Markopoulo Hellas", "Aspropyrgos Hellas", "Timisoara"
            ]

            data = {
                "SMO": ["NE", "NE", "NE", "NE", "CE", "CE", "DACH", "DACH", "FBNL", "FBNL", "SE", "SE", "SE", "SE", "SEE"],
                "Code": ["4856", "4101", "6788", "C447", "9120", "A752", "4830", "4853", "4106", "4108",
                        "976", "4863", "5683", "8486", "B145"],
                "DC": ["London DC", "Skelmersdale", "DHL NORDIC SVC CTR-KLIPPAN-PGI", "PRL LOGISTICS LTD-DUBLIN-PG IO",
                    "SOCHACZEW CEN DC-PL-PGIO", "HOPI DC-STRANCICE-PGIOSA", "EUSKIRCHEN PLANT-ENTREPRENUER",
                    "CRAILSHEIM PLANT-ENTREPRENEUR", "AMIENS PLANT", "MECHELEN DC", "LUIS SIMOES LOGISTICA-MATO-IO",
                    "POMEZIA PLANT-ENTREPRENUER", "EXEL DC MATARO FHC - ENT", "STCKHSE ITALIA DC-LISCATE-PGIO",
                    "UNILOG SA-MARKOPOULO-PG HELLAS"]
            }

            # Initialize session state
            if "selected_dcs" not in st.session_state:
                st.session_state.selected_dcs = []

            # UI: simulate st.pills with multiselect
            selection = st.pills(
                "Select all applicable DC locations",
                options=locations,
                selection_mode="multi",
                default=st.session_state.selected_dcs
            )

            df = pd.DataFrame(data)
            popover2 = st.popover("ℹ️ Show DC SAP codes")
            popover2.dataframe(df, hide_index=True)
            # on2 = st.toggle("Show DC code library")
            # if on2:
            #     st.dataframe(df, hide_index=True)

            # Update session state only if changed
            if set(selection) != set(st.session_state.selected_dcs):
                st.session_state.selected_dcs = selection

            # Create DataFrame with editable MSU column
            df_data = {
                "DC": st.session_state.selected_dcs,
                "MSU": [0] * len(st.session_state.selected_dcs)
            }
            df = pd.DataFrame(df_data)

            st.write("Introduce the yearly MSU breakdown per DC")
            # Show editable data table
            edited_df = st.data_editor(
                df,
                use_container_width=True,
                column_config={
                    "MSU": st.column_config.NumberColumn("MSU", step=0.01, format="%f"),
                },
                disabled=["DC"],
                hide_index=True
            )

            total_msu = (edited_df["MSU"].sum())

            progress_fraction = min(total_msu / yearly_volume, 1.0) if yearly_volume > 0 else 0

            c1, c2 = st.columns([0.6, 0.4])
            with c1:
                # Show progress bar
                progress_bar = st.progress(progress_fraction)
            with c2:
                # Optional: Show percent text
                st.write(f":blue[{progress_fraction*100:.1f}%] of yearly volume [:blue[{yearly_volume:.2f} MSU]]")
            if total_msu > yearly_volume:
                st.error(f"⚠️ The sum of your MSU (:red[{total_msu:.1f}]) column should not exceed your total yearly volume (:red[{yearly_volume} MSU])")
            elif total_msu == yearly_volume and total_msu != 0:
                st.badge("Sum of MSU per DC = Total yearly MSU", icon=":material/check:", color="green")
        except:
            st.info("Please fill in all inputs above before continuing")

        if edited_df["MSU"].sum() == yearly_volume:
            # =================================================== Current and New Combined ===================================================
            try:
                if su_factor_c and su_factor_n and su_factor_c > 0 and su_factor_n > 0:
                    df_combined = edited_df[["DC", "MSU"]].copy()

                    # Compute current scenario
                    df_combined["Cases_Current"] = (df_combined["MSU"] / su_factor_c) * 1000

                    def trucks_and_weights_current(row):
                        if row["DC"] in ["London", "Skelmersdale"]:
                            divisor = cases_per_truck_current_uk if cases_per_truck_current_uk > 0 else 1
                            weight_per_truck = truck_uk_weight_c
                        else:
                            divisor = cases_per_truck_current_eu if cases_per_truck_current_eu > 0 else 1
                            weight_per_truck = truck_eu_weight_c
                        trucks = row["Cases_Current"] / divisor
                        weight_per_truck_tonnes = weight_per_truck / 1000
                        total_weight = trucks * weight_per_truck_tonnes
                        return pd.Series([trucks, total_weight])

                    df_combined[["Trucks_Current", "Weight Current [t]"]] = df_combined.apply(trucks_and_weights_current, axis=1)

                    # Compute new scenario
                    df_combined["Cases_New"] = (df_combined["MSU"] / su_factor_n) * 1000

                    def trucks_and_weights_new(row):
                        if row["DC"] in ["London", "Skelmersdale"]:
                            divisor = cases_per_truck_new_uk if cases_per_truck_new_uk > 0 else 1
                            weight_per_truck = truck_uk_weight_n
                        else:
                            divisor = cases_per_truck_new_eu if cases_per_truck_new_eu > 0 else 1
                            weight_per_truck = truck_eu_weight_n
                        trucks = row["Cases_New"] / divisor
                        weight_per_truck_tonnes = weight_per_truck / 1000
                        total_weight = trucks * weight_per_truck_tonnes
                        return pd.Series([trucks, total_weight])

                    df_combined[["Trucks_New", "Weight New [t]"]] = df_combined.apply(trucks_and_weights_new, axis=1)

                    # Add editable CO2e columns
                    df_combined["Current CO2e [kg]"] = 0.0
                    df_combined["New CO2e [kg]"] = 0.0

                    # Final table
                    df_display = df_combined[[
                        "DC",
                        "Weight Current [t]",
                        "Weight New [t]",
                        "Current CO2e [kg]",
                        "New CO2e [kg]"
                    ]].copy()

                    st.write("")
                    c1, c2 = st.columns([0.8, 0.2])
                    with c1:
                        st.info("6️⃣ Use [EcoTransit](https://emissioncalculator.ecotransit.world/) to fill in the **current** and **new** CO2e values.")

                    with c2:
                        popover_c = st.popover("ℹ️ Job aid")
                        popover_c.image("help_aid_co2.png", caption="EcoTransit Tool")

                    df_display = st.data_editor(
                        df_display,
                        use_container_width=True,
                        hide_index=True,
                        column_config={
                            "Current CO2e [kg]": st.column_config.NumberColumn(
                                "Current CO2e [kg]",
                                help="From [EcoTransit](https://emissioncalculator.ecotransit.world/)",
                                step=0.01,
                                format="%.2f"
                            ),
                            "New CO2e [kg]": st.column_config.NumberColumn(
                                "New CO2e [kg]",
                                help="From [EcoTransit](https://emissioncalculator.ecotransit.world/)",
                                step=0.01,
                                format="%.2f"
                            )
                        },
                        disabled=[col for col in df_display.columns if col not in ["Current CO2e [kg]", "New CO2e [kg]"]]
                    )
            except:
                st.info("Please fill in all inputs above before continuing")

            # =============================================================== Savings =============================================================
            try:
                if su_factor_c and su_factor_n and su_factor_c > 0 and su_factor_n > 0:
                    total_trucks_current = df_combined["Trucks_Current"].sum()
                    total_trucks_new = df_combined["Trucks_New"].sum()

                    total_co2_current = df_display["Current CO2e [kg]"].sum()
                    total_co2_new = df_display["New CO2e [kg]"].sum()

                    trucks_saved = total_trucks_current - total_trucks_new
                    co2_saved = total_co2_current - total_co2_new

                    trucks_pct_saved = (trucks_saved / total_trucks_current) * 100 if total_trucks_current > 0 else 0
                    co2_pct_saved = (co2_saved / total_co2_current) * 100 if total_co2_current > 0 else 0

                    savings_data = {
                        "Trucks Saved": [int(trucks_saved)],
                        "Trucks Saved [%]": [trucks_pct_saved],
                        "CO2e Saved [kg]": [int(co2_saved)],
                        "CO2e Saved [%]": [co2_pct_saved]
                    }

                    df_savings = pd.DataFrame(savings_data)

                    def highlight_savings(val):
                        if isinstance(val, (float, int)):
                            if val > 0:
                                return "background-color: #d4edda"  # light green
                            elif val < 0:
                                return "background-color: #f8d7da"  # light red
                        return ""

                    styled_df = df_savings.style.applymap(
                        highlight_savings,
                        subset=["Trucks Saved [%]", "CO2e Saved [%]"]
                    ).format({
                        "Trucks Saved [%]": "{:.1f}%",
                        "CO2e Saved [%]": "{:.1f}%"
                    })

                    st.subheader("Savings")
                    st.dataframe(styled_df, use_container_width=True, hide_index=True)
            except:
                st.info("Please fill in all inputs above before continuing")

        elif edited_df["MSU"].sum() < yearly_volume:
            st.info("Please introduce all volumes for the selected DCs to continue")
else:
    st.info("Please fill in all Initiative Master Data before continuing")

# ============================================== SEA CO2 SAVINGS ===================================================================

if "🚢 Sea" in transport_modes:
    with st.container(border=True):
        st.subheader("🚢 Sea")
        try:
            # Calculations
            containers_c = cases_total_c / cases_sea_c
            containers_n = cases_total_n / cases_sea_n
            container_weight_c = case_weight_c * cases_sea_c
            container_weight_n = case_weight_n * cases_sea_n
            container_weight_total_c = container_weight_c * containers_c
            container_weight_total_n = container_weight_n * containers_n

            container_saving = containers_c - containers_n
            container_saving_percentage = 100 * container_saving / containers_c

            # Convert to tonnes
            weight_tonnes_c = container_weight_total_c / 1000
            weight_tonnes_n = container_weight_total_n / 1000

            # Comparison table (only CO2e columns editable)
            combined_df = pd.DataFrame({
                "Container Weight Current [t]": [weight_tonnes_c],
                "Container Weight New [t]": [weight_tonnes_n],
                "CO2e Current [kg]": [0],
                "CO2e New [kg]": [0]
            })

            c1, c2 = st.columns([0.8, 0.2])
            with c1:
                st.info("7️⃣ Use [EcoTransit](https://emissioncalculator.ecotransit.world/) to fill in the **current** and **new** CO2e values.")

            with c2:
                popover_c = st.popover("ℹ️ Job aid")
                popover_c.image("help_aid_co2.png", caption="EcoTransit Tool")
            edited_df = st.data_editor(
                combined_df,
                column_config={
                    "Container Weight Current [t]": st.column_config.Column(disabled=True),
                    "Container Weight New [t]": st.column_config.Column(disabled=True),
                    "CO2e Current [kg]": st.column_config.Column(),
                    "CO2e New [kg]": st.column_config.Column(),
                },
                num_rows="fixed",
                hide_index=True
            )

            # Compute savings if CO2 values were edited
            co2_current = edited_df["CO2e Current [kg]"][0]
            co2_new = edited_df["CO2e New [kg]"][0]
            co2_saving = co2_current - co2_new
            co2_saving_percentage = 100 * co2_saving / co2_current if co2_current else 0

            savings_df = pd.DataFrame({
                "Containers Saved": [f"{container_saving:.0f}"],
                "Containers Saved [%]": [f"{container_saving_percentage:.2f}%"],
                "CO2e Saved [kg]": [co2_saving],
                "CO2e Saved [%]": [f"{co2_saving_percentage:.2f}%" if co2_current else "N/A"]
            })


            # Function to apply conditional formatting for percentage columns
            def highlight_percentages(val):
                if isinstance(val, str) and val.endswith('%'):
                    try:
                        num = float(val.strip('%'))
                        if num > 0:
                            return 'background-color: #d4edda'  # green
                        elif num < 0:
                            return 'background-color: #f8d7da'  # red
                    except:
                        pass
                return ''

            st.subheader("Savings")
            st.dataframe(
                savings_df.style.applymap(highlight_percentages, subset=["Containers Saved [%]", "CO2e Saved [%]"]), hide_index=True
            )
        except:
            st.info("Please fill in all inputs above before continuing")
        

# ============================================= FINAL DOWNLOAD SECTION =====================================================

st.header("Results Export", divider="red")

try:
    output = io.BytesIO()
    with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
        wb = writer.book  # workbook for formatting

        # Initiative Info
        pd.DataFrame({
            "CM": [cm],
            "Initiative Name": [initiative_name],
            "FPC Example": [fpc],
            "Description": [initiative_description]
        }).to_excel(writer, sheet_name="1. Initiative Info", index=False)

        # Volumes
        pd.DataFrame({
            "Yearly Volume (MSU)": [yearly_volume],
            "Current SU Factor": [su_factor_c],
            "New SU Factor": [su_factor_n],
            "Current Items/Case": [items_case_c],
            "New Items/Case": [items_case_n],
            "Total Current Cases": [cases_total_c],
            "Total New Cases": [cases_total_n],
            "Total Current Items": [items_total_c],
            "Total New Items": [items_total_n]
        }).to_excel(writer, sheet_name="2. Volumes", index=False)

        # Transportation
        pd.DataFrame({
            "Transport Modes": [", ".join(transport_modes)],
            "EU Pallet Type (Current)": [pallet_type_eu_c if "🚚 Road" in transport_modes else None],
            "EU Pallet Type (New)": [pallet_type_eu_n if "🚚 Road" in transport_modes else None],
            "UK Pallet Type (Current)": [pallet_type_uk_c if "🚚 Road" in transport_modes else None],
            "UK Pallet Type (New)": [pallet_type_uk_n if "🚚 Road" in transport_modes else None],
            "Cases per Truck EU (Current)": [cases_per_truck_current_eu if "🚚 Road" in transport_modes else None],
            "Cases per Truck EU (New)": [cases_per_truck_new_eu if "🚚 Road" in transport_modes else None],
            "Cases per Truck UK (Current)": [cases_per_truck_current_uk if "🚚 Road" in transport_modes else None],
            "Cases per Truck UK (New)": [cases_per_truck_new_uk if "🚚 Road" in transport_modes else None],
            "Sea Cases/Container (Current)": [cases_sea_c if "🚢 Sea" in transport_modes else None],
            "Sea Cases/Container (New)": [cases_sea_n if "🚢 Sea" in transport_modes else None]
        }).to_excel(writer, sheet_name="3. Transportation", index=False)

        # Weights
        pd.DataFrame({
            "Case Weight (Current)": [case_weight_c],
            "Case Weight (New)": [case_weight_n],
            "Truck EU Weight (Current)": [truck_eu_weight_c if "🚚 Road" in transport_modes else None],
            "Truck EU Weight (New)": [truck_eu_weight_n if "🚚 Road" in transport_modes else None],
            "Truck UK Weight (Current)": [truck_uk_weight_c if "🚚 Road" in transport_modes else None],
            "Truck UK Weight (New)": [truck_uk_weight_n if "🚚 Road" in transport_modes else None]
        }).to_excel(writer, sheet_name="4. Weights", index=False)

        # Material Savings with conditional formatting
        if material_data:
            material_rows = []
            for material, (current_kg, new_kg) in material_data.items():
                current_t = current_kg / 1000
                new_t = new_kg / 1000
                saving_pct = ((current_kg - new_kg) / current_kg * 100) if current_kg else 0
                material_rows.append({
                    "Material": material,
                    "Current [t]": round(current_t, 2),
                    "New [t]": round(new_t, 2),
                    "Saving [%]": round(saving_pct, 2)
                })
            df_mat = pd.DataFrame(material_rows)
            df_mat.to_excel(writer, sheet_name="5. Material Savings", index=False)
            ws = writer.sheets["5. Material Savings"]
            col_letter = chr(65 + df_mat.columns.get_loc("Saving [%]"))
            rng = f"{col_letter}2:{col_letter}{len(df_mat)+1}"
            ws.conditional_format(rng, {"type": "cell", "criteria": ">", "value": 0,
                                        "format": wb.add_format({"bg_color": "#d4edda"})})
            ws.conditional_format(rng, {"type": "cell", "criteria": "<", "value": 0,
                                        "format": wb.add_format({"bg_color": "#f8d7da"})})

        # Road CO2 tables
        try:
            df_display.to_excel(writer, sheet_name="Road CO2", index=False)
            df_savings.to_excel(writer, sheet_name="Road CO2 Savings", index=False)
            ws2 = writer.sheets["Road CO2 Savings"]
            for col in ["% Trucks Saved", "% CO2e Saved"]:
                col_letter = chr(65 + df_savings.columns.get_loc(col))
                rng = f"{col_letter}2:{col_letter}{len(df_savings)+1}"
                ws2.conditional_format(rng, {"type": "cell", "criteria": ">", "value": 0,
                                                "format": wb.add_format({"bg_color": "#d4edda"})})
                ws2.conditional_format(rng, {"type": "cell", "criteria": "<", "value": 0,
                                                "format": wb.add_format({"bg_color": "#f8d7da"})})
        except:
            pass

        # Sea CO2 tables
        try:
            edited_df.to_excel(writer, sheet_name="Sea CO2", index=False)
            savings_df.to_excel(writer, sheet_name="Sea CO2 Savings", index=False)
            ws3 = writer.sheets["Sea CO2 Savings"]
            for col in ["Containers Saved [%]", "CO2e Saved [%]"]:
                col_letter = chr(65 + savings_df.columns.get_loc(col))
                rng = f"{col_letter}2:{col_letter}{len(savings_df)+1}"
                ws3.conditional_format(rng, {"type": "cell", "criteria": ">", "value": 0,
                                                "format": wb.add_format({"bg_color": "#d4edda"})})
                ws3.conditional_format(rng, {"type": "cell", "criteria": "<", "value": 0,
                                                "format": wb.add_format({"bg_color": "#f8d7da"})})
        except:
            pass

    st.download_button(
        label="📄 Download Excel Report",
        data=output.getvalue(),
        file_name=f"{initiative_name}_sustainability_report.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        on_click=st.balloons 
    )
except:
    st.info("Please complete the exercise before generating the report")

with st.sidebar:
    with st.container(border=True):
        st.subheader("🧠 Which step do you need help with? (1–7)")

        if "last_help_response" not in st.session_state:
            st.session_state.last_help_response = None

        user_query = st.chat_input("i.e. Step 1")

        if user_query:
            query = user_query.lower().strip()
            step_matches = {
                "1": "step 1", "one": "step 1",
                "2": "step 2", "two": "step 2",
                "3": "step 3", "three": "step 3",
                "4": "step 4", "four": "step 4",
                "5": "step 5", "five": "step 5",
                "6": "step 6", "six": "step 6",
                "7": "step 7", "seven": "step 7"
            }
            step = step_matches.get(query, query)

            if "step 1" in step or "base data" in step:
                response = (
                    "🧾 **Step 1: Base Data**\n\n"
                    "Begin by filling in general information about the initiative:\n"
                    "- `CM`: Select the Contract Manufacturer\n"
                    "- `Initiative Name`: Name of the sustainability project\n"
                    "- `FPC Number Example`: Provide a known FPC for reference\n"
                    "- `Initiative Description`: Describe the change in 1 sentence\n\n"
                    "🎯 This configures the core identity of the initiative and shows in the export."
                )
            elif "step 2" in step or "volumes" in step:
                response = (
                    "📊 **Step 2: Volumes**\n\n"
                    "Enter key volume-related data:\n"
                    "- `Total yearly volume` in MSU (thousands of statistical units)\n"
                    "- `Case SU factor` for Current and New formats\n"
                    "- `Items per case` for Current and New formats\n\n"
                    "📌 These values are used to calculate:\n"
                    "- Total cases per year\n"
                    "- Total items shipped\n"
                    "- Inputs for later truck/container and weight calculations"
                )
            elif "step 3" in step or "transportation" in step:
                response = (
                    "🚚 **Step 3: Transportation**\n\n"
                    "1. Select transport modes: `🚚 Road` and/or `🚢 Sea`\n\n"
                    "If **Sea**:\n"
                    "- Input `cases per container` for Current and New formats\n\n"
                    "If **Road**:\n"
                    "- Choose pallet types (B1/B2 for EU, C1/C2 for UK)\n"
                    "- Input `cases per pallet` to compute `cases per truck`\n\n"
                    "🧠 Pallet → Truck logic is predefined (e.g., B1 = 66 pallets/truck)"
                )
            elif "step 4" in step or "weight" in step:
                response = (
                    "⚖️ **Step 4: Weight**\n\n"
                    "Enter the case weight (kg) for both formats:\n"
                    "- `Case Weight (Current)`\n"
                    "- `Case Weight (New)`\n\n"
                    "📦 Used to calculate:\n"
                    "- Truck weight (per DC and route)\n"
                    "- Container weight for Sea lanes\n"
                    "- Final weight values are shown in tonnes"
                )
            elif "step 5" in step or "material" in step:
                response = (
                    "📦 **Step 5: Material Data**\n\n"
                    "Optional input if your initiative changes packaging:\n"
                    "- Select changed materials: Corrugate, Plastic, Glass, etc.\n"
                    "- For each selected type:\n"
                    "   - Enter kg/case for Current and New\n\n"
                    "📊 Tool shows total tonnes saved and % difference with color indicators\n"
                    "🔎 Source: `FPP → Bill of Materials → EBOM W&D` tab"
                )
            elif "step 6" in step or "road co2" in step:
                response = (
                    "🌍 **Step 6: Road CO₂ Emissions**\n\n"
                    "1. Select DCs and assign MSU per DC\n"
                    "2. The tool computes:\n"
                    "   - Cases\n"
                    "   - Trucks\n"
                    "   - Weight (tonnes)\n\n"
                    "3. Open [EcoTransit](https://emissioncalculator.ecotransit.world/):\n"
                    "   - Use DC lane and weight per lane\n"
                    "   - Copy **CO₂e [kg]** for Current and New scenarios\n"
                    "   - Paste into the editable CO₂ table\n\n"
                    "✅ Output: savings in trucks and CO₂e, with visual formatting"
                )
            elif "step 7" in step or "sea co2" in step:
                response = (
                    "🚢 **Step 7: Sea CO₂ Emissions**\n\n"
                    "Based on MSU and `cases/container`, the tool computes:\n"
                    "- Number of containers (Current and New)\n"
                    "- Container weight and total sea tonnage\n\n"
                    "Then:\n"
                    "1. Use [EcoTransit](https://emissioncalculator.ecotransit.world/) with route + tonnage\n"
                    "2. Input CO₂e [kg] for Current and New formats\n"
                    "3. Review containers saved and CO₂e saved as output"
                )
            elif "how" in query or "instructions" in query or "guide" in query:
                response = (
                    "📘 **Full Tool Usage Guide**\n\n"
                    "1. **Base Data** – Define initiative and FPC\n"
                    "2. **Volumes** – Enter yearly MSU and SU factors\n"
                    "3. **Transportation** – Road or Sea + unit configuration\n"
                    "4. **Weight** – Case weight input → automated truck/container weight\n"
                    "5. **Material** – Optional: packaging data per case\n"
                    "6. **Road CO₂** – EcoTransit per DC, based on trucked weight\n"
                    "7. **Sea CO₂** – EcoTransit per container, based on MSU shipping"
                )
            else:
                response = (
                    "🤔 I couldn’t match that to a known step.\n"
                    "Try typing: `1`, `step 3`, `weight`, `sea CO₂`, or `how do I use the tool?`"
                )

            st.session_state.last_help_response = response

        if st.session_state.last_help_response:
            with st.chat_message("assistant"):
                st.markdown(st.session_state.last_help_response)
