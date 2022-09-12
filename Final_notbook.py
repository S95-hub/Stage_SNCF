import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import pytz
from datetime import datetime, timedelta,timezone,time

st.title("Application web")
element = st.empty()


   
def main_page():
   
    #st.sidebar.markdown("# API")
    st.markdown("<h2 style='text-align: center; color: black;'>API TEMPS REEL</h2>", unsafe_allow_html=True)
    
    #st.markdown("<h1 style='text-align: center; color: white;'>My Streamlit App</h1>", unsafe_allow_html=True)
    # token
    import requests
    import json
    url = "https://as.api.iledefrance-mobilites.fr/api/oauth/token"
    client_id= "66b127d3-d0ac-4e04-b81e-d701709811c2" 
    client_secret= "e1a6a3c1-c290-4392-bf08-89779a679e5b"
    data = dict(
        grant_type='client_credentials',scope='read-data',client_id= client_id ,client_secret=client_secret)
    response = requests.post(url, data=data)
    jsonData = response.json()
    token = jsonData['access_token']
    # --- recuperer les donnees sous format json
    url = "https://traffic.api.iledefrance-mobilites.fr/v1/tr-global/estimated-timetable"
    params =dict(LineRef='ALL')
    headers = {'Accept-Encoding' : 'gzip','Authorization' : 'Bearer ' + token}
    response = requests.get(url, headers=headers)
    print(response)
    if response.status_code != 200:
        print('Status:', response.status_code, 'Erreur sur la requête; fin de programme')
    # exit()
    jsonData = response.json()
    
   # --- ceeration de dataframe api temps reel
    js = jsonData["Siri"]["ServiceDelivery"]["EstimatedTimetableDelivery"][0]["EstimatedJourneyVersionFrame"][0]["EstimatedVehicleJourney"]
    df = pd.DataFrame(js)
    df["LineRef"] = df["LineRef"].apply(lambda x: x["value"])
    df["LineReF"] = df["LineRef"].apply(lambda x : x.split("::")[1].replace(":",""))
    df["VehicleMode"] = df['VehicleMode'].apply(lambda x : str(x)[1:-1])
    df = df[(df["VehicleMode"] == "'BUS'") | (df["VehicleMode"] == "a") ]
    # --- Fonction qui reccupere l'exepeteddeparture et stoppoint 
    def find_ref(l): 
        return [(j["StopPointRef"]["value"],j["ExpectedDepartureTime"] if "ExpectedDepartureTime" in j.keys() else np.nan)for j in l]
    
    # manipulation
    df["new_ref_exp"] = df["EstimatedCalls"].apply(lambda x : find_ref(x["EstimatedCall"]))
    df = df.explode("new_ref_exp")
    df['StopPointRef'],df['ExpectedDepartureTime'] = df["new_ref_exp"].str
    
    # --- calculer le temps d'attente
    df['ExpectedDepartureTime'] = pd.to_datetime(df['ExpectedDepartureTime'])
    df['ExpectedDepartureTime'] = df['ExpectedDepartureTime'].dt.tz_convert('Europe/Paris')
    now = datetime.now()
    df["current_time"] = now
    df["current_time"] = pd.DatetimeIndex(df["current_time"]).tz_localize('Europe/Paris')
    df["temps_attente"] = df["ExpectedDepartureTime"]-df["current_time"]
    df["temps_attente"] = df["temps_attente"].apply(lambda x : str(x)[7:12])
    
    # --- filttrer le dataframe
    #df1 = df[df["ExpectedDepartureTime"].isnull() != True]
    #df1["DestinationName"] = df1["DestinationName"].apply(lambda x : str(x[0]["value"]))
    #df1 = df1.loc[:,["LineReF","StopPointRef","DestinationName","ExpectedDepartureTime","current_time","temps_attente"]]
    df1 = df.loc[:,["LineReF","StopPointRef","DestinationName","ExpectedDepartureTime","temps_attente"]]
    
    # les valeurs manquantes
    #df_null = df[df["ExpectedDepartureTime"].isnull() == True]
    #df_null= df_null.loc[:,["LineReF", "StopPointRef","DestinationName","ExpectedDepartureTime"]]
    st.sidebar.header("Lire les données de l'API temps réel")
    # checkbox wdget
    checkbox = st.sidebar.checkbox("Reveal data.")
    if checkbox:
        st.dataframe(df1)
   
   
    
    st.markdown("selectionner sur un bus") 
    st.sidebar.header("Selectionner un bus sur API temps réel")
    bus = df1["LineReF"].unique()
    bus_selection = st.sidebar.selectbox("Select your line:",   bus)
    #df1[df1["LineReF"] == zone_selection]
    st.dataframe(df1[df1["LineReF"] == bus_selection])
    #st.write(df1[df1["LineReF"] == zone_selection])
   
    
    st.empty()
    

        
        
        
        
        

        
        
