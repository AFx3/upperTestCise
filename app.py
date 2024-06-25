from fastapi import FastAPI, HTTPException
import uvicorn
import json
import os
import requests
from datetime import datetime

app = FastAPI()

next_id = 1  # next ID to assign to the messages
data = {}  # dictionary to store messages with unique IDs

# path to the file where JSON data will be saved
data_file_path = os.path.join(os.path.dirname(__file__), "saved_data.json")

@app.post("/api/v1/message/send")
async def salva_dati(dati_json: dict):
    global next_id, data

    try:
        # assign an incremental ID
        dati_json["id"] = next_id

        # append message to the dictionary
        data[next_id] = dati_json

        # increment the ID counter
        next_id += 1

        # load existing data from the file (if it exists)
        try:
            with open(data_file_path, "r") as f:
                existing_data = json.load(f)
                # Update next_id from the loaded data (if present)
                if "next_id" in existing_data:
                    next_id = existing_data["next_id"]
        except (FileNotFoundError, json.JSONDecodeError):
            existing_data = {}

        # save the updated data to the file, including next_id
        with open(data_file_path, "w") as f:
            existing_data["next_id"] = next_id  # store next_id for future use
            existing_data.update(data)
            json.dump(existing_data, f, indent=4)

        # Automatically forward the saved data as a pull or discovery request
        if dati_json.get("pullType") == "Discover":
            forward_response = await send_discovery_request(dati_json)
        elif dati_json.get("pullType") == "Subscribe":
            forward_response = await send_subscribe_request(dati_json)
        elif dati_json.get("pullType") == "Unsubscribe":
            forward_response = await send_unsubscribe_request(dati_json)

        else:
            forward_response = await send_pull_request(dati_json)

        return {
            "Response": f"Message correctly received with ID: {next_id - 1}",
            "ForwardingResponse": forward_response
        }

    except Exception as e:
        # Handle errors and return error message
        raise HTTPException(status_code=500, detail=f"Error: {e}")


async def send_pull_request(data):
    url_rest = "http://10.50.1.130:8080/adaptor/api/v1/CISEMessageServiceREST/sendPullRequest"
    headers = {'Content-Type': 'application/json'}

    # Create the payload dynamically using received data
    payload = create_request_pull(data)

    try:
        response = requests.post(url_rest, headers=headers, json=payload)
        if response.status_code == 200:
            return response.json()
        else:
            return {
                "error": f"Error in the HTTP request: {response.status_code}",
                "content": response.text
            }
    except Exception as e:
        return {"error": f"Error during HTTP request: {e}"}


def create_request_pull(data):
    json_data = {
        "pullType": "Request",
        "discoveryProfile": {
            "ServiceRole": "Provider",
            "ServiceStatus": "Online",
        }
    }

    if data.get("Type") is not None:
        json_data["discoveryProfile"]['ServiceType'] = data["Type"]
    if data.get("informationSecurityLevel") is not None:
        json_data["informationSecurityLevel"] = data["informationSecurityLevel"]
    if data.get("informationSensitivityLevel") is not None:
        json_data["informationSensitivity"] = data["informationSensitivity"]  
    if data.get("personalData") is not None:
        json_data["personalData"] = data["personalData"] 
    if data.get("purpose") is not None:
        json_data["purpose"] = data["purpose"]    
    if data.get("serviceOperation") is not None:
        json_data["serviceOperation"] = data["serviceOperation"]
    if data.get("responseTimeOut") is not None:
        json_data["responseTimeOut"] = data["responseTimeOut"]    
    if data.get("name") is not None:
        json_data["name"] = data["name"]
    if data.get("mmsi") is not None:
        json_data["mmsi"] = data["mmsi"]
    if data.get("imoNumber") is not None:
        json_data["imoNumber"] = data["imoNumber"]
    if data.get("serviceID") is not None:
        json_data["serviceID"] = data["serviceID"] 
    if data.get("seaBasin") is not None:
        json_data["seaBasin"] = data["seaBasin"]  
    if data.get("country") is not None:
        json_data["country"] = data["country"]
    if data.get("community") is not None:
        json_data["community"] = data["community"]   
    if data.get("bbox") is not None:
        json_data["bbox"] = data["bbox"] 
    if data.get("startDate") is not None:
        json_data["startDate"] = data["startDate"]
    if data.get("endDate") is not None:
        json_data["endDate"] = data["endDate"]
    if data.get("anomalyType") is not None:
        json_data["anomalyType"] = data["anomalytype"]
    if data.get("locationDocumentType") is not None:
        json_data["locationDocumentType"] = data["locationDocumentType"]
    if data.get("eventDocumentType") is not None:
        json_data["eventDocumentType"] = data["eventDocumentType"]
    if data.get("irregularMigrationIncidentType") is not None:
        json_data["irregularMigrationIncidentType"] = data["irregularMigrationIncidentType"]
    if data.get("version") is not None:
        json_data["version"] = data["version"]
    if data.get("legalName") is not None:
        json_data["legalName"] = data["legalName"]
    if data.get("description") is not None:
        json_data["description"] = data["description"]
    if data.get("subject") is not None:
        json_data["subject"] = data["subject"]
    if data.get("referenceURI") is not None:
        json_data["referenceURI"] = data["referenceURI"]
    if data.get("maxFrequency") is not None:
        json_data["maxFrequency"] = data["maxFrequency"]
    if data.get("refreshRate") is not None:
        json_data["refreshRate"] = data["refreshRate"]
    if data.get("subscriptionEnd") is not None:
        json_data["subscriptionEnd"] = data["subscriptionEnd"]

    return json_data


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
    
    return json_data


async def send_discovery_request(dataReq):
    url_rest = "http://10.50.1.130:8080/adaptor/api/v1/CISEMessageServiceREST/sendPullRequest"
    headers = {'Content-Type': 'application/json'}
    payload = create_request_discovery(dataReq)
    
    try:
        response = requests.post(url_rest, headers=headers, json=payload)
        if response.status_code == 200:
            return response.json()
        else:
            return {
                "error": f"Error in the HTTP request: {response.status_code}",
                "content": response.text
            }
    except Exception as e:
        return {"error": f"Error during HTTP request: {e}"}
    
def send_subscribe_request(dataReq):
    url_rest = "http://10.50.1.130:8080/adaptor/api/v1/CISEMessageServiceREST/sendPullRequest"
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


#function to create the payload of the unsubscribe request
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
    url_rest = "http://10.50.1.130:8080/adaptor/api/v1/CISEMessageServiceREST/sendPullRequest"
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




if __name__ == "__main__":
    uvicorn.run(app, host="10.50.1.181", port=8000)
