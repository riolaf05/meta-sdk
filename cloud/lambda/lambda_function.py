"""
AWS Lambda Function per Meta WhatsApp Business Catalog API
Gestisce l'aggiunta di prodotti/listing ai cataloghi Meta tramite API Gateway
"""

import json
import os
import requests
import logging
from typing import Dict, Any, Optional

# Configurazione logging
logger = logging.getLogger()
logger.setLevel(logging.INFO)

class MetaCatalogManager:
    """Gestore per l'integrazione con Meta Catalog API."""
    
    def __init__(self):
        """Inizializza il gestore con le variabili d'ambiente."""
        self.access_token = os.environ.get('META_ACCESS_TOKEN')
        self.catalog_id = os.environ.get('META_CATALOG_ID')
        self.business_id = os.environ.get('META_BUSINESS_ID')
        self.app_id = os.environ.get('META_APP_ID')
        self.app_secret = os.environ.get('META_APP_SECRET')
        self.base_url = os.environ.get('META_BASE_URL', 'https://graph.facebook.com/v18.0')
        
        # Validazione configurazione
        required_vars = ['META_ACCESS_TOKEN', 'META_CATALOG_ID']
        missing_vars = [var for var in required_vars if not os.environ.get(var)]
        
        if missing_vars:
            raise ValueError(f"Variabili d'ambiente mancanti: {', '.join(missing_vars)}")
    
    def detect_catalog_type(self) -> str:
        """Rileva automaticamente il tipo di catalogo."""
        try:
            url = f"{self.base_url}/{self.catalog_id}"
            headers = {'Authorization': f'Bearer {self.access_token}'}
            params = {'fields': 'name,vertical,id'}
            
            response = requests.get(url, headers=headers, params=params, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                vertical = data.get('vertical', 'commerce')
                logger.info(f"Catalog type detected: {vertical}")
                return vertical or 'commerce'
            else:
                logger.error(f"Failed to detect catalog type: {response.status_code}")
                return 'commerce'  # Default fallback
                
        except Exception as e:
            logger.error(f"Error detecting catalog type: {str(e)}")
            return 'commerce'  # Default fallback
    
    def add_home_listing(self, listing_data: Dict[str, Any]) -> Dict[str, Any]:
        """Aggiunge un home listing al catalogo."""
        try:
            url = f"{self.base_url}/{self.catalog_id}/home_listings"
            headers = {
                'Authorization': f'Bearer {self.access_token}',
                'Content-Type': 'application/json'
            }
            
            # Validazione campi obbligatori per home_listings
            required_fields = ['home_listing_id', 'name', 'description', 'price', 
                             'currency', 'url', 'address', 'images', 'availability', 'year_built']
            
            missing_fields = [field for field in required_fields if field not in listing_data]
            if missing_fields:
                return {
                    'success': False,
                    'error': f'Campi obbligatori mancanti: {", ".join(missing_fields)}'
                }
            
            # Validazione address
            address = listing_data.get('address', {})
            required_address_fields = ['street_address', 'city', 'region', 'country', 
                                     'postal_code', 'latitude', 'longitude']
            
            missing_address_fields = [field for field in required_address_fields 
                                    if field not in address]
            if missing_address_fields:
                return {
                    'success': False,
                    'error': f'Campi address obbligatori mancanti: {", ".join(missing_address_fields)}'
                }
            
            # Assicurati che il prezzo sia integer
            if isinstance(listing_data.get('price'), str):
                try:
                    listing_data['price'] = int(listing_data['price'])
                except ValueError:
                    return {
                        'success': False,
                        'error': 'Il prezzo deve essere un numero intero'
                    }
            
            response = requests.post(url, headers=headers, json=listing_data, timeout=30)
            
            if response.status_code == 200:
                result = response.json()
                return {
                    'success': True,
                    'id': result.get('id'),
                    'message': 'Home listing aggiunto con successo'
                }
            else:
                error_data = response.json()
                error_msg = error_data.get('error', {}).get('message', 'Errore sconosciuto')
                return {
                    'success': False,
                    'error': f'Errore Meta API: {error_msg}',
                    'status_code': response.status_code
                }
                
        except Exception as e:
            logger.error(f"Error adding home listing: {str(e)}")
            return {
                'success': False,
                'error': f'Errore interno: {str(e)}'
            }
    
    def add_commerce_product(self, product_data: Dict[str, Any]) -> Dict[str, Any]:
        """Aggiunge un prodotto commerce al catalogo."""
        try:
            url = f"{self.base_url}/{self.catalog_id}/products"
            headers = {
                'Authorization': f'Bearer {self.access_token}',
                'Content-Type': 'application/json'
            }
            
            # Validazione campi obbligatori per prodotti commerce
            required_fields = ['retailer_id', 'name', 'description', 'price', 
                             'currency', 'availability', 'condition', 'image_url', 'url']
            
            missing_fields = [field for field in required_fields if field not in product_data]
            if missing_fields:
                return {
                    'success': False,
                    'error': f'Campi obbligatori mancanti: {", ".join(missing_fields)}'
                }
            
            # Assicurati che il prezzo sia integer
            if isinstance(product_data.get('price'), str):
                try:
                    product_data['price'] = int(product_data['price'])
                except ValueError:
                    return {
                        'success': False,
                        'error': 'Il prezzo deve essere un numero intero'
                    }
            
            response = requests.post(url, headers=headers, json=product_data, timeout=30)
            
            if response.status_code == 200:
                result = response.json()
                return {
                    'success': True,
                    'id': result.get('id'),
                    'message': 'Prodotto commerce aggiunto con successo'
                }
            else:
                error_data = response.json()
                error_msg = error_data.get('error', {}).get('message', 'Errore sconosciuto')
                return {
                    'success': False,
                    'error': f'Errore Meta API: {error_msg}',
                    'status_code': response.status_code
                }
                
        except Exception as e:
            logger.error(f"Error adding commerce product: {str(e)}")
            return {
                'success': False,
                'error': f'Errore interno: {str(e)}'
            }

def lambda_handler(event: Dict[str, Any], context: Any) -> Dict[str, Any]:
    """
    Handler principale della Lambda function.
    
    Payload atteso:
    {
        "type": "home_listing" | "commerce_product",
        "data": { ... dati del prodotto/listing ... }
    }
    """
    
    try:
        logger.info(f"Received event: {json.dumps(event)}")
        
        # Parse del body se è una stringa JSON
        if isinstance(event.get('body'), str):
            try:
                body = json.loads(event['body'])
            except json.JSONDecodeError:
                return {
                    'statusCode': 400,
                    'headers': {
                        'Content-Type': 'application/json',
                        'Access-Control-Allow-Origin': '*'
                    },
                    'body': json.dumps({
                        'success': False,
                        'error': 'Invalid JSON in request body'
                    })
                }
        else:
            body = event.get('body', {})
        
        # Validazione payload
        if not body or 'type' not in body or 'data' not in body:
            return {
                'statusCode': 400,
                'headers': {
                    'Content-Type': 'application/json',
                    'Access-Control-Allow-Origin': '*'
                },
                'body': json.dumps({
                    'success': False,
                    'error': 'Payload deve contenere "type" e "data"'
                })
            }
        
        item_type = body['type']
        item_data = body['data']
        
        # Inizializza il gestore Meta Catalog
        try:
            catalog_manager = MetaCatalogManager()
        except ValueError as e:
            return {
                'statusCode': 500,
                'headers': {
                    'Content-Type': 'application/json',
                    'Access-Control-Allow-Origin': '*'
                },
                'body': json.dumps({
                    'success': False,
                    'error': f'Configurazione mancante: {str(e)}'
                })
            }
        
        # Gestisci in base al tipo
        if item_type == 'home_listing':
            result = catalog_manager.add_home_listing(item_data)
        elif item_type == 'commerce_product':
            result = catalog_manager.add_commerce_product(item_data)
        else:
            return {
                'statusCode': 400,
                'headers': {
                    'Content-Type': 'application/json',
                    'Access-Control-Allow-Origin': '*'
                },
                'body': json.dumps({
                    'success': False,
                    'error': f'Tipo non supportato: {item_type}. Usa "home_listing" o "commerce_product"'
                })
            }
        
        # Restituisci il risultato
        status_code = 200 if result['success'] else 400
        
        return {
            'statusCode': status_code,
            'headers': {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*'
            },
            'body': json.dumps(result)
        }
        
    except Exception as e:
        logger.error(f"Unhandled error in lambda_handler: {str(e)}")
        return {
            'statusCode': 500,
            'headers': {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*'
            },
            'body': json.dumps({
                'success': False,
                'error': f'Errore interno del server: {str(e)}'
            })
        }