# page 2
def page2():
    
    #st.sidebar.markdown("# TIM ❄️")
    st.markdown("<h1 style='text-align: center; color: black;'>TIM ❄️</h1>", unsafe_allow_html=True)
    
    import requests
    import json
    url = "https://as.api.iledefrance-mobilites.fr/api/oauth/token"
    client_id= "66b127d3-d0ac-4e04-b81e-d701709811c2" 
    client_secret= "e1a6a3c1-c290-4392-bf08-89779a679e5b"
    data = dict(
        grant_type='client_credentials',scope='read-data',client_id= client_id ,client_secret=client_secret)
    response = requests.post(url, data=data)
    jsonData = response.json()
    token = jsonData['access_token']
    # --- recuperer les donnees sous format json
    url = "https://traffic.api.iledefrance-mobilites.fr/v1/tr-global/estimated-timetable"
    params =dict(LineRef='ALL')
    headers = {'Accept-Encoding' : 'gzip','Authorization' : 'Bearer ' + token}
    response = requests.get(url, headers=headers)
    print(response)
    if response.status_code != 200:
        print('Status:', response.status_code, 'Erreur sur la requête; fin de programme')
    # exit()
    jsonData = response.json()
    
    
     # --- ceeration de dataframe api temps reel
    js = jsonData["Siri"]["ServiceDelivery"]["EstimatedTimetableDelivery"][0]["EstimatedJourneyVersionFrame"][0]["EstimatedVehicleJourney"]
    df = pd.DataFrame(js)
    df["LineRef"] = df["LineRef"].apply(lambda x: x["value"])
    df["LineReF"] = df["LineRef"].apply(lambda x : x.split("::")[1].replace(":",""))
    df["VehicleMode"] = df['VehicleMode'].apply(lambda x : str(x)[1:-1])
    df = df[(df["VehicleMode"] == "'BUS'") | (df["VehicleMode"] == "a") ]
    # --- Fonction qui reccupere l'exepeteddeparture et stoppoint 
    def find_ref(l): 
        return [(j["StopPointRef"]["value"],j["ExpectedDepartureTime"] if "ExpectedDepartureTime" in j.keys() else np.nan) for j in l]
    
    
    # manipulation
    df["new_ref_exp"] = df["EstimatedCalls"].apply(lambda x : find_ref(x["EstimatedCall"]))
    df = df.explode("new_ref_exp")
    df['StopPointRef'],df['ExpectedDepartureTime'] = df["new_ref_exp"].str
    
    # --- calculer le temps d'attente
    df['ExpectedDepartureTime'] = pd.to_datetime(df['ExpectedDepartureTime'])
    df['ExpectedDepartureTime'] = df['ExpectedDepartureTime'].dt.tz_convert('Europe/Paris')
    now = datetime.now()
    df["current_time"] = now
    df["current_time"] = pd.DatetimeIndex(df["current_time"]).tz_localize('Europe/Paris')
    df["temps_attente"] = df["ExpectedDepartureTime"]-df["current_time"]
    df["temps_attente"] = df["temps_attente"].apply(lambda x : str(x)[7:12])
    
    # --- filttrer le dataframe
    df1 = df[df["ExpectedDepartureTime"].isnull() != True]
    #df1["DestinationName"] = df1["DestinationName"].apply(lambda x : str(x[0]["value"]))
    df1 = df1.loc[:,["LineReF","StopPointRef","DestinationName","ExpectedDepartureTime","current_time","temps_attente"]]
    
    
    import xml.etree.ElementTree as et
    etree = et.parse("Prod-12Mai2022_Config.xml")
    eroot = etree.getroot()
    liste_bus = []
    for root_elm in  eroot.findall(".//Afficheur"):
         for ligne in root_elm.findall("Ligne"):
                liste_bus.append((root_elm.find("Titre").text,ligne.find('LineRef').text,ligne.find('Name').text,ligne.find('MonitoringRef').text))
                
                
    df_xml = pd.DataFrame(liste_bus, columns=["Titre",'LineReF',"Name", 'MonitoringRef'])
    df_xml["LineReF"] = df_xml["LineReF"].apply(lambda x : x.split("::")[1].replace(":",""))
    
    df_api_xml = pd.merge(df1,df_xml,on='LineReF', how='inner')
    df_api_xml["ZdAId"] = df_api_xml["MonitoringRef"].apply(lambda x : int(x.split(":")[-2].replace(":","")))
    relation = pd.read_csv("relations.csv", sep = ";")
    relation = relation.loc[:,["ZdCId","ZdAId","ArRId"]]
    df2 = relation.merge(df_api_xml, on='ZdAId', how='inner')
    df_finaly = df2.loc[:,["ZdCId","Titre","StopPointRef","LineReF","Name","DestinationName","temps_attente"]]
    df_test_1 = df_finaly.copy()
    df_test_1 = df_test_1[df_test_1["temps_attente"] != ' +23:']
    #df_test_1["DestinationName"] = df_test_1["DestinationName"].apply(lambda x : str(x[0]["value"]))
    df_test_1 = df_test_1[df_test_1["StopPointRef"].shift(-1) != df_test_1["StopPointRef"]]
    st.sidebar.header("Lire les données du TIM")
    
    # checkbox wdget
    checkbox = st.sidebar.checkbox("Reveal Data.")
    if checkbox:
        st.dataframe(df_test_1)
    
    
    st.markdown("selectionner une zone de correspondance") 
    st.sidebar.header("Selectionner une zone de correspondance sur TIM")
    zone = df_test_1["ZdCId"].unique()
    zone_selection = st.sidebar.selectbox("Select your area:",   zone)
    #df1[df1["LineReF"] == zone_selection]
    st.dataframe(df_test_1[df_test_1["ZdCId"] == zone_selection])
    #st.write(df_test_1[df_test_1["LineReF"] == zone_selection])
    
    st.markdown("selectionner un bus") 
    st.sidebar.header("Selectionner un bus sur TIM")
    bus = df_test_1["LineReF"].unique()
    bus_selection = st.sidebar.selectbox("Select your line:",   bus)
    #df1[df1["LineReF"] == zone_selection]
    st.dataframe(df_test_1[df_test_1["LineReF"] == bus_selection])
    #st.write(df_test_1[df_test_1["LineReF"] == zone_selection]
    
    st.markdown("selectionner une gare") 
    #st.markdown("<h1 style='text-align: center; color: white;'>API TEMPS REEL</h1>", unsafe_allow_html=True)
    st.sidebar.header("Selectionner une gare sur TIM")
    station = df_test_1["Titre"].unique()
    station_selection = st.sidebar.selectbox("Select your station:",   station)
    #df1[df1["LineReF"] == zone_selection]
    st.dataframe(df_test_1[df_test_1["Titre"] == station_selection])
    #st.write(df_test_1[df_test_1["LineReF"] == zone_selection])


    
