#!/usr/bin/env python3
"""
🔍 Debug Permissions - Meta Business Catalog
============================================

Script di debug per analizzare i permessi e la configurazione
dell'access token per il Catalog API.
"""

import sys
from pathlib import Path
import requests
import json

# Aggiungi il percorso src al PYTHONPATH
sys.path.insert(0, str(Path(__file__).parent / 'src'))

def debug_access_token():
    """Debug delle informazioni sull'access token."""
    
    try:
        from src.config import Config
        
        config = Config()
        
        print("🔐 Debug Access Token")
        print("=" * 25)
        
        if not config.META_ACCESS_TOKEN:
            print("❌ META_ACCESS_TOKEN non configurato!")
            return False
        
        # Test del token con debug_token endpoint
        url = f"{config.META_BASE_URL}/debug_token"
        params = {
            'input_token': config.META_ACCESS_TOKEN,
            'access_token': config.META_ACCESS_TOKEN
        }
        
        response = requests.get(url, params=params)
        
        if response.status_code == 200:
            data = response.json()
            token_data = data.get('data', {})
            
            print(f"✅ Token valido")
            print(f"🆔 App ID: {token_data.get('app_id', 'N/A')}")
            print(f"👤 User ID: {token_data.get('user_id', 'N/A')}")
            print(f"📅 Scadenza: {token_data.get('expires_at', 'Mai (long-lived)')}")
            print(f"🔍 Tipo: {token_data.get('type', 'N/A')}")
            print(f"✅ Valido: {token_data.get('is_valid', False)}")
            
            # Mostra permessi (scopes)
            scopes = token_data.get('scopes', [])
            print(f"\n🔑 Permessi del Token ({len(scopes)}):")
            for scope in sorted(scopes):
                print(f"  ✅ {scope}")
                
            # Controlla permessi necessari per catalogo
            required_scopes = ['catalog_management', 'business_management']
            missing_scopes = [scope for scope in required_scopes if scope not in scopes]
            
            if missing_scopes:
                print(f"\n❌ Permessi Mancanti per Catalog API:")
                for scope in missing_scopes:
                    print(f"  ❌ {scope}")
                return False
            else:
                print(f"\n✅ Tutti i permessi necessari sono presenti!")
                return True
                
        else:
            print(f"❌ Errore nel debug token: {response.status_code}")
            try:
                error_data = response.json()
                print(f"   Dettagli: {error_data}")
            except:
                print(f"   Response: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Errore nel debug token: {e}")
        return False

def debug_app_permissions():
    """Debug dei permessi dell'app."""
    
    try:
        from src.config import Config
        
        config = Config()
        
        print("\n🏗️ Debug App Permissions")
        print("=" * 28)
        
        if not config.META_APP_ID:
            print("❌ META_APP_ID non configurato!")
            return False
        
        # Test permessi app
        url = f"{config.META_BASE_URL}/{config.META_APP_ID}/permissions"
        headers = {'Authorization': f'Bearer {config.META_ACCESS_TOKEN}'}
        
        response = requests.get(url, headers=headers)
        
        if response.status_code == 200:
            data = response.json()
            permissions = data.get('data', [])
            
            print(f"✅ App ID: {config.META_APP_ID}")
            print(f"🔑 Permessi App ({len(permissions)}):")
            
            for perm in permissions:
                status = perm.get('status', 'unknown')
                permission = perm.get('permission', 'unknown')
                emoji = "✅" if status == "granted" else "❌" if status == "declined" else "⏳"
                print(f"  {emoji} {permission}: {status}")
                
            return True
            
        else:
            print(f"❌ Errore nel recupero permessi app: {response.status_code}")
            try:
                error_data = response.json()
                print(f"   Dettagli: {error_data}")
            except:
                print(f"   Response: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Errore nel debug permessi app: {e}")
        return False

