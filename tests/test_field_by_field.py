#!/usr/bin/env python3
"""
Test per identificare esattamente quale parametro è invalid
"""

import requests
from src.config import Config

def test_individual_fields():
    """Test campo per campo per identificare il problema."""
    
    config = Config()
    
    url = f"{config.META_BASE_URL}/{config.CATALOG_ID}/home_listings"
    headers = {
        'Authorization': f'Bearer {config.META_ACCESS_TOKEN}',
        'Content-Type': 'application/json'
    }
    
    print("🧪 Test Campi Individuali")
    print("=" * 30)
    
    # Base payload minimale
    base_payload = {
        "home_listing_id": "TEST_FIELD_001",
        "name": "Test Field",
        "description": "Test per campo specifico",
        "price": "100000",
        "currency": "EUR", 
        "url": "https://example.com/test",
    }
    
    # Test 1: Solo campi base (senza address)
    print("1️⃣ Test senza address...")
    response = requests.post(url, headers=headers, json=base_payload)
    print(f"Status: {response.status_code}")
    if response.status_code != 200:
        error_msg = response.json().get('error', {}).get('message', 'Errore sconosciuto')
        print(f"Errore: {error_msg}")
    print()
    
    # Test 2: Con address minimo
    print("2️⃣ Test con address minimo...")
    payload_with_address = base_payload.copy()
    payload_with_address["address"] = {
        "street_address": "Via Test, 1",
        "city": "Roma", 
        "region": "Lazio",
        "country": "IT",
        "postal_code": "00100"
    }
    
    response = requests.post(url, headers=headers, json=payload_with_address)
    print(f"Status: {response.status_code}")
    if response.status_code != 200:
        error_msg = response.json().get('error', {}).get('message', 'Errore sconosciuto')
        print(f"Errore: {error_msg}")
    print()
    
    # Test 3: Aggiunta coordinate 
    print("3️⃣ Test aggiungendo coordinate...")
    payload_with_coords = payload_with_address.copy()
    payload_with_coords["address"]["latitude"] = 41.9028
    payload_with_coords["address"]["longitude"] = 12.4964
    
    response = requests.post(url, headers=headers, json=payload_with_coords)
    print(f"Status: {response.status_code}")
    if response.status_code != 200:
        error_msg = response.json().get('error', {}).get('message', 'Errore sconosciuto')
        print(f"Errore: {error_msg}")
    print()
    
    # Test 4: Aggiunta immagini
    print("4️⃣ Test aggiungendo immagini...")
    payload_with_images = payload_with_coords.copy()
    payload_with_images["images"] = [
        {"image_url": "https://images.unsplash.com/photo-1600596542815-ffad4c1539a9?w=800"}
    ]
    
    response = requests.post(url, headers=headers, json=payload_with_images)
    print(f"Status: {response.status_code}")
    if response.status_code != 200:
        error_msg = response.json().get('error', {}).get('message', 'Errore sconosciuto')
        print(f"Errore: {error_msg}")
    print()
    
    # Test 5: Aggiunta campi property
    print("5️⃣ Test aggiungendo campi property...")
    payload_complete = payload_with_images.copy()
    payload_complete.update({
        "availability": "for_sale",
        "listing_type": "for_sale", 
        "property_type": "house"
    })
    
    response = requests.post(url, headers=headers, json=payload_complete)
    print(f"Status: {response.status_code}")
    if response.status_code != 200:
        error_msg = response.json().get('error', {}).get('message', 'Errore sconosciuto')
        print(f"Errore: {error_msg}")
    else:
        print("✅ Successo!")
        result = response.json()
        print(f"ID: {result.get('id', 'N/A')}")
    print()
    
    # Test 6: Con year_built
    if response.status_code != 200:
        print("6️⃣ Test aggiungendo year_built...")
        payload_complete["year_built"] = 2020
        
        response = requests.post(url, headers=headers, json=payload_complete)
        print(f"Status: {response.status_code}")
        if response.status_code != 200:
            error_msg = response.json().get('error', {}).get('message', 'Errore sconosciuto')
            print(f"Errore: {error_msg}")
        else:
            print("✅ Successo!")
            result = response.json()
            print(f"ID: {result.get('id', 'N/A')}")

if __name__ == "__main__":
    test_individual_fields()