import pandapower as pp
import pandas as pd
import numpy as np
import streamlit as st
import requests
import json
import re
from PIL import Image

@st.cache_data
def import_data():

    # proxies = {
    #               "http"  : "http://proxy.invzb.uk.corporg.net:8083",
    #               "https" : "http://proxy.invzb.uk.corporg.net:8083"
    #             }

    # url = "https://www.nationalgrideso.com/document/275586/download"
    # response = requests.get(url, proxies = proxies)
    # if response.status_code == 200:
    #     NGET_Circuits = pd.read_excel(response.content, sheet_name="B-2-1c", skiprows=[0])
    #     NGET_Circuit_Changes = pd.read_excel(response.content, sheet_name="B-2-2c", skiprows=[0])
    #     NGET_Subs = pd.read_excel(response.content, sheet_name="B-1-1c", skiprows=[0])
    #     NGET_Tx = pd.read_excel(response.content, sheet_name="B-3-1c", skiprows=[0])
    #     NGET_Tx_Changes = pd.read_excel(response.content, sheet_name="B-3-2c", skiprows=[0])
    # #     NGET_Reactive = pd.read_excel(response.content, sheet_name = "B-4-1c", skiprows=[0])
    # #     NGET_Reactive_Changes = pd.read_excel(response.content, sheet_name = "B-4-2c", skiprows=[0])
    # else:
    #     print("Failed to download ETYS Appendix B file from https://www.nationalgrideso.com/document/275586/download")

    # url = "https://data.nationalgrideso.com/api/3/action/datastore_search"
    # params = {
    #     "resource_id": "6a1d99c2-a3c5-4ae0-b66a-21e4c15a9ae6",
    #     "limit": 10000,
    #     "offset": 0,
    #     "filters": json.dumps({
    #         "scenario": "LW",
    #         "year": "27"
    #     })
    # }
    # all_data = []
    # while True:
    #     response = requests.get(url, params=params, proxies = proxies)
    #     if response.status_code == 200:
    #         data_dict = response.json()["result"]["records"]
    #         all_data.extend(data_dict)
    #         if len(data_dict) < 10000:
    #             break
    #         params["offset"] += 10000
    #     else:
    #         print(f"Error: {response.status_code} - {response.reason}")
    #         break
    # FES_2022_GSP_Dem = pd.DataFrame.from_dict(all_data)
    # FES_2022_GSP_Dem = FES_2022_GSP_Dem.groupby('GSP').agg(
    #     {'DemandPk': 'sum', 'DemandAM': 'sum', 'DemandPM': 'sum'}).reset_index()


    # url = "https://data.nationalgrideso.com/api/3/action/datastore_search"
    # resource_ids = ["000d08b9-12d9-4396-95f8-6b3677664836", "17becbab-e3e8-473f-b303-3806f43a6a10",
    #                 "64f7908f-f787-4977-93e1-5342a5f1357f"]
    # df_names = ["FES_2022_GSP_Info", "TEC_Register", "IC_Register"]
    # dfs = {}
    # for i, res_id in enumerate(resource_ids):
    #     params = {
    #         "resource_id": res_id,
    #         "limit": 10000,
    #         "offset": 0,
    #     }
    #     all_data = []
    #     while True:
    #         response = requests.get(url, params=params, proxies = proxies)
    #         if response.status_code == 200:
    #             data_dict = response.json()["result"]["records"]
    #             all_data.extend(data_dict)
    #             if len(data_dict) < 10000:
    #                 break
    #             params["offset"] += 10000
    #         else:
    #             print(f"Error: {response.status_code} - {response.reason}")
    #             break
    #     dfs[df_names[i]] = pd.DataFrame.from_dict(all_data)
    # TEC_Register = dfs["TEC_Register"]
    # TEC_Register.to_csv("TEC_Reg.csv")
    # IC_Register = dfs["IC_Register"]
    # IC_Register.to_csv("IC_Reg.csv")

    #macos
    Sub_Coordinates = pd.read_csv('./data/CRM_Sub_Coordinates_WGS84.csv')
    Sub_Coordinates.dropna(inplace = True)
    TEC_Register = pd.read_csv('./data/TEC_Reg.csv')
    IC_Register = pd.read_csv('./data/IC_Reg.csv')
    FES_2022_GSP_Dem = pd.read_csv('./data/FES_Dem.csv')
    NGET_Circuits = pd.read_excel('./data/Appendix B 2022.xlsx', sheet_name="B-2-1c", skiprows=[0])
    NGET_Circuit_Changes = pd.read_excel('./data/Appendix B 2022.xlsx', sheet_name="B-2-2c", skiprows=[0])
    NGET_Subs = pd.read_excel('./data/Appendix B 2022.xlsx', sheet_name="B-1-1c", skiprows=[0])
    NGET_Tx = pd.read_excel('./data/Appendix B 2022.xlsx', sheet_name="B-3-1c", skiprows=[0])
    NGET_Tx_Changes = pd.read_excel('./data/Appendix B 2022.xlsx', sheet_name="B-3-2c", skiprows=[0])
    Neptune_Contingencies_Unfiltered=pd.read_excel(r'C:\Users\kieran.frost2\DC_Power_Flow\data\Neptune_Contingencies.xlsx',sheet_name='Contingencies')
    Neptune_Contingency_Circuits_All=pd.read_excel(r'C:\Users\kieran.frost2\DC_Power_Flow\data\Neptune_Contingencies.xlsx',sheet_name='Circuits')
    #windows
    # Sub_Coordinates = pd.read_csv(r"C:\Users\nathanael.sims\PycharmProjects\DC_Power_Flow_Project\data\CRM_Sub_Coordinates_WGS84.csv")
    # Sub_Coordinates.dropna(inplace = True)
    # TEC_Register = pd.read_csv(r"C:\Users\nathanael.sims\PycharmProjects\DC_Power_Flow_Project\data\TEC_Reg.csv")
    # IC_Register = pd.read_csv(r"C:\Users\nathanael.sims\PycharmProjects\DC_Power_Flow_Project\data\IC_Reg.csv")
    # FES_2022_GSP_Dem = pd.read_csv(r"C:\Users\nathanael.sims\PycharmProjects\DC_Power_Flow_Project\data\FES_Dem.csv")
    # NGET_Circuits = pd.read_excel(r"C:\Users\nathanael.sims\PycharmProjects\DC_Power_Flow_Project\data\Appendix B 2022.xlsx", sheet_name="B-2-1c", skiprows=[0])
    # NGET_Circuit_Changes = pd.read_excel(r"C:\Users\nathanael.sims\PycharmProjects\DC_Power_Flow_Project\data\Appendix B 2022.xlsx", sheet_name="B-2-2c", skiprows=[0])
    # NGET_Subs = pd.read_excel(r"C:\Users\nathanael.sims\PycharmProjects\DC_Power_Flow_Project\data\Appendix B 2022.xlsx", sheet_name="B-1-1c", skiprows=[0])
    # NGET_Tx = pd.read_excel(r"C:\Users\nathanael.sims\PycharmProjects\DC_Power_Flow_Project\data\Appendix B 2022.xlsx", sheet_name="B-3-1c", skiprows=[0])
    # NGET_Tx_Changes = pd.read_excel(r"C:\Users\nathanael.sims\PycharmProjects\DC_Power_Flow_Project\data\Appendix B 2022.xlsx", sheet_name="B-3-2c", skiprows=[0])

    return TEC_Register, IC_Register, FES_2022_GSP_Dem, NGET_Circuits, NGET_Circuit_Changes, NGET_Subs, NGET_Tx, NGET_Tx_Changes, Sub_Coordinates,Neptune_Contingencies_Unfiltered,Neptune_Contingency_Circuits_All

