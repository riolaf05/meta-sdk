#!/usr/bin/env python3
"""
🏠 Demo App - WhatsApp Business Catalog Manager
===============================================

Script demo unificato per aggiungere prodotti al catalogo WhatsApp Business.
Supporta sia cataloghi commerce generici che cataloghi real estate (home_listings).

Esegui semplicemente: python demo.py
"""

import sys
from pathlib import Path

# Aggiungi il percorso src al PYTHONPATH
sys.path.insert(0, str(Path(__file__).parent / 'src'))

def detect_catalog_type():
    """Rileva automaticamente il tipo di catalogo."""
    try:
        from src.config import Config
        import requests
        
        config = Config()
        
        print("🔍 Rilevamento Tipo Catalogo")
        print("=" * 28)
        
        if not config.META_ACCESS_TOKEN or not config.CATALOG_ID:
            print("❌ Configurazione incompleta")
            return None, "Configurazione incompleta"
        
        # Ottieni informazioni sul catalogo
        url = f"{config.META_BASE_URL}/{config.CATALOG_ID}"
        headers = {'Authorization': f'Bearer {config.META_ACCESS_TOKEN}'}
        params = {'fields': 'name,vertical,id'}
        
        response = requests.get(url, headers=headers, params=params)
        
        if response.status_code == 200:
            data = response.json()
            vertical = data.get('vertical', 'commerce')
            name = data.get('name', 'N/A')
            catalog_id = data.get('id', 'N/A')
            
            print(f"📊 Nome Catalogo: {name}")
            print(f"🆔 ID Catalogo: {catalog_id}")
            print(f"🏷️ Vertical: {vertical or 'None (default commerce)'}")
            
            if vertical == 'home_listings':
                print(f"🏠 Tipo Rilevato: Real Estate (home_listings)")
            else:
                print(f"🛒 Tipo Rilevato: Commerce (products)")
                if not vertical:
                    print(f"💡 Nota: Catalogo non ha vertical specifico, usando commerce")
            
            return vertical or 'commerce', None
        else:
            print(f"❌ Errore API: {response.status_code}")
            return None, f"Errore API: {response.status_code}"
            
    except Exception as e:
        print(f"❌ Errore: {str(e)}")
        return None, str(e)

def add_commerce_products():
    """Aggiunge prodotti per cataloghi commerce standard."""
    
    try:
        from src.config import Config
        import requests
        
        config = Config()
        
        print("📦 Aggiunta Prodotti Commerce al Catalogo")
        print("=" * 42)
        
        # URL endpoint per prodotti commerce
        url = f"{config.META_BASE_URL}/{config.CATALOG_ID}/products"
        headers = {
            'Authorization': f'Bearer {config.META_ACCESS_TOKEN}',
            'Content-Type': 'application/json'
        }
        
        products = [
            {
                "retailer_id": "IPHONE_15_PRO",
                "name": "iPhone 15 Pro 256GB",
                "description": "Ultimo iPhone con chip A17 Pro, fotocamera da 48MP e display Super Retina XDR da 6.1 pollici.",
                "price": 139900, # €1399.00 in centesimi (integer)
                "currency": "EUR",
                "availability": "in stock",
                "condition": "new",
                "brand": "Apple",
                "category": "Elettronica",
                "image_url": "https://images.unsplash.com/photo-1592750475338-74b7b21085ab?w=800",
                "url": "https://www.apple.com/iphone-15-pro"
            },
            {
                "retailer_id": "TSHIRT_001",
                "name": "T-Shirt Premium Cotton",
                "description": "T-shirt di alta qualità in 100% cotone biologico. Disponibile in vari colori e taglie.",
                "price": 2999, # €29.99 in centesimi (integer)
                "currency": "EUR", 
                "availability": "in stock",
                "condition": "new",
                "brand": "EcoWear",
                "category": "Abbigliamento",
                "image_url": "https://images.unsplash.com/photo-1521572163474-6864f9cf17ab?w=800",
                "url": "https://www.example-store.com/tshirt-001"
            }
        ]
        
        success_count = 0
        
        for i, product in enumerate(products, 1):
            print(f"📦 Aggiungendo prodotto {i}/{len(products)}: {product['name']}")
            
            try:
                response = requests.post(url, headers=headers, json=product)
                
                if response.status_code == 200:
                    result = response.json()
                    print(f"   ✅ Aggiunto con successo!")
                    print(f"   🆔 Product ID: {result.get('id', 'N/A')}")
                    success_count += 1
                else:
                    error_data = response.json()
                    error_msg = error_data.get('error', {}).get('message', 'Errore sconosciuto')
                    print(f"   ❌ Errore: {error_msg}")
                    
            except Exception as e:
                print(f"   ❌ Errore: {e}")
            
            print()
        
        print(f"🎉 Aggiunti {success_count}/{len(products)} prodotti commerce!")
        return success_count > 0
        
    except Exception as e:
        print(f"❌ Errore nell'aggiunta prodotti commerce: {e}")
        return False

