import streamlit as st
import pandas as pd
import io

# Create a placeholder for the dynamic title
title_placeholder = st.empty()

# Static default title
default_title = "♻️ Sustainability Calculator"

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
    ), index=None)
with c2:
    initiative_name = st.text_input("Initiative Name")
with c3:
    fpc = st.text_input("FPC number example", help="For the current execution, provide an example of any released FPC.")

initiative_description = st.text_input("Describe the initiative in one sentence")

# Update the title with the initiative name if present
if initiative_name:
    title_placeholder.title(f"♻️ Sustainability Calculator :blue[{initiative_name}]")
else:
    title_placeholder.title(default_title)

# ================================================================== 2. VOLUMES ====================================================================================
st.subheader("2️⃣ Volumes")
c1, c2 = st.columns(2)
with c1:
    yearly_volume = st.number_input("Total yearly volume (MSU)", step=0.01, format="%f")
with c2:
    st.write('')

c1, c2 = st.columns(2)
with c1:
    su_factor_c = st.number_input(":blue[**Current**] Case SU factor", step=0.001, format="%.3f")
    items_case_c = st.number_input(":blue[**Current**] Items/Case", step=1, format="%d")
with c2:
    su_factor_n = st.number_input(":red[**New**] Case SU factor", step=0.001, format="%.3f")
    items_case_n = st.number_input(":red[**New**] Items/Case", step=1, format="%d")

cases_total_c = (yearly_volume / su_factor_c) * 1000 if su_factor_c else 0
cases_total_n = (yearly_volume / su_factor_n) * 1000 if su_factor_n else 0
items_total_c = cases_total_c * items_case_c
items_total_n = cases_total_n * items_case_n

# ================================================================== 3. TRANSPORTATION ====================================================================================
st.subheader("3️⃣ Transportation")
transport_modes = st.multiselect("Select all transportation modes", ["🚚 Road", "🚢 Sea"])

if "🚢 Sea" in transport_modes:
    c1, c2 = st.columns(2)
    with c1:
        cases_sea_c = st.number_input(":blue[**Current**] number of Cases/Container", step=1, format="%d")
    with c2:
        cases_sea_n = st.number_input(":red[**New**] number of Cases/Container", step=1, format="%d")

if "🚚 Road" in transport_modes:
    pallet_factors = {"B1": 66, "B2": 33, "C1": 52, "C2": 26}
    cases_per_truck_current_eu = cases_per_truck_current_uk = 0
    cases_per_truck_new_eu = cases_per_truck_new_uk = 0

    # EU Pallets
    c1, c2, c3, c4 = st.columns(4)
    with c1:
        pallet_type_eu_c = st.selectbox(":blue[**Current**] EU pallet type", ["B1", "B2", "N/A"], index=None)
    with c2:
        if pallet_type_eu_c == "B1":
            cases_b1_c = st.number_input(":blue[**Current**] Cases/Pallet B1", step=1, format="%d")
            cases_per_truck_current_eu = cases_b1_c * pallet_factors["B1"]
        elif pallet_type_eu_c == "B2":
            cases_b2_c = st.number_input(":blue[**Current**] Cases/Pallet B2", step=1, format="%d")
            cases_per_truck_current_eu = cases_b2_c * pallet_factors["B2"]

    with c3:
        pallet_type_eu_n = st.selectbox(":red[**New**] EU pallet type", ["B1", "B2", "N/A"], index=None)
    with c4:
        if pallet_type_eu_n == "B1":
            cases_b1_n = st.number_input(":red[**New**] Cases/Pallet B1", step=1, format="%d")
            cases_per_truck_new_eu = cases_b1_n * pallet_factors["B1"]
        elif pallet_type_eu_n == "B2":
            cases_b2_n = st.number_input(":red[**New**] Cases/Pallet B2", step=1, format="%d")
            cases_per_truck_new_eu = cases_b2_n * pallet_factors["B2"]

    # UK Pallets
    c5, c6, c7, c8 = st.columns(4)
    with c5:
        pallet_type_uk_c = st.selectbox(":blue[**Current**] UK pallet type", ["C1", "C2", "N/A"], index=None)
    with c6:
        if pallet_type_uk_c == "C1":
            cases_c1_c = st.number_input(":blue[**Current**] Cases/Pallet C1", step=1, format="%d")
            cases_per_truck_current_uk = cases_c1_c * pallet_factors["C1"]
        elif pallet_type_uk_c == "C2":
            cases_c2_c = st.number_input(":blue[**Current**] Cases/Pallet C2", step=1, format="%d")
            cases_per_truck_current_uk = cases_c2_c * pallet_factors["C2"]

    with c7:
        pallet_type_uk_n = st.selectbox(":red[**New**] UK pallet type", ["C1", "C2", "N/A"], index=None)
    with c8:
        if pallet_type_uk_n == "C1":
            cases_c1_n = st.number_input(":red[**New**] Cases/Pallet C1", step=1, format="%d")
            cases_per_truck_new_uk = cases_c1_n * pallet_factors["C1"]
        elif pallet_type_uk_n == "C2":
            cases_c2_n = st.number_input(":red[**New**] Cases/Pallet C2", step=1, format="%d")
            cases_per_truck_new_uk = cases_c2_n * pallet_factors["C2"]

