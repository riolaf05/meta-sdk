#!/usr/bin/env python3
"""
Script per visualizzare i prodotti nel catalogo WhatsApp Business.
"""

import sys
from pathlib import Path

# Aggiungi il percorso src al PYTHONPATH
sys.path.insert(0, str(Path(__file__).parent / 'src'))

def list_catalog_products():
    """Lista tutti i prodotti nel catalogo usando l'endpoint corretto."""
    
    try:
        from src.config import Config, logger
        import requests
        
        config = Config()
        
        if not config.META_ACCESS_TOKEN or not config.CATALOG_ID:
            print("❌ Configurazione incompleta!")
            print("📝 Assicurati di aver configurato META_ACCESS_TOKEN e CATALOG_ID nel file .env")
            return
        
        print("🔍 Visualizzazione Prodotti Catalogo WhatsApp Business")
        print("=" * 55)
        print(f"📦 Catalog ID: {config.CATALOG_ID}")
        print()
        
        # URL corretto per l'API Meta Graph
        url = f"{config.META_BASE_URL}/{config.CATALOG_ID}/products"
        headers = {
            'Authorization': f'Bearer {config.META_ACCESS_TOKEN}',
            'Content-Type': 'application/json'
        }
        params = {
            'limit': 25,  # Limita a 25 prodotti per pagina
            'fields': 'id,name,retailer_id,price,currency,availability,condition,description,image_url,url'
        }
        
        print("🌐 Chiamata API Meta...")
        response = requests.get(url, headers=headers, params=params)
        
        if response.status_code == 200:
            data = response.json()
            products = data.get('data', [])
            
            print(f"✅ Recuperati {len(products)} prodotti dal catalogo")
            print()
            
            if products:
                for i, product in enumerate(products, 1):
                    print(f"📦 Prodotto {i}:")
                    print(f"   🆔 ID Meta: {product.get('id', 'N/A')}")
                    print(f"   🏷️  Retailer ID: {product.get('retailer_id', 'N/A')}")
                    print(f"   📝 Nome: {product.get('name', 'N/A')}")
                    
                    # Gestisci il prezzo (potrebbe essere in centesimi)
                    price = product.get('price')
                    currency = product.get('currency', 'EUR')
                    if price:
                        if isinstance(price, (int, str)) and str(price).isdigit():
                            # Prezzo in centesimi, convertilo in euro
                            price_euro = int(price) / 100
                            print(f"   💰 Prezzo: €{price_euro:.2f} ({price} centesimi)")
                        else:
                            print(f"   💰 Prezzo: {price} {currency}")
                    
                    print(f"   📊 Disponibilità: {product.get('availability', 'N/A')}")
                    print(f"   🔧 Condizione: {product.get('condition', 'N/A')}")
                    
                    # Descrizione (limitata)
                    description = product.get('description', '')
                    if description:
                        desc_short = description[:100] + "..." if len(description) > 100 else description
                        print(f"   📖 Descrizione: {desc_short}")
                    
                    # URL immagine
                    image_url = product.get('image_url')
                    if image_url:
                        print(f"   🖼️  Immagine: {image_url[:50]}...")
                    
                    print("-" * 50)
                
                # Info paginazione
                paging = data.get('paging', {})
                if 'next' in paging:
                    print("📄 Ci sono più prodotti. Usa la paginazione per vedere tutti.")
                
            else:
                print("📭 Nessun prodotto trovato nel catalogo.")
                print()
                print("💡 Suggerimenti:")
                print("1. Verifica che il Catalog ID sia corretto")
                print("2. Aggiungi prodotti tramite Commerce Manager o la nostra app")
                print("3. Controlla che il catalogo sia collegato al WhatsApp Business Account")
        
        elif response.status_code == 400:
            error_data = response.json()
            error_msg = error_data.get('error', {}).get('message', 'Errore sconosciuto')
            print(f"❌ Errore API Meta (400): {error_msg}")
            print()
            print("🛠️  Possibili soluzioni:")
            print("1. Verifica che il Catalog ID sia corretto")
            print("2. Controlla che l'Access Token abbia i permessi corretti")
            print("3. Assicurati che il catalogo sia di tipo 'commerce'")
            
        elif response.status_code == 401:
            print("❌ Errore di autenticazione (401)")
            print("🔑 Controlla che l'Access Token sia valido e non scaduto")
            
        elif response.status_code == 403:
            print("❌ Accesso negato (403)")
            print("🚫 L'Access Token non ha i permessi necessari per accedere al catalogo")
            
        else:
            print(f"❌ Errore HTTP {response.status_code}")
            print(f"📄 Risposta: {response.text}")
    
    except ImportError as e:
        print(f"❌ Errore nell'importazione: {e}")
        print("💡 Assicurati che l'ambiente virtuale sia attivato")
    
    except Exception as e:
        print(f"❌ Errore inaspettato: {e}")

def show_catalog_info():
    """Mostra informazioni sul catalogo."""
    
    try:
        from src.config import Config
        import requests
        
        config = Config()
        
        if not config.META_ACCESS_TOKEN or not config.CATALOG_ID:
            print("❌ Configurazione incompleta!")
            return
        
        print("📋 Informazioni Catalogo")
        print("=" * 25)
        
        # URL per informazioni catalogo
        url = f"{config.META_BASE_URL}/{config.CATALOG_ID}"
        headers = {
            'Authorization': f'Bearer {config.META_ACCESS_TOKEN}',
            'Content-Type': 'application/json'
        }
        params = {
            'fields': 'id,name,product_count,vertical,business'
        }
        
        response = requests.get(url, headers=headers, params=params)
        
        if response.status_code == 200:
            data = response.json()
            print(f"📦 Nome: {data.get('name', 'N/A')}")
            print(f"🆔 ID: {data.get('id', 'N/A')}")
            print(f"📊 Prodotti: {data.get('product_count', 0)}")
            print(f"🏷️  Vertical: {data.get('vertical', 'N/A')}")
            print(f"🏢 Business: {data.get('business', {}).get('name', 'N/A')}")
        else:
            print(f"❌ Errore nel recupero informazioni: {response.status_code}")
            print(f"📄 Risposta: {response.text}")
    
    except Exception as e:
        print(f"❌ Errore: {e}")

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "info":
        show_catalog_info()
    else:
        list_catalog_products()