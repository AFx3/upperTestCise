import requests
import json
import websocket
from datetime import datetime

############################################### CONFIG PARAMS ########################################################

url_rest = "http://10.50.1.130:8080/adaptor/api/v1/CISEMessageServiceREST/sendPullRequest" # URL per le richieste REST 
url_websocket = "ws://10.50.1.130:8080/adaptor/adp" # URL per il websocket

############################################### USER CHOICE ########################################################

# funzione per ottenere la scelta dell'utente
def get_user_choice():
    print("Seleziona l'azione da eseguire:")
    print("0. ESCI")
    print("1. Invia la Pull Request")
    print("2. Esegui la Discovery")
    print("3. Esegui la Subscribe")
    print("4. Esegui la Unsubscribe")
    choice = input("Inserisci il numero corrispondente all'azione: ")
    
    return choice

############################################## PULL req ########################################################

# funzione per CREARE il payload della PULL REQUEST
def create_request_pull(dataReq):
    json_data = {
        "pullType": "Request",
        "discoveryProfile": {
            "ServiceRole": "Provider",
            "ServiceStatus": "Online",
            "ServiceType": dataReq["serviceType"]
        }
    }
    # dizionario vuoto per l'entità, lo vado a popolare prendendo i dati da dataReq se presenti con valore non nullo, aggiungendo la oppia chiave:valore 
    entity = {}
    if dataReq.get("name") is not None:
        entity["name"] = dataReq["name"]
    if dataReq.get("mmsi") is not None:
        entity["mmsi"] = dataReq["mmsi"]
    if dataReq.get("imoNumber") is not None:
        entity["imoNumber"] = dataReq["imoNumber"]

    # verifico se il dizionario entity contiene almeno una coppia chiave-valore. 
    # se sì, aggiunge il dizionario entity come valore della chiave entity nel dizionario json_data["discoveryProfile"]
    if entity:
        json_data["discoveryProfile"]["entity"] = entity
    
    if dataReq.get("informationSecurityLevel") is not None:
        json_data["informationSecurityLevel"] = dataReq["informationSecurityLevel"]
        
    if dataReq.get("informationSensitivity") is not None:
        json_data["informationSensitivity"] = dataReq["informationSensitivity"]
        
    if dataReq.get("personalData") is not None:
        json_data["personalData"] = dataReq["personalData"]
        
    if dataReq.get("purpose") is not None:
        json_data["purpose"] = dataReq["purpose"]
        
    if dataReq.get("senderServiceType") is not None:
        json_data["senderServiceType"] = dataReq["senderServiceType"]
        
    # quindi popola il dizionario entity con i dati se presenti in dataReq (che è sempre un dizionario) e aggiunge questo dizionario a json_data solo se contiene dati    
  
    return json_data

# funzione per INVIARE la PULL REQUEST come POST
def send_pull_request(dataReq):
    # headers per la richiesta HTTP post specificando che si trasmette un payload JSON
    headers = {'Content-Type': 'application/json'}
    
    # creo payload della richiesta usando create_request_pull passandogli il dizionario (vedi sezione #### dizionari richieste #####) che sarà dataReq_pull
    payload = create_request_pull(dataReq)
    
    try:
        # invia una richiesta POST all'URL specificato con gli header e il payload
        response = requests.post(url_rest, headers=headers, json=payload)
        # stampa il codice di stato della risposta 
        print(f"Status code: {response.status_code}")
        
        if response.status_code == 200: # se la risposta ha codice di stato 200 (OK)
            print("Risposta ricevuta con successo:")
            print(json.dumps(response.json(), indent=4)) # stampa la risposta JSON ricevuta formattata con indentazione
        else:
            # se la risposta ha un codice di errore, stampa il codice di stato e il contenuto della risposta
            print(f"Errore nella richiesta HTTP: {response.status_code}")
            print("Contenuto della risposta:", response.text)
    except Exception as e:
        # gestisce eventuali eccezioni che possono verificarsi durante l'invio della richiesta
        print(f"Errore durante la richiesta HTTP: {e}")


# da qui in poi non commento perchè le funzioni sono analoghe a quelle sopra, cambia solo il tipo di richiesta e il payload
        
############################################## DISCOVERY ########################################################