# ================================================================== 4. WEIGHT DATA ====================================================================================
st.subheader("4️⃣ Weight")
c1, c2 = st.columns(2)
with c1:
    case_weight_c = st.number_input(":blue[**Current**] Case Weight [kg]")
with c2:
    case_weight_n = st.number_input(":red[**New**] Case Weight [kg]")

try:
    truck_eu_weight_c = case_weight_c * cases_per_truck_current_eu
    truck_eu_weight_n = case_weight_n * cases_per_truck_new_eu
    truck_uk_weight_c = case_weight_c * cases_per_truck_current_uk
    truck_uk_weight_n = case_weight_n * cases_per_truck_new_uk
except:  # You can specify a more specific exception if desire
    st.info("Please fill in all inputs above before continuing")


# ================================================================== 5. MATERIAL ====================================================================================
try:
    st.subheader("5️⃣ Material Data")
    material_types = st.multiselect("Select all types of material included in your CUP that have suffered a change in weight",
                                    ["Corrugate (Case)", "Carton", "Paper", "Plastic", "Glass", "Metal", "Other"])

    material_data = {}

    c1, c2 = st.columns(2)
    with c1:
        if "Corrugate (Case)" in material_types:
            kg_corrugate_c = st.number_input(":blue[**Current**] corrugate kg/case", format="%.3f")
        if "Carton" in material_types:
            kg_carton_c = st.number_input(":blue[**Current**] carton kg/case", format="%.3f")
        if "Paper" in material_types:
            kg_paper_c = st.number_input(":blue[**Current**] paper kg/case", format="%.3f")
        if "Plastic" in material_types:
            kg_plastic_c = st.number_input(":blue[**Current**] plastic kg/case", format="%.3f")
        if "Glass" in material_types:
            kg_glass_c = st.number_input(":blue[**Current**] glass kg/case", format="%.3f")
        if "Metal" in material_types:
            kg_metal_c = st.number_input(":blue[**Current**] metal kg/case", format="%.3f")
        if "Other" in material_types:
            kg_other_c = st.number_input(":blue[**Current**] other kg/case", format="%.3f")
    with c2:
        if "Corrugate (Case)" in material_types:
            kg_corrugate_n = st.number_input(":red[**New**] corrugate kg/case", format="%.3f")
            material_data["Corrugate (Case)"] = (cases_total_c * kg_corrugate_c,
                                                cases_total_n * kg_corrugate_n)
        if "Carton" in material_types:
            kg_carton_n = st.number_input(":red[**New**] carton kg/case", format="%.3f")
            material_data["Carton"] = (cases_total_c * kg_carton_c, cases_total_n * kg_carton_n)
        if "Paper" in material_types:
            kg_paper_n = st.number_input(":red[**New**] paper kg/case", format="%.3f")
            material_data["Paper"] = (cases_total_c * kg_paper_c, cases_total_n * kg_paper_n)
        if "Plastic" in material_types:
            kg_plastic_n = st.number_input(":red[**New**] plastic kg/case", format="%.3f")
            material_data["Plastic"] = (cases_total_c * kg_plastic_c, cases_total_n * kg_plastic_n)
        if "Glass" in material_types:
            kg_glass_n = st.number_input(":red[**New**] glass kg/case", format="%.3f")
            material_data["Glass"] = (cases_total_c * kg_glass_c, cases_total_n * kg_glass_n)
        if "Metal" in material_types:
            kg_metal_n = st.number_input(":red[**New**] metal kg/case", format="%.3f")
            material_data["Metal"] = (cases_total_c * kg_metal_c, cases_total_n * kg_metal_n)
        if "Other" in material_types:
            kg_other_n = st.number_input(":red[**New**] other kg/case", format="%.3f")
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
                    "Saving [%]": round(saving_pct, 2)
                })

            df_all = pd.DataFrame(rows)

            styled_df = df_all.style.applymap(
                highlight_savings_cells,
                subset=["Saving [%]"]
            ).format({
                "Current [t]": "{:.2f}",
                "New [t]": "{:.2f}",
                "Saving [%]": "{:.2f}"
            })

            st.dataframe(styled_df, use_container_width=True, hide_index=True)
    except Exception as e:
        st.info(f"{e}Please fill in all inputs above before continuing")


