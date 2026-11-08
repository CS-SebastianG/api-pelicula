import boto3
import uuid
import os
import json


def log(tipo, log_datos):
    print(json.dumps({"tipo": tipo, "log_datos": log_datos}, default=str))


def lambda_handler(event, context):
    try:
        tenant_id = event['body']['tenant_id']
        pelicula_datos = event['body']['pelicula_datos']
        nombre_tabla = os.environ["TABLE_NAME"]
        uuidv4 = str(uuid.uuid4())
        pelicula = {
            'tenant_id': tenant_id,
            'uuid': uuidv4,
            'pelicula_datos': pelicula_datos
        }
        dynamodb = boto3.resource('dynamodb')
        table = dynamodb.Table(nombre_tabla)
        response = table.put_item(Item=pelicula)
        # Salida (json)
        log("INFO", pelicula)
        return {
            'statusCode': 200,
            'pelicula': pelicula,
            'response': response
        }
    except KeyError as e:
        log("ERROR", {
            "error": "KeyError",
            "mensaje": "Falta el campo " + str(e),
            "entrada": event.get('body') if isinstance(event, dict) else None
        })
        return {
            'statusCode': 400,
            'error': 'Falta el campo ' + str(e)
        }
    except Exception as e:
        log("ERROR", {
            "error": type(e).__name__,
            "mensaje": str(e),
            "entrada": event.get('body') if isinstance(event, dict) else None
        })
        return {
            'statusCode': 500,
            'error': 'Error interno: ' + type(e).__name__
        }
