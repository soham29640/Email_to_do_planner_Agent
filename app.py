import streamlit as st
import numpy as np
import pandas as pd

if "show_sidebar" not in st.session_state:
    st.session_state.show_sidebar = False

col1, col2 = st.columns([1, 10])  
with col1:
    if st.button("☰"):
        st.session_state.show_sidebar = not st.session_state.show_sidebar

if st.session_state.show_sidebar:
    with st.container():
        st.subheader("Choose one option")
        option = st.radio("Choose one:", ["Class Routine", "Study Routine"])
        st.session_state.show = option

if "show" not in st.session_state:
    st.session_state.show = "Class Routine"

if st.session_state.show == "Class Routine":
    df_main = pd.read_excel("5th Sem Timetable.xlsx", sheet_name="5th Sem Core")
    df_main = df_main.dropna(how='all') 

    df_elec = pd.read_excel("5th Sem Timetable.xlsx", sheet_name="5th Sem Elective")
    df_elec = df_elec.dropna(how='all')  

    if "Section" in df_main.columns:

        df_main_cse21 = df_main[df_main["Section"] == "CSE-21"]
        df_main_cse21 = df_main_cse21.reset_index(drop=True)

        # HPC_CS-20 extraction
        df_elec_HPC_CS20 = df_elec[df_elec["Section(DE)"] == "HPC_CS-20"]
        df_elec_HPC_CS20 = df_elec_HPC_CS20.reset_index(drop=True)

        found_hpc = []
        for idx, row in df_elec_HPC_CS20.iterrows():
            day = row["DAY"]
            for i in range(2, len(df_elec_HPC_CS20.columns)):
                if row[df_elec_HPC_CS20.columns[i]] == "HPC(DE)":
                    time = df_elec_HPC_CS20.columns[i]
                    roomno = row[df_elec_HPC_CS20.columns[i - 1]]
                    found_hpc.append((day, time, roomno))

        # DMDW_CS-5 extraction
        df_elec_DMDW_CS5 = df_elec[df_elec["Section(DE)"] == "DMDW_CS-5"]
        df_elec_DMDW_CS5 = df_elec_DMDW_CS5.reset_index(drop=True)

        found_dmdw = []
        for idx, row in df_elec_DMDW_CS5.iterrows():
            day = row["DAY"]
            for i in range(2, len(df_elec_DMDW_CS5.columns)):
                if row[df_elec_DMDW_CS5.columns[i]] == "DMDW(DE)":
                    time = df_elec_DMDW_CS5.columns[i]
                    roomno = row[df_elec_DMDW_CS5.columns[i - 1]]
                    found_dmdw.append((day, time, roomno))

        # Display class routine
        st.subheader("📘 Class Routine - CSE-21")    
        st.dataframe(df_main_cse21)

        # Display elective findings
        st.markdown("### 🔍 HPC_CS-20 - Schedule")
        if found_hpc:
            for day, time, room in found_hpc:
                st.write(f"📘 On **{day}** at **{time}**, Room: `{room}`")
        else:
            st.info("No HPC(DE) found in HPC_CS-20")

        st.markdown("### 🔍 DMDW_CS-5 - Schedule")
        if found_dmdw:
            for day, time, room in found_dmdw:
                st.write(f"📘 On **{day}** at **{time}**, Room: `{room}`")
        else:
            st.info("No DMDW(DE) found in DMDW_CS-5")

    else:
        st.warning("No 'Section' column found in the Excel file.")

elif st.session_state.show == "Study Routine":
    st.subheader("📖 Study Routine")
    st.markdown("Study routine content goes here...")
