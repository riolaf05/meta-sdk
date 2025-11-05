#!/usr/bin/env python3
"""
Esempio: Importazione batch di prodotti da file CSV/JSON.

Questo script dimostra come importare grandi quantità di prodotti
da file CSV o JSON nel catalogo WhatsApp Business.
"""

import sys
import json
import csv
from pathlib import Path
from typing import List, Dict, Any

# Aggiungi il percorso src al PYTHONPATH
sys.path.insert(0, str(Path(__file__).parent.parent / 'src'))

from src.whatsapp_catalog_manager import WhatsAppCatalogManager
from src.config import logger

def create_sample_csv_data() -> str:
    """
    Crea dati CSV di esempio e restituisce il contenuto.
    
    Returns:
        str: Contenuto CSV di esempio
    """
    csv_content = """retailer_id,name,description,price,currency,availability,condition,brand,category,image_url
BATCH_001,Smartphone XYZ Pro,"Smartphone di ultima generazione con fotocamera avanzata",899.99,EUR,in stock,new,TechBrand,Elettronica > Smartphone,https://example.com/phone1.jpg
BATCH_002,Laptop Gaming Ultra,"Laptop da gaming con GPU dedicata e processore potente",1599.00,EUR,in stock,new,GameTech,Elettronica > Computer,https://example.com/laptop1.jpg  
BATCH_003,Cuffie Wireless Premium,"Cuffie bluetooth con cancellazione del rumore attiva",299.99,EUR,limited stock,new,AudioPro,Elettronica > Audio,https://example.com/headphones1.jpg
BATCH_004,Smartwatch Fitness,"Orologio intelligente per il monitoraggio della salute",199.50,EUR,in stock,new,FitTech,Elettronica > Wearables,https://example.com/watch1.jpg
BATCH_005,Tablet Creativo,"Tablet per disegno digitale con penna stylus inclusa",649.00,EUR,out of stock,new,ArtTech,Elettronica > Tablet,https://example.com/tablet1.jpg"""
    
    return csv_content

def create_sample_json_data() -> List[Dict[str, Any]]:
    """
    Crea dati JSON di esempio per l'importazione.
    
    Returns:
        List[Dict]: Lista di prodotti in formato JSON
    """
    return [
        {
            "retailer_id": "JSON_001",
            "name": "Scarpe da Running Pro",
            "description": "Scarpe da corsa professionali con ammortizzazione avanzata e suola antiscivolo",
            "price": "129.99",
            "currency": "EUR",
            "availability": "in stock", 
            "condition": "new",
            "brand": "RunMax",
            "category": "Abbigliamento > Scarpe > Running",
            "size": "42",
            "color": "Nero/Rosso",
            "gender": "unisex",
            "image_url": "https://images.unsplash.com/photo-1542291026-7eec264c27ff?w=500"
        },
        {
            "retailer_id": "JSON_002",
            "name": "Zaino Outdoor Impermeabile",
            "description": "Zaino tecnico da 30L, impermeabile e resistente, perfetto per trekking e viaggi",
            "price": "89.90",
            "currency": "EUR",
            "availability": "in stock",
            "condition": "new", 
            "brand": "AdventurePack",
            "category": "Sport > Outdoor > Zaini",
            "color": "Verde Militare",
            "material": "Nylon ripstop",
            "image_url": "https://images.unsplash.com/photo-1553062407-98eeb64c6a62?w=500"
        },
        {
            "retailer_id": "JSON_003", 
            "name": "Macchina del Caffè Espresso",
            "description": "Macchina per caffè espresso professionale con macinacaffè integrato",
            "price": "459.00",
            "currency": "EUR",
            "availability": "in stock",
            "condition": "new",
            "brand": "CoffeeMax",
            "category": "Casa e Giardino > Elettrodomestici > Caffè",
            "color": "Acciaio inox",
            "image_url": "https://images.unsplash.com/photo-1495474472287-4d71bcdd2085?w=500"
        }
    ]

def parse_csv_data(csv_content: str) -> List[Dict[str, Any]]:
    """
    Parsa i dati CSV e restituisce una lista di prodotti.
    
    Args:
        csv_content: Contenuto del file CSV
        
    Returns:
        List[Dict]: Lista di prodotti
    """
    products = []
    
    # Parsing del CSV
    csv_reader = csv.DictReader(csv_content.strip().split('\\n'))
    
    for row in csv_reader:
        # Pulisci e valida i dati
        product = {k.strip(): v.strip() for k, v in row.items() if v.strip()}
        
        # Converti campi numerici se necessario
        if 'price' in product:
            try:
                # Assicura che il prezzo sia in formato numerico
                price_clean = product['price'].replace(',', '.')
                float(price_clean)  # Test di validità
                product['price'] = price_clean
            except ValueError:
                logger.warning(f"Prezzo non valido per prodotto {product.get('retailer_id', 'unknown')}: {product.get('price')}")
        
        products.append(product)
    
    return products