@st.cache_data
def manipulate_static_data_sheets(TEC_Register,IC_Register,FES_2022_GSP_Dem,NGET_Circuits,NGET_Circuit_Changes,NGET_Subs,NGET_Tx,NGET_Tx_Changes,Sub_Coordinates,Neptune_Contingencies_Unfiltered,Neptune_Contingency_Circuits_All):
    TEC_Register = TEC_Register[~TEC_Register["Project Name"].isin(["Drax (Coal)",
                                                                       "Dungeness B",
                                                                       "Hartlepool",
                                                                       "Hinkley Point B",
                                                                       "Uskmouth",
                                                                       "Sutton Bridge",
                                                                       "Ratcliffe on Soar",
                                                                       "West Burton A"])]
    TEC_Register["Generator Name"] = TEC_Register["Project Name"] + " (" + TEC_Register["Customer Name"] + ")"
    TEC_Register.drop(columns=["Stage", "Project ID", "Project Name", "Customer Name"], inplace=True, axis=1)
    TEC_Register = TEC_Register[TEC_Register["HOST TO"] == "NGET"]
    TEC_Register['MW Effective From'] = pd.to_datetime(TEC_Register['MW Effective From'], errors='coerce')
    TEC_Register = TEC_Register[
        (TEC_Register['MW Effective From'].isnull()) | (TEC_Register['MW Effective From'] < pd.to_datetime("2028-01-01"))]
    TEC_Register['MW Effective From'] = TEC_Register['MW Effective From'].dt.strftime('%d-%m-%Y')
    TEC_Register.reset_index(inplace=True)

    IC_Register["Generator Name"] = IC_Register["Project Name"] + " (" + IC_Register["Connection Site"] + ")"
    IC_Register = IC_Register[IC_Register["HOST TO"] == "NGET"]
    IC_Register['MW Effective From'] = pd.to_datetime(IC_Register['MW Effective From'], errors='coerce')
    IC_Register = IC_Register[
        (IC_Register['MW Effective From'].isnull()) | (IC_Register['MW Effective From'] < pd.to_datetime("2028-01-01"))]
    IC_Register['MW Effective From'] = IC_Register['MW Effective From'].dt.strftime('%d-%m-%Y')
    IC_Register.reset_index(inplace=True)

    ##create list of bus ids from NGET Circuit and Transformer data in ETYS
    bus_ids_cct = pd.unique(NGET_Circuits[['Node 1', 'Node 2']].values.ravel('K'))
    bus_ids_tx = pd.unique(NGET_Tx[['Node1', 'Node2']].values.ravel('K'))
    bus_ids = np.union1d(bus_ids_cct, bus_ids_tx)

    ##convert list into dataframe and add derived voltage value into a vn_kv column. Filter out any non-400kV & 275kV.
    bus_ids_data = {"name": bus_ids, "vn_kv": []}
    for bus_id in bus_ids:
        if bus_id[4] == "4":
            bus_ids_data["vn_kv"].append(400)
        elif bus_id[4] == "2":
            bus_ids_data["vn_kv"].append(275)
        else:
            bus_ids_data["vn_kv"].append("")
    bus_ids_df = pd.DataFrame(bus_ids_data)
    bus_ids_df = bus_ids_df[bus_ids_df["vn_kv"] != ""]
    bus_ids_df.reset_index(drop=True, inplace=True)
    bus_ids_df["index"] = bus_ids_df.reset_index().index
    
    '''
        CONTINGENCY WORK
    '''
    Neptune_Contingency_Node_Numbers=pd.Series(pd.concat([Neptune_Contingencies_Unfiltered['CCT_ID Outage 1'],Neptune_Contingencies_Unfiltered['CCT_ID Outage 2']]).unique())
    Neptune_Contingency_Lines_Decomposed=Neptune_Contingency_Circuits_All[Neptune_Contingency_Circuits_All['CCT_ID'].isin(Neptune_Contingency_Node_Numbers)] #LINE NAME AND NODES CONNECTED
    Neptune_Contingency_Lines_Decomposed=Neptune_Contingency_Lines_Decomposed.reset_index(drop=True)
    
    Net_Nodes=pd.Series(pd.concat([NGET_Circuits['Node 1'],NGET_Circuits['Node 2'],NGET_Tx['Node1'],NGET_Tx['Node2']]).unique())
    Contingency_Nodes=pd.Series(pd.concat([Neptune_Contingency_Lines_Decomposed['Bus 1'],Neptune_Contingency_Lines_Decomposed['Bus 2']]).unique())
    
    Neptune_Conflictions = Contingency_Nodes[~Contingency_Nodes.isin(Net_Nodes)] #39 Name Changes Needed
    Neptune_Conflictions_Resolved=pd.DataFrame(columns=['Neptune','Net'])
    Neptune_Conflictions_Resolved['Neptune']=Neptune_Conflictions
    Neptune_Conflictions_Resolved=Neptune_Conflictions_Resolved.reset_index(drop=True)
    i=0
    
    #REPLACING ENTRIES IN NEPTUNE WHERE RUNNING ARRANGEMENTS HAVE BEEN ALTERED
    for entry in Neptune_Conflictions:
        entry=list(entry)
        if entry[5]=='1':
            entry[5]= 'A'
        elif entry[5]=='2':
            entry[5]='B'
        elif entry[5]=='A':
            entry[5]=='1'
        elif entry[5]=='B':
            entry[5]=='2'
        entry=''.join(entry)
        Neptune_Conflictions_Resolved.loc[i,'Net']=entry
        i+=1

    Neptune_Conflictions_Resolved = Neptune_Conflictions_Resolved[Neptune_Conflictions_Resolved['Net'].isin(Net_Nodes)] #24 NAMES NEED CHANGING TO MATCH THOSE FOUND IN THE NET  
    
    #----------------------------------------
    #Replacing in Index Help Guide - Neptune_Contingency_Lines_Decomposed

    i=0
    for entry in Neptune_Conflictions_Resolved['Neptune']:
        Neptune_Contingency_Lines_Decomposed=Neptune_Contingency_Lines_Decomposed.replace(entry,Neptune_Conflictions_Resolved.iloc[i]['Net'])
        i+=1

    #----------------------------------------

    #REMOVING THE NODES CAN'T SOLVE FROM THE LINE DATABASE

    #producing contingencies in usable format and then generating line names from the buses
    Neptune_Contingencies_Filtered=Neptune_Contingencies_Unfiltered[['CCT_ID Outage 1','CCT_ID Outage 2']].copy()
    Neptune_Contingencies_Filtered['cont1 - bus1'],Neptune_Contingencies_Filtered['cont1 - bus2'],Neptune_Contingencies_Filtered['cont2 - bus1'],Neptune_Contingencies_Filtered['cont2 - bus2'],Neptune_Contingencies_Filtered['line1'],Neptune_Contingencies_Filtered['line2']='','','','','',''

    a=[]
    for i in range(Neptune_Contingencies_Filtered.shape[0]):
        try:
            temp=(Neptune_Contingency_Lines_Decomposed.index[Neptune_Contingency_Lines_Decomposed['CCT_ID'] == Neptune_Contingencies_Filtered.iloc[i]['CCT_ID Outage 1']].to_list())[0] #FIND ROW NUMBER OF PLANNED CCT_ID SO CAN EXTRACT BUS NODES
            Neptune_Contingencies_Filtered.loc[i,'cont1 - bus1']=Neptune_Contingency_Lines_Decomposed.iloc[temp]['Bus 1']
            Neptune_Contingencies_Filtered.loc[i,'cont1 - bus2']=Neptune_Contingency_Lines_Decomposed.iloc[temp]['Bus 2']
            temp=(Neptune_Contingency_Lines_Decomposed.index[Neptune_Contingency_Lines_Decomposed['CCT_ID'] == Neptune_Contingencies_Filtered.iloc[i]['CCT_ID Outage 2']].to_list())[0] #FIND ROW NUMBER OF PLANNED CCT_ID SO CAN EXTRACT BUS NODES
            Neptune_Contingencies_Filtered.loc[i,'cont2 - bus1']=Neptune_Contingency_Lines_Decomposed.iloc[temp]['Bus 1']
            Neptune_Contingencies_Filtered.loc[i,'cont2 - bus2']=Neptune_Contingency_Lines_Decomposed.iloc[temp]['Bus 2']    
            Neptune_Contingencies_Filtered.loc[i,'line1']=str(Neptune_Contingencies_Filtered.loc[i,'cont1 - bus1'])+'-'+str(Neptune_Contingencies_Filtered.loc[i,'cont1 - bus2'])
            Neptune_Contingencies_Filtered.loc[i,'line2']=str(Neptune_Contingencies_Filtered.loc[i,'cont2 - bus1'])+'-'+str(Neptune_Contingencies_Filtered.loc[i,'cont2 - bus2'])
        except:
            a.append(i)
            
    Neptune_Contingencies_Filtered=Neptune_Contingencies_Filtered.drop(Neptune_Contingencies_Filtered.index[a]) #REMOVING THE PROBLEM CONTINGENCIES

    return bus_ids_df, TEC_Register, IC_Register,Neptune_Contingencies_Filtered



