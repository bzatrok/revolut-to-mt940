# app.py
from flask import Flask, render_template, request, send_file, jsonify
import os
from werkzeug.utils import secure_filename
from revolut import RevolutCsvReader
from mt940 import Mt940Writer
import tempfile
import time

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['OUTPUT_FOLDER'] = 'output'

# Ensure upload and output directories exist
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
os.makedirs(app.config['OUTPUT_FOLDER'], exist_ok=True)

@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        try:
            if 'file' not in request.files:
                return jsonify({'error': 'No file uploaded'}), 400
            
            file = request.files['file']
            iban = request.form['iban']
            
            if file.filename == '':
                return jsonify({'error': 'No file selected'}), 400
            
            # Add simulated processing time
            time.sleep(2.0)
            
            if file:
                # Create temporary file for CSV processing
                with tempfile.NamedTemporaryFile(delete=False, suffix='.csv') as temp_csv:
                    file.save(temp_csv.name)
                    
                    try:
                        # Generate output filename
                        output_filename = f"{secure_filename(iban)}_revolut_{secure_filename(file.filename)}.940"
                        output_path = os.path.join(app.config['OUTPUT_FOLDER'], output_filename)
                        
                        # Process the file
                        reader = RevolutCsvReader(temp_csv.name)
                        transactions = reader.get_all_transactions()
                        
                        if not transactions:
                            return jsonify({'error': 'No valid transactions found in the CSV file'}), 400
                        
                        with Mt940Writer(output_path, iban, transactions[0].datetime.strftime('%Y-%m')) as writer:
                            for transaction in transactions:
                                writer.write_transaction(transaction)
                        
                        # Return the generated file
                        return send_file(
                            output_path,
                            as_attachment=True,
                            download_name=output_filename,
                            mimetype='application/octet-stream'
                        )
                    except ValueError as e:
                        error_msg = str(e)
                        if 'Headers do not match' in error_msg:
                            return jsonify({'error': 'Invalid file format: This does not appear to be a valid Revolut CSV export. Please ensure you\'re uploading the correct transaction statement file from Revolut.'}), 400
                        elif 'No completed transactions' in error_msg:
                            return jsonify({'error': 'No completed transactions found. Please ensure your CSV contains completed transactions only.'}), 400
                        else:
                            return jsonify({'error': f'Processing error: {error_msg}'}), 400
                    except Exception as e:
                        return jsonify({'error': f'An unexpected error occurred: {str(e)}'}), 500
                    finally:
                        # Clean up temporary file
                        if os.path.exists(temp_csv.name):
                            os.unlink(temp_csv.name)
        except Exception as e:
            return jsonify({'error': f'Server error: {str(e)}'}), 500
    
    return render_template('upload.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=False, port=5110)