def import_from_csv(manager: WhatsAppCatalogManager, csv_content: str) -> Dict[str, Any]:
    """
    Importa prodotti da dati CSV.
    
    Args:
        manager: Instance del WhatsAppCatalogManager
        csv_content: Contenuto del file CSV
        
    Returns:
        Dict: Risultati dell'importazione
    """
    print("📄 Parsing dati CSV...")
    
    try:
        products = parse_csv_data(csv_content)
        print(f"✅ Trovati {len(products)} prodotti nel CSV")
        
        # Importazione batch
        print("📦 Avvio importazione batch...")
        results = manager.batch_add_products(products, chunk_size=10)
        
        # Analizza risultati
        successful = sum(1 for r in results if r['success'])
        failed = sum(1 for r in results if not r['success'])
        
        print(f"✅ Importazione completata: {successful}/{len(products)} prodotti importati")
        
        if failed > 0:
            print(f"❌ Errori: {failed}")
            print("🔍 Prodotti con errori:")
            for result in results:
                if not result['success']:
                    print(f"  - {result['retailer_id']}: {result['error']}")
        
        return {
            'total': len(products),
            'successful': successful,
            'failed': failed,
            'results': results
        }
        
    except Exception as e:
        logger.error(f"Errore nell'importazione CSV: {e}")
        raise

def import_from_json(manager: WhatsAppCatalogManager, json_data: List[Dict[str, Any]]) -> Dict[str, Any]:
    """
    Importa prodotti da dati JSON.
    
    Args:
        manager: Instance del WhatsAppCatalogManager
        json_data: Lista di prodotti in formato JSON
        
    Returns:
        Dict: Risultati dell'importazione
    """
    print("📄 Elaborazione dati JSON...")
    print(f"✅ Trovati {len(json_data)} prodotti nel JSON")
    
    try:
        # Importazione batch
        print("📦 Avvio importazione batch...")
        results = manager.batch_add_products(json_data, chunk_size=5)
        
        # Analizza risultati
        successful = sum(1 for r in results if r['success'])
        failed = sum(1 for r in results if not r['success'])
        
        print(f"✅ Importazione completata: {successful}/{len(json_data)} prodotti importati")
        
        if failed > 0:
            print(f"❌ Errori: {failed}")
            print("🔍 Prodotti con errori:")
            for result in results:
                if not result['success']:
                    print(f"  - {result['retailer_id']}: {result['error']}")
        
        return {
            'total': len(json_data),
            'successful': successful, 
            'failed': failed,
            'results': results
        }
        
    except Exception as e:
        logger.error(f"Errore nell'importazione JSON: {e}")
        raise

def save_sample_files():
    """Salva file di esempio per test."""
    
    # Salva CSV di esempio
    csv_content = create_sample_csv_data()
    csv_file = Path("sample_products.csv")
    
    with open(csv_file, 'w', encoding='utf-8') as f:
        f.write(csv_content)
    print(f"💾 File CSV di esempio salvato: {csv_file}")
    
    # Salva JSON di esempio
    json_data = create_sample_json_data()
    json_file = Path("sample_products.json")
    
    with open(json_file, 'w', encoding='utf-8') as f:
        json.dump(json_data, f, indent=2, ensure_ascii=False)
    print(f"💾 File JSON di esempio salvato: {json_file}")
    
    return csv_file, json_file

def main():
    """Funzione principale per l'importazione batch."""
    
    print("📦 Importazione Batch Prodotti WhatsApp Business")
    print("=" * 50)
    
    try:
        # Inizializza il manager
        manager = WhatsAppCatalogManager()
        print(f"✅ Manager inizializzato - Catalog ID: {manager.catalog_id or 'Non configurato'}")
        print()
        
        # Crea file di esempio
        print("📁 Creazione file di esempio...")
        csv_file, json_file = save_sample_files()
        print()
        
        # Test importazione CSV
        print("🔄 Test Importazione CSV")
        print("-" * 25)
        
        csv_content = create_sample_csv_data()
        
        if manager.catalog_id:
            csv_results = import_from_csv(manager, csv_content)
            print(f"📊 Risultati CSV: {csv_results['successful']}/{csv_results['total']} prodotti importati")
        else:
            print("⚠️  Catalog ID non configurato - simulazione importazione CSV")
            products = parse_csv_data(csv_content)
            print(f"✅ CSV parsing completato: {len(products)} prodotti validati")
        
        print()
        
        # Test importazione JSON
        print("🔄 Test Importazione JSON")
        print("-" * 26)
        
        json_data = create_sample_json_data()
        
        if manager.catalog_id:
            json_results = import_from_json(manager, json_data)
            print(f"📊 Risultati JSON: {json_results['successful']}/{json_results['total']} prodotti importati")
        else:
            print("⚠️  Catalog ID non configurato - simulazione importazione JSON")
            for product in json_data:
                validated = manager.validate_product_data(product)
                print(f"✅ Prodotto validato: {validated['name']}")
        
        print()
        print("🎉 Importazione batch completata!")
        print()
        print("💡 Come usare i tuoi file:")
        print("1. Prepara il tuo file CSV/JSON con i prodotti")
        print("2. Usa le funzioni import_from_csv() o import_from_json()")
        print("3. Monitora i risultati per eventuali errori")
        print("4. I prodotti saranno disponibili nel catalogo WhatsApp")
        
    except Exception as e:
        print(f"❌ Errore durante l'importazione batch: {e}")
        logger.error(f"Errore nell'esempio importazione batch: {e}")

if __name__ == "__main__":
    main()