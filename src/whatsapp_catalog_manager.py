"""
WhatsApp Business Catalog Manager - Classe principale per la gestione dei cataloghi.

Questo modulo fornisce un'interfaccia completa per interagire con l'API Graph di Meta
per gestire cataloghi WhatsApp Business, inclusi prodotti e messaggistica.
"""

import json
import time
from typing import Dict, List, Optional, Union, Any
from urllib.parse import urljoin
import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

from .config import Config, ProductValidationRules, logger


class MetaAPIException(Exception):
    """Eccezione personalizzata per errori dell'API Meta."""
    
    def __init__(self, message: str, status_code: Optional[int] = None, response_data: Optional[dict] = None):
        self.message = message
        self.status_code = status_code
        self.response_data = response_data
        super().__init__(self.message)


class RateLimiter:
    """Gestisce il rate limiting per le chiamate API."""
    
    def __init__(self, max_requests_per_hour: int = 180):
        self.max_requests = max_requests_per_hour
        self.requests_made = 0
        self.reset_time = time.time() + 3600  # 1 ora da ora
    
    def wait_if_needed(self) -> None:
        """Aspetta se necessario per rispettare il rate limit."""
        current_time = time.time()
        
        # Reset del contatore ogni ora
        if current_time >= self.reset_time:
            self.requests_made = 0
            self.reset_time = current_time + 3600
        
        # Se abbiamo raggiunto il limite, aspetta
        if self.requests_made >= self.max_requests:
            sleep_time = self.reset_time - current_time
            if sleep_time > 0:
                logger.warning(f"Rate limit raggiunto. Aspetto {sleep_time:.2f} secondi...")
                time.sleep(sleep_time)
                self.requests_made = 0
                self.reset_time = time.time() + 3600
    
    def record_request(self) -> None:
        """Registra una richiesta effettuata."""
        self.requests_made += 1


