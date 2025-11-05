"""
Modulo di configurazione per l'app Meta SDK WhatsApp Business Catalog Manager.
Gestisce il caricamento delle variabili d'ambiente e la configurazione dell'applicazione.
"""

import os
import logging
from pathlib import Path
from typing import Optional
from dotenv import load_dotenv

# Carica le variabili d'ambiente dal file .env
load_dotenv()

class Config:
    """
    Classe di configurazione centralizzata per l'applicazione.
    Carica e valida tutte le variabili d'ambiente necessarie.
    """
    
    # Meta/Facebook Configuration
    META_ACCESS_TOKEN: str = os.getenv('META_ACCESS_TOKEN', '')
    META_APP_ID: str = os.getenv('META_APP_ID', '')
    META_APP_SECRET: str = os.getenv('META_APP_SECRET', '')
    WHATSAPP_BUSINESS_ACCOUNT_ID: str = os.getenv('WHATSAPP_BUSINESS_ACCOUNT_ID', '')
    PHONE_NUMBER_ID: str = os.getenv('PHONE_NUMBER_ID', '')
    
    # Azure Communication Services Configuration (opzionale)
    AZURE_COMMUNICATION_SERVICES_CONNECTION_STRING: str = os.getenv('AZURE_COMMUNICATION_SERVICES_CONNECTION_STRING', '')
    WHATSAPP_CHANNEL_ID: str = os.getenv('WHATSAPP_CHANNEL_ID', '')
    
    # Catalog Configuration
    CATALOG_ID: str = os.getenv('CATALOG_ID', '')
    
    # API Configuration
    META_GRAPH_API_VERSION: str = os.getenv('META_GRAPH_API_VERSION', 'v18.0')
    META_BASE_URL: str = f"https://graph.facebook.com/{META_GRAPH_API_VERSION}"
    
    # Rate Limiting Configuration
    MAX_REQUESTS_PER_HOUR: int = int(os.getenv('MAX_REQUESTS_PER_HOUR', '180'))
    REQUEST_TIMEOUT: int = int(os.getenv('REQUEST_TIMEOUT', '30'))
    MAX_RETRIES: int = int(os.getenv('MAX_RETRIES', '3'))
    RETRY_DELAY: int = int(os.getenv('RETRY_DELAY', '5'))
    
    # Batch Operation Limits
    MAX_BATCH_SIZE: int = int(os.getenv('MAX_BATCH_SIZE', '50'))
    
    # Logging Configuration
    LOG_LEVEL: str = os.getenv('LOG_LEVEL', 'INFO')
    LOG_FILE: str = os.getenv('LOG_FILE', 'whatsapp_catalog.log')
    
    # Data Validation
    MAX_PRODUCT_NAME_LENGTH: int = 150
    MAX_PRODUCT_DESCRIPTION_LENGTH: int = 9999
    SUPPORTED_CURRENCIES: list = ['EUR', 'USD', 'GBP', 'JPY', 'CNY', 'CAD', 'AUD']
    SUPPORTED_AVAILABILITY_STATUS: list = ['in stock', 'out of stock', 'preorder', 'available for order', 'discontinued']
    SUPPORTED_CONDITIONS: list = ['new', 'refurbished', 'used', 'open_box']
    
    # File Upload Configuration
    MAX_IMAGE_SIZE_MB: int = int(os.getenv('MAX_IMAGE_SIZE_MB', '10'))
    SUPPORTED_IMAGE_FORMATS: list = ['jpg', 'jpeg', 'png', 'webp']
    
    # Default Values
    DEFAULT_CURRENCY: str = os.getenv('DEFAULT_CURRENCY', 'EUR')
    DEFAULT_AVAILABILITY: str = os.getenv('DEFAULT_AVAILABILITY', 'in stock')
    DEFAULT_CONDITION: str = os.getenv('DEFAULT_CONDITION', 'new')
    
    @classmethod
    def validate_config(cls) -> bool:
        """
        Valida la configurazione verificando che tutti i campi obbligatori siano presenti.
        
        Returns:
            bool: True se la configurazione è valida, False altrimenti
        """
        required_fields = [
            ('META_ACCESS_TOKEN', cls.META_ACCESS_TOKEN),
            ('WHATSAPP_BUSINESS_ACCOUNT_ID', cls.WHATSAPP_BUSINESS_ACCOUNT_ID),
            ('PHONE_NUMBER_ID', cls.PHONE_NUMBER_ID),
        ]
        
        missing_fields = []
        for field_name, field_value in required_fields:
            if not field_value:
                missing_fields.append(field_name)
        
        if missing_fields:
            logger = logging.getLogger(__name__)
            logger.error(f"Campi obbligatori mancanti nella configurazione: {', '.join(missing_fields)}")
            return False
        
        return True
    
    @classmethod
    def get_catalog_url(cls, catalog_id: Optional[str] = None) -> str:
        """
        Costruisce l'URL per accedere al catalogo.
        
        Args:
            catalog_id: ID del catalogo (opzionale, usa quello di default se non specificato)
        
        Returns:
            str: URL completo per l'API del catalogo
        """
        cat_id = catalog_id or cls.CATALOG_ID
        return f"{cls.META_BASE_URL}/{cat_id}/products"
    
    @classmethod
    def get_whatsapp_url(cls, phone_id: Optional[str] = None) -> str:
        """
        Costruisce l'URL per inviare messaggi WhatsApp.
        
        Args:
            phone_id: ID del numero di telefono (opzionale, usa quello di default se non specificato)
        
        Returns:
            str: URL completo per l'API WhatsApp
        """
        phone_number_id = phone_id or cls.PHONE_NUMBER_ID
        return f"{cls.META_BASE_URL}/{phone_number_id}/messages"
    
    @classmethod
    def get_headers(cls) -> dict:
        """
        Restituisce gli header HTTP standard per le richieste API.
        
        Returns:
            dict: Dictionary con gli header HTTP
        """
        return {
            'Authorization': f'Bearer {cls.META_ACCESS_TOKEN}',
            'Content-Type': 'application/json',
            'User-Agent': 'WhatsAppCatalogManager/1.0'
        }
    
    @classmethod
    def setup_logging(cls) -> logging.Logger:
        """
        Configura il sistema di logging dell'applicazione.
        
        Returns:
            logging.Logger: Logger configurato
        """
        # Crea directory logs se non esiste
        log_dir = Path('logs')
        log_dir.mkdir(exist_ok=True)
        
        # Configura il logging
        log_file_path = log_dir / cls.LOG_FILE
        
        # Configurazione del formatter
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        
        # Configurazione del logger principale
        logger = logging.getLogger('whatsapp_catalog_manager')
        logger.setLevel(getattr(logging, cls.LOG_LEVEL.upper(), logging.INFO))
        
        # Rimuovi handler esistenti per evitare duplicati
        logger.handlers.clear()
        
        # Handler per file
        file_handler = logging.FileHandler(log_file_path, encoding='utf-8')
        file_handler.setLevel(logging.DEBUG)
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)
        
        # Handler per console
        console_handler = logging.StreamHandler()
        console_handler.setLevel(getattr(logging, cls.LOG_LEVEL.upper(), logging.INFO))
        console_handler.setFormatter(formatter)
        logger.addHandler(console_handler)
        
        return logger

