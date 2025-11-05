#!/usr/bin/env python3
"""
Esempio: Aggiunta di singoli prodotti al catalogo WhatsApp Business.

Questo script dimostra come aggiungere diversi tipi di prodotti al catalogo,
inclusi elettronica, abbigliamento, casa e giardino.
"""

import sys
from pathlib import Path

# Aggiungi il percorso src al PYTHONPATH
sys.path.insert(0, str(Path(__file__).parent.parent / 'src'))

from src.whatsapp_catalog_manager import WhatsAppCatalogManager
from src.config import logger

def create_electronics_product():
    """Crea un prodotto di elettronica - Smartphone."""
    return {
        "retailer_id": "ELEC_SAMSUNG_S24_001",
        "name": "Samsung Galaxy S24 Ultra",
        "description": "Smartphone flagship Samsung con display Dynamic AMOLED 6.8\", fotocamera da 200MP, processore Snapdragon 8 Gen 3 e S Pen integrata. Perfetto per professionisti e creativi.",
        "price": "1299.00",
        "currency": "EUR",
        "availability": "in stock",
        "condition": "new",
        "brand": "Samsung",
        "category": "Elettronica > Smartphone > Android",
        "image_url": "https://images.samsung.com/is/image/samsung/p6pim/it/2401/gallery/it-galaxy-s24-s928-sm-s928bzwdeue-thumb-539573547",
        "url": "https://www.samsung.com/it/smartphones/galaxy-s24/",
        "additional_image_urls": [
            "https://images.samsung.com/is/image/samsung/p6pim/it/2401/gallery/it-galaxy-s24-s928-sm-s928bzwdeue-thumb-539573548",
            "https://images.samsung.com/is/image/samsung/p6pim/it/2401/gallery/it-galaxy-s24-s928-sm-s928bzwdeue-thumb-539573549"
        ]
    }

def create_fashion_product():
    """Crea un prodotto di abbigliamento - Giacca."""
    return {
        "retailer_id": "FASH_JACKET_WINTER_002", 
        "name": "Giacca Invernale Impermeabile",
        "description": "Giacca tecnica invernale con imbottitura in piuma d'oca, tessuto impermeabile e traspirante. Ideale per attività all'aperto e uso quotidiano durante l'inverno.",
        "price": "159.99",
        "currency": "EUR",
        "availability": "in stock",
        "condition": "new",
        "brand": "OutdoorPro",
        "category": "Abbigliamento > Giacche > Invernali",
        "size": "L",
        "color": "Nero",
        "material": "Nylon ripstop, Piuma d'oca",
        "gender": "unisex",
        "age_group": "adult",
        "image_url": "https://images.unsplash.com/photo-1578662996442-48f60103fc96?w=500&q=80"
    }

def create_home_product():
    """Crea un prodotto per la casa - Lampada."""
    return {
        "retailer_id": "HOME_LAMP_LED_003",
        "name": "Lampada da Tavolo Smart LED",
        "description": "Lampada da tavolo intelligente con controllo RGB, dimmer regolabile, compatibile con Alexa e Google Home. Design moderno perfetto per ufficio o casa.",
        "price": "79.90",
        "currency": "EUR", 
        "availability": "limited stock",
        "condition": "new",
        "brand": "SmartHome",
        "category": "Casa e Giardino > Illuminazione > Lampade da Tavolo",
        "color": "Bianco",
        "material": "Metallo, Plastica",
        "image_url": "https://images.unsplash.com/photo-1507473885765-e6ed057f782c?w=500&q=80"
    }

def create_book_product():
    """Crea un prodotto libro - Manuale tecnico."""
    return {
        "retailer_id": "BOOK_PYTHON_GUIDE_004",
        "name": "Python per WhatsApp Business - Guida Completa",
        "description": "Manuale completo per sviluppatori che vogliono integrare WhatsApp Business nelle loro applicazioni. Include esempi pratici, API reference e best practices.",
        "price": "34.99",
        "currency": "EUR",
        "availability": "in stock", 
        "condition": "new",
        "brand": "TechBooks",
        "category": "Libri > Informatica > Programmazione",
        "image_url": "https://images.unsplash.com/photo-1544716278-ca5e3f4abd8c?w=500&q=80"
    }

