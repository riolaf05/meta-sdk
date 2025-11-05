# Configurazione Meta Business Manager e Risoluzione Problemi Permessi

## Panoramica
Questa guida spiega come configurare correttamente Meta Business Manager, creare un'app Facebook con i permessi appropriati e risolvere i problemi di autorizzazione per l'utilizzo del Catalog API di WhatsApp Business.

## Problema Comune
Se ricevi errori come:
- `"Unsupported post request. Object with ID 'XXXXXXX' does not exist"`
- `"missing permissions"`
- `"Invalid access token"`

Significa che la tua app Facebook non è configurata correttamente con i permessi necessari per gestire i cataloghi.

## 🚀 Passaggi per la Configurazione Completa

### 1. Crea/Configura Meta Business Account

1. **Vai a [Meta Business Suite](https://business.facebook.com/)**
2. **Crea un nuovo account business** se non ne hai uno:
   - Nome azienda: Il nome che i clienti vedranno
   - Sito web: Un sito web valido che verifichi la tua attività
   - Email aziendale: Email associata al tuo account Facebook
   - Numero di telefono aziendale: Per contatti clienti

3. **Completa la verifica aziendale** (consigliata ma non obbligatoria):
   - Va su **Impostazioni Business** → **Verifica Business**
   - Carica i documenti richiesti (licenza commerciale, etc.)

## 🚀 Parte 1: Creare un'App Meta e un Utente di Sistema

### Passo 1: Crea un Account Sviluppatore Meta
1. **Se non lo hai ancora fatto**: Vai su [developers.facebook.com](https://developers.facebook.com) e registrati come sviluppatore

### Passo 2: Crea una Nuova App
1. **Nella dashboard degli sviluppatori**: Clicca su **"Crea App"** (Create App)
2. **Scegli il tipo**: Seleziona **"Business"** (o "Other" → "Business")
3. **Configura l'app**: Segui i passaggi per nominarla e collegarla al tuo Business Manager

### Passo 3: Aggiungi la Marketing API all'App
1. **Nella dashboard dell'app**: Nel menu a sinistra, clicca su **"Aggiungi Prodotto"** (Add Product)
2. **Trova Marketing API**: Cerca "Marketing API" (o simile, a seconda degli aggiornamenti UI di Meta) e aggiungila
3. **Configura per Catalogo**: Durante la configurazione, seleziona il use case per gestione catalogo

### Passo 4: Crea un Utente di Sistema nel Business Manager
1. **Vai su Business Settings**: Accedi a [business.facebook.com/settings](https://business.facebook.com/settings)
2. **Naviga agli Utenti di Sistema**: Nel menu a sinistra, sotto "Account" o "Utenti", seleziona **"Utenti di Sistema"** (System Users)
3. **Crea Utente**: Clicca su **"Aggiungi Utente di Sistema"** (+ Add)
4. **Configura Utente**:
   - Inserisci un nome per l'utente (es. "Catalog Manager System User")
   - Seleziona il **Ruolo Admin** (consigliato per controllo completo, ma valuta le tue esigenze di sicurezza)

## 🔐 Parte 2: Assegnare i Permessi (Assets) e Generare il Token

### Passo 5: Assegna l'App all'Utente di Sistema
1. **Seleziona l'Utente**: Rimani nella sezione "Utenti di Sistema" e seleziona l'utente appena creato
2. **Aggiungi App**: Clicca su **"Aggiungi Risorse"** (Add Assets) o "Assign Assets"
3. **Configura App**:
   - Nella finestra che appare, seleziona **"App"** come tipo di risorsa
   - Scegli l'app che hai creato al Passo 2
   - Abilita **"Controllo Completo"** (Full Control) o almeno **"Manage app"**
   - Clicca su **"Salva modifiche"**

### Passo 6: Assegna il Catalogo all'Utente di Sistema
1. **Aggiungi Catalogo**: Sempre con l'utente selezionato, clicca nuovamente su **"Aggiungi Risorse"**
2. **Configura Catalogo**:
   - Seleziona **"Cataloghi"** (Catalogs) come tipo di risorsa
   - Scegli il catalogo prodotti specifico che vuoi gestire
   - Assegna **"Manage catalog"** o permessi pertinenti
   - Salva le modifiche

### Passo 7: Genera il Token di Accesso
1. **Inizia Generazione**: Seleziona l'utente di sistema e clicca su **"Genera Nuovo Token"** (Generate New Token)
2. **Seleziona App**: Scegli l'app associata
3. **Seleziona Autorizzazioni**: Abilita le seguenti autorizzazioni (Permissions/Scopes):
   - ✅ `catalog_management` (OBBLIGATORIO per gestione catalogo)
   - ✅ `business_management` (OBBLIGATORIO per Business Portfolio)
   - ✅ `ads_management` (se usi advertising)
   - ✅ `whatsapp_business_management` (se usi WhatsApp)
   - ✅ `whatsapp_business_messaging` (se usi WhatsApp)
4. **Genera e Salva**: 
   - Clicca su **"Genera Token"**
   - ⚠️ **IMPORTANTE**: Copia immediatamente il token generato
   - **Non potrai più visualizzarlo** una volta chiusa la finestra!

## ⚙️ Configurazione Finale

### Passo 8: Verifica Accesso Business Asset

1. **Per WhatsApp Business Account** (se applicabile):
   - Va a **Account** → **Account WhatsApp**
   - Seleziona il tuo WABA
   - Tab **"Accesso Account WhatsApp"**
   - Aggiungi l'utente sistema con permessi **"Completi"**

2. **Per Catalogo**:
   - Va a **Account** → **Cataloghi**
   - Seleziona il tuo catalogo
   - Tab **"Accesso Catalogo"**
   - Verifica che l'utente sistema abbia permessi **"Gestione"**

### Passo 9: Aggiorna Configurazione App

Modifica il file `.env` con i nuovi valori:

```bash
# SOSTITUISCI CON I TUOI VALORI CORRETTI
META_ACCESS_TOKEN="IL_TOKEN_GENERATO_DALL_UTENTE_SISTEMA"
META_CATALOG_ID="IL_TUO_CATALOG_ID"
META_BUSINESS_ID="IL_TUO_BUSINESS_ID"
META_APP_ID="IL_TUO_APP_ID"
META_APP_SECRET="IL_TUO_APP_SECRET"

# OPZIONALI (se usi WhatsApp)
WHATSAPP_BUSINESS_ACCOUNT_ID="IL_TUO_WABA_ID"
WHATSAPP_PHONE_NUMBER_ID="IL_TUO_PHONE_NUMBER_ID"
```

### 7. Test della Configurazione

Testa la configurazione con:

```bash
python demo.py
```

Se tutto è configurato correttamente, dovresti vedere:
- ✅ Connessione al catalogo riuscita
- ✅ Tipo di catalogo rilevato
- ✅ Prodotti aggiunti con successo

## 🔧 Risoluzione Problemi Comuni

### Errore: "Unsupported post request"
- **Causa**: App non connessa al Business Portfolio o permessi mancanti
- **Soluzione**: Verifica che l'app sia aggiunta al Business Portfolio con permessi completi

### Errore: "Invalid access token" 
- **Causa**: Token scaduto o generato senza permessi corretti
- **Soluzione**: Rigenera il token dall'utente sistema con tutti i permessi necessari

### Errore: "Object does not exist"
- **Causa**: L'utente sistema non ha accesso al catalogo/WABA
- **Soluzione**: Assegna l'accesso Business Asset all'utente sistema

### Errore: "Insufficient permissions"
- **Causa**: App non ha i permessi `catalog_management` o `business_management`
- **Soluzione**: Richiedi i permessi tramite App Review

### Limiti di Rate
- **Cataloghi**: 200 chiamate/ora per app per catalogo (5000 per cataloghi attivi)
- **WhatsApp**: Vari limiti in base al tipo di endpoint
- **Soluzione**: Implementa retry logic e rispetta gli header delle rate limit

## 📚 Link Utili

- [Facebook App Dashboard](https://developers.facebook.com/apps/)
- [Meta Business Suite](https://business.facebook.com/)
- [Meta Business Settings](https://business.facebook.com/settings/)
- [WhatsApp Manager](https://business.facebook.com/wa/manage/home/)
- [Catalog API Documentation](https://developers.facebook.com/docs/marketing-api/catalog)
- [WhatsApp Business Platform](https://developers.facebook.com/docs/whatsapp)

## ⚠️ Note Importanti

1. **Business Verification**: Non è obbligatoria per iniziare, ma è consigliata per scalare
2. **App Review**: Richiesto per alcuni permessi avanzati, ma `catalog_management` è solitamente disponibile immediatamente
3. **Token Security**: Non condividere mai i tuoi access token e rigenerarli periodicamente
4. **Rate Limiting**: Implementa sempre la gestione delle rate limit nelle tue app di produzione

## 🆘 Supporto

Se continui ad avere problemi:
1. Verifica che tutti i passaggi siano stati seguiti correttamente
2. Controlla i log dell'app in Facebook Developers
3. Crea un ticket di supporto Meta Business se necessario
4. Consulta la [Developer Community](https://www.facebook.com/groups/fbdevelopers/)