def add_real_estate_listings():
    """Aggiunge listing per cataloghi real estate (home_listings)."""
    
    try:
        from src.config import Config
        import requests
        
        config = Config()
        
        print("🏠 Aggiunta Home Listings al Catalogo Real Estate")
        print("=" * 48)
        
        # URL endpoint specifico per home_listings
        url = f"{config.META_BASE_URL}/{config.CATALOG_ID}/home_listings"
        headers = {
            'Authorization': f'Bearer {config.META_ACCESS_TOKEN}',
            'Content-Type': 'application/json'
        }
        
        listings = [
            {
                "home_listing_id": "VILLA_ROMA_001",
                "name": "Villa di Lusso a Roma Nord",
                "description": "Splendida villa di 400mq con giardino di 1000mq, 5 camere da letto, 4 bagni, garage per 3 auto.",
                "price": 950000,  # Integer, non string
                "currency": "EUR",
                "url": "https://www.example-realestate.com/villa-roma-001",
                "images": [
                    {"image_url": "https://picsum.photos/800/600?random=1"}
                ],
                "address": {
                    "street_address": "Via dei Parioli, 25",
                    "city": "Roma",
                    "region": "Lazio", 
                    "country": "IT",
                    "postal_code": "00135",
                    "latitude": 41.9028,
                    "longitude": 12.4964
                },
                "availability": "for_sale",
                "year_built": 2018
            },
            {
                "home_listing_id": "APT_MILANO_002",
                "name": "Appartamento Moderno Milano Centro",
                "description": "Appartamento di 120mq completamente ristrutturato nel centro di Milano. 3 camere, 2 bagni, cucina moderna.",
                "price": 750000,  # Integer, non string
                "currency": "EUR",
                "url": "https://www.example-realestate.com/apt-milano-002",
                "images": [
                    {"image_url": "https://picsum.photos/800/600?random=2"}
                ],
                "address": {
                    "street_address": "Via Montenapoleone, 12",
                    "city": "Milano", 
                    "region": "Lombardia",
                    "country": "IT",
                    "postal_code": "20121",
                    "latitude": 45.4642,
                    "longitude": 9.1900
                },
                "availability": "for_sale",
                "year_built": 2020
            }
        ]
        
        success_count = 0
        
        for i, listing in enumerate(listings, 1):
            print(f"🏠 Aggiungendo listing {i}/{len(listings)}: {listing['name']}")
            
            try:
                response = requests.post(url, headers=headers, json=listing)
                
                if response.status_code == 200:
                    result = response.json()
                    print(f"   ✅ Aggiunto con successo!")
                    print(f"   🆔 Listing ID: {result.get('id', 'N/A')}")
                    success_count += 1
                else:
                    error_data = response.json()
                    error_msg = error_data.get('error', {}).get('message', 'Errore sconosciuto')
                    print(f"   ❌ Errore: {error_msg}")
                    
            except Exception as e:
                print(f"   ❌ Errore: {e}")
            
            print()
        
        print(f"🎉 Aggiunti {success_count}/{len(listings)} listing real estate!")
        return success_count > 0
        
    except Exception as e:
        print(f"❌ Errore nell'aggiunta listing real estate: {e}")
        return False

def view_catalog_status():
    """Mostra lo stato del catalogo dopo l'aggiunta."""
    
    try:
        from src.config import Config
        import requests
        
        config = Config()
        
        print("\n📊 Stato del Catalogo")
        print("=" * 22)
        
        url = f"{config.META_BASE_URL}/{config.CATALOG_ID}"
        headers = {'Authorization': f'Bearer {config.META_ACCESS_TOKEN}'}
        params = {'fields': 'id,name,product_count,vertical,business'}
        
        response = requests.get(url, headers=headers, params=params)
        
        if response.status_code == 200:
            data = response.json()
            print(f"📦 Nome: {data.get('name', 'N/A')}")
            print(f"🆔 ID: {data.get('id', 'N/A')}")
            print(f"📊 Prodotti/Listing: {data.get('product_count', 0)}")
            print(f"🏷️  Tipo: {data.get('vertical', 'N/A')}")
            print(f"🏢 Business: {data.get('business', {}).get('name', 'N/A')}")
        else:
            print(f"❌ Errore nel recupero stato: {response.status_code}")
            
    except Exception as e:
        print(f"❌ Errore: {e}")

def main():
    """Funzione principale del demo."""
    
    print("🚀 WhatsApp Business Catalog Demo")
    print("=" * 35)
    print()
    
    # Rileva tipo di catalogo
    catalog_type, error = detect_catalog_type()
    
    if error:
        print(f"❌ Errore nella rilevazione catalogo: {error}")
        print()
        print("💡 Assicurati che:")
        print("1. Il file .env sia configurato correttamente")
        print("2. META_ACCESS_TOKEN sia valido e non scaduto")
        print("3. CATALOG_ID sia corretto")
        return
    
    print(f"🏷️  Tipo catalogo rilevato: {catalog_type}")
    print()
    
    # Aggiungi prodotti in base al tipo
    success = False
    
    if catalog_type == "home_listings":
        success = add_real_estate_listings()
    else:
        success = add_commerce_products()
    
    # Mostra stato finale
    view_catalog_status()
    
    # Guida finale
    print()
    print("📋 Dove Visualizzare i Risultati:")
    print("1. 🌐 Meta Commerce Manager: https://business.facebook.com/commerce/")
    print("2. 📱 WhatsApp Business App → Impostazioni → Catalogo")
    print("3. 🔧 Graph API Explorer: https://developers.facebook.com/tools/explorer/")
    print("4. 🐍 Script Python: python view_catalog.py")
    
    if success:
        print()
        print("🎉 Demo completata con successo!")
    else:
        print()
        print("⚠️  Demo completata con alcuni errori. Controlla la configurazione.")
        print()
        print("🔍 Per debug avanzato:")
        print("   python debug_permissions.py")
        print()
        print("📖 Per configurazione app:")
        print("   Leggi META_BUSINESS_SETUP.md")

if __name__ == "__main__":
    main()