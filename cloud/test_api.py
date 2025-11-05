#!/usr/bin/env python3
"""
Script di test per l'API Gateway Meta Catalog
"""

import requests
import json
import sys
from typing import Dict, Any

# Configurazione (modifica con i tuoi valori)
API_GATEWAY_URL = "https://YOUR_API_GATEWAY_URL/catalog"
API_KEY = "YOUR_API_KEY"

def test_home_listing():
    """Test aggiunta home listing tramite API Gateway."""
    
    payload = {
        "type": "home_listing",
        "data": {
            "home_listing_id": "API_TEST_VILLA_001",
            "name": "Villa Test API Gateway",
            "description": "Villa di test aggiunta tramite API Gateway",
            "price": 750000,
            "currency": "EUR",
            "url": "https://example.com/test-villa",
            "images": [
                {"image_url": "https://picsum.photos/800/600?random=10"}
            ],
            "address": {
                "street_address": "Via Test API, 1",
                "city": "Milano",
                "region": "Lombardia",
                "country": "IT",
                "postal_code": "20121",
                "latitude": 45.4642,
                "longitude": 9.1900
            },
            "availability": "for_sale",
            "year_built": 2021
        }
    }
    
    headers = {
        "Content-Type": "application/json",
        "x-api-key": API_KEY
    }
    
    print("🏠 Test Home Listing via API Gateway")
    print("=" * 40)
    print(f"URL: {API_GATEWAY_URL}")
    print(f"Payload: {json.dumps(payload, indent=2)}")
    print()
    
    try:
        response = requests.post(API_GATEWAY_URL, headers=headers, json=payload, timeout=30)
        
        print(f"📊 Status Code: {response.status_code}")
        print(f"📄 Response: {response.text}")
        
        if response.status_code == 200:
            result = response.json()
            if result.get('success'):
                print(f"✅ Successo! Listing ID: {result.get('id')}")
                return True
            else:
                print(f"❌ Errore: {result.get('error')}")
        else:
            print(f"❌ Errore HTTP: {response.status_code}")
            
    except Exception as e:
        print(f"❌ Errore: {e}")
    
    return False

def test_commerce_product():
    """Test aggiunta prodotto commerce tramite API Gateway."""
    
    payload = {
        "type": "commerce_product",
        "data": {
            "retailer_id": "API_TEST_PRODUCT_001",
            "name": "Prodotto Test API Gateway",
            "description": "Prodotto di test aggiunto tramite API Gateway",
            "price": 5999,
            "currency": "EUR",
            "availability": "in stock",
            "condition": "new",
            "brand": "TestBrand",
            "category": "Test",
            "image_url": "https://picsum.photos/800/600?random=20",
            "url": "https://example.com/test-product"
        }
    }
    
    headers = {
        "Content-Type": "application/json",
        "x-api-key": API_KEY
    }
    
    print("🛒 Test Commerce Product via API Gateway")
    print("=" * 42)
    print(f"URL: {API_GATEWAY_URL}")
    print(f"Payload: {json.dumps(payload, indent=2)}")
    print()
    
    try:
        response = requests.post(API_GATEWAY_URL, headers=headers, json=payload, timeout=30)
        
        print(f"📊 Status Code: {response.status_code}")
        print(f"📄 Response: {response.text}")
        
        if response.status_code == 200:
            result = response.json()
            if result.get('success'):
                print(f"✅ Successo! Product ID: {result.get('id')}")
                return True
            else:
                print(f"❌ Errore: {result.get('error')}")
        else:
            print(f"❌ Errore HTTP: {response.status_code}")
            
    except Exception as e:
        print(f"❌ Errore: {e}")
    
    return False

def generate_curl_examples():
    """Genera esempi di comando cURL."""
    
    print("📋 Esempi cURL")
    print("=" * 15)
    
    print("\n🏠 Home Listing:")
    print(f"""curl -X POST "{API_GATEWAY_URL}" \\
  -H "Content-Type: application/json" \\
  -H "x-api-key: {API_KEY}" \\
  -d '{{
    "type": "home_listing",
    "data": {{
      "home_listing_id": "CURL_VILLA_001",
      "name": "Villa cURL Test",
      "description": "Villa aggiunta tramite cURL",
      "price": 650000,
      "currency": "EUR",
      "url": "https://example.com/curl-villa",
      "images": [
        {{"image_url": "https://picsum.photos/800/600?random=30"}}
      ],
      "address": {{
        "street_address": "Via cURL, 1",
        "city": "Roma",
        "region": "Lazio", 
        "country": "IT",
        "postal_code": "00100",
        "latitude": 41.9028,
        "longitude": 12.4964
      }},
      "availability": "for_sale",
      "year_built": 2019
    }}
  }}'""")
    
    print("\n🛒 Commerce Product:")
    print(f"""curl -X POST "{API_GATEWAY_URL}" \\
  -H "Content-Type: application/json" \\
  -H "x-api-key: {API_KEY}" \\
  -d '{{
    "type": "commerce_product",
    "data": {{
      "retailer_id": "CURL_PRODUCT_001",
      "name": "Prodotto cURL Test",
      "description": "Prodotto aggiunto tramite cURL",
      "price": 2999,
      "currency": "EUR",
      "availability": "in stock",
      "condition": "new",
      "brand": "cURLBrand",
      "category": "Test",
      "image_url": "https://picsum.photos/800/600?random=40",
      "url": "https://example.com/curl-product"
    }}
  }}'""")

if __name__ == "__main__":
    print("🧪 Meta Catalog API Gateway - Test Script")
    print("=" * 45)
    
    if API_GATEWAY_URL == "https://YOUR_API_GATEWAY_URL/catalog" or API_KEY == "YOUR_API_KEY":
        print("❌ Configura prima API_GATEWAY_URL e API_KEY nello script!")
        print("   Ottieni questi valori dopo aver fatto 'terraform apply'")
        sys.exit(1)
    
    print(f"🔗 API URL: {API_GATEWAY_URL}")
    print(f"🔑 API Key: {API_KEY[:10]}...")
    print()
    
    # Test dei diversi tipi
    print("1️⃣ Test Home Listing...")
    success1 = test_home_listing()
    print()
    
    print("2️⃣ Test Commerce Product...")  
    success2 = test_commerce_product()
    print()
    
    # Genera esempi cURL
    generate_curl_examples()
    
    # Risultati finali
    print(f"\n📊 Risultati:")
    print(f"   Home Listing: {'✅' if success1 else '❌'}")
    print(f"   Commerce Product: {'✅' if success2 else '❌'}")
    
    if success1 or success2:
        print("\n🎉 Test completati con successo!")
    else:
        print("\n❌ Tutti i test sono falliti. Controlla la configurazione.")
        print("💡 Suggerimenti:")
        print("   - Verifica API_GATEWAY_URL e API_KEY")
        print("   - Controlla che l'infrastruttura sia deployata")
        print("   - Verifica i log CloudWatch per errori dettagliati")