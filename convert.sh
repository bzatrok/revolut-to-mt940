#!/bin/bash

# Create output directory if it doesn't exist
mkdir -p output

# Prompt for input file path
read -p "Enter input file path: " input_file
# Prompt for output file name
read -p "Enter output file name: " output_file
# Prompt for account IBAN
read -p "Enter account IBAN: " account_iban
# Execute the Python script with provided parameters
python3 main.py \
--in "$input_file" \
--out output/"$account_iban"_revolut_"$output_file".940 \
--account-iban "$account_iban"