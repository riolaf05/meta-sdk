# 🚀 Guida Rapida - WhatsApp Business Catalog

## ⚡ Avvio Veloce

1. **Configura il file `.env`:**
   ```
   META_ACCESS_TOKEN=il_tuo_token_meta
   CATALOG_ID=il_tuo_catalog_id
   WABA_ID=il_tuo_waba_id
   ```

2. **Attiva ambiente virtuale:**
   ```bash
   .venv\Scripts\activate
   ```

3. **Esegui demo:**
   ```bash
   python demo.py
   ```

## 📋 File Principali

- **`demo.py`** - Script demo unificato per aggiungere prodotti
- **`view_catalog.py`** - Visualizza prodotti esistenti nel catalogo
- **`README.md`** - Documentazione completa con istruzioni dettagliate

## 🔧 Dove Prendere i Valori di Configurazione

### META_ACCESS_TOKEN
1. Vai su https://developers.facebook.com/tools/explorer/
2. Seleziona la tua app Meta
3. Aggiungi permessi: `catalog_management`, `business_management`
4. Genera token

### CATALOG_ID e WABA_ID  
1. Vai su https://business.facebook.com/commerce/
2. Seleziona il tuo catalogo
3. L'ID è nell'URL: `/commerce/catalogs/{CATALOG_ID}`
4. WABA_ID si trova in WhatsApp Manager

## 🎯 Supporto Automatico

Il demo rileva automaticamente:
- **Commerce**: Prodotti generici (iPhone, abbigliamento, ecc.)
- **Real Estate**: Immobili (case, appartamenti con GPS)

## � Problemi Permessi?

Se ricevi errori tipo "Unsupported post request" o "missing permissions":

**➡️ Leggi [META_BUSINESS_SETUP.md](META_BUSINESS_SETUP.md)** per la configurazione completa di Meta Business Manager con Commerce API e risoluzione problemi di autorizzazione.

## �📞 Link Utili

- **Meta Commerce Manager**: https://business.facebook.com/commerce/
- **Meta for Developers**: https://developers.facebook.com/
- **WhatsApp Business API**: https://developers.facebook.com/docs/whatsapp/
- **Graph API Explorer**: https://developers.facebook.com/tools/explorer/

---

**Per istruzioni dettagliate**, consulta il file `README.md` completo.