def debug_catalog_access():
    """Debug dell'accesso al catalogo."""
    
    try:
        from src.config import Config
        
        config = Config()
        
        print("\n📦 Debug Catalog Access")
        print("=" * 25)
        
        if not config.CATALOG_ID:
            print("❌ CATALOG_ID non configurato!")
            return False
        
        # Test accesso catalogo - prova diversi endpoint
        endpoints_to_test = [
            ('GET Info', f"{config.META_BASE_URL}/{config.CATALOG_ID}", {}),
            ('GET Products', f"{config.META_BASE_URL}/{config.CATALOG_ID}/products", {}),
            ('GET Home Listings', f"{config.META_BASE_URL}/{config.CATALOG_ID}/home_listings", {}),
            ('GET with Fields', f"{config.META_BASE_URL}/{config.CATALOG_ID}", {
                'fields': 'id,name,vertical,business,product_count'
            })
        ]
        
        headers = {'Authorization': f'Bearer {config.META_ACCESS_TOKEN}'}
        
        for test_name, url, params in endpoints_to_test:
            print(f"\n🧪 Test {test_name}:")
            print(f"   URL: {url}")
            
            response = requests.get(url, headers=headers, params=params)
            
            if response.status_code == 200:
                data = response.json()
                print(f"   ✅ Successo!")
                
                # Mostra info essenziali
                if 'id' in data:
                    print(f"   🆔 ID: {data.get('id')}")
                if 'name' in data:
                    print(f"   📦 Nome: {data.get('name')}")
                if 'vertical' in data:
                    print(f"   🏷️  Vertical: {data.get('vertical')}")
                if 'product_count' in data:
                    print(f"   📊 Prodotti: {data.get('product_count')}")
                if 'business' in data:
                    business = data.get('business', {})
                    if isinstance(business, dict) and 'name' in business:
                        print(f"   🏢 Business: {business.get('name')}")
                
                # Per liste, mostra conteggio
                if 'data' in data and isinstance(data['data'], list):
                    print(f"   📋 Elementi: {len(data['data'])}")
                    
            else:
                print(f"   ❌ Errore {response.status_code}")
                try:
                    error_data = response.json()
                    error_msg = error_data.get('error', {}).get('message', 'Errore sconosciuto')
                    print(f"   💬 Messaggio: {error_msg}")
                except:
                    print(f"   📄 Response: {response.text[:200]}...")
        
        return True
        
    except Exception as e:
        print(f"❌ Errore nel debug catalogo: {e}")
        return False

def debug_business_assets():
    """Debug dell'accesso agli asset business."""
    
    try:
        from src.config import Config
        
        config = Config()
        
        print("\n🏢 Debug Business Assets")
        print("=" * 26)
        
        # Test accesso agli asset del business
        url = f"{config.META_BASE_URL}/me/businesses"
        headers = {'Authorization': f'Bearer {config.META_ACCESS_TOKEN}'}
        
        response = requests.get(url, headers=headers)
        
        if response.status_code == 200:
            data = response.json()
            businesses = data.get('data', [])
            
            print(f"✅ Business accessibili: {len(businesses)}")
            
            for business in businesses:
                print(f"\n🏢 Business: {business.get('name', 'N/A')}")
                print(f"   🆔 ID: {business.get('id', 'N/A')}")
                
                # Per ogni business, prova a ottenere i cataloghi
                business_id = business.get('id')
                if business_id:
                    catalogs_url = f"{config.META_BASE_URL}/{business_id}/owned_product_catalogs"
                    cat_response = requests.get(catalogs_url, headers=headers)
                    
                    if cat_response.status_code == 200:
                        cat_data = cat_response.json()
                        catalogs = cat_data.get('data', [])
                        print(f"   📦 Cataloghi: {len(catalogs)}")
                        
                        for catalog in catalogs:
                            cat_id = catalog.get('id')
                            cat_name = catalog.get('name')
                            is_current = cat_id == config.CATALOG_ID
                            marker = "👈 CURRENT" if is_current else ""
                            print(f"     - {cat_name} (ID: {cat_id}) {marker}")
                    else:
                        print(f"   ❌ Errore cataloghi: {cat_response.status_code}")
            
            return True
            
        else:
            print(f"❌ Errore nel recupero business: {response.status_code}")
            try:
                error_data = response.json()
                print(f"   Dettagli: {error_data}")
            except:
                print(f"   Response: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Errore nel debug business: {e}")
        return False

