# WhatsApp Business Catalog Manager

Una applicazione Python per interagire con Meta (Facebook) tramite SDK per gestire cataloghi WhatsApp Business. Questo progetto consente di aggiungere, modificare e gestire prodotti in cataloghi WhatsApp Business utilizzando le API di Meta.

## 📋 Prerequisiti

Prima di iniziare, assicurati di avere:

### 1. Account e Configurazioni Meta
- **WhatsApp Business Account (WABA)** registrato con Azure Communication Services
- **Facebook Business Manager Account** 
- **Meta App** configurata con i permessi necessari
- **Access Token** per l'API Graph di Meta
- **Phone Number ID** per WhatsApp Business

### 2. Ambiente di Sviluppo
- Python 3.8 o superiore
- pip (Python package manager)
- Git
- Account Azure (per Azure Communication Services)

### 3. Permessi API Necessari
La tua Meta App deve avere i seguenti permessi (vedi sezione "Impostazione Permessi dell'App Meta" per istruzioni dettagliate):

#### Permessi Obbligatori:
- `whatsapp_business_management` - Gestire il WhatsApp Business Account
- `whatsapp_business_messaging` - Inviare e ricevere messaggi WhatsApp
- `catalog_management` - Creare, modificare ed eliminare prodotti nel catalogo
- `business_management` - Accedere ai dati del business Meta

#### Permessi Utili (Opzionali):
- `pages_messaging` - Integrazioni con Facebook Pages
- `instagram_basic` - Integrazioni con Instagram Business

## 🚀 Installazione

### 1. Clona il Repository
```bash
git clone https://github.com/tuousername/meta-sdk.git
cd meta-sdk
```

### 2. Crea un Ambiente Virtuale
```bash
python -m venv .venv
```

### 3. Attiva l'Ambiente Virtuale

**Su Windows:**
```powershell
.venv\Scripts\Activate.ps1
```

**Su Linux/macOS:**
```bash
source .venv/bin/activate
```

### 4. Installa le Dipendenze
```bash
pip install -r requirements.txt
```

### 5. Configura le Variabili d'Ambiente
Copia il file `.env.example` in `.env` e compila con i tuoi valori:

```bash
cp .env.example .env
```

Modifica il file `.env` con i tuoi parametri:
```env
# Meta/Facebook Configuration
META_ACCESS_TOKEN=your_meta_access_token_here
META_APP_ID=your_app_id_here
META_APP_SECRET=your_app_secret_here
WHATSAPP_BUSINESS_ACCOUNT_ID=your_waba_id_here
PHONE_NUMBER_ID=your_phone_number_id_here

# Azure Communication Services (se utilizzato)
AZURE_COMMUNICATION_SERVICES_CONNECTION_STRING=your_connection_string_here
WHATSAPP_CHANNEL_ID=your_channel_id_here

# Catalog Configuration
CATALOG_ID=your_catalog_id_here

# Logging
LOG_LEVEL=INFO
```

## 🏗️ Struttura del Progetto

```
meta-sdk/
├── .venv/                    # Ambiente virtuale Python
├── src/                      # Codice sorgente principale
│   ├── __init__.py
│   ├── config.py            # Configurazioni e variabili d'ambiente
│   ├── meta_client.py       # Client per API Meta Graph
│   └── whatsapp_catalog_manager.py  # Manager per cataloghi WhatsApp
├── examples/                 # Esempi d'uso
│   ├── __init__.py
│   ├── add_product_example.py
│   ├── batch_import_example.py
│   └── manage_catalog_example.py
├── docs/                     # Documentazione
├── tests/                    # Test unitari (opzionale)
├── .env.example             # Template variabili d'ambiente
├── .gitignore              # File da ignorare in Git
├── requirements.txt        # Dipendenze Python
├── main.py                # Script principale
└── README.md              # Questo file
```

## 🔧 Configurazione Dettagliata

### 1. Come Ottenere META_ACCESS_TOKEN

Il Meta Access Token è essenziale per accedere alle API di Meta. Ecco come ottenerlo:

