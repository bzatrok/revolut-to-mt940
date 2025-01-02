# app.py
from flask import Flask, render_template, request, send_file
import os
from werkzeug.utils import secure_filename
from revolut import RevolutCsvReader
from mt940 import Mt940Writer
import tempfile

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['OUTPUT_FOLDER'] = 'output'

# Ensure upload and output directories exist
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
os.makedirs(app.config['OUTPUT_FOLDER'], exist_ok=True)

@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        if 'file' not in request.files:
            return 'No file uploaded', 400
        
        file = request.files['file']
        iban = request.form['iban']
        
        if file.filename == '':
            return 'No file selected', 400
            
        if file:
            # Create temporary file for CSV processing
            with tempfile.NamedTemporaryFile(delete=False) as temp_csv:
                file.save(temp_csv.name)
                
                # Generate output filename
                output_filename = f"{secure_filename(iban)}_revolut_{secure_filename(file.filename)}.940"
                output_path = os.path.join(app.config['OUTPUT_FOLDER'], output_filename)
                
                # Process the file
                reader = RevolutCsvReader(temp_csv.name)
                transactions = reader.get_all_transactions()
                
                with Mt940Writer(output_path, iban, transactions[0].datetime.strftime('%Y-%m')) as writer:
                    for transaction in transactions:
                        writer.write_transaction(transaction)
                
                # Clean up temporary file
                os.unlink(temp_csv.name)
                
                # Return the generated file
                return send_file(
                    output_path,
                    as_attachment=True,
                    download_name=output_filename,
                    mimetype='application/octet-stream'
                )
    
    return render_template('upload.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=False, port=5110)