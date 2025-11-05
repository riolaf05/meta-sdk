#!/usr/bin/env python3
"""
🔍 Debug Invalid Parameter - Home Listings
==========================================

Script per identificare quale parametro causa l'errore "Invalid parameter"
testando un campo alla volta.
"""

import sys
from pathlib import Path
import requests
import json

# Aggiungi il percorso src al PYTHONPATH
sys.path.insert(0, str(Path(__file__).parent / 'src'))

def test_field_by_field():
    """Test aggiungendo un campo alla volta per identificare il problema."""
    
    try:
        from src.config import Config
        
        config = Config()
        
        print("🔍 Test Field-by-Field per Invalid Parameter")
        print("=" * 45)
        
        url = f"{config.META_BASE_URL}/{config.CATALOG_ID}/home_listings"
        headers = {
            'Authorization': f'Bearer {config.META_ACCESS_TOKEN}',
            'Content-Type': 'application/json'
        }
        
        # Test step-by-step aggiungendo un campo alla volta
        base_listing = {
            "home_listing_id": "DEBUG_TEST_001"
        }
        
        fields_to_test = [
            ("name", "Test Listing Debug"),
            ("description", "Test listing per debug"),
            ("price", "100000"),
            ("currency", "EUR"),
            ("url", "https://example.com/test"),
            ("address", {
                "street_address": "Via Test, 1",
                "city": "Roma",
                "country": "IT",
                "postal_code": "00100",
                "latitude": 41.9028,
                "longitude": 12.4964
            }),
            ("images", [{"image_url": "https://images.unsplash.com/photo-1600596542815-ffad4c1539a9?w=800"}]),
            ("availability", "for_sale"),
            ("listing_type", "for_sale"),
            ("property_type", "house"),
            ("year_built", 2020)
        ]
        
        current_listing = base_listing.copy()
        
        for field_name, field_value in fields_to_test:
            print(f"\n🧪 Test aggiungendo campo: {field_name}")
            
            # Aggiungi il campo corrente
            current_listing[field_name] = field_value
            
            print(f"   📦 Payload corrente:")
            print(f"   {json.dumps(current_listing, indent=4)}")
            
            # Test POST
            response = requests.post(url, headers=headers, json=current_listing)
            
            print(f"   📊 Status: {response.status_code}")
            
            if response.status_code == 200:
                print(f"   ✅ SUCCESSO! Il listing funziona fino al campo '{field_name}'")
                result = response.json()
                listing_id = result.get('id')
                
                # Elimina il listing di test
                if listing_id:
                    delete_url = f"{config.META_BASE_URL}/{listing_id}"
                    requests.delete(delete_url, headers=headers)
                    print(f"   🗑️  Listing test eliminato")
                
                break
            else:
                try:
                    error_data = response.json()
                    error = error_data.get('error', {})
                    message = error.get('message', 'Sconosciuto')
                    
                    print(f"   ❌ Errore: {message}")
                    
                    # Se l'errore cambia, significa che il campo precedente era problematico
                    if "Invalid parameter" not in message:
                        print(f"   💡 Il campo '{field_name}' potrebbe aver risolto l'errore precedente!")
                    
                except Exception as parse_error:
                    print(f"   📄 Response: {response.text[:100]}...")
        
        return False
        
    except Exception as e:
        print(f"❌ Errore nel test: {e}")
        return False

def test_address_components():
    """Test specifico per i componenti dell'address che potrebbero essere problematici."""
    
    try:
        from src.config import Config
        
        config = Config()
        
        print("\n🔍 Test Componenti Address")
        print("=" * 27)
        
        url = f"{config.META_BASE_URL}/{config.CATALOG_ID}/home_listings"
        headers = {
            'Authorization': f'Bearer {config.META_ACCESS_TOKEN}',
            'Content-Type': 'application/json'
        }
        
        # Test diversi formati di coordinate
        coordinate_tests = [
            ("Float", 41.9028, 12.4964),
            ("String", "41.9028", "12.4964"),
            ("Int", 41, 12)
        ]
        
        for coord_type, lat, lng in coordinate_tests:
            print(f"\n🧪 Test coordinate come {coord_type}")
            
            test_listing = {
                "home_listing_id": f"DEBUG_COORD_{coord_type}",
                "name": f"Test Coordinate {coord_type}",
                "description": "Test per formato coordinate",
                "price": "100000",
                "currency": "EUR",
                "address": {
                    "street_address": "Via Test, 1",
                    "city": "Roma",
                    "country": "IT",
                    "postal_code": "00100",
                    "latitude": lat,
                    "longitude": lng
                }
            }
            
            response = requests.post(url, headers=headers, json=test_listing)
            
            print(f"   📊 Status: {response.status_code}")
            
            if response.status_code == 200:
                print(f"   ✅ Formato {coord_type} funziona!")
                result = response.json()
                listing_id = result.get('id')
                if listing_id:
                    delete_url = f"{config.META_BASE_URL}/{listing_id}"
                    requests.delete(delete_url, headers=headers)
                return True
            else:
                try:
                    error_data = response.json()
                    error = error_data.get('error', {})
                    message = error.get('message', 'Sconosciuto')
                    print(f"   ❌ Errore: {message}")
                except:
                    print(f"   ❌ Errore nel parsing response")
        
        return False
        
    except Exception as e:
        print(f"❌ Errore nel test coordinate: {e}")
        return False

def main():
    """Test per identificare il parametro invalido."""
    
    print("🔍 Debug Invalid Parameter Error")
    print("=" * 35)
    print()
    
    # Test campo per campo
    success1 = test_field_by_field()
    
    # Test componenti address
    success2 = test_address_components()
    
    if not (success1 or success2):
        print("\n⚠️  Nessun test riuscito.")
        print("💡 Possibili cause dell'errore 'Invalid parameter':")
        print("1. 🔢 Formato numerico sbagliato (price, coordinates)")
        print("2. 📅 year_built in formato non supportato")
        print("3. 🌐 URL non validi")
        print("4. 📍 Coordinate fuori range o formato sbagliato")
        print("5. 💰 Valuta non supportata per il mercato")
        print()
        print("🔍 Suggerimento: Prova Graph API Explorer manualmente")
        print("   https://developers.facebook.com/tools/explorer/")

if __name__ == "__main__":
    main()