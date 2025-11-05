# Meta WhatsApp Catalog API Gateway - Cloud Infrastructure

Questa cartella contiene l'infrastruttura AWS per esporre un API Gateway che permette di aggiungere prodotti al catalogo Meta WhatsApp Business tramite chiamate HTTP autenticate.

## 🏗️ Architettura

```
Internet → API Gateway (+ API Key) → Lambda Function → Meta Graph API
```

### Componenti:
- **API Gateway**: Espone endpoint REST con autenticazione tramite `x-api-key`
- **Lambda Function**: Contiene la logica per aggiungere prodotti/listing ai cataloghi Meta
- **CloudWatch**: Log e monitoring delle chiamate
- **IAM**: Ruoli e permessi per Lambda

## 📋 Prerequisiti

1. **AWS CLI** configurato con credenziali appropriate
2. **Terraform** >= 1.0 installato
3. **Account Meta Business** configurato (vedi `../META_BUSINESS_SETUP.md`)
4. **Credenziali Meta** valide (Access Token, Catalog ID, etc.)

### Permessi AWS Richiesti

Il tuo utente/ruolo AWS deve avere i seguenti permessi:
- `lambda:*`
- `apigateway:*`
- `iam:*`
- `logs:*`
- `cloudwatch:*`

## 🚀 Setup e Deployment

### Passo 1: Configurazione Variabili

1. **Copia il file delle variabili**:
   ```bash
   cd cloud
   cp terraform.tfvars.example terraform.tfvars
   ```

2. **Modifica `terraform.tfvars`** con i tuoi valori:
   ```hcl
   # AWS
   aws_region = "eu-west-1"
   
   # Project
   project_name = "meta-catalog-api"
   resource_prefix = "real-estate"  # Prefisso per tutte le risorse
   
   # API Key (genera una chiave sicura)
   api_key_value = "tua-api-key-sicura-qui"
   
   # Meta Configuration (dai tuoi file .env)
   meta_access_token = "EAAG...your_token"
   meta_catalog_id   = "841572311756772"
   meta_business_id  = "your_business_id"
   meta_app_id       = "your_app_id"
   meta_app_secret   = "your_app_secret"
   ```

### Passo 2: Deploy Infrastructure

1. **Inizializza Terraform**:
   ```bash
   terraform init
   ```

2. **Pianifica il deployment**:
   ```bash
   terraform plan
   ```

3. **Applica le modifiche**:
   ```bash
   terraform apply
   ```

4. **Salva gli output**:
   ```bash
   terraform output
   ```

### Passo 3: Verifica Deploy

Dopo il deployment, otterrai:
- **API Gateway URL**: `https://xxxxxxxxx.execute-api.eu-west-1.amazonaws.com/prod/catalog`
- **API Key ID**: Per monitoring
- **Lambda Function Name**: `real-estate-meta-catalog-api-function`

## 📡 Utilizzo API

### Endpoint

```
POST https://YOUR_API_GATEWAY_URL/catalog
```

### Headers Richiesti

```
Content-Type: application/json
x-api-key: YOUR_API_KEY
```

### Payload per Home Listings

```json
{
  "type": "home_listing",
  "data": {
    "home_listing_id": "VILLA_001",
    "name": "Villa di Lusso",
    "description": "Splendida villa con giardino",
    "price": 850000,
    "currency": "EUR",
    "url": "https://example.com/villa-001",
    "images": [
      {"image_url": "https://picsum.photos/800/600?random=1"}
    ],
    "address": {
      "street_address": "Via Roma, 1",
      "city": "Roma",
      "region": "Lazio",
      "country": "IT",
      "postal_code": "00100",
      "latitude": 41.9028,
      "longitude": 12.4964
    },
    "availability": "for_sale",
    "year_built": 2020
  }
}
```

### Payload per Commerce Products

```json
{
  "type": "commerce_product",
  "data": {
    "retailer_id": "PRODUCT_001",
    "name": "iPhone 15 Pro",
    "description": "Latest iPhone model",
    "price": 139900,
    "currency": "EUR",
    "availability": "in stock",
    "condition": "new",
    "brand": "Apple",
    "category": "Electronics",
    "image_url": "https://picsum.photos/800/600?random=2",
    "url": "https://example.com/iphone-15-pro"
  }
}
```

## 🧪 Esempi cURL

