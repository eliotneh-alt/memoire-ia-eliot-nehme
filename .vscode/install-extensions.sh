#!/bin/bash

# Chemin vers le fichier extensions.json
extensions_file="path/to/extensions.json"

# Lire le fichier extensions.json et extraire les recommandations
extensions=$(jq -r '.recommendations[]' "$extensions_file")

# Installer chaque extension
for extension in $extensions; do
    code --install-extension "$extension"
done