# indicateurs statistique    
   
def page3():
   
    #st.sidebar.markdown("# API")
    st.markdown("<h2 style='text-align: center; color: black;'>Indicateurs Statistiques</h2>", unsafe_allow_html=True)
    
    #st.markdown("<h1 style='text-align: center; color: white;'>My Streamlit App</h1>", unsafe_allow_html=True)
    # token
    import requests
    import json
    url = "https://as.api.iledefrance-mobilites.fr/api/oauth/token"
    client_id= "66b127d3-d0ac-4e04-b81e-d701709811c2" 
    client_secret= "e1a6a3c1-c290-4392-bf08-89779a679e5b"
    data = dict(
        grant_type='client_credentials',scope='read-data',client_id= client_id ,client_secret=client_secret)
    response = requests.post(url, data=data)
    jsonData = response.json()
    token = jsonData['access_token']
    # --- recuperer les donnees sous format json
    url = "https://traffic.api.iledefrance-mobilites.fr/v1/tr-global/estimated-timetable"
    params =dict(LineRef='ALL')
    headers = {'Accept-Encoding' : 'gzip','Authorization' : 'Bearer ' + token}
    response = requests.get(url, headers=headers)
    print(response)
    if response.status_code != 200:
        print('Status:', response.status_code, 'Erreur sur la requête; fin de programme')
    # exit()
    jsonData = response.json()
    
   # --- ceeration de dataframe api temps reel
    js = jsonData["Siri"]["ServiceDelivery"]["EstimatedTimetableDelivery"][0]["EstimatedJourneyVersionFrame"][0]["EstimatedVehicleJourney"]
    df = pd.DataFrame(js)
    df["LineRef"] = df["LineRef"].apply(lambda x: x["value"])
    df["LineReF"] = df["LineRef"].apply(lambda x : x.split("::")[1].replace(":",""))
    df["VehicleMode"] = df['VehicleMode'].apply(lambda x : str(x)[1:-1])
    df = df[(df["VehicleMode"] == "'BUS'") | (df["VehicleMode"] == "a") ]
    # --- Fonction qui reccupere l'exepeteddeparture et stoppoint 
    def find_ref(l): 
        return [(j["StopPointRef"]["value"],j["ExpectedDepartureTime"] if "ExpectedDepartureTime" in j.keys() else "Nan")for j in l]
    
    # manipulation
    df["new_ref_exp"] = df["EstimatedCalls"].apply(lambda x : find_ref(x["EstimatedCall"]))
    df = df.explode("new_ref_exp")
    df['StopPointRef'],df['ExpectedDepartureTime'] = df["new_ref_exp"].str
    
    
    import xml.etree.ElementTree as et
    etree = et.parse("Prod-12Mai2022_Config.xml")
    eroot = etree.getroot()
    liste_bus = []
    for root_elm in  eroot.findall(".//Afficheur"):
         for ligne in root_elm.findall("Ligne"):
                liste_bus.append((root_elm.find("Titre").text,ligne.find('LineRef').text,ligne.find('Name').text,ligne.find('MonitoringRef').text))
                
                
    df_xml = pd.DataFrame(liste_bus, columns=["Titre",'LineReF',"Name", 'MonitoringRef'])
    df_xml["LineReF"] = df_xml["LineReF"].apply(lambda x : x.split("::")[1].replace(":",""))
    
    df1= pd.merge(df,df_xml,on='LineReF', how='inner')
    # --- calculer le temps d'attente
    #df['ExpectedDepartureTime'] = pd.to_datetime(df['ExpectedDepartureTime'])
    #df['ExpectedDepartureTime'] = df['ExpectedDepartureTime'].dt.tz_convert('Europe/Paris')
    #now = datetime.now()
    #df["current_time"] = now
    #df["current_time"] = pd.DatetimeIndex(df["current_time"]).tz_localize('Europe/Paris')
    #df["temps_attente"] = df["ExpectedDepartureTime"]-df["current_time"]
    #df["temps_attente"] = df["temps_attente"].apply(lambda x : str(x)[7:12])
    
    # --- filttrer le dataframe
    #df1 = df[df["ExpectedDepartureTime"] != "Nan"]
    #df1["DestinationName"] = df1["DestinationName"].map(lambda x : str(x[0]["value"]))
    df1 = df1.loc[:,["LineReF","StopPointRef","DestinationName","Titre","ExpectedDepartureTime"]]
    
    # les valeurs manquantes
    df_null = df[df["ExpectedDepartureTime"] == "Nan"]
    #df_null= df_null.loc[:,["LineReF", "StopPointRef","DestinationName","ExpectedDepartureTime"]]
    st.sidebar.header("Lire les données de l'API temps réel")
    # checkbox wdget
    checkbox = st.sidebar.checkbox("Reveal data.")
    if checkbox:
        st.dataframe(df1)
                 
    
    
    st.markdown("<h7 style='text-align: center; color: black;'>Nombres de bus par arrêt</h7>", unsafe_allow_html=True)
    st.sidebar.header("Sélectionner un arrêt pour voir le nombre de bus qui passe sur API temps réel")
    arret = df1["StopPointRef"].unique()
    arret_selection = st.sidebar.selectbox("Select your stop : ", arret)
    st.write(df1[df1["StopPointRef"] == arret_selection]["LineReF"].unique())
    

    st.markdown("<h7 style='text-align: center; color: black;'>les bus qui ont les plus grands valeurs manquantest</h7>",unsafe_allow_html=True)
    st.sidebar.header("Les bus qui n'ont pas d'ExpectedDepeparture")
    bus_null = df_null["LineReF"].unique()
    bus_selectin = st.sidebar.selectbox("Select your line:",   bus_null)
    #df_null[df_null["LineReF"] == bus_selectin]["LineReF"].value_counts()
    st.write(df_null[df_null["LineReF"]==bus_selectin]["LineReF"].value_counts().to_frame( 'nb_null').reset_index().sort_values(by='nb_null', ascending=False))
    
    # digramme en bare pour les 5 bus qui ont les plus grands expecteddeparturetime manquantes.
    st.markdown("<h7 style='text-align: center; color: black;'>Digramme en bare pour les 5 bus qui ont les plus grands expecteddeparturetime manquantes.</h7>",unsafe_allow_html=True)
    #st.write(df_null["LineReF"].value_counts()[:5])
    st.bar_chart(data=df_null["LineReF"].value_counts()[:5], use_container_width=True)
    
    st.markdown("selectionner sur un arret")
    df1 = df1.sort_values(by = 'StopPointRef')
    stop = df1["StopPointRef"].unique().tolist()
    stop_selection = st.sidebar.selectbox("Select your stop:",   stop)
    st.dataframe((df1[df1["StopPointRef"] == stop_selection].groupby(["Titre","StopPointRef","LineReF"])["ExpectedDepartureTime"].value_counts(normalize = True)*100).to_frame("percent").reset_index())
    
    
    st.markdown("<h7 style='text-align: center; color: black;'>Les différentes destinations d'un bus données.</h7>",unsafe_allow_html=True)
    depart_bus = df1["LineReF"].unique().tolist()
    depart_bus_selection = st.sidebar.selectbox("Select your line:",   depart_bus)
    df1[df1["LineReF"]== depart_bus_selection]
    
    #depart_bus["DestinationName"].value_counts().plot(kind="bar")
    #depart_bus["DestinationName"].value             
 





page_names_to_funcs = {
    "API": main_page,
    "TIM": page2,
     "IS" : page3}

selected_page = st.sidebar.selectbox("Select a page", page_names_to_funcs.keys())
page_names_to_funcs[selected_page]()









