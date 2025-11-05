#!/usr/bin/env python3
"""
Test per verificare se il catalogo funziona con prodotti commerce normali
"""

import requests
from src.config import Config

def test_commerce_products():
    """Test aggiunta prodotti commerce per verificare se il catalogo funziona."""
    
    config = Config()
    
    # Test prodotti commerce normali
    url = f"{config.META_BASE_URL}/{config.CATALOG_ID}/products"
    headers = {
        'Authorization': f'Bearer {config.META_ACCESS_TOKEN}',
        'Content-Type': 'application/json'
    }
    
    print("🛒 Test Prodotti Commerce")
    print("=" * 25)
    
    product_payload = {
        "retailer_id": "TEST_COMMERCE_001",
        "name": "Test Commerce Product",
        "description": "Prodotto test per verificare il catalogo",
        "price": "29.99",
        "currency": "EUR",
        "url": "https://example.com/product",
        "image_url": "https://images.unsplash.com/photo-1600596542815-ffad4c1539a9?w=800",
        "availability": "in stock",
        "condition": "new"
    }
    
    print("📦 Tentativo aggiunta prodotto commerce...")
    response = requests.post(url, headers=headers, json=product_payload)
    print(f"Status: {response.status_code}")
    
    if response.status_code == 200:
        print("✅ Successo! Il catalogo funziona per prodotti commerce")
        result = response.json()
        print(f"ID prodotto: {result.get('id', 'N/A')}")
        return True
    else:
        try:
            error_msg = response.json().get('error', {}).get('message', 'Errore sconosciuto')
            print(f"❌ Errore: {error_msg}")
        except:
            print(f"❌ Errore: {response.text}")
    
    return False

def test_catalog_info():
    """Verifica info del catalogo per capire il tipo supportato."""
    
    config = Config()
    
    url = f"{config.META_BASE_URL}/{config.CATALOG_ID}"
    headers = {
        'Authorization': f'Bearer {config.META_ACCESS_TOKEN}',
    }
    
    print("\n📊 Info Catalogo")
    print("=" * 15)
    
    response = requests.get(url, headers=headers)
    print(f"Status: {response.status_code}")
    
    if response.status_code == 200:
        catalog_info = response.json()
        print(f"Nome: {catalog_info.get('name', 'N/A')}")
        print(f"Vertical: {catalog_info.get('vertical', 'N/A')}")
        print(f"ID: {catalog_info.get('id', 'N/A')}")
        
        # Se è home_listings, verifichiamo le capacità
        if catalog_info.get('vertical') == 'home_listings':
            print("✅ Catalogo configurato per home_listings")
        else:
            print(f"⚠️  Catalogo NON configurato per home_listings. Vertical: {catalog_info.get('vertical')}")
        
        return catalog_info
    else:
        error_msg = response.json().get('error', {}).get('message', 'Errore sconosciuto')
        print(f"❌ Errore nel recupero info catalogo: {error_msg}")
        return None

if __name__ == "__main__":
    # Prima verifichiamo il tipo di catalogo
    catalog_info = test_catalog_info()
    
    # Poi proviamo se funziona con prodotti commerce
    commerce_success = test_commerce_products()
    
    print("\n🔍 Analisi:")
    if catalog_info and catalog_info.get('vertical') != 'home_listings':
        print("🎯 PROBLEMA IDENTIFICATO: Il catalogo non è configurato per home_listings!")
        print("   Per usare home_listings, il catalogo deve avere vertical='home_listings'")
        print("   Il tuo catalogo ha vertical='" + str(catalog_info.get('vertical')) + "'")
        print("\n💡 SOLUZIONE: Usa prodotti commerce normali invece di home_listings")
    elif not commerce_success:
        print("❌ Problema generale con il catalogo - né commerce né home_listings funzionano")
    else:
        print("✅ Il catalogo funziona per commerce, il problema è specifico per home_listings")