class WhatsAppCatalogManager:
    """
    Classe principale per gestire cataloghi WhatsApp Business tramite Meta Graph API.
    
    Fornisce metodi per:
    - Gestione prodotti (CRUD operations)
    - Invio messaggi WhatsApp con prodotti
    - Gestione cataloghi
    - Validazione dati
    """
    
    def __init__(self, access_token: Optional[str] = None, catalog_id: Optional[str] = None, 
                 phone_number_id: Optional[str] = None):
        """
        Inizializza il manager del catalogo WhatsApp Business.
        
        Args:
            access_token: Token di accesso Meta (usa quello in .env se non specificato)
            catalog_id: ID del catalogo (usa quello in .env se non specificato)
            phone_number_id: ID del numero WhatsApp (usa quello in .env se non specificato)
        """
        self.config = Config()
        self.access_token = access_token or self.config.META_ACCESS_TOKEN
        self.catalog_id = catalog_id or self.config.CATALOG_ID
        self.phone_number_id = phone_number_id or self.config.PHONE_NUMBER_ID
        self.waba_id = self.config.WHATSAPP_BUSINESS_ACCOUNT_ID
        
        # Validazione parametri essenziali
        if not self.access_token:
            raise ValueError("Access token è richiesto. Forniscilo nel costruttore o nel file .env")
        
        # Rate limiter
        self.rate_limiter = RateLimiter(self.config.MAX_REQUESTS_PER_HOUR)
        
        # Configura session HTTP con retry automatico
        self.session = requests.Session()
        retry_strategy = Retry(
            total=self.config.MAX_RETRIES,
            status_forcelist=[429, 500, 502, 503, 504],
            allowed_methods=["HEAD", "GET", "POST", "PUT", "DELETE", "OPTIONS", "TRACE"],
            backoff_factor=self.config.RETRY_DELAY
        )
        adapter = HTTPAdapter(max_retries=retry_strategy)
        self.session.mount("http://", adapter)
        self.session.mount("https://", adapter)
        
        logger.info(f"WhatsAppCatalogManager inizializzato con catalog_id: {self.catalog_id}")
    
    def _make_request(self, method: str, url: str, **kwargs) -> requests.Response:
        """
        Effettua una richiesta HTTP con gestione rate limiting e retry.
        
        Args:
            method: Metodo HTTP (GET, POST, PUT, DELETE)
            url: URL della richiesta
            **kwargs: Parametri aggiuntivi per requests
            
        Returns:
            requests.Response: Risposta della richiesta
            
        Raises:
            MetaAPIException: Se la richiesta fallisce
        """
        # Aspetta se necessario per rate limiting
        self.rate_limiter.wait_if_needed()
        
        # Prepara headers
        headers = self.config.get_headers()
        if 'headers' in kwargs:
            headers.update(kwargs['headers'])
        kwargs['headers'] = headers
        
        # Timeout di default
        kwargs.setdefault('timeout', self.config.REQUEST_TIMEOUT)
        
        try:
            logger.debug(f"Richiesta {method} a {url}")
            response = self.session.request(method, url, **kwargs)
            self.rate_limiter.record_request()
            
            # Log della risposta
            logger.debug(f"Risposta {response.status_code}: {response.text[:500]}")
            
            # Gestione errori HTTP
            if not response.ok:
                error_data = None
                try:
                    error_data = response.json()
                except json.JSONDecodeError:
                    pass
                
                error_message = f"Errore API Meta: {response.status_code}"
                if error_data and 'error' in error_data:
                    error_message += f" - {error_data['error'].get('message', 'Errore sconosciuto')}"
                
                raise MetaAPIException(error_message, response.status_code, error_data)
            
            return response
            
        except requests.RequestException as e:
            logger.error(f"Errore nella richiesta HTTP: {e}")
            raise MetaAPIException(f"Errore di connessione: {e}")
    
    def validate_product_data(self, product_data: dict) -> Dict[str, Any]:
        """
        Valida e normalizza i dati del prodotto.
        
        Args:
            product_data: Dati del prodotto da validare
            
        Returns:
            dict: Dati del prodotto validati e normalizzati
            
        Raises:
            ValueError: Se i dati non sono validi
        """
        is_valid, errors = ProductValidationRules.validate_product_data(product_data)
        
        if not is_valid:
            error_message = "Errori di validazione prodotto:\\n" + "\\n".join(errors)
            logger.error(error_message)
            raise ValueError(error_message)
        
        # Normalizza i dati
        normalized_data = product_data.copy()
        
        # Normalizza il prezzo (rimuovi simboli di valuta e converti in formato numerico)
        if 'price' in normalized_data:
            price_str = str(normalized_data['price'])
            # Rimuovi simboli comuni di valuta e spazi
            price_clean = ''.join(c for c in price_str if c.isdigit() or c in '.,')
            price_clean = price_clean.replace(',', '.')
            try:
                price_float = float(price_clean)
                # Meta richiede il prezzo come numero intero in centesimi
                # Es: 29.99 EUR diventa 2999 (centesimi)
                normalized_data['price'] = int(price_float * 100)
            except ValueError:
                raise ValueError(f"Formato prezzo non valido: {price_str}")
        
        # Normalizza valuta
        if 'currency' in normalized_data:
            normalized_data['currency'] = normalized_data['currency'].upper()
        
        # Aggiungi valori di default se mancanti
        normalized_data.setdefault('availability', self.config.DEFAULT_AVAILABILITY)
        normalized_data.setdefault('condition', self.config.DEFAULT_CONDITION)
        normalized_data.setdefault('currency', self.config.DEFAULT_CURRENCY)
        
        logger.debug(f"Dati prodotto validati: {normalized_data['retailer_id']}")
        return normalized_data
    
    def add_product(self, product_data: dict) -> Dict[str, Any]:
        """
        Aggiunge un nuovo prodotto al catalogo.
        
        Args:
            product_data: Dizionario con i dati del prodotto
            
        Returns:
            dict: Risposta dell'API con i dettagli del prodotto creato
            
        Example:
            product_data = {
                "retailer_id": "PROD_001",
                "name": "iPhone 15 Pro",
                "description": "Ultimo modello iPhone",
                "price": "1199.00",
                "currency": "EUR",
                "availability": "in stock",
                "condition": "new",
                "brand": "Apple",
                "image_url": "https://example.com/iphone.jpg"
            }
        """
        if not self.catalog_id:
            raise ValueError("Catalog ID è richiesto per aggiungere prodotti")
        
        # Valida i dati del prodotto
        validated_data = self.validate_product_data(product_data)
        
        # URL per aggiungere prodotto
        url = self.config.get_catalog_url(self.catalog_id)
        
        # Effettua la richiesta
        try:
            response = self._make_request('POST', url, json=validated_data)
            result = response.json()
            
            logger.info(f"Prodotto aggiunto al catalogo: {validated_data['retailer_id']}")
            return result
            
        except MetaAPIException as e:
            logger.error(f"Errore nell'aggiunta del prodotto: {e.message}")
            raise
    
    def update_product(self, retailer_id: str, updated_data: dict) -> Dict[str, Any]:
        """
        Aggiorna un prodotto esistente nel catalogo.
        
        Args:
            retailer_id: ID univoco del prodotto da aggiornare
            updated_data: Dati da aggiornare
            
        Returns:
            dict: Risposta dell'API
        """
        if not self.catalog_id:
            raise ValueError("Catalog ID è richiesto per aggiornare prodotti")
        
        # URL specifico del prodotto
        url = f"{self.config.get_catalog_url(self.catalog_id)}/{retailer_id}"
        
        # Valida solo i dati forniti (update parziale)
        if updated_data:
            # Crea un prodotto temporaneo con dati minimi per la validazione
            temp_product = {
                'retailer_id': retailer_id,
                'name': 'temp',
                'description': 'temp',
                'price': '1.00',
                'currency': 'EUR',
                'availability': 'in stock',
                'condition': 'new'
            }
            temp_product.update(updated_data)
            validated_temp = self.validate_product_data(temp_product)
            
            # Estrai solo i campi aggiornati
            validated_data = {k: v for k, v in validated_temp.items() if k in updated_data}
        else:
            validated_data = updated_data
        
        try:
            response = self._make_request('POST', url, json=validated_data)
            result = response.json()
            
            logger.info(f"Prodotto aggiornato: {retailer_id}")
            return result
            
        except MetaAPIException as e:
            logger.error(f"Errore nell'aggiornamento del prodotto {retailer_id}: {e.message}")
            raise
    
    def get_product(self, retailer_id: str) -> Dict[str, Any]:
        """
        Ottiene i dettagli di un prodotto specifico.
        
        Args:
            retailer_id: ID univoco del prodotto
            
        Returns:
            dict: Dettagli del prodotto
        """
        if not self.catalog_id:
            raise ValueError("Catalog ID è richiesto per ottenere prodotti")
        
        url = f"{self.config.get_catalog_url(self.catalog_id)}/{retailer_id}"
        
        try:
            response = self._make_request('GET', url)
            result = response.json()
            
            logger.debug(f"Prodotto ottenuto: {retailer_id}")
            return result
            
        except MetaAPIException as e:
            logger.error(f"Errore nel recupero del prodotto {retailer_id}: {e.message}")
            raise
    
    def list_products(self, limit: int = 100, after: Optional[str] = None) -> Dict[str, Any]:
        """
        Lista tutti i prodotti nel catalogo.
        
        Args:
            limit: Numero massimo di prodotti da restituire (max 100)
            after: Cursor per paginazione
            
        Returns:
            dict: Lista dei prodotti con metadata di paginazione
        """
        if not self.catalog_id:
            raise ValueError("Catalog ID è richiesto per listare prodotti")
        
        url = self.config.get_catalog_url(self.catalog_id)
        params = {'limit': min(limit, 100)}
        
        if after:
            params['after'] = after
        
        try:
            response = self._make_request('GET', url, params=params)
            result = response.json()
            
            logger.debug(f"Recuperati {len(result.get('data', []))} prodotti dal catalogo")
            return result
            
        except MetaAPIException as e:
            logger.error(f"Errore nel recupero della lista prodotti: {e.message}")
            raise
    
    def delete_product(self, retailer_id: str) -> bool:
        """
        Elimina un prodotto dal catalogo.
        
        Args:
            retailer_id: ID univoco del prodotto da eliminare
            
        Returns:
            bool: True se eliminato con successo
        """
        if not self.catalog_id:
            raise ValueError("Catalog ID è richiesto per eliminare prodotti")
        
        url = f"{self.config.get_catalog_url(self.catalog_id)}/{retailer_id}"
        
        try:
            response = self._make_request('DELETE', url)
            
            logger.info(f"Prodotto eliminato: {retailer_id}")
            return True
            
        except MetaAPIException as e:
            logger.error(f"Errore nell'eliminazione del prodotto {retailer_id}: {e.message}")
            raise
    
    def batch_add_products(self, products_data: List[dict], chunk_size: Optional[int] = None) -> List[Dict[str, Any]]:
        """
        Aggiunge più prodotti in batch per migliorare le performance.
        
        Args:
            products_data: Lista di dizionari con i dati dei prodotti
            chunk_size: Dimensione dei chunk per elaborazione (default: MAX_BATCH_SIZE)
            
        Returns:
            list: Lista delle risposte per ogni prodotto
        """
        chunk_size = chunk_size or self.config.MAX_BATCH_SIZE
        results = []
        
        logger.info(f"Inizio aggiunta batch di {len(products_data)} prodotti")
        
        for i in range(0, len(products_data), chunk_size):
            chunk = products_data[i:i + chunk_size]
            logger.debug(f"Elaborazione chunk {i//chunk_size + 1}: prodotti {i+1}-{min(i+chunk_size, len(products_data))}")
            
            for product_data in chunk:
                try:
                    result = self.add_product(product_data)
                    results.append({
                        'success': True,
                        'retailer_id': product_data.get('retailer_id'),
                        'result': result
                    })
                except Exception as e:
                    logger.error(f"Errore nell'aggiunta del prodotto {product_data.get('retailer_id', 'unknown')}: {e}")
                    results.append({
                        'success': False,
                        'retailer_id': product_data.get('retailer_id'),
                        'error': str(e)
                    })
            
            # Piccola pausa tra i chunk per evitare rate limiting
            if i + chunk_size < len(products_data):
                time.sleep(1)
        
        successful = sum(1 for r in results if r['success'])
        logger.info(f"Batch completato: {successful}/{len(products_data)} prodotti aggiunti con successo")
        
        return results
    
    def send_product_message(self, phone_number: str, product_retailer_id: str, 
                           message: str = "", header_text: str = "") -> Dict[str, Any]:
        """
        Invia un messaggio WhatsApp con un singolo prodotto.
        
        Args:
            phone_number: Numero di telefono destinatario (formato internazionale)
            product_retailer_id: ID del prodotto nel catalogo
            message: Messaggio di accompagnamento (opzionale)
            header_text: Testo dell'header (opzionale)
            
        Returns:
            dict: Risposta dell'API WhatsApp
        """
        if not self.phone_number_id:
            raise ValueError("Phone Number ID è richiesto per inviare messaggi")
        
        if not self.catalog_id:
            raise ValueError("Catalog ID è richiesto per inviare messaggi prodotto")
        
        # Pulisci il numero di telefono
        clean_phone = phone_number.replace('+', '').replace(' ', '').replace('-', '')
        
        # Costruisci il messaggio
        message_data = {
            "messaging_product": "whatsapp",
            "to": clean_phone,
            "type": "interactive",
            "interactive": {
                "type": "product",
                "body": {
                    "text": message or "Guarda questo prodotto dal nostro catalogo!"
                },
                "action": {
                    "catalog_id": self.catalog_id,
                    "product_retailer_id": product_retailer_id
                }
            }
        }
        
        # Aggiungi header se fornito
        if header_text:
            message_data["interactive"]["header"] = {
                "type": "text",
                "text": header_text
            }
        
        url = self.config.get_whatsapp_url(self.phone_number_id)
        
        try:
            response = self._make_request('POST', url, json=message_data)
            result = response.json()
            
            logger.info(f"Messaggio prodotto inviato a {clean_phone}: {product_retailer_id}")
            return result
            
        except MetaAPIException as e:
            logger.error(f"Errore nell'invio del messaggio prodotto: {e.message}")
            raise
    
    def send_catalog_message(self, phone_number: str, body_text: str = "Guarda il nostro catalogo!", 
                           header_text: str = "", footer_text: str = "") -> Dict[str, Any]:
        """
        Invia un messaggio WhatsApp con l'intero catalogo.
        
        Args:
            phone_number: Numero di telefono destinatario
            body_text: Testo del corpo del messaggio
            header_text: Testo dell'header (opzionale)
            footer_text: Testo del footer (opzionale)
            
        Returns:
            dict: Risposta dell'API WhatsApp
        """
        if not self.phone_number_id:
            raise ValueError("Phone Number ID è richiesto per inviare messaggi")
        
        if not self.catalog_id:
            raise ValueError("Catalog ID è richiesto per inviare messaggi catalogo")
        
        # Pulisci il numero di telefono
        clean_phone = phone_number.replace('+', '').replace(' ', '').replace('-', '')
        
        # Costruisci il messaggio
        message_data = {
            "messaging_product": "whatsapp",
            "to": clean_phone,
            "type": "interactive",
            "interactive": {
                "type": "catalog_message",
                "body": {
                    "text": body_text
                },
                "action": {
                    "name": "catalog_message",
                    "parameters": {
                        "thumbnail_product_retailer_id": ""  # Usa il primo prodotto come thumbnail
                    }
                }
            }
        }
        
        # Aggiungi header se fornito
        if header_text:
            message_data["interactive"]["header"] = {
                "type": "text", 
                "text": header_text
            }
        
        # Aggiungi footer se fornito
        if footer_text:
            message_data["interactive"]["footer"] = {
                "text": footer_text
            }
        
        url = self.config.get_whatsapp_url(self.phone_number_id)
        
        try:
            response = self._make_request('POST', url, json=message_data)
            result = response.json()
            
            logger.info(f"Messaggio catalogo inviato a {clean_phone}")
            return result
            
        except MetaAPIException as e:
            logger.error(f"Errore nell'invio del messaggio catalogo: {e.message}")
            raise
    
    def get_catalog_info(self) -> Dict[str, Any]:
        """
        Ottiene informazioni sul catalogo.
        
        Returns:
            dict: Informazioni del catalogo
        """
        if not self.catalog_id:
            raise ValueError("Catalog ID è richiesto")
        
        url = f"{self.config.META_BASE_URL}/{self.catalog_id}"
        params = {
            'fields': 'id,name,product_count,vertical'
        }
        
        try:
            response = self._make_request('GET', url, params=params)
            result = response.json()
            
            logger.debug(f"Informazioni catalogo ottenute: {self.catalog_id}")
            return result
            
        except MetaAPIException as e:
            logger.error(f"Errore nel recupero informazioni catalogo: {e.message}")
            raise
    
    def __str__(self) -> str:
        """Rappresentazione string dell'oggetto."""
        return f"WhatsAppCatalogManager(catalog_id='{self.catalog_id}', phone_id='{self.phone_number_id}')"
    
    def __repr__(self) -> str:
        """Rappresentazione repr dell'oggetto."""
        return self.__str__()