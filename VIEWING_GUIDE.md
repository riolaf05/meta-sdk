# 📦 Guida: Dove Visualizzare i Prodotti del Catalogo WhatsApp Business

## 🎯 Opzioni di Visualizzazione

### 1. 🌐 Meta Commerce Manager (Raccomandato)
**URL:** https://business.facebook.com/commerce/

**Come accedere:**
1. Vai su https://business.facebook.com/commerce/
2. Accedi con il tuo account Facebook Business
3. Seleziona il tuo Business Manager
4. Clicca su "Cataloghi" nel menu laterale
5. Trova il catalogo "real_estate" (ID: 841572311756772)
6. Clicca sul catalogo per vedere tutti i prodotti

**Vantaggi:**
- ✅ Interfaccia grafica completa
- ✅ Gestione completa dei prodotti (aggiungi, modifica, elimina)
- ✅ Preview di come appariranno su WhatsApp
- ✅ Statistiche e analytics
- ✅ Gestione delle immagini e media

### 2. 📱 WhatsApp Business App
**Come accedere:**
1. Apri WhatsApp Business sul tuo telefono
2. Vai su Impostazioni → Strumenti Business → Catalogo
3. Visualizza i prodotti aggiunti
4. Condividi i prodotti nelle chat

**Vantaggi:**
- ✅ Visualizzazione mobile nativa
- ✅ Test diretto dell'esperienza cliente
- ✅ Condivisione immediata con i clienti

### 3. 🔧 Meta Graph API Explorer
**URL:** https://developers.facebook.com/tools/explorer/

**Come usarlo:**
1. Vai su https://developers.facebook.com/tools/explorer/
2. Seleziona la tua app Meta
3. Inserisci l'Access Token
4. Usa questa query per vedere i prodotti:
   ```
   GET /{catalog-id}/products?fields=id,name,retailer_id,price,currency,description,image_url
   ```
5. Sostituisci `{catalog-id}` con: `841572311756772`

**Vantaggi:**
- ✅ Accesso diretto all'API
- ✅ Dati JSON completi
- ✅ Test delle chiamate API
- ✅ Debug avanzato

### 4. 🐍 Script Python (Nostro)
**Come usarlo:**
```bash
# Attiva l'ambiente virtuale
.venv\Scripts\activate

# Visualizza i prodotti
python view_catalog.py

# Visualizza info catalogo
python view_catalog.py info
```

**Vantaggi:**
- ✅ Integrazione con il nostro codice
- ✅ Formattazione personalizzata
- ✅ Debugging dettagliato
- ✅ Automazione possibile

## 🚀 Per Aggiungere Prodotti Reali

### Opzione A: Script Python
```bash
# Aggiungi i prodotti immobiliari di esempio
python add_products.py
```

### Opzione B: Commerce Manager
1. Vai su https://business.facebook.com/commerce/
2. Seleziona il catalogo "real_estate"
3. Clicca "Aggiungi prodotti"
4. Compila i campi richiesti
5. Carica le immagini
6. Salva

### Opzione C: API diretta
Usa il nostro `WhatsAppCatalogManager` con `validation_only=False`:

```python
from src.whatsapp_catalog_manager import WhatsAppCatalogManager

manager = WhatsAppCatalogManager()
result = manager.add_product(product_data, validation_only=False)
```

## ⚠️ Note Importanti

### 🔑 Access Token
- Il token Meta può scadere
- Per rinnovarlo: Meta for Developers → App → Tokens
- I token di sviluppo durano 1-2 ore
- Per produzione usa i token a lungo termine

### ⏰ Sincronizzazione
- I prodotti possono richiedere 5-15 minuti per apparire
- La cache di Meta può causare ritardi
- Usa F5 per aggiornare nelle interfacce web

### 🔍 Troubleshooting

**Prodotti non visibili:**
1. Controlla che il Catalog ID sia corretto: `841572311756772`
2. Verifica l'Access Token (non scaduto)
3. Assicurati che `validation_only=False` negli script
4. Controlla i permessi dell'app Meta

**Errore 401 (Unauthorized):**
1. Rinnova l'Access Token
2. Verifica i permessi dell'app:
   - `catalog_management`
   - `business_management`

**Errore 400 (Bad Request):**
1. Controlla il formato dei dati del prodotto
2. Verifica che i campi obbligatori siano presenti
3. Controlla il formato del prezzo (deve essere in centesimi)

## 📞 Link Utili

- **Meta for Developers:** https://developers.facebook.com/
- **WhatsApp Business API Docs:** https://developers.facebook.com/docs/whatsapp/
- **Catalog Management API:** https://developers.facebook.com/docs/marketing-api/catalog/
- **Graph API Explorer:** https://developers.facebook.com/tools/explorer/
- **Business Manager:** https://business.facebook.com/

## 🎯 Prossimi Passi

1. **Testa l'aggiunta prodotti:** `python add_products.py`
2. **Verifica su Commerce Manager:** Controlla che i prodotti appaiano
3. **Testa su WhatsApp:** Prova a condividere i prodotti nelle chat
4. **Implementa l'automazione:** Usa le nostre classi per integrare con il tuo sistema

---

**Catalogo Corrente:**
- 📦 Nome: real_estate
- 🆔 ID: 841572311756772  
- 🏢 Business: Weaving Tech
- 🏷️ Vertical: home_listings