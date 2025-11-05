#!/usr/bin/env python3
"""
Helper script per il deployment dell'infrastruttura AWS
"""

import os
import subprocess
import sys
import json
from pathlib import Path

def run_command(cmd, check=True):
    """Esegue un comando e restituisce il risultato."""
    print(f"🔧 Eseguendo: {cmd}")
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    
    if check and result.returncode != 0:
        print(f"❌ Errore: {result.stderr}")
        sys.exit(1)
    
    return result

def check_prerequisites():
    """Verifica che i prerequisiti siano soddisfatti."""
    print("🔍 Verifica prerequisiti...")
    
    # Verifica Terraform
    result = run_command("terraform version", check=False)
    if result.returncode != 0:
        print("❌ Terraform non trovato. Installalo da: https://www.terraform.io/downloads.html")
        sys.exit(1)
    
    # Verifica AWS CLI
    result = run_command("aws --version", check=False)
    if result.returncode != 0:
        print("❌ AWS CLI non trovato. Installalo da: https://aws.amazon.com/cli/")
        sys.exit(1)
    
    # Verifica configurazione AWS
    result = run_command("aws configure list", check=False)
    if result.returncode != 0:
        print("❌ AWS CLI non configurato. Esegui: aws configure")
        sys.exit(1)
    
    # Verifica file terraform.tfvars
    if not Path("terraform.tfvars").exists():
        print("❌ File terraform.tfvars mancante!")
        print("   Copia terraform.tfvars.example in terraform.tfvars e configuralo")
        sys.exit(1)
    
    print("✅ Tutti i prerequisiti soddisfatti!")

def init_terraform():
    """Inizializza Terraform."""
    print("\n🚀 Inizializzazione Terraform...")
    run_command("terraform init")

def plan_deployment():
    """Pianifica il deployment."""
    print("\n📋 Pianificazione deployment...")
    run_command("terraform plan")
    
    response = input("\n❓ Procedere con il deployment? (y/N): ")
    return response.lower() == 'y'

def apply_deployment():
    """Applica il deployment."""
    print("\n🚀 Deployment in corso...")
    run_command("terraform apply -auto-approve")

def get_outputs():
    """Ottiene gli output del deployment."""
    print("\n📊 Recupero informazioni deployment...")
    result = run_command("terraform output -json")
    
    try:
        outputs = json.loads(result.stdout)
        return outputs
    except json.JSONDecodeError:
        print("❌ Errore nel parsing degli output Terraform")
        return {}

def display_results(outputs):
    """Mostra i risultati del deployment."""
    print("\n🎉 Deployment completato con successo!")
    print("=" * 50)
    
    if 'api_gateway_url' in outputs:
        api_url = outputs['api_gateway_url']['value']
        print(f"🔗 API Gateway URL: {api_url}")
    
    if 'api_key_id' in outputs:
        api_key_id = outputs['api_key_id']['value']
        print(f"🔑 API Key ID: {api_key_id}")
    
    if 'lambda_function_name' in outputs:
        function_name = outputs['lambda_function_name']['value']
        print(f"⚡ Lambda Function: {function_name}")
    
    if 'cloudwatch_log_group' in outputs:
        log_group = outputs['cloudwatch_log_group']['value']
        print(f"📋 CloudWatch Logs: {log_group}")
    
    print("\n📋 Prossimi passi:")
    print("1. Aggiorna test_api.py con API_GATEWAY_URL e API_KEY")
    print("2. Esegui: python test_api.py")
    print("3. Monitora i log: aws logs tail " + outputs.get('cloudwatch_log_group', {}).get('value', '/aws/lambda/real-estate-meta-catalog-api-function') + " --follow")

def destroy_infrastructure():
    """Distrugge l'infrastruttura."""
    print("\n⚠️  ATTENZIONE: Stai per distruggere l'intera infrastruttura!")
    response = input("❓ Sei sicuro? Digita 'destroy' per confermare: ")
    
    if response != 'destroy':
        print("❌ Operazione annullata")
        return
    
    print("\n🗑️  Distruzione infrastruttura in corso...")
    run_command("terraform destroy -auto-approve")
    print("✅ Infrastruttura distrutta")

def main():
    """Funzione principale."""
    print("🏗️  Meta Catalog API Gateway - Deployment Helper")
    print("=" * 55)
    
    # Verifica che siamo nella cartella corretta
    if not Path("main.tf").exists():
        print("❌ Esegui questo script dalla cartella cloud/")
        sys.exit(1)
    
    if len(sys.argv) > 1:
        command = sys.argv[1]
        
        if command == "destroy":
            destroy_infrastructure()
            return
        elif command == "plan":
            check_prerequisites()
            init_terraform()
            plan_deployment()
            return
        elif command == "init":
            check_prerequisites()
            init_terraform()
            return
        else:
            print(f"❌ Comando non riconosciuto: {command}")
            print("Comandi disponibili: deploy, destroy, plan, init")
            sys.exit(1)
    
    # Deployment completo
    check_prerequisites()
    init_terraform()
    
    if plan_deployment():
        apply_deployment()
        outputs = get_outputs()
        display_results(outputs)
    else:
        print("❌ Deployment annullato")

if __name__ == "__main__":
    main()