def create_food_product():
    """Crea un prodotto alimentare - Caffè."""
    return {
        "retailer_id": "FOOD_COFFEE_ARABICA_005",
        "name": "Caffè Arabica Premium - Torrefazione Artigianale",
        "description": "Blend premium di caffè Arabica 100%, tostato artigianalmente. Note di cioccolato e caramello, perfetto per espresso e moka. Confezione da 1kg.",
        "price": "28.50",
        "currency": "EUR",
        "availability": "in stock",
        "condition": "new", 
        "brand": "CaffèArtigiano",
        "category": "Alimentari > Bevande > Caffè",
        "image_url": "https://images.unsplash.com/photo-1559056199-641a0ac8b55e?w=500&q=80"
    }

def create_beauty_product():
    """Crea un prodotto di bellezza - Crema viso."""
    return {
        "retailer_id": "BEAUTY_FACE_CREAM_006",
        "name": "Crema Viso Idratante Anti-Età",
        "description": "Crema viso premium con acido ialuronico, vitamina C e retinolo. Idrata profondamente e riduce i segni dell'invecchiamento. Adatta a tutti i tipi di pelle.",
        "price": "45.00",
        "currency": "EUR",
        "availability": "in stock",
        "condition": "new",
        "brand": "BeautyLux",
        "category": "Bellezza > Cura del Viso > Creme",
        "gender": "unisex",
        "image_url": "https://images.unsplash.com/photo-1556228720-195a672e8a03?w=500&q=80"
    }

def main():
    """Funzione principale per aggiungere esempi di prodotti."""
    
    print("🛍️  Esempi di Aggiunta Prodotti al Catalogo WhatsApp")
    print("=" * 55)
    
    try:
        # Inizializza il manager
        manager = WhatsAppCatalogManager()
        print(f"✅ Manager inizializzato - Catalog ID: {manager.catalog_id}")
        print()
        
        # Lista di prodotti di esempio
        products = [
            ("📱 Elettronica", create_electronics_product()),
            ("👕 Abbigliamento", create_fashion_product()),
            ("🏠 Casa e Giardino", create_home_product()),
            ("📚 Libri", create_book_product()),
            ("☕ Alimentari", create_food_product()),
            ("💄 Bellezza", create_beauty_product())
        ]
        
        successful_additions = 0
        failed_additions = 0
        
        for category, product_data in products:
            print(f"{category}: {product_data['name']}")
            print(f"💰 Prezzo: {product_data['price']} {product_data['currency']}")
            print(f"🏷️  SKU: {product_data['retailer_id']}")
            
            try:
                if manager.catalog_id:
                    # Aggiunta reale al catalogo
                    result = manager.add_product(product_data)
                    print(f"✅ Aggiunto con successo! ID: {result.get('id', 'N/A')}")
                    successful_additions += 1
                else:
                    # Solo validazione se non abbiamo catalog_id
                    validated_data = manager.validate_product_data(product_data)
                    print("✅ Dati validati correttamente (simulazione)")
                    successful_additions += 1
                    
            except Exception as e:
                print(f"❌ Errore: {e}")
                failed_additions += 1
                logger.error(f"Errore nell'aggiunta del prodotto {product_data['retailer_id']}: {e}")
            
            print("-" * 40)
        
        # Riepilogo
        print(f"📊 Riepilogo:")
        print(f"✅ Prodotti aggiunti con successo: {successful_additions}")
        print(f"❌ Errori: {failed_additions}")
        print(f"📦 Totale prodotti processati: {len(products)}")
        
        if manager.catalog_id and successful_additions > 0:
            print()
            print("🎉 I prodotti sono ora disponibili nel tuo catalogo WhatsApp!")
            print("📱 Puoi inviarli ai clienti tramite WhatsApp Business")
            
            # Esempio di invio messaggio
            print()
            print("💡 Esempio invio messaggio prodotto:")
            print(f"   manager.send_product_message('+391234567890', '{products[0][1]['retailer_id']}')")
        
    except Exception as e:
        print(f"❌ Errore durante l'esecuzione: {e}")
        logger.error(f"Errore nell'esempio aggiunta prodotti: {e}")

if __name__ == "__main__":
    main()