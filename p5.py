import requests
import json
import websocket
from datetime import datetime

############################################### CONFIG PARAMS ########################################################

url_rest = "http://10.50.1.130:8080/adaptor/api/v1/CISEMessageServiceREST/sendPullRequest" # REST URL to send POST requests 
url_websocket = "ws://10.50.1.130:8080/adaptor/adp" # URL to connect to the adaptor via websocket

############################################### USER CHOICE ########################################################

# function to execute the user choice (sending requests or closing the program)
def get_user_choice():
    print("SELECT the correspondin action NUMBER:")
    print("0. EXIT")
    print("1. Send Pull Request")
    print("2. Discovery")
    print("3. Subscribe")
    print("4. Unsubscribe")
    choice = input("Insert the number here: ")
    
    return choice

############################################## PULL req ########################################################

# function to create the payload of the pull request
def create_request_pull(dataReq):
    json_data = {
        "pullType": "Request",
        "discoveryProfile": {
            "ServiceRole": "Provider",
            "ServiceStatus": "Online",
            "ServiceType": dataReq["serviceType"]
        }
    }
    # empty dictionary for the entity, I populate it by taking the data from dataReq if present with a non-null value, adding the key: value pair
    entity = {}
    if dataReq.get("name") is not None:
        entity["name"] = dataReq["name"]
    if dataReq.get("mmsi") is not None:
        entity["mmsi"] = dataReq["mmsi"]
    if dataReq.get("imoNumber") is not None:
        entity["imoNumber"] = dataReq["imoNumber"]

    # verifico se il dizionario entity contiene almeno una coppia chiave-valore. 
    # se sì, aggiunge il dizionario entity come valore della chiave entity nel dizionario json_data["discoveryProfile"]
    
    # verify if the entity dictionary contains at least one key-value pair
    # if so, add the entity dictionary as the value of the entity key in the json_data["discoveryProfile"] dictionary
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
        
    # then populate the entity dictionary with the data if present in dataReq (which is always a dictionary) and add this dictionary to json_data only if it contains data
    # finally, return the json_data dictionary as a JSON string
    return json_data


# function to SEND the PULL REQUEST as POST
def send_pull_request(dataReq):
 
    # headers for the HTTP post request specifying that a JSON payload is transmitted
    headers = {'Content-Type': 'application/json'}
    
    # create the request payload using create_request_pull by passing it the dictionary (see section #### request dictionaries ####) which will be dataReq_pull
    payload = create_request_pull(dataReq)
    
    try:
        # send a POST request to the specified URL with the headers and payload
        response = requests.post(url_rest, headers=headers, json=payload)
    
        #print the response status code
        print(f"Status code: {response.status_code}")
        
        # if the response has a status code of 200, print the JSON response received formatted with indentation
        if response.status_code == 200:
            
            print("Response correctly received:")
            print(json.dumps(response.json(), indent=4)) 
            
        else:
        
            # otherwise, print the status code and the response content
            print(f"Errore in the HTTP request: {response.status_code}")
            print("Response content:", response.text)
            
    except Exception as e:
    
        # handles any exceptions that may occur during the request
        print(f"Error during HTTP request: {e}")


# from here on I don't comment because the functions are analogous to those above, only the type of request and the payload change
        
############################################## DISCOVERY ########################################################

# function to create the payload of the discovery request
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

# function to SEND the DISCOVERY POST REQUEST
def send_discovery_request(dataReq):
    headers = {'Content-Type': 'application/json'}
    payload = create_request_discovery(dataReq)
    
    try:
        response = requests.post(url_rest, headers=headers, data=payload)
        print(f"Status code: {response.status_code}")
        
        if response.status_code == 200:
            print("Response correctly received:")
            print(json.dumps(response.json(), indent=4))
        else:
            print(f"Error in the HTTP request: {response.status_code}")
            print("Response content:", response.text)
    except Exception as e:
        print(f"Error HTTP request: {e}")

############################################## SUBSCRIBE ########################################################