### 1. Aggiungere un Home Listing

```bash
curl -X POST "https://YOUR_API_GATEWAY_URL/catalog" \
  -H "Content-Type: application/json" \
  -H "x-api-key: YOUR_API_KEY" \
  -d '{
    "type": "home_listing",
    "data": {
      "home_listing_id": "VILLA_ROMA_001",
      "name": "Villa di Lusso a Roma Nord",
      "description": "Splendida villa di 400mq con giardino",
      "price": 950000,
      "currency": "EUR",
      "url": "https://example.com/villa-roma-001",
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
    }
  }'
```

### 2. Aggiungere un Prodotto Commerce

```bash
curl -X POST "https://YOUR_API_GATEWAY_URL/catalog" \
  -H "Content-Type: application/json" \
  -H "x-api-key: YOUR_API_KEY" \
  -d '{
    "type": "commerce_product",
    "data": {
      "retailer_id": "IPHONE_15_PRO",
      "name": "iPhone 15 Pro 256GB",
      "description": "Ultimo iPhone con chip A17 Pro",
      "price": 139900,
      "currency": "EUR",
      "availability": "in stock",
      "condition": "new",
      "brand": "Apple",
      "category": "Elettronica",
      "image_url": "https://picsum.photos/800/600?random=2",
      "url": "https://example.com/iphone-15-pro"
    }
  }'
```

### 3. Risposta di Successo

```json
{
  "success": true,
  "id": "25994362446821031",
  "message": "Home listing aggiunto con successo"
}
```

### 4. Risposta di Errore

```json
{
  "success": false,
  "error": "Campi obbligatori mancanti: address, images"
}
```

## 🔧 Monitoring e Debug

### CloudWatch Logs

```bash
# Visualizza i log Lambda
aws logs tail /aws/lambda/real-estate-meta-catalog-api-function --follow
```

### API Gateway Logs

Puoi abilitare i log dettagliati nell'AWS Console:
1. API Gateway → Stages → prod → Logs/Tracing
2. Abilita "Enable CloudWatch Logs"
3. Log level: INFO o ERROR

### Test Local

Prima del deploy, puoi testare la Lambda localmente:

```bash
# Nella cartella lambda/
python lambda_function.py
```

## 🛡️ Sicurezza

### API Key Management

1. **Rotazione Regolare**: Rigenera l'API key periodicamente
2. **Accesso Limitato**: Condividi la chiave solo con servizi autorizzati
3. **Rate Limiting**: L'API Gateway ha limiti configurati (10 req/sec, 1000/giorno)

### Variables d'Ambiente

Le credenziali Meta sono memorizzate come variabili d'ambiente Lambda, non in chiaro nel codice.

## 📊 Rate Limits

- **API Gateway**: 10 richieste/secondo, burst 20
- **Usage Plan**: 1000 richieste/giorno
- **Meta API**: 200 richieste/ora per catalogo

## 🧹 Cleanup

Per rimuovere completamente l'infrastruttura:

```bash
terraform destroy
```

## 🔍 Troubleshooting

### Errore: "Invalid API Key"
- Verifica che l'header `x-api-key` sia corretto
- Controlla che l'API key sia associata al Usage Plan

### Errore: "Execution failed due to configuration error"
- Verifica le variabili d'ambiente Lambda
- Controlla i permessi IAM

### Errore Meta API: "Invalid parameter"
- Verifica che tutti i campi obbligatori siano presenti
- Controlla che il prezzo sia un integer, non string
- Verifica che le coordinate siano valide

### Lambda Timeout
- La Lambda ha timeout di 30 secondi
- Se necessario, aumenta il timeout in `main.tf`

## 📚 Link Utili

- [AWS API Gateway Documentation](https://docs.aws.amazon.com/apigateway/)
- [AWS Lambda Documentation](https://docs.aws.amazon.com/lambda/)
- [Meta Graph API Documentation](https://developers.facebook.com/docs/graph-api/)
- [Terraform AWS Provider](https://registry.terraform.io/providers/hashicorp/aws/)

## 🆘 Supporto

Per problemi:
1. Controlla i log CloudWatch
2. Verifica la configurazione in `terraform.tfvars`
3. Testa prima con il demo locale (`python demo.py`)
4. Consulta la documentazione Meta Business Setup (`../META_BUSINESS_SETUP.md`)