@st.cache_data
def create_static_network_elements(bus_ids_df,NGET_Circuits,NGET_Tx):
    ##create blank network
    net = pp.create_empty_network()
    ##add contents from bus_ids_df into net create_bus
    for index, row in bus_ids_df.iterrows():
        voltage_level = row["vn_kv"]
        bus_name = row["name"]
        index = row["index"]
        # geodata = row["geodata"]
        pp.create_bus(net, vn_kv=voltage_level, name=bus_name, index=index, type="b", zone=None,
                      in_service=True, max_vm_pu=1.05, min_vm_pu=0.95)

    for k, row in NGET_Circuits.iterrows():
        if row['B (% on 100 MVA)'] > 0.00:
            if len(row['Node 1']) >= 5 and row['Node 1'][4] in ['4', '2']:
                if (net.bus['name'] == row['Node 1']).any():
                    Node_1_row1 = int(net.bus.loc[net.bus['name'] == row['Node 1']].index[0])
                else:
                    Node_1_row1 = 0
                if (net.bus['name'] == row['Node 2']).any():
                    Node_2_row1 = int(net.bus.loc[net.bus['name'] == row['Node 2']].index[0])
                else:
                    Node_2_row1 = 0
                if row['OHL Length (km)'] + row['Cable Length (km)'] > 1:
                    length = row['OHL Length (km)'] + row['Cable Length (km)']
                else:
                    length == 0.1
                name = f"{row['Node 1']}-{row['Node 2']}"
                base_voltage = 400.0 if row['Node 1'][4] == '4' else 275.0
                base_impedance = (base_voltage ** 2) / 100.0
                r_ohm_per_km = row['R (% on 100 MVA)'] * base_impedance / (100 * length)
                if row['R (% on 100 MVA)'] < 0.001:
                    r_ohm_per_km = 0.1
                x_ohm_per_km = row['X (% on 100 MVA)'] * base_impedance / (100 * length)
                if row['X (% on 100 MVA)'] < 0.001:
                    x_ohm_per_km = 0.1
                c_nf_per_km = 1
                # c_nf_per_km = (row['B (% on 100 MVA)'] / (2 * 3.141592654 * 50 * base_voltage**2)) * 10**3
                max_i_ka = (row['Spring Rating (MVA)'] / (1.732050808 * base_voltage))
                pp.create_line_from_parameters(net, from_bus=Node_1_row1, to_bus=Node_2_row1, length_km=length,
                                               r_ohm_per_km=r_ohm_per_km, x_ohm_per_km=x_ohm_per_km,
                                               c_nf_per_km=c_nf_per_km, max_i_ka=max_i_ka, name=name, df=1.0, parallel=1)

    for z, row in NGET_Circuits.iterrows():
        if row['B (% on 100 MVA)'] == 0.0:
            if len(row['Node 1']) >= 5 and row['Node 1'][4] in ['4', '2']:
                if (net.bus['name'] == row['Node 1']).any():
                    Node_1_row1 = int(net.bus.loc[net.bus['name'] == row['Node 1']].index[0])
                else:
                    Node_1_row1 = 0
                if (net.bus['name'] == row['Node 2']).any():
                    Node_2_row1 = int(net.bus.loc[net.bus['name'] == row['Node 2']].index[0])
                else:
                    Node_2_row1 = 0
                name = f"{row['Node 1']}-{row['Node 2']}"
                r_pu = row['R (% on 100 MVA)'] if float(row['R (% on 100 MVA)']) > 0.0001 else 0.0001
                x_pu = row['X (% on 100 MVA)'] if float(row['X (% on 100 MVA)']) > 0.0001 else 0.0001
                sn_mva = row['Spring Rating (MVA)']
                pp.create_impedance(net, from_bus=Node_1_row1, to_bus=Node_2_row1, rft_pu=r_pu, xft_pu=x_pu, rtf_pu=r_pu,
                                    xtf_pu=x_pu, sn_mva=sn_mva, name=name, in_service=True)

    for l, row in NGET_Tx.iterrows():
        if len(row['Node1']) >= 5 and row['Node1'][4] == '4' and row['Node2'][4] == '2':
            if (net.bus['name'] == row['Node1']).any():
                Node_1_row2 = int(net.bus.loc[net.bus['name'] == row['Node1']].index[0])
            else:
                Node_1_row2 = 0
            if (net.bus['name'] == row['Node2']).any():
                Node_2_row2 = int(net.bus.loc[net.bus['name'] == row['Node2']].index[0])
            else:
                Node_2_row2 = 0
            name = f"{row['Node1']}-{row['Node2']} - SGT"
            sn_mva = row['Rating (MVA)']
            vkr_percent = row['R (% on 100MVA)']
            vk_percent = row['X (% on 100MVA)']
            pfe_kw = 60
            i0_percent = 0.06
            pp.create_transformer_from_parameters(net, hv_bus=Node_1_row2, lv_bus=Node_2_row2, sn_mva=sn_mva,
                                                  vn_hv_kv=400.0, vn_lv_kv=275.0, vkr_percent=vkr_percent,
                                                  vk_percent=vk_percent, pfe_kw=pfe_kw, i0_percent=i0_percent, name=name)

    for y, row in NGET_Tx.iterrows():
        if len(row['Node1']) >= 5 and (row['Node1'][4] == '4' and row['Node2'][4] == '4') or (
                row['Node1'][4] == '2' and row['Node2'][4] == '2'):
            if (net.bus['name'] == row['Node1']).any():
                Node_1_row2 = int(net.bus.loc[net.bus['name'] == row['Node1']].index[0])
            else:
                Node_1_row2 = 0
            if (net.bus['name'] == row['Node2']).any():
                Node_2_row2 = int(net.bus.loc[net.bus['name'] == row['Node2']].index[0])
            else:
                Node_2_row2 = 0
            name = f"{row['Node1']}-{row['Node2']}"
            r_pu = row['R (% on 100MVA)'] if float(row['R (% on 100MVA)']) > 0.0001 else 0.0001
            x_pu = row['X (% on 100MVA)'] if float(row['X (% on 100MVA)']) > 0.0001 else 0.0001
            sn_mva = row['Rating (MVA)']
            pp.create_impedance(net, from_bus=Node_1_row1, to_bus=Node_2_row2, rft_pu=r_pu, xft_pu=x_pu, rtf_pu=r_pu,
                                xtf_pu=x_pu, sn_mva=sn_mva, name=name, in_service=True)

    pp.create_ext_grid(net, bus=155, vm_pu=1, va_degree=0, name='Heysham_Slack_Bus', in_service=True,
                       s_sc_min_mva=14000, rx_min=0.2)

    return net