# funzione per CREARE il payload 
def create_request_discovery(dataReq):
    json_data = {
        "pullType": "Discover",
        "discoveryProfile": {
            "ServiceStatus": "Online",
            "ServiceRole": "Provider",
            "ServiceOperation": "Pull"  
        }
    }
    
    if dataReq.get("serviceOperation") is not None:
        json_data["discoveryProfile"]["ServiceOperation"] = dataReq["serviceOperation"]
    
    if dataReq.get("serviceOperation") is not None:
        json_data["discoveryProfile"]["ServiceOperation"] = dataReq["serviceOperation"]    
        
    if dataReq.get("serviceType") is not None:
        json_data["discoveryProfile"]["ServiceType"] = dataReq["serviceType"]
        
    if dataReq.get("serviceID") is not None:
        json_data["discoveryProfile"]["ServiceID"] = dataReq["serviceID"]
        
    if dataReq.get("seaBasin") is not None:
        json_data["discoveryProfile"]["SeaBasin"] = dataReq["seaBasin"]
        
    if dataReq.get("country") is not None:
        json_data["discoveryProfile"]["Country"] = dataReq["country"]
        
    if dataReq.get("community") is not None:
        json_data["discoveryProfile"]["Community"] = dataReq["community"]
    
    return json.dumps(json_data)

# funzione per inviare la POST 
def send_discovery_request(dataReq):
    headers = {'Content-Type': 'application/json'}
    payload = create_request_discovery(dataReq)
    
    try:
        response = requests.post(url_rest, headers=headers, data=payload)
        print(f"Status code: {response.status_code}")
        
        if response.status_code == 200:
            print("Risposta ricevuta con successo:")
            print(json.dumps(response.json(), indent=4))
        else:
            print(f"Errore nella richiesta HTTP: {response.status_code}")
            print("Contenuto della risposta:", response.text)
    except Exception as e:
        print(f"Errore durante la richiesta HTTP: {e}")

############################################## SUBSCRIBE ########################################################

# funzione per CREARE il payload della SUBSCRIBE POST REQUEST
def create_request_subscribe(dataReq):
    json_data = {
        "pullType": "Subscribe",
        "recipient": {
            "serviceRoleType": "Provider"
        },
        "subscriptionCapability": {
            "MaxFrequency": "",  
            "RefreshRate": "",
            "SubscriptionEnd": "" 
        },
        "senderServiceType": ""
    }

    if dataReq.get("serviceOperation") is not None:
        json_data["recipient"]["serviceOperation"] = dataReq["serviceOperation"]
    
    if dataReq.get("serviceType") is not None:
        json_data["recipient"]["serviceType"] = dataReq["serviceType"]
        json_data["senderServiceType"] = dataReq["serviceType"]
        
    if dataReq.get("serviceID") is not None:
        json_data["recipient"]["serviceId"] = dataReq["serviceID"]
        
    if dataReq.get("maxFrequency") is not None:
        # converti il valore della frequenza massima in iso8601 (errore adaptor che non riesce a fare il parsing del valore intero)
        duration_seconds = int(dataReq["maxFrequency"])
        duration_isoformat = "PT{}S".format(duration_seconds)  # durata in formato ISO8601
        json_data["subscriptionCapability"]["MaxFrequency"] = duration_isoformat
        
    if dataReq.get("refreshRate") is not None:
        # converti il valore del refresh rate in un formato iso8601
        refresh_seconds = int(dataReq["refreshRate"])
        refresh_isoformat = "PT{}S".format(refresh_seconds)  # durata in formato ISO8601
        json_data["subscriptionCapability"]["RefreshRate"] = refresh_isoformat
        
    if dataReq.get("subscriptionEnd") is not None:
        json_data["subscriptionCapability"]["SubscriptionEnd"] = datetime.now().isoformat()
    
        
    if dataReq.get("dataFreshness") is not None:
        # converti il valore refresh rate in formato iso8601
        fresh_seconds = int(dataReq["dataFreshness"])
        fresh_isoformat = "PT{}S".format(fresh_seconds)  # durata in formato ISO8601
        json_data["subscriptionCapability"]["RefreshRate"] = fresh_isoformat    
        
    if dataReq.get("seaBasin") is not None:
        json_data["subscriptionCapability"]["SeaBasin"] = dataReq["seaBasin"]

    return json.dumps(json_data)


# funzione per INVIARE la SUBSCRIBE POST REQUEST
def send_subscribe_request(dataReq):
    headers = {'Content-Type': 'application/json'}
    payload = create_request_subscribe(dataReq)
    
    try:
        response = requests.post(url_rest, headers=headers, data=payload)
        print(f"Status code: {response.status_code}")
        
        if response.status_code == 200:
            print("Risposta ricevuta con successo:")
            print(json.dumps(response.json(), indent=4))
        else:
            print(f"Errore nella richiesta HTTP: {response.status_code}")
            print("Contenuto della risposta:", response.text)
    except Exception as e:
        print(f"Errore durante la richiesta HTTP: {e}")

