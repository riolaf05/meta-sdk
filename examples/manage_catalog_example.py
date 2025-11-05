#!/usr/bin/env python3
"""
Esempio: Gestione completa del catalogo WhatsApp Business.

Questo script dimostra tutte le funzionalità principali del manager,
incluso CRUD operations su prodotti e invio di messaggi.
"""

import sys
from pathlib import Path
from typing import List, Dict, Any

# Aggiungi il percorso src al PYTHONPATH
sys.path.insert(0, str(Path(__file__).parent.parent / 'src'))

from src.whatsapp_catalog_manager import WhatsAppCatalogManager
from src.config import logger

def demo_catalog_operations(manager: WhatsAppCatalogManager):
    """Dimostra le operazioni base del catalogo."""
    
    print("📋 Demo: Operazioni Catalogo")
    print("-" * 30)
    
    try:
        if manager.catalog_id:
            # Ottieni informazioni catalogo
            catalog_info = manager.get_catalog_info()
            print(f"📦 Nome Catalogo: {catalog_info.get('name', 'N/A')}")
            print(f"📊 Numero Prodotti: {catalog_info.get('product_count', 0)}")
            print(f"🏷️  Vertical: {catalog_info.get('vertical', 'N/A')}")
        else:
            print("⚠️  Catalog ID non configurato")
        
    except Exception as e:
        print(f"❌ Errore operazioni catalogo: {e}")

def demo_product_lifecycle(manager: WhatsAppCatalogManager):
    """Dimostra il ciclo di vita completo di un prodotto."""
    
    print("\n🔄 Demo: Ciclo di Vita Prodotto")
    print("-" * 35)
    
    # Prodotto di test
    test_product = {
        "retailer_id": "DEMO_LIFECYCLE_001",
        "name": "Prodotto Demo - Ciclo di Vita",
        "description": "Questo è un prodotto di esempio per dimostrare il ciclo di vita completo: creazione, lettura, aggiornamento, eliminazione.",
        "price": "49.99",
        "currency": "EUR",
        "availability": "in stock",
        "condition": "new",
        "brand": "DemoBrand",
        "category": "Demo > Test",
        "image_url": "https://images.unsplash.com/photo-1505740420928-5e560c06d30e?w=500"
    }
    
    try:
        # 1. CREATE - Aggiungi prodotto
        print("➕ 1. Aggiunta prodotto...")
        if manager.catalog_id:
            create_result = manager.add_product(test_product)
            print(f"✅ Prodotto creato con ID: {create_result.get('id', 'N/A')}")
        else:
            validated = manager.validate_product_data(test_product)
            print(f"✅ Dati prodotto validati: {validated['name']}")
        
        retailer_id = test_product['retailer_id']
        
        # 2. READ - Leggi prodotto
        print(f"\n📖 2. Lettura prodotto {retailer_id}...")
        if manager.catalog_id:
            read_result = manager.get_product(retailer_id)
            print(f"✅ Prodotto trovato: {read_result.get('name', 'N/A')}")
            print(f"💰 Prezzo: {read_result.get('price', 'N/A')}")
        else:
            print("✅ Simulazione lettura prodotto completata")
        
        # 3. UPDATE - Aggiorna prodotto
        print(f"\n🔄 3. Aggiornamento prodotto {retailer_id}...")
        update_data = {
            "price": "39.99",
            "availability": "limited stock",
            "description": "Descrizione aggiornata - Ora in offerta limitata!"
        }
        
        if manager.catalog_id:
            update_result = manager.update_product(retailer_id, update_data)
            print("✅ Prodotto aggiornato con successo")
            print(f"💰 Nuovo prezzo: {update_data['price']} EUR")
        else:
            print("✅ Simulazione aggiornamento prodotto completata")
        
        # 4. LIST - Lista prodotti
        print(f"\n📋 4. Lista prodotti nel catalogo...")
        if manager.catalog_id:
            products_list = manager.list_products(limit=3)
            products_data = products_list.get('data', [])
            print(f"📊 Trovati {len(products_data)} prodotti (max 3 mostrati):")
            
            for i, product in enumerate(products_data, 1):
                print(f"  {i}. {product.get('name', 'N/A')} - ID: {product.get('retailer_id', 'N/A')}")
        else:
            print("✅ Simulazione lista prodotti completata")
        
        # 5. DELETE - Elimina prodotto (opzionale - commentato per sicurezza)
        print(f"\n🗑️  5. Eliminazione prodotto {retailer_id}...")
        print("⚠️  Eliminazione disabilitata per sicurezza")
        print(f"💡 Per eliminare: manager.delete_product('{retailer_id}')")
        
        # Uncomment per eliminare realmente:
        # if manager.catalog_id:
        #     delete_result = manager.delete_product(retailer_id)
        #     print("✅ Prodotto eliminato con successo")
        # else:
        #     print("✅ Simulazione eliminazione prodotto completata")
        
    except Exception as e:
        print(f"❌ Errore nel ciclo di vita del prodotto: {e}")
        logger.error(f"Errore demo lifecycle: {e}")