@st.cache_data
def filter_tec_ic_to_recognizables(net,NGET_Subs,TEC_Register,IC_Register,FES_2022_GSP_Dem):
    net.bus['fullname'] = ""
    for i, row1 in net.bus.iterrows():
        if len(net.bus.loc[i, 'name']) >= 5:
            node = net.bus.loc[i, 'name'][5]
        else:
            node = ''
        for j, row2 in NGET_Subs.iterrows():
            if row2['Site Code'] in row1['name']:
                voltage = '400kV' if net.bus.loc[i, 'vn_kv'] == 400.0 else '275kV'
                if node != '':
                    net.bus.loc[i, 'fullname'] = row2['Site Name'] + ' ' + voltage + ' Node:' + node
                else:
                    net.bus.loc[i, 'fullname'] = row2['Site Name'] + ' ' + voltage

    TEC_Register = TEC_Register.dropna(subset=['Connection Site'])
    for i, row in TEC_Register.iterrows():
        connection_site = str(row["Connection Site"]).upper()
        x = None
        match = re.search(r"\d+", connection_site)
        if match:
            x = connection_site[:match.start()]
        elif "GSP" in connection_site:
            x = connection_site.split("GSP")[0].strip()
        if x:
            mask = net.bus["fullname"].str.contains(fr"\b{x}\b", case=False)
            if mask.any():
                TEC_Register.loc[i, "bus"] = net.bus[mask].index[0]

    TEC_Register.reset_index(drop=True, inplace=True)
    TEC_Register_With_Bus = TEC_Register[pd.to_numeric(TEC_Register['bus'], errors='coerce').notnull()]
    TEC_Register_With_Bus.reset_index(drop=True, inplace=True)
    TEC_Register_With_Bus['Gen_Type'] = ""
    for i, row in TEC_Register_With_Bus.iterrows():
        if re.search('(?i).*nuclear.*', f"{row['Plant Type']} {row['Generator Name']}"):
            TEC_Register_With_Bus.at[i, 'Gen_Type'] = "Nuclear"
        elif re.search('(?i).*wind.*', f"{row['Plant Type']} {row['Generator Name']}"):
            TEC_Register_With_Bus.at[i, 'Gen_Type'] = "Wind"
        elif re.search('(?i).*pv|solar.*', f"{row['Plant Type']} {row['Generator Name']}"):
            TEC_Register_With_Bus.at[i, 'Gen_Type'] = "PV"
        elif re.search('(?i).*CCGT|CHP|Biomass| gas .*', f"{row['Plant Type']} {row['Generator Name']}"):
            TEC_Register_With_Bus.at[i, 'Gen_Type'] = "CCGT/CHP/Biomass"
        elif re.search('(?i).*pump|hydro.*', f"{row['Plant Type']} {row['Generator Name']}"):
            TEC_Register_With_Bus.at[i, 'Gen_Type'] = "Hydro/Pump"
        elif re.search('(?i).*energy storage|battery|bess.*', f"{row['Plant Type']} {row['Generator Name']}"):
            TEC_Register_With_Bus.at[i, 'Gen_Type'] = "BESS"
        else:
            TEC_Register_With_Bus.at[i, 'Gen_Type'] = "Other"

    IC_Register = IC_Register.dropna(subset=['Connection Site'])
    for i, row in IC_Register.iterrows():
        connection_site = str(row["Connection Site"]).upper()
        x = None
        match = re.search(r"\d+", connection_site)
        if match:
            x = connection_site[:match.start()]
        elif "GSP" in connection_site:
            x = connection_site.split("GSP")[0].strip()
        if x:
            mask = net.bus["fullname"].str.contains(fr"\b{x}\b", case=False)
            if mask.any():
                IC_Register.loc[i, "bus"] = net.bus[mask].index[0]

    IC_Register.reset_index(drop=True, inplace=True)
    IC_Register_With_Bus = IC_Register[pd.to_numeric(IC_Register['bus'], errors='coerce').notnull()]
    IC_Register_With_Bus.reset_index(drop=True, inplace=True)

    FES_2022_GSP_Dem['bus_id'] = ""
    FES_2022_GSP_Dem['Demand_Summer_Peak'] = ""
    for m, row in FES_2022_GSP_Dem.iterrows():
        if (net.bus['name'].str.lower().str[:4] == row['GSP'].lower()[:4]).any():
            FES_2022_GSP_Dem.loc[m,"bus_id"] = int(net.bus.loc[net.bus['name'].str.lower().str[:4] == row['GSP'].lower()[:4]].index[0])
        else:
            continue
        FES_2022_GSP_Dem.loc[m,'Demand_Summer_Peak'] = (int(FES_2022_GSP_Dem.loc[m,'DemandPk']) + int(FES_2022_GSP_Dem.loc[m,'DemandPM']))/2
    FES_2022_GSP_Dem = FES_2022_GSP_Dem[FES_2022_GSP_Dem['bus_id']!=""]

    tot_wind = TEC_Register_With_Bus.loc[TEC_Register_With_Bus['Gen_Type'] == 'Wind', ['MW Connected', 'MW Increase / Decrease']].sum(axis=1).clip(lower=0).sum()

    return TEC_Register_With_Bus, IC_Register_With_Bus, FES_2022_GSP_Dem, tot_wind