# function to create the payload of the subscribe request
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
        
        # convert the value of the maximum frequency to iso8601 (adaptor error that cannot parse the integer value)
        duration_seconds = int(dataReq["maxFrequency"])
        duration_isoformat = "PT{}S".format(duration_seconds)  # durata in formato ISO8601
        json_data["subscriptionCapability"]["MaxFrequency"] = duration_isoformat
        
    if dataReq.get("refreshRate") is not None:
        # convert the refresh rate value to iso8601
        refresh_seconds = int(dataReq["refreshRate"])
        refresh_isoformat = "PT{}S".format(refresh_seconds)  # durata in formato ISO8601
        json_data["subscriptionCapability"]["RefreshRate"] = refresh_isoformat
        
    if dataReq.get("subscriptionEnd") is not None:
        json_data["subscriptionCapability"]["SubscriptionEnd"] = datetime.now().isoformat()
    
        
    if dataReq.get("dataFreshness") is not None:
        # convert the data freshness value to iso8601
        fresh_seconds = int(dataReq["dataFreshness"])
        fresh_isoformat = "PT{}S".format(fresh_seconds)  # durata in formato ISO8601
        json_data["subscriptionCapability"]["RefreshRate"] = fresh_isoformat    
        
    if dataReq.get("seaBasin") is not None:
        json_data["subscriptionCapability"]["SeaBasin"] = dataReq["seaBasin"]

    return json.dumps(json_data)


# function to SEND the SUBSCRIBE POST REQUEST
def send_subscribe_request(dataReq):
    headers = {'Content-Type': 'application/json'}
    payload = create_request_subscribe(dataReq)
    
    try:
        response = requests.post(url_rest, headers=headers, data=payload)
        print(f"Status code: {response.status_code}")
        
        if response.status_code == 200:
            print("Response correctly received:")
            print(json.dumps(response.json(), indent=4))
        else:
            print(f"Errore during HTTP request: {response.status_code}")
            print("response content:", response.text)
    except Exception as e:
        print(f"Errore during HTTP request: {e}")

############################################## UNSUBSCRIBE ########################################################

# function to create the payload of the unsubscribe request
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


# function to SEND the UNSUBSCRIBE POST REQUEST
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
        
############################################## REQUESTS DICTIONARIES ########################################################

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


# function to handle the opening of the websocket connection, once the connection is established, the user chooses the request to send
def on_open(ws):
    print("Connessione al websocket stabilita.")
    
    # get the user choice, use the while loop to continue asking the user's choice, with 0 I close the program
    while True:
        
        choice = get_user_choice() # var to match the user choice
        # do the corresponding action to the user input
        match choice:
            case "1":
                print("SENDING PULL REQUEST...")
                send_pull_request(dataReq_pull)
            case "2":
                print("SENDING DISCOVERY...")
                send_discovery_request(dataReq_discovery)
            case "3":
                print("SENDING SUBSCRIBE REQUEST...")
                send_subscribe_request(dataReq_subscribe)
            case "4":
                print("SENDING UNSUBSCRIBE REQUEST...")
                send_unsubscribe_request(dataReq_unsubscribe)
            case "0": 
                print("Closing the program...")
                # close the websocket connection
                ws.close()
                # close the program
                exit()
            case _:
                print("Invalid input.")
                # if the user enters an invalid input, the loop continues
            
    
# function to handle the reception of websocket messages
def on_message(ws, message):
    print("Messagge riceived:", message)

# function to handle the websocket connection error
def on_error(ws, error):
    print("Websocket error:", error)

# function to handle the closure of the websocket connection
def on_close(ws, close_status_code, close_msg): # delete the comment in the main() to see the diagnostic if the connection is not successful
    print("Websocket connection closed correctly.")
    
################################################ MAIN ########################################################

# function to run the program
def main():
    # connect to the websocket with a separate thread
    ws = websocket.WebSocketApp(url_websocket,
                                on_open=on_open,
                                on_message=on_message,
                                #on_error=on_error,         DELETE THIS COMMENT IF YOU WANT TO SEE THE DIAGNOSTIC IF THE CONNECTION IS NOT SUCCESSFUL
                                on_close=on_close)
    ws.run_forever()

# call the main function and run the program
if __name__ == "__main__":
    main()
