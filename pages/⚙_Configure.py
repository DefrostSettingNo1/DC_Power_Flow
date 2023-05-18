import streamlit as st

from main import import_data, manipulate_static_data_sheets, create_static_network_elements, \
    filter_tec_ic_to_recognizables, create_load_gen, run_imbalance, delete_load_gen, run_and_critical

TEC_Register, IC_Register, FES_2022_GSP_Dem, NGET_Circuits, NGET_Circuit_Changes, NGET_Subs, NGET_Tx, NGET_Tx_Changes, Sub_Coordinates = import_data()
bus_ids_df, TEC_Register, IC_Register = manipulate_static_data_sheets(TEC_Register,IC_Register,FES_2022_GSP_Dem,NGET_Circuits,NGET_Circuit_Changes,NGET_Subs,NGET_Tx,NGET_Tx_Changes,Sub_Coordinates)
net = create_static_network_elements(bus_ids_df,NGET_Circuits,NGET_Tx)
TEC_Register_With_Bus, IC_Register_With_Bus, FES_2022_GSP_Dem = filter_tec_ic_to_recognizables(net,NGET_Subs,TEC_Register,IC_Register,FES_2022_GSP_Dem)
st.session_state.coord = Sub_Coordinates
# .rename(columns={'Geolocation (Latitude)': 'latitude', 'Geolocation (Longitude)': 'longitude', 'Site Name': 'name'})

# future dev is to add SGT into column_data and ensure that trafo outages are translated into outage in run_and_critical in main.py
# column_data = net.line["name"].tolist() + net.trafo["name"].tolist()
column_data = net.line["name"].tolist()

# ext_grid_imb = 0

st.title("Set Network Background")
st.text('\n')
st.subheader(":blue[Define your network background below (if different to default):]")
st.text('\n')
with st.expander("Outages"):
    st.title("Select Outage(s)")
    outage_list = column_data
    st.session_state.outages = st.multiselect(
        "Select your outage(s)",
        outage_list
    )

# gen_dem_expander = st.expander("Generation and Demand Background")
expander_gen = st.expander("Scale Generation and Demand")
with expander_gen:
    st.title("Define generation and demand scaling factors")
    container_gen = st.container()
    with container_gen:
        check = st.checkbox(":blue[**Click here to define your own load and generation background.**]")
        if check:
            st.session_state.user_input_1 = st.number_input("Type scaling factor for E&W FES LTW 2027 Demand (range 0.5 to 1)", min_value=0.5, max_value=1.0, value=1.0, step=0.05)
            st.session_state.user_input_2 = st.number_input("Type scaling factor for E&W Interconnector (range -1 to 1)", min_value=-1.0, max_value=1.0, value=0.0, step=0.05)
            st.session_state.user_input_3 = st.number_input("Type scaling factor for E&W Wind (range 0 to 1)", min_value=0.0, max_value=1.0, value=0.5, step=0.05)
            st.session_state.user_input_4 = st.number_input("Type scaling factor for E&W PV (range 0 to 1)", min_value=0.0, max_value=1.0, value=0.0, step=0.05)
            st.session_state.user_input_5 = st.number_input("Type scaling factor for E&W Nuclear (range 0 to 1)", min_value=0.0, max_value=1.0, value=0.9, step=0.05)
            st.session_state.user_input_6 = st.number_input("Type scaling factor for E&W BESS (range 0 to 1)", min_value=0.0, max_value=1.0, value=0.5, step=0.05)
            st.session_state.user_input_7 = st.number_input("Type scaling factor for all other generation in E&W (range 0 to 1)", min_value=0.0, max_value=1.0, value=0.35, step=0.05)
            st.write("B6 transfer (N-S) = {}".format("4.6GW" if st.session_state.user_input_3 == "" else "{}GW".format(round(float(st.session_state.user_input_3) * 7, 2))))
            st.markdown("***_Note B6 transfer is calculated as: Wind scaling factor * 7GW (capped at 6GW)_**")

            # review below code due to improvement made introducing number_input above instead of old text_input
            # st.session_state.text_inputs = ["1" if st.session_state.user_input_1 == "" else st.session_state.user_input_1,
            #                "0" if st.session_state.user_input_2 == "" else st.session_state.user_input_2,
            #                "0.5" if st.session_state.user_input_3 == "" else st.session_state.user_input_3,
            #                "0" if st.session_state.user_input_4 == "" else st.session_state.user_input_4,
            #                "0.7" if st.session_state.user_input_5 == "" else st.session_state.user_input_5,
            #                "0.6" if st.session_state.user_input_6 == "" else st.session_state.user_input_6,
            #                "0.3" if st.session_state.user_input_7 == "" else st.session_state.user_input_7,
            #                "4.6GW" if st.session_state.user_input_3 == "" else "{}GW".format(
            #                    round(float(st.session_state.user_input_3) * 7),1)
            #                ]
            st.session_state.text_inputs = [st.session_state.user_input_1,
                                            st.session_state.user_input_2,
                                            st.session_state.user_input_3,
                                            st.session_state.user_input_4,
                                            st.session_state.user_input_5,
                                            st.session_state.user_input_6,
                                            st.session_state.user_input_7,
                                            round(float(st.session_state.user_input_3) * 7, 2)]
        else:
            st.session_state.text_inputs = [1, 0, 0.5, 0, 0.9, 0.5, 0.35, f"{0.5*7}GW"]
        check_button = st.button("Check imbalance")
        if check_button:
            demand_scaling, scale_interconnector, scale_wind, scale_pv, scale_nuclear, scale_bess, scale_all_other = [float(st.session_state.text_inputs[i]) for i in range(7)]
            net = create_load_gen(demand_scaling, scale_interconnector, scale_wind, scale_pv, scale_nuclear, scale_bess,scale_all_other, net, FES_2022_GSP_Dem, TEC_Register_With_Bus, IC_Register_With_Bus)
            net, line_tx_results_pre_int_sorted = run_imbalance(net)
            st.session_state.ext_grid_imb = round(float(net.res_ext_grid["p_mw"].sum()), 1)
            net = delete_load_gen(net)
            if -500 < st.session_state.ext_grid_imb < 500:
                st.success("User input saved! Imbalance less than 500MW")
            else:
                st.error("Please readjust scaling to reduce imbalance to less than 500MW. If you would like to apply the default values please clear your input(s)")
            st.metric("**Imbalance:**", f"{st.session_state.ext_grid_imb} MW")

