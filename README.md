# Convert Revolut export file to MT940 format

This tool converts Revolut export files (in CSV) to MT940 format. You can use the MT940 to import statements in bookkeeping software like SnelStart, Exact Online, Moneybird, and e-Boekhouden.nl. 

Now available with a modern web interface and Docker support for easy deployment!

## Disclaimer
This script comes without any warranty whatsoever. Do not use it in production. Do not use it if you are not familiar with how banks work, how bookkeeping software works, and if you do not have the technical know-how to make changes to this script yourself if something breaks. If you do use this script it might kill your cat or start World War 3. Don't come to me, I warned you.

## Features

* **Web Interface**: Modern, responsive web application with drag-and-drop file upload
* **Docker Support**: Easy deployment with Docker and Docker Compose
* **Multiple Software Support**: Compatible with SnelStart, Exact Online, Moneybird, e-Boekhouden.nl
* **Real-time Validation**: IBAN validation and file format checking
* **User-Friendly**: Professional loading animations and clear error messages
* Parses the Revolut CSV file and extracts: timestamp, transaction type, transaction description, transaction reference, transaction amount, fee amount, balance after transaction, counterparty IBAN
* This information is converted into a valid MT940 file
* Revolut charges fees for transactions. These are included in the transaction (as Revolut sees it). This could cause problems when importing into bookkeeping software as the amounts do not match up. This script will not include fees in transactions but insert "fake" transactions for each deducted fee. You will see those transactions separately in your bookkeeping software but in Revolut they are included in the transaction

## Limitations

* Apart from loading transactions into SnelStart, it has not been tested on any other tasks. It might or might not work for your use case.
* Revolut does not export the counterparty IBAN for transactions that you *receive*. As such, the IBAN field in MT940 for credit transactions are usually empty.
* The export files from Revolut are missing some key data fields when the transaction is still pending (status is not *COMPLETED*). Only export completed transactions.

## Installation

### Option 1: Web Interface (Recommended)

```bash
git clone https://github.com/yourusername/revolut-to-mt940.git
cd revolut-to-mt940
pip install -r requirements.txt
python app.py
```

Then open your browser at `http://localhost:5110`

### Option 2: Docker

```bash
git clone https://github.com/yourusername/revolut-to-mt940.git
cd revolut-to-mt940
docker-compose up
```

Then open your browser at `http://localhost:5110`

### Option 3: Command Line

```bash
git clone https://github.com/yourusername/revolut-to-mt940.git
cd revolut-to-mt940
```

## Usage

### Web Interface
1. Open the web application at `http://localhost:5110`
2. Enter your Revolut IBAN (format: XX##REVO##########)
3. Drag and drop or select your Revolut CSV file
4. Click "Convert to MT940"
5. The MT940 file will automatically download

### Command Line

Export your statement from Revolut as CSV, then:

```bash
./convert.sh
```

Or run manually:

```bash
python3 main.py \
	--in /path/to/revolut.csv \
	--out /path/to/mt.940 \
	--account-iban <your revolut account IBAN>
```


## License

MIT