############################################## UNSUBSCRIBE ########################################################

# funzione per CREARE il payload della richiesta di annullamento sottoscrizione
def create_request_unsubscribe(dataReq):
    json_data = {
        "pullType": "Unsubscribe",
        "recipient": {
            "serviceOperation": "Subscribe"
        },
        "senderServiceType": ""
    }

    if dataReq.get("serviceType") is not None:
        json_data["recipient"]["serviceType"] = dataReq["serviceType"]
        json_data["senderServiceType"] = dataReq["serviceType"]
        
    if dataReq.get("serviceID") is not None:
        json_data["recipient"]["serviceId"] = dataReq["serviceID"]

    return json.dumps(json_data)


# funzione per INVIARE la POST di unsubcribe
def send_unsubscribe_request(dataReq):
    headers = {'Content-Type': 'application/json'}
    payload = create_request_unsubscribe(dataReq)
    
    try:
        response = requests.post(url_rest, headers=headers, data=payload)
        print(f"Status code: {response.status_code}")
        
        if response.status_code == 200:
            print("Risposta ricevuta con successo:")
            print(json.dumps(response.json(), indent=4))
        else:
            print(f"Errore nella richiesta HTTP: {response.status_code}")
            print("Contenuto della risposta:", response.text)
    except Exception as e:
        print(f"Errore durante la richiesta HTTP: {e}")
        
############################################## DIZIONARI RICHIESTE ########################################################

dataReq_pull = {    
    "serviceType": "VesselService",  
    "serviceOperation": "Pull",
    "informationSecurityLevel": "EUConfidential",
    "informationSensitivity": "Red",
    "purpose": "VTM"
}

dataReq_discovery = {    
    #"serviceOperation": "Pull",
    #"serviceType": "VesselService",
    #"country": "IT",
    #"ServiceRole": "Provider",
    #"ServiceStatus": "Online"
    "seaBasin": "Mediterranean"
         
}

dataReq_subscribe = {
    "serviceType": "VesselService",
    "serviceOperation": "Subscribe",
    "maxFrequency": "60",
    "refreshRate": "30",
    "subscriptionEnd": datetime.now().isoformat(),
    "dataFreshness": "60",
    #"seaBasin": "MediterraneanSea",
    "serviceID": "0000"
}

dataReq_unsubscribe = {
    "serviceType": "VesselService",
    #"serviceOperation": "Subscribe"
    "serviceID": "0000"
}



#################################################### WEBSOCKET ########################################################

# funzione per gestire l'apertura della connessione websocket, una volta stabilita la connessione, utente sceglie la richiesta da inviare:
def on_open(ws):
    print("Connessione al websocket stabilita.")
    
    # get scelta dell'utente, uso il while loop per continuare a chiedere la scelta dell'utente, con 0 chiudo il programma
    while True:
        
        choice = get_user_choice() # var per confrontare la scelta dell'utente da input
    
        # esegui l'azione corrispondente all'input
        match choice:
            case "1":
                print("Invio PULL REQUEST...")
                send_pull_request(dataReq_pull)
            case "2":
                print("Invio DISCOVERY...")
                send_discovery_request(dataReq_discovery)
            case "3":
                print("Invio SUBSCRIBE REQUEST...")
                send_subscribe_request(dataReq_subscribe)
            case "4":
                print("Invio UNSUBSCRIBE REQUEST...")
                send_unsubscribe_request(dataReq_unsubscribe)
            case "0": 
                print("Chiudo il programma...")
                # chiudi la connessione websocket
                ws.close()
                # chiudi il programma
                exit()
            case _:
                print("Scelta non valida.")
                # rimane nel loop
            
    
# funzione che mostra i messaggi ricevuti dal socket
def on_message(ws, message):
    print("Messaggio ricevuto:", message)

# funzione per gestire un eventuale errore nella connessione
def on_error(ws, error):
    print("Errore websocket:", error)

# funzione per la chiusura della connessione websocket
def on_close(ws, close_status_code, close_msg): # togliere commento nel main se la connessione non va a buon fine per diagnostica
    print("Connessione websocket chiusa.")
    
################################################ MAIN ########################################################

# funzione MAIN
def main():
    # Connessione al websocket
    ws = websocket.WebSocketApp(url_websocket,
                                on_open=on_open,
                                on_message=on_message,
                                #on_error=on_error,         togliere commento per diagnostica se connessione non riuscita
                                on_close=on_close)

    # mi collego al websocket con un thread separato
    ws.run_forever()

# eseguo il programma
if __name__ == "__main__":
    main()
