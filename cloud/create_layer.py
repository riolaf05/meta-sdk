#!/usr/bin/env python3
"""
Script semplice per creare un Lambda Layer con le dipendenze requests
"""

import os
import shutil
import subprocess
import sys
from pathlib import Path
import zipfile

def create_lambda_layer():
    """Crea un Lambda Layer con le dipendenze Python."""
    
    print("📦 Creazione Lambda Layer per dipendenze...")
    
    script_dir = Path(__file__).parent
    layer_dir = script_dir / "lambda-layer"
    python_dir = layer_dir / "python"
    
    # Pulizia directory precedente
    if layer_dir.exists():
        shutil.rmtree(layer_dir)
    
    # Crea struttura directory per layer
    python_dir.mkdir(parents=True, exist_ok=True)
    
    print(f"📂 Layer directory: {layer_dir}")
    
    # Installa requests nel layer
    requirements_file = script_dir / "lambda" / "requirements.txt"
    if requirements_file.exists():
        print("📥 Installazione dipendenze da requirements.txt...")
        cmd = f"pip install --no-user -r {requirements_file} -t {python_dir}"
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
        
        if result.returncode != 0:
            print(f"❌ Errore installazione: {result.stderr}")
            # Prova senza --no-user
            cmd = f"pip install -r {requirements_file} -t {python_dir}"
            result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
            
            if result.returncode != 0:
                print(f"❌ Errore installazione (retry): {result.stderr}")
                sys.exit(1)
        
        print("✅ Dipendenze installate nel layer")
    else:
        # Installa solo requests se non c'è requirements.txt
        print("📥 Installazione requests...")
        cmd = f"pip install --no-user requests -t {python_dir}"
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
        
        if result.returncode != 0:
            print(f"❌ Errore installazione: {result.stderr}")
            # Prova senza --no-user
            cmd = f"pip install requests -t {python_dir}"
            result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
            
            if result.returncode != 0:
                print(f"❌ Errore installazione (retry): {result.stderr}")
                sys.exit(1)
    
    # Crea il file ZIP per il layer
    layer_zip = script_dir / "lambda_layer.zip"
    
    print(f"🗜️ Creazione ZIP: {layer_zip}")
    
    with zipfile.ZipFile(layer_zip, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for root, dirs, files in os.walk(layer_dir):
            for file in files:
                file_path = Path(root) / file
                # Calcola il path relativo dalla directory layer
                arc_path = file_path.relative_to(layer_dir)
                zipf.write(file_path, arc_path)
    
    print(f"✅ Layer ZIP creato: {layer_zip}")
    print(f"📊 Dimensione: {layer_zip.stat().st_size / 1024 / 1024:.1f} MB")
    
    # Pulizia directory temporanea
    shutil.rmtree(layer_dir)
    
    return layer_zip

if __name__ == "__main__":
    create_lambda_layer()