def create_load_gen(demand_scaling, scale_interconnector, scale_wind, scale_pv, scale_nuclear, scale_bess, scale_gas, scale_pump, scale_all_other, net, FES_2022_GSP_Dem, TEC_Register_With_Bus, IC_Register_With_Bus):
    # global FES_2022_GSP_Dem
    for m, row in FES_2022_GSP_Dem.iterrows():
        load_name = f"{row['GSP']}__FES-LTW-2027"
        load_bus = row['bus_id']
        Demand_Winter_Peak = row['DemandPk']
        Demand_Summer_AM_Min = row['DemandAM']
        Demand_Summer_PM_Min = row['DemandPM']
        Demand_Summer_Peak = row['Demand_Summer_Peak']
        p_mw = Demand_Summer_Peak * demand_scaling
        q_mvar = 0
        pp.create_load(net, bus=load_bus, p_mw=p_mw, q_mvar=q_mvar, const_z_percent=0, const_i_percent=0, name=load_name,
                       scaling=1, in_service=True)
    # global TEC_Register_With_Bus
    for n, row in TEC_Register_With_Bus.iterrows():
        gen_name = row['Generator Name']
        gen_bus = row['bus']
        type_gen = row['Gen_Type']
        max_p_mw = float(row['MW Connected']) + float(row['MW Increase / Decrease']) if float(row['MW Connected']) + float(
            row['MW Increase / Decrease']) > 0 else 0
        if re.search('(?i).*nuclear.*', f"{row['Plant Type']} {row['Generator Name']}"):
            scaling = scale_nuclear
        elif re.search('(?i).*wind.*', f"{row['Plant Type']} {row['Generator Name']}"):
            scaling = scale_wind
        elif re.search('(?i).*pv|solar.*', f"{row['Plant Type']} {row['Generator Name']}"):
            scaling = scale_pv
        elif re.search('(?i).*CCGT|CHP|Biomass| gas .*', f"{row['Plant Type']} {row['Generator Name']}"):
            scaling = scale_gas
        elif re.search('(?i).*pump|hydro.*', f"{row['Plant Type']} {row['Generator Name']}"):
            scaling = scale_pump
        elif re.search('(?i).*energy storage|battery|bess.*', f"{row['Plant Type']} {row['Generator Name']}"):
            scaling = scale_bess
        else:
            scaling = scale_all_other
        p_mw = max_p_mw * scaling
        pp.create_sgen(net, bus=gen_bus, p_mw=p_mw, q_mvar=0, name=gen_name, type=type_gen, scaling=1, in_service=True, max_p_mw=max_p_mw)
    # global IC_Register_With_Bus
    for n, row in IC_Register_With_Bus.iterrows():
        if 0 <= scale_interconnector <= 1:
            gen_name = row['Generator Name']
            gen_bus = row['bus']
            max_p_mw = row['MW Import - Total']
            scaling = scale_interconnector
            p_mw = max_p_mw * scaling
            pp.create_sgen(net, bus=gen_bus, p_mw=p_mw, q_mvar=0, name=gen_name, type="Interconnector", scaling=1, in_service=True, max_p_mw=max_p_mw)
        elif -1 <= scale_interconnector < 0:
            load_name = row['Generator Name']
            load_bus = row['bus']
            max_p_mw = row['MW Import - Total']
            scaling = scale_interconnector
            p_mw = float(row['MW Export - Total']) * -1 * scaling
            q_mvar = 0
            pp.create_load(net, bus=load_bus, p_mw=p_mw, q_mvar=q_mvar, type="Interconnector", const_z_percent=0, const_i_percent=0, name=load_name,
                           scaling=1, in_service=True)

    tot_wind = TEC_Register_With_Bus.loc[TEC_Register_With_Bus['Gen_Type'] == 'Wind', ['MW Connected', 'MW Increase / Decrease']].sum(axis=1).clip(lower=0).sum()
    b6_transfer_mw_0 = (-3.353e-6) * (scale_wind*tot_wind) ** 2 + 0.3758 * (scale_wind*tot_wind) - 61.84
    b6_transfer_mw = b6_transfer_mw_0 if b6_transfer_mw_0 < 6001 else 6000

    if b6_transfer_mw > 4000:
        w_link = 2200
        ac_route_1 = (b6_transfer_mw - w_link) * 0.56
        ac_route_2 = (b6_transfer_mw - w_link) * 0.44
    else:
        w_link = b6_transfer_mw / 3
        ac_route_1 = (b6_transfer_mw - w_link) * 0.56
        ac_route_2 = (b6_transfer_mw - w_link) * 0.44

    # create sgen for Harker
    pp.create_sgen(net, bus=148, p_mw=ac_route_2, q_mvar=0, name=".B6 transfer - Harker", type="B6 Transfer", scaling=1, in_service=True, max_p_mw=max_p_mw)
    # create sgen for Blyth
    pp.create_sgen(net, bus=23, p_mw=ac_route_1, q_mvar=0, name=".B6 transfer - Blyth + Stella West", type="B6 Transfer", scaling=1, in_service=True, max_p_mw=max_p_mw)
    # create sgen for Western Link
    pp.create_sgen(net, bus=124, p_mw=w_link, q_mvar=0, name=".B6 transfer - Western Link", type="B6 Transfer", scaling=1, in_service=True, max_p_mw=max_p_mw)

    return net

