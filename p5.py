import requests
import json
import websocket

# URL per le richieste REST 
url_rest = "http://10.50.1.130:8080/adaptor/api/v1/CISEMessageServiceREST/sendPullRequest"

# URL per il websocket
url_websocket = "ws://10.50.1.130:8080/adaptor/adp"

# funzione per CREARE il payload della pull request
def create_request_pull(dataReq):
    json_data = {
        "pullType": "Request",
        "discoveryProfile": {
            "ServiceRole": "Provider",
            "ServiceStatus": "Online",
            "ServiceType": dataReq["serviceType"]
        }
    }
    
    entity = {}
    if dataReq.get("name") is not None:
        entity["name"] = dataReq["name"]
    if dataReq.get("mmsi") is not None:
        entity["mmsi"] = dataReq["mmsi"]
    if dataReq.get("imoNumber") is not None:
        entity["imoNumber"] = dataReq["imoNumber"]

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
  
    return json_data

# funzione per INVIARE la pull request come POST
def send_pull_request(dataReq):
    headers = {'Content-Type': 'application/json'}
    payload = create_request_pull(dataReq)
    
    try:
        response = requests.post(url_rest, headers=headers, json=payload)
        print(f"Status code: {response.status_code}")
        
        if response.status_code == 200:
            print("Risposta ricevuta con successo:")
            print(json.dumps(response.json(), indent=4))
        else:
            print(f"Errore nella richiesta HTTP: {response.status_code}")
            print("Contenuto della risposta:", response.text)
    except Exception as e:
        print(f"Errore durante la richiesta HTTP: {e}")


# funzione per CREARE il payload della richiesta di discovery
def create_request_discovery(dataReq):
    json_data = {
        "pullType": "Discover",
        "discoveryProfile": {
            "ServiceStatus": "Online",
            "ServiceRole": "Provider",
            "ServiceOperation": dataReq["serviceOperation"]
        }
    }
    
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

# funzione per INVIARE la POST di discovery
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

# Dati di esempio per le richieste
dataReq_pull = {    
    "serviceType": "VesselService",  # Cambiato da "vessels" a "VesselService"
    "serviceOperation": "Pull",
    # "name": "Example Vessel",
    # "mmsi": "123456789",
    # "imoNumber": "987654321",
    "informationSecurityLevel": "EUConfidential",
    "informationSensitivity": "Red",
    # "personalData": False,
    "purpose": "VTM",
    # "senderServiceType": "example_sender_service_type"
}

dataReq_discovery = {    
    "serviceOperation": "Pull",
    #"serviceType": "VesselService",
    "ServiceRole": "Provider",
    "ServiceStatus": "Online"          
}

# funzione per gestire l'apertura della connessione websocket
def on_open(ws):
    print("Connessione al websocket stabilita.")
    
    # Esegui i test cases
    print("Invio DISCOVERY...")
    send_discovery_request(dataReq_discovery)
    print("\n")
    print("Invio PULL REQUEST...")
    send_pull_request(dataReq_pull)

# Funzione per gestire la ricezione dei messaggi websocket
def on_message(ws, message):
    print("Messaggio ricevuto:", message)

# Funzione per gestire l'errore della connessione websocket
def on_error(ws, error):
    print("Errore websocket:", error)

# Funzione per gestire la chiusura della connessione websocket
def on_close():
    print("Connessione websocket chiusa.")

# Connessione al websocket
ws = websocket.WebSocketApp(url_websocket,
                            on_open=on_open,
                            on_message=on_message,
                            on_error=on_error,
                            on_close=on_close)

# Mi collego al websocket con un thread separato
ws.run_forever()