outages = st.session_state.outages
list_o = ""
for i in outages:
    list_o += "- " + f":blue[{i}]" + "\n"

list_n = ""
types_for_list_n = ["Demand:","Interconnector:","Wind:","PV: ","Nuclear:","BESS:","All other generation:", "B6 transfer (N->S):"]
for i, j in zip(st.session_state.text_inputs, types_for_list_n):
    list_n += "- " + j + "  " + f"**:blue[{i}]**" + "\n"

st.text('\n')

st.divider()

st.subheader(":blue[The following Network Background is being applied:]")

with st.container():
    st.write("**Outage Background:**")
    st.markdown(list_o)

st.text('\n')

with st.container():
    st.write("**Generation and Demand Background:**")
    st.markdown(list_n)
    st.text('\n')

st.text('\n')

st.subheader("**:orange[Click _'Run DC Power Flow Analysis'_ in the sidebar to run all contingencies]**")

with st.sidebar:
    st.text('\n')
    if st.button("⚡  **Run DC Power Flow Analysis**  ⚡"):
        demand_scaling, scale_interconnector, scale_wind, scale_pv, scale_nuclear, scale_bess, scale_all_other = [
            float(st.session_state.text_inputs[i]) for i in range(7)]
        net = create_load_gen(demand_scaling, scale_interconnector, scale_wind, scale_pv, scale_nuclear, scale_bess,
                              scale_all_other, net, FES_2022_GSP_Dem, TEC_Register_With_Bus, IC_Register_With_Bus)
        net, line_tx_results_pre_int_sorted = run_imbalance(net)
        st.session_state.line_tx_results_pre_int_sorted = line_tx_results_pre_int_sorted
        st.session_state.gen_info = net.sgen[["name","p_mw","q_mvar","in_service","max_p_mw"]]
        st.session_state.load_info = net.load[["name","p_mw","q_mvar","in_service"]]
        st.session_state.bus_info = net.bus[["name", "vn_kv", "in_service"]]
        st.session_state.line_info = net.line[["name", "length_km", "max_i_ka", "in_service"]]
        st.session_state.ext_grid_imb = round(float(net.res_ext_grid["p_mw"].sum()),1)
        if -500 < st.session_state.ext_grid_imb < 500:
            st.markdown(f":green[Imbalance = **{st.session_state.ext_grid_imb} MW**]")
            with st.spinner(text=":orange[DC power flow contingencies running...]"):
                overall_result_sorted, outage_line_name, critical_lines, line_tx_results_pre_sorted = run_and_critical(outages, net)
                st.session_state.overall_result_sorted = overall_result_sorted
                st.session_state.outage_line_name = outage_line_name
                st.session_state.critical_lines = critical_lines
                st.session_state.line_tx_results_pre_sorted = line_tx_results_pre_sorted
            st.success("**Done! Please view the Results page.**")
        else:
            st.markdown(st.session_state.ext_grid_imb)
            st.error("**There is an imbalance > 500MW, please review your scaling factors above.**")