@st.cache_data
def contingency_line_net_nodes(net,Neptune_Contingencies_Filtered):
    '''
    MAIN BODY FOR LOOP
    1) CHECK EVERYTHING FOR LINE 1
    2) CHECK EVERYTGING FOR LINE 2
    
    STEPS BEING:
        1.IF LINE IN NET - APPEND LINE INDEX TO Neptune_Net_Line_Indices
        2.IF LINE IS NOT IN NET - SWAP THE BUS NODES DECLARING THE LINE AND SEARCH FOR THIS - E.G. SELLAFIELD LINES OPP. WAY ROUND IN NEPTUNE 
        3.IF NOT REMOVE CONNECTION NODE AND SEARCH FOR THIS IN THE REDACTED LIST OF NETWORK LINES Net_Line_Names_Removed_Nodes
        4.IF NONE OF THESE WORK FORGET THE CONTINGENCY CASE
        
    '''
    
    #SHOULD REALLY DEFINE A FUNCTION FOR THIS AS CAN RE-USE FOR BOTH EXCEP NUMBER e.g. 1 OR 2
    
    Neptune_Net_Line_Indices=pd.DataFrame(columns=['line1','line2'])
    Net_Line_Names=pd.Series(net.line["name"])
    Net_Line_Names_Removed_Nodes=net.line['name'].apply(lambda x: re.sub('(?<=\w{5})\w','',x)) #removing connection points as this may be where issues arise from
    
    #Line 1
    for i in range(Neptune_Contingencies_Filtered.shape[0]):
        if(Net_Line_Names.str.contains(Neptune_Contingencies_Filtered.iloc[i]['line1']).any()): #if cont name in net name
            Neptune_Net_Line_Indices.loc[i,'line1']=Net_Line_Names.index[Net_Line_Names==Neptune_Contingencies_Filtered.iloc[i]['line1']]
        else: #otherwise
            temp=str(Neptune_Contingencies_Filtered.loc[i,'cont1 - bus2'])+'-'+str(Neptune_Contingencies_Filtered.loc[i,'cont1 - bus1']) #flip to/from buses
            if(Net_Line_Names.str.contains(temp).any()): #and if this works add it
                Neptune_Net_Line_Indices.loc[i,'line1']=Net_Line_Names.index[Net_Line_Names==temp]
            else:#else find line manually neglecting connection nodes
                temp=re.sub('(?<=\w{5})\w','',Neptune_Contingencies_Filtered.iloc[i]['line1'])
                if(Net_Line_Names_Removed_Nodes.str.contains(temp).any()): #and add if this is found
                    Neptune_Net_Line_Indices.loc[i,'line1']=Net_Line_Names_Removed_Nodes.index[Net_Line_Names_Removed_Nodes==temp]
    #Line 2 - same as for Line 1           
        if(Net_Line_Names.str.contains(Neptune_Contingencies_Filtered.iloc[i]['line2']).any()):
            Neptune_Net_Line_Indices.loc[i,'line2']=Net_Line_Names.index[Net_Line_Names==Neptune_Contingencies_Filtered.iloc[i]['line2']]             
        else:
            temp=str(Neptune_Contingencies_Filtered.loc[i,'cont2 - bus2'])+'-'+str(Neptune_Contingencies_Filtered.loc[i,'cont2 - bus1'])
            if(Net_Line_Names.str.contains(temp).any()):
                Neptune_Net_Line_Indices.loc[i,'line2']=Net_Line_Names.index[Net_Line_Names==temp]
            else:
                temp=re.sub('(?<=\w{5})\w','',Neptune_Contingencies_Filtered.iloc[i]['line2'])          
                if(Net_Line_Names_Removed_Nodes.str.contains(temp).any()):
                    Neptune_Net_Line_Indices.loc[i,'line2']=Net_Line_Names_Removed_Nodes.index[Net_Line_Names_Removed_Nodes==temp]#
            
    
    #DOUBLE ENTRIES ARE FOUND - NEED TO DO MORE PROCESSING        
            
    Neptune_Net_Line_Indices=(Neptune_Net_Line_Indices[~Neptune_Net_Line_Indices.isnull().any(axis=1)]).reset_index(drop=True)
    Neptune_Net_Line_Indices_For_Removal=pd.DataFrame()
    
    '''
    GETTING ONLY 2 LINES IN A CONTINGENCY
    > if a continency could be e.g. line1 = [141,142] and line2=[143,144]
    > produce all possible combinations e.g. 141-143, 141-144,142-143,142-144
    > remove duplicates e.g. if line 141 in both lists, a contingency 141-141 would be created which isn't valid'
    > then remove mirrored contingencies which do the same thing i.e. 141-142 is the same as 142-141
    '''
    for i in range(Neptune_Net_Line_Indices.shape[0]):
        if(type(Neptune_Net_Line_Indices.iloc[i]['line1'])==np.ndarray): #if multiple possible lines in line1
            for j in range(len(Neptune_Net_Line_Indices.iloc[i]['line1'])): # go through each instance
                if(type(Neptune_Net_Line_Indices.iloc[i]['line2'])==np.ndarray): #if multiple lines in line2
                    for k in range(len(Neptune_Net_Line_Indices.iloc[i]['line2'])): #go through each instance
                        temp=pd.DataFrame([Neptune_Net_Line_Indices.iloc[i]['line1'][j],Neptune_Net_Line_Indices.iloc[i]['line2'][k]]).T
                        Neptune_Net_Line_Indices_For_Removal=pd.concat([Neptune_Net_Line_Indices_For_Removal,temp],ignore_index=True)
                else:
                    temp=pd.DataFrame(Neptune_Net_Line_Indices.iloc[i]['line1'][j],Neptune_Net_Line_Indices.iloc[i]['line2']).T
                    Neptune_Net_Line_Indices_For_Removal=pd.concat([Neptune_Net_Line_Indices_For_Removal,temp],ignore_index=True)
        else: #no multi-lines in line1
           if(type(Neptune_Net_Line_Indices.iloc[i]['line2'])==np.ndarray):
               for k in range(len(Neptune_Net_Line_Indices.iloc[i]['line2'])):
                   temp=pd.DataFrame([Neptune_Net_Line_Indices.iloc[i]['line1'],Neptune_Net_Line_Indices.iloc[i]['line2'][k]]).T
                   Neptune_Net_Line_Indices_For_Removal=pd.concat([Neptune_Net_Line_Indices_For_Removal,temp],ignore_index=True)
           else:
               temp=pd.DataFrame([Neptune_Net_Line_Indices.iloc[i]['line1'],Neptune_Net_Line_Indices.iloc[i]['line2']]).T
               Neptune_Net_Line_Indices_For_Removal=pd.concat([Neptune_Net_Line_Indices_For_Removal,temp],ignore_index=True)

    Neptune_Net_Line_Indices_For_Removal.columns=['line1','line2']
    Neptune_Net_Line_Indices_For_Removal = Neptune_Net_Line_Indices_For_Removal[Neptune_Net_Line_Indices_For_Removal['line1'] != Neptune_Net_Line_Indices_For_Removal['line2']] #ensure same line isn't being taken out twice - happens due to logic used
    Neptune_Net_Line_Indices_For_Removal=Neptune_Net_Line_Indices_For_Removal.apply(lambda r: sorted(r), axis = 1).drop_duplicates() #remove mirrored contingencies i.e. removing lines 141,142 is the same as removing 142,141
    
    return Neptune_Net_Line_Indices_For_Removal
    