def test_post_permission():
    """Test specifico per permessi POST al catalogo."""
    
    try:
        from src.config import Config
        
        config = Config()
        
        print("\n🧪 Test POST Permissions")
        print("=" * 25)
        
        # Prepara un payload di test molto semplice
        test_product = {
            "retailer_id": "TEST_PERMISSION_CHECK",
            "name": "Test Permission Product",
            "description": "Prodotto di test per verificare permessi POST",
            "price": "1000",
            "currency": "EUR",
            "availability": "in stock",
            "condition": "new"
        }
        
        # Test POST con dry-run (se supportato)
        url = f"{config.META_BASE_URL}/{config.CATALOG_ID}/products"
        headers = {
            'Authorization': f'Bearer {config.META_ACCESS_TOKEN}',
            'Content-Type': 'application/json'
        }
        
        print(f"🎯 Test POST a: {url}")
        print(f"📦 Payload: {json.dumps(test_product, indent=2)}")
        
        # Prima prova con un POST normale (che probabilmente fallirà ma ci darà info utili)
        response = requests.post(url, headers=headers, json=test_product)
        
        print(f"\n📊 Risultato POST:")
        print(f"   Status Code: {response.status_code}")
        
        if response.status_code == 200:
            print("   ✅ POST riuscito! (eliminare il prodotto di test se necessario)")
            data = response.json()
            if 'id' in data:
                product_id = data['id']
                print(f"   🆔 Prodotto creato: {product_id}")
                
                # Prova a eliminare il prodotto di test
                delete_url = f"{config.META_BASE_URL}/{product_id}"
                del_response = requests.delete(delete_url, headers=headers)
                if del_response.status_code == 200:
                    print("   🗑️  Prodotto di test eliminato")
                else:
                    print(f"   ⚠️  Impossibile eliminare prodotto test: {del_response.status_code}")
                    
        else:
            try:
                error_data = response.json()
                error_info = error_data.get('error', {})
                
                print(f"   ❌ Errore: {error_info.get('message', 'Sconosciuto')}")
                print(f"   🔍 Tipo: {error_info.get('type', 'N/A')}")
                print(f"   📝 Codice: {error_info.get('code', 'N/A')}")
                print(f"   🔗 Subcode: {error_info.get('error_subcode', 'N/A')}")
                
                # Analizza il tipo di errore
                error_code = error_info.get('code')
                if error_code == 200:  # Permissions error
                    print("\n💡 Questo è un errore di permessi!")
                    print("   Possibili cause:")
                    print("   - Token non ha permesso 'catalog_management'")
                    print("   - App non connessa al Business Portfolio")
                    print("   - Catalogo non associato all'app")
                elif error_code == 190:  # Token error
                    print("\n💡 Questo è un errore di token!")
                    print("   Possibili cause:")
                    print("   - Token scaduto o non valido")
                    print("   - Token non generato correttamente")
                
            except:
                print(f"   📄 Response raw: {response.text}")
        
        return response.status_code == 200
        
    except Exception as e:
        print(f"❌ Errore nel test POST: {e}")
        return False

def main():
    """Funzione principale del debug."""
    
    print("🔍 Meta Business Catalog - Debug Permissions")
    print("=" * 45)
    print()
    
    # Array per tracciare i risultati
    tests = [
        ("Access Token", debug_access_token),
        ("App Permissions", debug_app_permissions), 
        ("Catalog Access", debug_catalog_access),
        ("Business Assets", debug_business_assets),
        ("POST Permissions", test_post_permission)
    ]
    
    results = {}
    
    for test_name, test_func in tests:
        try:
            result = test_func()
            results[test_name] = result
        except Exception as e:
            print(f"❌ Errore nel test '{test_name}': {e}")
            results[test_name] = False
    
    # Riassunto finale
    print("\n" + "=" * 45)
    print("📊 RIASSUNTO DEBUG")
    print("=" * 45)
    
    all_passed = True
    for test_name, result in results.items():
        emoji = "✅" if result else "❌"
        print(f"{emoji} {test_name}")
        if not result:
            all_passed = False
    
    print()
    if all_passed:
        print("🎉 Tutti i test sono passati! Il problema potrebbe essere nel payload o endpoint specifico.")
    else:
        print("⚠️  Alcuni test sono falliti. Controlla la configurazione seguendo META_BUSINESS_SETUP.md")
    
    print()
    print("📚 Guide di riferimento:")
    print("1. 📖 META_BUSINESS_SETUP.md - Configurazione completa")
    print("2. 🌐 https://developers.facebook.com/tools/explorer/ - Graph API Explorer")
    print("3. 🏢 https://business.facebook.com/ - Meta Business Manager")

if __name__ == "__main__":
    main()