# ================================================================== CO2 EMISSIONS ====================================================================================

st.header("CO2 Emissions", divider="red")
st.subheader("Annual Volume Breakdown")

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
    on2 = st.toggle("Show DC code library")
    if on2:
        st.dataframe(df, hide_index=True)

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

    # )
    total_msu = edited_df["MSU"].sum()

    progress_fraction = min(total_msu / yearly_volume, 1.0) if yearly_volume > 0 else 0

    c1, c2 = st.columns([0.6, 0.4])
    with c1:
        # Show progress bar
        progress_bar = st.progress(progress_fraction)
    with c2:
        # Optional: Show percent text
        st.write(f"[:blue[{progress_fraction*100:.1f}%]] of yearly volume :blue[{yearly_volume:.2f} MSU]")
    if total_msu > yearly_volume:
        st.error(f"⚠️ The sum of your MSU column should not exceed your total yearly volume (:red[{yearly_volume} MSU])")
    elif total_msu == yearly_volume and total_msu != 0:
        st.success(f"✅ The sum of your MSU column is exactly equal to your total yearly volume!")
except:
    st.info("Please fill in all inputs above before continuing")

if edited_df["MSU"].sum() == yearly_volume:
    # =================================================== Current ===================================================================
    try:
        # Compute and show table for current SU factor
        if su_factor_c and su_factor_c > 0:
            df_current = edited_df[["DC", "MSU"]].copy()
            df_current["Cases"] = (df_current["MSU"] / su_factor_c) * 1000

            def trucks_and_weights_current(row):
                if row["DC"] in ["London", "Skelmersdale"]:
                    divisor = cases_per_truck_current_uk if cases_per_truck_current_uk > 0 else 1
                    weight_per_truck = truck_uk_weight_c
                else:
                    divisor = cases_per_truck_current_eu if cases_per_truck_current_eu > 0 else 1
                    weight_per_truck = truck_eu_weight_c
                trucks = row["Cases"] / divisor
                weight_per_truck_tonnes = weight_per_truck / 1000
                total_weight = trucks * weight_per_truck_tonnes
                return pd.Series([trucks, weight_per_truck_tonnes, total_weight])

            df_current[["Trucks", "Weight/Truck [t]", "Total Shipped Weight [t]"]] = df_current.apply(trucks_and_weights_current, axis=1)
            df_current["CO2e"] = 0.0  # Add editable CO2e column

            st.subheader("Current")
            df_current = st.data_editor(
                df_current,
                use_container_width=True,
                hide_index=True,
                column_config={
                    "Trucks": st.column_config.NumberColumn(
                        "Trucks",
                        format="%.0f"
                    ),
                    "CO2e": st.column_config.NumberColumn(
                        "CO2e",
                        help="From [EcoTransit](https://emissioncalculator.ecotransit.world/)",
                        step=0.01,
                        format="%.2f"
                    )
                },
                disabled=[col for col in df_current.columns if col != "CO2e"]
            )
        else:
            st.write("")
    except:
        st.info("Please fill in all inputs above before continuing")

    # =========================================================== New ===============================================================
    try:
        # Compute and show table for new SU factor
        if su_factor_n and su_factor_n > 0:
            df_new = edited_df[["DC", "MSU"]].copy()
            df_new["Cases"] = (df_new["MSU"] / su_factor_n) * 1000

            def trucks_and_weights_new(row):
                if row["DC"] in ["London", "Skelmersdale"]:
                    divisor = cases_per_truck_new_uk if cases_per_truck_new_uk > 0 else 1
                    weight_per_truck = truck_uk_weight_n
                else:
                    divisor = cases_per_truck_new_eu if cases_per_truck_new_eu > 0 else 1
                    weight_per_truck = truck_eu_weight_n
                trucks = row["Cases"] / divisor
                weight_per_truck_tonnes = weight_per_truck / 1000
                total_weight = trucks * weight_per_truck_tonnes
                return pd.Series([trucks, weight_per_truck_tonnes, total_weight])

            df_new[["Trucks", "Weight/Truck [t]", "Total Shipped Weight [t]"]] = df_new.apply(trucks_and_weights_new, axis=1)
            df_new["CO2e"] = 0.0  # Add editable CO2e column

            st.subheader("New")
            df_new = st.data_editor(
                df_new,
                use_container_width=True,
                hide_index=True,
                column_config={
                    "Trucks": st.column_config.NumberColumn(
                        "Trucks",
                        format="%.0f"
                    ),
                    "CO2e": st.column_config.NumberColumn(
                        "CO2e",
                        help="From [EcoTransit](https://emissioncalculator.ecotransit.world/)",
                        step=0.01,
                        format="%.2f"
                    )
                },
                disabled=[col for col in df_new.columns if col != "CO2e"]
            )
        else:
            st.write("")
    except:
        st.info("Please fill in all inputs above before continuing")


    # =============================================================== Savings =============================================================
    try:
        # Compute and show Savings table
        if su_factor_c and su_factor_n and su_factor_c > 0 and su_factor_n > 0:
            total_trucks_current = df_current["Trucks"].sum()
            total_trucks_new = df_new["Trucks"].sum()

            total_co2_current = df_current["CO2e"].sum()
            total_co2_new = df_new["CO2e"].sum()

            trucks_saved = total_trucks_current - total_trucks_new
            co2_saved = total_co2_current - total_co2_new

            trucks_pct_saved = (trucks_saved / total_trucks_current) * 100 if total_trucks_current > 0 else 0
            co2_pct_saved = (co2_saved / total_co2_current) * 100 if total_co2_current > 0 else 0

            savings_data = {
                "Trucks Saved": [int(trucks_saved)],
                "% Trucks Saved": [trucks_pct_saved],
                "CO2e Saved": [int(co2_saved)],
                "% CO2e Saved": [co2_pct_saved]
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
                subset=["% Trucks Saved", "% CO2e Saved"]
            ).format({
                "% Trucks Saved": "{:.1f}%",
                "% CO2e Saved": "{:.1f}%"
            })

            st.subheader("🌍 Savings")
            st.dataframe(styled_df, use_container_width=True, hide_index=True)
    except:
        st.info("Please fill in all inputs above before continuing")



    # ============================== RESULTS SECTION ==============================

    st.header("Results", divider="red")

    try:
        def generate_report():
            # Collect all inputs and results into a dictionary or dataframes
            report_data = {}

            # Base Data
            report_data["Base Data"] = {
                "CM": cm,
                "Initiative Name": initiative_name,
                "FPC Number": fpc,
                "Initiative Description": initiative_description,
                "Yearly Volume (MSU)": yearly_volume,
                "Current SU factor": su_factor_c,
                "New SU factor": su_factor_n,
                "Current Items/Case": items_case_c,
                "New Items/Case": items_case_n
            }

            # Transportation data - store what is relevant and selected
            report_data["Transportation"] = {
                "Transport Modes": transport_modes
            }
            if "🚢 Sea" in transport_modes:
                report_data["Transportation"].update({
                    "Current Cases/Container (Sea)": cases_sea_c,
                    "New Cases/Container (Sea)": cases_sea_n
                })
            if "🚚 Road" in transport_modes:
                report_data["Transportation"].update({
                    "Current EU pallet type": pallet_type_eu_c,
                    "Current Cases/Pallet EU": cases_per_truck_current_eu,
                    "New EU pallet type": pallet_type_eu_n,
                    "New Cases/Pallet EU": cases_per_truck_new_eu,
                    "Current UK pallet type": pallet_type_uk_c,
                    "Current Cases/Pallet UK": cases_per_truck_current_uk,
                    "New UK pallet type": pallet_type_uk_n,
                    "New Cases/Pallet UK": cases_per_truck_new_uk
                })

            # Weight Data
            report_data["Weight"] = {
                "Current Case Weight (kg)": case_weight_c,
                "New Case Weight (kg)": case_weight_n,
                "Truck EU Weight Current (kg)": truck_eu_weight_c,
                "Truck EU Weight New (kg)": truck_eu_weight_n,
                "Truck UK Weight Current (kg)": truck_uk_weight_c,
                "Truck UK Weight New (kg)": truck_uk_weight_n,
            }

            # Material Data
            material_summary = []
            for mat, (curr_kg, new_kg) in material_data.items():
                saving_kg = curr_kg - new_kg
                saving_pct = ((saving_kg / curr_kg) * 100) if curr_kg else 0
                material_summary.append({
                    "Material": mat,
                    "Current kg total": curr_kg,
                    "New kg total": new_kg,
                    "Saving kg": saving_kg,
                    "Saving %": saving_pct
                })
            df_material = pd.DataFrame(material_summary)

            # DC Data and Emissions (if available)
            df_current_report = None
            df_new_report = None
            df_savings_report = None
            if su_factor_c and su_factor_c > 0 and 'df_current' in locals():
                df_current_report = df_current.copy()
            if su_factor_n and su_factor_n > 0 and 'df_new' in locals():
                df_new_report = df_new.copy()
            if su_factor_c and su_factor_n and su_factor_c > 0 and su_factor_n > 0:
                df_savings_report = df_savings.copy()

            # Write to Excel in memory buffer
            output = io.BytesIO()
            with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
                # Write base and transportation data as sheets with 1-row DataFrame
                pd.DataFrame([report_data["Base Data"]]).to_excel(writer, sheet_name='Base Data', index=False)
                pd.DataFrame([report_data["Transportation"]]).to_excel(writer, sheet_name='Transportation', index=False)
                pd.DataFrame([report_data["Weight"]]).to_excel(writer, sheet_name='Weight', index=False)

                # Write material summary
                df_material.to_excel(writer, sheet_name='Material Savings', index=False)

                # Write DC related data if available
                if df_current_report is not None:
                    df_current_report.to_excel(writer, sheet_name='Current Emissions', index=False)
                if df_new_report is not None:
                    df_new_report.to_excel(writer, sheet_name='New Emissions', index=False)
                if df_savings_report is not None:
                    df_savings_report.to_excel(writer, sheet_name='Savings Summary', index=False)

                writer.save()
            output.seek(0)
            return output

        # Generate Excel file in memory
        excel_file = generate_report()

        # Create a single download button
        st.download_button(
            label="📄 Download Report",
            data=excel_file,
            file_name=f"sustainability_calculator_{initiative_name}.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            type="primary"
        )
    except:
        st.info("Please fill in all inputs above before downloading the results report")