def run_imbalance(net):
    pp.rundcpp(net, numba=False)
    line_results_pre_int = net['res_line'].copy()
    tx_results_pre_int = net['res_trafo'].copy()
    tx_results_pre_int["ind"] = tx_results_pre_int.index
    line_results_pre_int["ind"] = line_results_pre_int.index
    tx_results_pre_int["name"] = net.trafo.loc[tx_results_pre_int["ind"],"name"]
    line_results_pre_int["name"] = net.line.loc[line_results_pre_int["ind"], "name"]
    tx_results_pre_int.rename(columns={'p_hv_mw': 'p_to_mw', 'q_hv_mvar': 'q_to_mvar'}, inplace=True)
    line_tx_results_pre_int = pd.concat([line_results_pre_int, tx_results_pre_int])
    line_tx_results_pre_int.reset_index(drop=True,inplace=True)
    line_tx_results_pre_int_sorted = (line_tx_results_pre_int.sort_values(by="loading_percent", ascending=False)).drop_duplicates(
        subset="name", keep="first")
    line_tx_results_pre_int_sorted = line_tx_results_pre_int_sorted[["name", "p_to_mw", "q_to_mvar",  "loading_percent"]]
    line_tx_results_pre_int_sorted[["p_to_mw", "q_to_mvar", "loading_percent"]] = line_tx_results_pre_int_sorted[["p_to_mw", "q_to_mvar", "loading_percent"]].round(1)
    line_tx_results_pre_int_sorted.reset_index(drop=True,inplace=True)
    return net, line_tx_results_pre_int_sorted

def delete_load_gen(net):
    net.sgen = net.sgen[0:0]
    net.load = net.load[0:0]
    return net