class ProductValidationRules:
    """
    Regole di validazione per i prodotti del catalogo.
    """
    
    REQUIRED_FIELDS = [
        'retailer_id',
        'name', 
        'description',
        'price',
        'currency',
        'availability',
        'condition'
    ]
    
    OPTIONAL_FIELDS = [
        'brand',
        'category',
        'image_url',
        'additional_image_urls',
        'url',
        'size',
        'color',
        'material',
        'pattern',
        'gender',
        'age_group',
        'inventory',
        'sale_price',
        'sale_price_effective_date'
    ]
    
    @classmethod
    def validate_product_data(cls, product_data: dict) -> tuple[bool, list[str]]:
        """
        Valida i dati di un prodotto secondo le regole di Meta.
        
        Args:
            product_data: Dictionary con i dati del prodotto
            
        Returns:
            tuple: (is_valid: bool, errors: list[str])
        """
        errors = []
        
        # Controlla campi obbligatori
        for field in cls.REQUIRED_FIELDS:
            if field not in product_data or not product_data[field]:
                errors.append(f"Campo obbligatorio mancante: {field}")
        
        # Valida lunghezza nome
        if 'name' in product_data:
            name = product_data['name']
            if len(name) > Config.MAX_PRODUCT_NAME_LENGTH:
                errors.append(f"Nome troppo lungo: {len(name)} caratteri (max {Config.MAX_PRODUCT_NAME_LENGTH})")
        
        # Valida lunghezza descrizione
        if 'description' in product_data:
            description = product_data['description']
            if len(description) > Config.MAX_PRODUCT_DESCRIPTION_LENGTH:
                errors.append(f"Descrizione troppo lunga: {len(description)} caratteri (max {Config.MAX_PRODUCT_DESCRIPTION_LENGTH})")
        
        # Valida valuta
        if 'currency' in product_data:
            currency = product_data['currency'].upper()
            if currency not in Config.SUPPORTED_CURRENCIES:
                errors.append(f"Valuta non supportata: {currency}. Supportate: {', '.join(Config.SUPPORTED_CURRENCIES)}")
        
        # Valida disponibilità
        if 'availability' in product_data:
            availability = product_data['availability']
            if availability not in Config.SUPPORTED_AVAILABILITY_STATUS:
                errors.append(f"Status disponibilità non valido: {availability}. Validi: {', '.join(Config.SUPPORTED_AVAILABILITY_STATUS)}")
        
        # Valida condizione
        if 'condition' in product_data:
            condition = product_data['condition']
            if condition not in Config.SUPPORTED_CONDITIONS:
                errors.append(f"Condizione non valida: {condition}. Valide: {', '.join(Config.SUPPORTED_CONDITIONS)}")
        
        # Valida prezzo
        if 'price' in product_data:
            try:
                price_str = str(product_data['price']).replace(',', '.')
                # Rimuovi simboli di valuta e spazi
                price_clean = ''.join(c for c in price_str if c.isdigit() or c == '.')
                price_float = float(price_clean)
                if price_float <= 0:
                    errors.append("Il prezzo deve essere maggiore di zero")
            except (ValueError, TypeError):
                errors.append(f"Formato prezzo non valido: {product_data['price']}")
        
        return len(errors) == 0, errors

# Inizializza la configurazione e il logger
config = Config()
logger = config.setup_logging()

# Valida la configurazione all'importazione del modulo
if not config.validate_config():
    logger.warning("Configurazione incompleta. Alcune funzionalità potrebbero non essere disponibili.")
else:
    logger.info("Configurazione caricata correttamente.")