def demo_messaging(manager: WhatsAppCatalogManager):
    """Dimostra l'invio di messaggi WhatsApp."""
    
    print("\n📱 Demo: Messaggistica WhatsApp")
    print("-" * 32)
    
    # Numero di test (sostituisci con un numero reale per test)
    test_phone = "+391234567890"
    
    try:
        if manager.phone_number_id and manager.catalog_id:
            print(f"📞 Numero di test: {test_phone}")
            print("⚠️  NOTA: Sostituisci con un numero reale per testare l'invio")
            
            # Messaggio singolo prodotto
            print("\n📦 1. Messaggio Singolo Prodotto:")
            print("   Codice esempio:")
            print(f"   manager.send_product_message('{test_phone}', 'DEMO_LIFECYCLE_001', 'Guarda questo prodotto!')")
            
            # Messaggio catalogo completo
            print("\n📋 2. Messaggio Catalogo Completo:")
            print("   Codice esempio:")
            print(f"   manager.send_catalog_message('{test_phone}', 'Esplora il nostro catalogo!')")
            
            # Per testare realmente, decommentare e usare un numero valido:
            # result = manager.send_product_message(test_phone, "DEMO_LIFECYCLE_001", "Prodotto di esempio!")
            # print(f"✅ Messaggio inviato: {result.get('messages', [{}])[0].get('id', 'N/A')}")
            
        else:
            missing = []
            if not manager.phone_number_id:
                missing.append("PHONE_NUMBER_ID")
            if not manager.catalog_id:
                missing.append("CATALOG_ID")
            
            print(f"⚠️  Messaggistica non disponibile. Configurare: {', '.join(missing)}")
            
    except Exception as e:
        print(f"❌ Errore demo messaggistica: {e}")
        logger.error(f"Errore demo messaging: {e}")

def demo_batch_operations(manager: WhatsAppCatalogManager):
    """Dimostra le operazioni batch."""
    
    print("\n📦 Demo: Operazioni Batch")
    print("-" * 26)
    
    # Prodotti di esempio per batch
    batch_products = [
        {
            "retailer_id": f"BATCH_DEMO_{i:03d}",
            "name": f"Prodotto Batch {i}",
            "description": f"Descrizione del prodotto numero {i} per demo batch operations",
            "price": f"{20 + i * 5}.99",
            "currency": "EUR",
            "availability": "in stock",
            "condition": "new",
            "brand": "BatchDemo",
            "category": "Demo > Batch",
            "image_url": "https://images.unsplash.com/photo-1560472355-a9a6f4c21fd4?w=500"
        }
        for i in range(1, 4)  # Solo 3 prodotti per demo
    ]
    
    try:
        print(f"📋 Preparazione {len(batch_products)} prodotti per import batch...")
        
        if manager.catalog_id:
            print("🚀 Avvio importazione batch...")
            results = manager.batch_add_products(batch_products, chunk_size=2)
            
            successful = sum(1 for r in results if r['success'])
            failed = sum(1 for r in results if not r['success'])
            
            print(f"✅ Batch completato: {successful}/{len(batch_products)} successi")
            
            if failed > 0:
                print(f"❌ Errori: {failed}")
                for result in results:
                    if not result['success']:
                        print(f"  - {result['retailer_id']}: {result['error']}")
        else:
            print("⚠️  Catalog ID non configurato - simulazione batch")
            for product in batch_products:
                validated = manager.validate_product_data(product)
                print(f"✅ Validato: {validated['name']}")
                
    except Exception as e:
        print(f"❌ Errore demo batch: {e}")
        logger.error(f"Errore demo batch: {e}")

def demo_error_handling(manager: WhatsAppCatalogManager):
    """Dimostra la gestione degli errori."""
    
    print("\n⚠️  Demo: Gestione Errori")
    print("-" * 24)
    
    # Test con dati non validi
    invalid_product = {
        "retailer_id": "",  # ID vuoto - errore
        "name": "A" * 200,  # Nome troppo lungo - errore
        "price": "prezzo non valido",  # Prezzo non numerico - errore
        "currency": "INVALID",  # Valuta non supportata - errore
    }
    
    try:
        print("🧪 Test validazione dati non validi...")
        manager.validate_product_data(invalid_product)
        print("❌ ERRORE: La validazione avrebbe dovuto fallire!")
        
    except ValueError as e:
        print("✅ Errori di validazione catturati correttamente:")
        error_lines = str(e).split('\\n')
        for line in error_lines[:3]:  # Mostra solo i primi 3 errori
            if line.strip():
                print(f"   - {line.strip()}")
        if len(error_lines) > 3:
            print(f"   ... e altri {len(error_lines) - 3} errori")
            
    except Exception as e:
        print(f"❌ Errore inaspettato: {e}")

def main():
    """Funzione principale per la demo completa."""
    
    print("🎯 WhatsApp Business Catalog Manager - Demo Completa")
    print("=" * 55)
    
    try:
        # Inizializza il manager
        manager = WhatsAppCatalogManager()
        print(f"✅ Manager inizializzato")
        print(f"🆔 Catalog ID: {manager.catalog_id or 'Non configurato'}")
        print(f"📱 Phone ID: {manager.phone_number_id or 'Non configurato'}")
        
        # Esegui tutte le demo
        demo_catalog_operations(manager)
        demo_product_lifecycle(manager)
        demo_messaging(manager)
        demo_batch_operations(manager)
        demo_error_handling(manager)
        
        print("\n🎉 Demo Completa Terminata!")
        print("\n📋 Riepilogo Funzionalità Dimostrate:")
        print("✅ Gestione informazioni catalogo")
        print("✅ CRUD operations sui prodotti")
        print("✅ Messaggistica WhatsApp")
        print("✅ Operazioni batch")
        print("✅ Validazione e gestione errori")
        
        print("\n🚀 Prossimi Passi:")
        print("1. Configura tutti i parametri nel file .env")
        print("2. Sostituisci i numeri di telefono di test con numeri reali")
        print("3. Personalizza i prodotti per il tuo business")
        print("4. Integra il manager nella tua applicazione")
        
    except Exception as e:
        print(f"❌ Errore durante la demo: {e}")
        logger.error(f"Errore nella demo completa: {e}")

if __name__ == "__main__":
    main()