#outage line index = outages planned for network
#def run_sim(net, l, outage_line_indx,line_results_sorted,tx_results_sorted,line_loading_max,critical_cont_singular,critical_cont_neptune,is_neptune):
def run_sim(net, l, outage_line_indx,line_results_sorted,tx_results_sorted,line_loading_max,critical_cont_neptune):
    net.line.loc[l, 'in_service'] = False
    net.line.loc[outage_line_indx, 'in_service'] = False
    pp.rundcpp(net, numba=False) #could change numba to #true
    line_results = net.res_line
    line_results["ind"] = line_results.index
    line_results["name"] = net.line.loc[line_results["ind"],"name"]
    line_results = line_results.sort_values(by="loading_percent",ascending=False)
    line_results = line_results.drop_duplicates(subset="name", keep="first") 
    line_results["loading_percent"] = line_results["loading_percent"].round(1)
    line_results["result"] = line_results["name"] + ": " + line_results["loading_percent"].astype(str) + "%"
    line_results_sorted = pd.concat([line_results_sorted,line_results], ignore_index=True)
    tx_results = net.res_trafo
    tx_results["ind"] = tx_results.index
    tx_results["name"] = net.trafo.loc[tx_results["ind"],"name"]
    tx_results = tx_results.sort_values(by="loading_percent",ascending=False)
    tx_results = tx_results.drop_duplicates(subset="name", keep="first")
    tx_results["loading_percent"] = tx_results["loading_percent"].round(1)
    tx_results["result"] = tx_results["name"] + ": " + tx_results["loading_percent"].astype(str) + "%"
    tx_results_sorted = pd.concat([tx_results_sorted, tx_results], ignore_index=True)
    
    if (net.res_line.loading_percent.max() > line_loading_max):
        #if(is_neptune==True):
        critical_cont_neptune.append(str(str(net.line.loc[l[0],'name'])+' & '+str(net.line.loc[l[1],'name'])))
        #elif(is_neptune==False):
            #critical_cont_singular.append(str(net.line.loc[l,'name']))
        #else:
            #print('Something in the background going wrong')
            
    net.line.loc[l, 'in_service'] = True

    #return line_results_sorted,tx_results_sorted,critical_cont_singular,critical_cont_neptune
    return line_results_sorted,tx_results_sorted,critical_cont_neptune


def run_and_critical(outage_line_name, net, Neptune_Net_Line_Indices_For_Removal):
    outage_line_indx = []
    outage_trafo_indx = []
    
    for string in outage_line_name:
        if string in net.line["name"].tolist():
            outage_line_indx.append(net.line[net.line["name"] == string].index[0])
        if string in net.trafo["name"].tolist():
            outage_trafo_indx.append(net.trafo[net.trafo["name"] == string].index[0])

            
    line_loading_max = 100
    #critical_cont_singular= []
    critical_cont_neptune=[]
    #critical_lines_indx = []
    line_results_sorted = pd.DataFrame() # container in order to store line results
    tx_results_sorted = pd.DataFrame() # container to store tranny results

    net.line.loc[outage_line_indx, 'in_service'] = False
    pp.rundcpp(net, numba=False) #test numba = true - initially false!
    line_results_pre = net['res_line'].copy()
    tx_results_pre = net['res_trafo'].copy()
    tx_results_pre["ind"] = tx_results_pre.index
    line_results_pre["ind"] = line_results_pre.index
    tx_results_pre["name"] = net.trafo.loc[tx_results_pre["ind"], "name"]
    line_results_pre["name"] = net.line.loc[line_results_pre["ind"], "name"]
    tx_results_pre.rename(columns={'p_hv_mw': 'p_to_mw', 'q_hv_mvar': 'q_to_mvar'}, inplace=True)
    line_tx_results_pre = pd.concat([line_results_pre, tx_results_pre])
    line_tx_results_pre.reset_index(drop=True, inplace=True)
    line_tx_results_pre_sorted = (
        line_tx_results_pre.sort_values(by="loading_percent", ascending=False)).drop_duplicates(
        subset="name", keep="first")
    line_tx_results_pre_sorted = line_tx_results_pre_sorted[["name", "p_to_mw", "q_to_mvar", "loading_percent"]]
    line_tx_results_pre_sorted[["p_to_mw", "q_to_mvar", "loading_percent"]] = line_tx_results_pre_sorted[
        ["p_to_mw", "q_to_mvar", "loading_percent"]].round(1)
    line_tx_results_pre_sorted.reset_index(drop=True, inplace=True)

    #lines = net.line.index
    
    #REMOVED CRITICAL_LINES_INDX AS NOT USED !!
    #for l in lines:
        #line_results_sorted,tx_results_sorted,critical_cont_singular,critical_cont_neptune=run_sim(net, l, outage_line_indx,line_results_sorted,tx_results_sorted,line_loading_max,critical_cont_singular,critical_cont_neptune,is_neptune=False)
    for m in Neptune_Net_Line_Indices_For_Removal:
        #line_results_sorted,tx_results_sorted,critical_cont_singular,critical_cont_neptune=run_sim(net, m, outage_line_indx,line_results_sorted,tx_results_sorted,line_loading_max,critical_cont_singular,critical_cont_neptune,is_neptune=True)
        line_results_sorted,tx_results_sorted,critical_cont_neptune=run_sim(net, m, outage_line_indx,line_results_sorted,tx_results_sorted,line_loading_max,critical_cont_neptune)

    line_results_sorted_a = pd.DataFrame()
    tx_results_sorted_a = pd.DataFrame()

    if len(line_results_sorted) > 1: #picking the max values of lines with worst values!!
        line_results_sorted_a = (line_results_sorted.sort_values(by="loading_percent",ascending=False)).drop_duplicates(subset="name", keep="first")
    if len(tx_results_sorted_a) > 1:
        tx_results_sorted_a = (tx_results_sorted.sort_values(by="loading_percent", ascending=False)).drop_duplicates(subset="name", keep="first")

    overall_result = pd.concat([line_results_sorted_a, tx_results_sorted_a])
    if len(overall_result) > 1:
        overall_result_sorted = (overall_result.sort_values(by="loading_percent",ascending=False)).drop_duplicates(subset="name", keep="first")
        overall_result_sorted = overall_result_sorted[["name", "p_to_mw", "q_to_mvar", "loading_percent"]]
        overall_result_sorted["p_to_mw"] = overall_result_sorted["p_to_mw"].round(1)
        overall_result_sorted["q_to_mvar"] = overall_result_sorted["q_to_mvar"].round(1)
    else:
        overall_result_sorted = pd.DataFrame()

    #critical_cont_singular.sort()
    critical_cont_neptune.sort()
    
    net.sgen.drop(net.sgen.index[0:], inplace=True)
    net.load.drop(net.load.index[0:], inplace=True) 
    net.ext_grid.drop(net.ext_grid.index[0:], inplace=True)

    overall_result_sorted.reset_index(drop=True,inplace=True)

    #return overall_result_sorted, outage_line_name, critical_cont_singular,critical_cont_neptune, line_tx_results_pre_sorted
    return overall_result_sorted, outage_line_name,critical_cont_neptune, line_tx_results_pre_sorted

    lists_to_delete = [line_results_sorted, tx_results_sorted, line_results_sorted_a, tx_results_sorted_a, overall_result, overall_result_sorted]

    for each in lists_to_delete:
        del globals()[each]