#### Metodo 1: Graph API Explorer (per test e sviluppo)
1. Vai su [Meta for Developers](https://developers.facebook.com/)
2. Accedi con il tuo account Facebook Business
3. Vai su **Strumenti** > **Graph API Explorer**
4. Nel menu a tendina **Meta App**, seleziona la tua app (o creane una nuova)
5. Nel menu **Permissions**, aggiungi i permessi necessari:
   - `whatsapp_business_management`
   - `whatsapp_business_messaging`
   - `catalog_management`
   - `business_management`
6. Clicca su **Generate Access Token**
7. Copia il token generato - questo è il tuo `META_ACCESS_TOKEN`

⚠️ **Nota**: I token dal Graph API Explorer scadono in 1-2 ore.

#### Metodo 2: Token di Lunga Durata (per produzione)
1. Ottieni prima un token temporaneo dal Graph API Explorer
2. Usa l'API per convertirlo in un token di lunga durata:
```bash
curl -i -X GET "https://graph.facebook.com/oauth/access_token?grant_type=fb_exchange_token&client_id={APP_ID}&client_secret={APP_SECRET}&fb_exchange_token={SHORT_TOKEN}"
```
3. Il token restituito dura 60 giorni

### 2. Come Ottenere META_APP_ID e META_APP_SECRET

#### Passo 1: Creare un'App Meta
1. Vai su [Meta for Developers](https://developers.facebook.com/)
2. Clicca su **Le mie app** > **Crea app**
3. Seleziona **Business** come tipo di app
4. Compila i dettagli dell'app:
   - **Nome app**: Es. "Il Mio Catalogo WhatsApp"
   - **Email di contatto**: La tua email aziendale
5. Clicca su **Crea app**

#### Passo 2: Ottenere APP_ID e APP_SECRET
1. Nella dashboard della tua app, vai su **Impostazioni** > **Di base**
2. Qui troverai:
   - **ID app**: Questo è il tuo `META_APP_ID`
   - **Chiave segreta dell'app**: Clicca su **Mostra** per vedere il `META_APP_SECRET`

#### Passo 3: Configurare i Permessi dell'App
1. Nella dashboard dell'app, vai su **Prodotti**
2. Aggiungi i seguenti prodotti:
   - **WhatsApp Business Platform**
   - **Facebook Login** (se necessario)
3. Per ogni prodotto, configura i permessi necessari

### 3. Come Ottenere WHATSAPP_BUSINESS_ACCOUNT_ID

#### Metodo 1: Tramite Business Manager
1. Vai su [Facebook Business Manager](https://business.facebook.com/)
2. Seleziona il tuo account business
3. Nel menu **Settings**, poi vai su **Account** > **WhatsApp Business Platform**
4. Seleziona il tuo WhatsApp Business Account
5. L'ID sarà visibile nell'URL o nelle informazioni dell'account

#### Metodo 2: Tramite Graph API Explorer
1. Nel [Graph API Explorer](https://developers.facebook.com/tools/explorer/)
2. Usa la query: `GET /me/businesses`
3. Trova il tuo business e annota l'`id`
4. Poi usa: `GET /{business-id}/whatsapp_business_accounts`
5. L'`id` restituito è il tuo `WHATSAPP_BUSINESS_ACCOUNT_ID`

### 4. Come Ottenere PHONE_NUMBER_ID

1. Nel [Graph API Explorer](https://developers.facebook.com/tools/explorer/)
2. Usa la query: `GET /{WHATSAPP_BUSINESS_ACCOUNT_ID}/phone_numbers`
3. Sostituisci `{WHATSAPP_BUSINESS_ACCOUNT_ID}` con il tuo WABA ID
4. Nella risposta, troverai un array di numeri di telefono
5. Copia l'`id` del numero che vuoi usare - questo è il tuo `PHONE_NUMBER_ID`

Esempio di risposta:
```json
{
  "data": [
    {
      "verified_name": "La Tua Azienda",
      "display_phone_number": "+39 123 456 7890",
      "id": "1234567890123456",  // <-- Questo è il PHONE_NUMBER_ID
      "quality_rating": "GREEN"
    }
  ]
}
```

### 5. Come Ottenere CATALOG_ID

#### Metodo 1: Tramite Commerce Manager
1. Vai su [Meta Commerce Manager](https://business.facebook.com/commerce/)
2. Se non hai un catalogo, clicca su **Crea catalogo**:
   - **Tipo di inventario**: Seleziona "E-commerce"
   - **Nome catalogo**: Es. "Catalogo WhatsApp"
   - Completa la configurazione
3. Una volta creato/selezionato il catalogo:
   - L'ID sarà visibile nell'URL: `commerce/catalogs/{CATALOG_ID}/`
   - Oppure nelle **Impostazioni del catalogo**

#### Metodo 2: Tramite Graph API
1. Nel [Graph API Explorer](https://developers.facebook.com/tools/explorer/)
2. Usa la query: `GET /{BUSINESS_ID}/owned_product_catalogs`
3. Sostituisci `{BUSINESS_ID}` con il tuo Business ID
4. L'`id` restituito è il tuo `CATALOG_ID`

#### Collegare il Catalogo a WhatsApp
1. Nel Commerce Manager, vai alle **Impostazioni del catalogo**
2. Nella sezione **Connessioni**, aggiungi il tuo WhatsApp Business Account
3. Conferma il collegamento

### 6. Impostazione Permessi dell'App Meta

Per funzionare correttamente, la tua app Meta deve avere i seguenti permessi:

#### Permessi Obbligatori:
- **whatsapp_business_management**: Gestire account WhatsApp Business
- **whatsapp_business_messaging**: Inviare messaggi WhatsApp
- **catalog_management**: Gestire cataloghi prodotti
- **business_management**: Accedere a dati del business

#### Permessi Opzionali (utili):
- **pages_messaging**: Messaggistica Facebook Pages
- **pages_manage_metadata**: Gestire metadati Pages
- **instagram_basic**: Accesso base Instagram

#### Come Richiedere i Permessi:
1. Nella dashboard della tua app Meta
2. Vai su **Revisione dell'app** > **Autorizzazioni e funzionalità**
3. Per ogni permesso necessario:
   - Clicca su **Richiedi**
   - Compila la documentazione richiesta
   - Spiega come userai il permesso
   - Fornisce screenshot/video se richiesti
4. Invia la richiesta per la revisione di Meta

⚠️ **Importante**: Alcuni permessi richiedono la revisione di Meta che può richiedere 7-14 giorni.

### 7. Configurare WhatsApp Business

#### Prerequisiti WhatsApp Business:
1. **Numero di Telefono**: Numero dedicato al business (non può essere usato su WhatsApp personale)
2. **Verifica Business**: Il tuo business deve essere verificato su Facebook
3. **Documentazione**: Potrebbe essere richiesta documentazione aziendale

#### Passi per la Configurazione:
1. Nel [Business Manager](https://business.facebook.com/), vai su **WhatsApp Business Platform**
2. Clicca su **Inizia** e segui il processo guidato
3. Verifica il numero di telefono
4. Completa il profilo business
5. Configura i webhook per ricevere messaggi (opzionale)

### 8. Test della Configurazione

Una volta ottenuti tutti i parametri, testa la configurazione:

```bash
# 1. Copia il file .env.example in .env
cp .env.example .env

# 2. Compila tutti i parametri nel file .env

# 3. Testa la configurazione
python main.py
```

Se tutto è configurato correttamente, dovresti vedere:
```
✅ Configurazione validata
📱 WABA ID: 123456789
📦 Catalog ID: 987654321
```

## 💻 Utilizzo

### Demo Unificata

1. **Attiva l'ambiente virtuale:**
   ```bash
   .venv\Scripts\activate
   ```

2. **Esegui la demo:**
   ```bash
   python demo.py
   ```

La demo rileva automaticamente il tipo di catalogo (commerce o real estate) e aggiunge i prodotti appropriati.

### Esempio di Output
```
🚀 WhatsApp Business Catalog Demo
=================================

🏷️  Tipo catalogo rilevato: home_listings

🏠 Aggiunta Home Listings al Catalogo Real Estate
================================================

🏠 Aggiungendo listing 1/2: Villa di Lusso a Roma Nord
   ✅ Aggiunto con successo!
   🆔 Listing ID: 123456789

🏠 Aggiungendo listing 2/2: Appartamento Moderno Milano Centro  
   ✅ Aggiunto con successo!
   🆔 Listing ID: 987654321

🎉 Aggiunti 2/2 listing real estate!

📊 Stato del Catalogo
======================
📦 Nome: real_estate
🆔 ID: 841572311756772
📊 Prodotti/Listing: 2
🏷️  Tipo: home_listings
🏢 Business: Weaving Tech

📋 Dove Visualizzare i Risultati:
1. 🌐 Meta Commerce Manager: https://business.facebook.com/commerce/
2. 📱 WhatsApp Business App → Impostazioni → Catalogo
3. 🔧 Graph API Explorer: https://developers.facebook.com/tools/explorer/
4. 🐍 Script Python: python view_catalog.py

🎉 Demo completata con successo!
```

### Script di Supporto

- `demo.py`: Demo unificata per aggiungere prodotti
- `view_catalog.py`: Visualizza prodotti esistenti nel catalogo

## 📚 Funzionalità Principali

### 🔍 Rilevamento Automatico
- **Tipo Catalogo**: Identifica automaticamente commerce vs real estate
- **Formato Dati**: Usa il formato corretto per ogni tipo di catalogo

### 📦 Gestione Prodotti
- **Commerce**: iPhone, abbigliamento, elettronica, ecc.
- **Real Estate**: Case, appartamenti, ville con coordinate GPS

### ✅ Operazioni Supportate
- ✅ Aggiungere prodotti/listing al catalogo
- ✅ Visualizzare cataloghi esistenti
- ✅ Validazione automatica dei dati
- ✅ Gestione errori con messaggi chiari
- ✅ Rate limiting per rispettare i limiti API

## 🔍 Dove Visualizzare i Prodotti

Dopo aver aggiunto prodotti al catalogo, puoi visualizzarli in diversi modi:

### 1. 🌐 Meta Commerce Manager (Raccomandato)
- **URL**: https://business.facebook.com/commerce/
- **Vantaggi**: Interfaccia completa, gestione prodotti, preview WhatsApp

### 2. 📱 WhatsApp Business App
- **Percorso**: Impostazioni → Strumenti Business → Catalogo
- **Vantaggi**: Visualizzazione mobile, test esperienza cliente

### 3. 🔧 Graph API Explorer
- **URL**: https://developers.facebook.com/tools/explorer/
- **Vantaggi**: Accesso diretto API, debugging avanzato

### 4. 🐍 Script Python
```python
python view_catalog.py        # Visualizza prodotti
python view_catalog.py info   # Info catalogo

result = manager.update_product("SKU_12345", updated_data)
print(f"Prodotto aggiornato: {result}")
```

### 3. Inviare un Messaggio Prodotto

```python
# Invia un prodotto specifico via WhatsApp
manager.send_product_message(
    phone_number="+39123456789",
    product_retailer_id="SKU_12345",
    message="Guarda questo fantastico iPhone 15 Pro!"
)
```

## 🛠️ Risoluzione Problemi

### Errori Comuni

#### 1. **Token di Accesso Scaduto**
```
Error: (#190) Error validating access token
```
**Soluzione:** Genera un nuovo access token da Meta for Developers.

#### 2. **Permessi Insufficienti**
```
Error: (#200) Requires business_management permission
```
**Soluzione:** Assicurati che la tua app abbia tutti i permessi necessari.

#### 3. **Catalog ID Non Valido**
```
Error: (#100) Invalid catalog ID
```
**Soluzione:** Verifica che il CATALOG_ID nel file `.env` sia corretto.

#### 4. **Formato Prodotto Non Valido**
```
Error: Product data validation failed
```
**Soluzione:** Controlla che tutti i campi obbligatori siano presenti e nel formato corretto.

### Debug e Logging

Il sistema di logging è configurato per aiutarti nel debug:

```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

I log includono:
- Richieste API complete
- Risposte del server
- Errori dettagliati
- Timing delle operazioni

## 📖 Documentazione API

### Campi Prodotto Supportati

#### Obbligatori:
- `retailer_id`: ID univoco del prodotto (stringa)
- `name`: Nome del prodotto (stringa, max 150 caratteri)
- `description`: Descrizione (stringa, max 9999 caratteri)
- `price`: Prezzo (stringa, formato: "XX.XX EUR")
- `currency`: Valuta (stringa, es: "EUR", "USD")
- `availability`: Disponibilità ("in stock", "out of stock", "preorder")
- `condition`: Condizione ("new", "refurbished", "used")

#### Opzionali:
- `brand`: Brand del prodotto
- `category`: Categoria (es: "Elettronica > Smartphone")
- `image_url`: URL dell'immagine principale
- `additional_image_urls`: Array di URL immagini aggiuntive
- `url`: URL della pagina prodotto
- `size`: Taglia (per abbigliamento)
- `color`: Colore
- `material`: Materiale
- `pattern`: Pattern/motivo
- `gender`: Genere target ("male", "female", "unisex")
- `age_group`: Gruppo età ("adult", "kids", "infant")

### Metodi Principali

#### `WhatsAppCatalogManager`

```python
# Inizializzazione
manager = WhatsAppCatalogManager(
    access_token="your_token",  # Opzionale se in .env
    catalog_id="your_catalog_id"  # Opzionale se in .env
)

# Gestione prodotti
add_product(product_data: dict) -> dict
update_product(retailer_id: str, updated_data: dict) -> dict
delete_product(retailer_id: str) -> bool
get_product(retailer_id: str) -> dict
list_products(limit: int = 100) -> list

# Gestione catalogo
get_catalog_info() -> dict
create_catalog(name: str, vertical: str = "commerce") -> dict

# Messaggistica
send_product_message(phone_number: str, product_retailer_id: str, message: str = "") -> dict
send_catalog_message(phone_number: str, body_text: str = "Guarda il nostro catalogo!") -> dict
```

## 🧪 Testing

Per eseguire i test (se implementati):

```bash
# Test unitari
python -m pytest tests/

# Test con coverage
python -m pytest tests/ --cov=src/

# Test di un singolo modulo
python -m pytest tests/test_whatsapp_catalog_manager.py -v
```

## 📈 Performance e Limiti

### Rate Limits Meta API
- **Graph API:** 200 chiamate per ora per utente
- **WhatsApp Business API:** 1000 messaggi al giorno (versione gratuita)
- **Catalog API:** 100 prodotti per chiamata batch

### Best Practices
1. **Batch Operations:** Usa le operazioni batch per più prodotti
2. **Caching:** Implementa caching per dati frequentemente richiesti
3. **Retry Logic:** Gestisci gli errori temporanei con retry automatico
4. **Monitoring:** Monitora usage e performance delle API

## 🤝 Contribuire

1. Fork del repository
2. Crea un branch per la tua feature (`git checkout -b feature/AmazingFeature`)
3. Commit delle modifiche (`git commit -m 'Add some AmazingFeature'`)
4. Push del branch (`git push origin feature/AmazingFeature`)
5. Apri una Pull Request

## 📄 Licenza

Questo progetto è sotto licenza MIT. Vedi il file `LICENSE` per dettagli.

## 🆘 Supporto

- **Documentazione Meta:** [WhatsApp Business Platform](https://developers.facebook.com/docs/whatsapp/)
- **Graph API Reference:** [Meta Graph API](https://developers.facebook.com/docs/graph-api/)
- **Issues:** Apri un issue su GitHub per bug o richieste di feature
- **Discussions:** Usa GitHub Discussions per domande generali

## 🔗 Link Utili

- [Meta for Developers](https://developers.facebook.com/)
- [WhatsApp Business API Docs](https://developers.facebook.com/docs/whatsapp/cloud-api/)
- [Meta Commerce Manager](https://business.facebook.com/commerce/)
- [Graph API Explorer](https://developers.facebook.com/tools/explorer/)
- [Azure Communication Services](https://azure.microsoft.com/services/communication-services/)

---

**Nota:** Questo progetto non è affiliato ufficialmente con Meta/Facebook. È un'implementazione di terze parti che utilizza le API pubbliche di Meta.