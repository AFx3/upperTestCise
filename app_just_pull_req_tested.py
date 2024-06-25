from fastapi import FastAPI, HTTPException
import uvicorn
import json
import os
import requests

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

        # Automatically forward the saved data as a pull request
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
    '''
    # Mapping for Type to valid ServiceType
    service_type_mapping = {
        "Vessel": "VesselService"
        # altri mappings
    }

    # type must exists
    if 'Type' in data:
        mapped_service_type = service_type_mapping.get(data['Type'], data['Type'])
        json_data['discoveryProfile']['ServiceType'] = mapped_service_type
    else:
        raise ValueError("'Type' field is required in the payload.")
    '''

    # needed for a success req.
    '''
    json_data['informationSecurityLevel'] = data.get('informationSecurityLevel', 'EUConfidential')
    json_data['informationSensitivity'] = data.get('informationSensitivity', 'Red')
    json_data['personalData'] = data.get('personalData', False)
    json_data['purpose'] = data.get('purpose', 'VTM')
    '''

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





    #json_data['Sender'] = data['identifier']['GeneratedBy']['IdentificationNumber']
    #if data.get("purpose") is not None:
    #    json_data["purpose"] = json_data["purpose"]


    #json_data['senderServiceType'] = data.get('senderServiceType', 'default_senderServiceType')



    # valori predefiniti per campi aggiuntivi se non sono presenti nei dati ricevuti
    #json_data['serviceOperation'] = data.get('serviceOperation', 'Pull')
    # OTTENGO ERRORE CON QUESTO CAMPO

    if data.get("serviceOperation") is not None:
        json_data["serviceOperation"] = data["serviceOperation"]


    return json_data



if __name__ == "__main__":
    uvicorn.run(app, host="10.50.1.181", port=8000)
