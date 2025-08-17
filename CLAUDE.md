# Revolut to MT940 Converter

## Purpose
This is a web application that converts Revolut bank statement CSV files to MT940 format, specifically designed for Dutch ZZP (freelance) entrepreneurs who need to process their Revolut transactions for quarterly VAT returns (BTW aangifte).

## Target Users
- Dutch ZZP entrepreneurs and freelancers
- Self-employed professionals using Revolut Business accounts
- Users who need MT940 files for accounting software integration

## Technical Specifications

### Backend
- **Framework**: Flask (Python)
- **Port**: 5110
- **Dependencies**: See `requirements.txt`
- **Processing**: Converts Revolut CSV to MT940 format
- **Validation**: Validates CSV headers and IBAN format
- **Error Handling**: Comprehensive error messages for invalid files

### Frontend
- **Design**: Modern, responsive web interface
- **Styling**: Custom CSS with orange/yellow gradient background
- **Animations**: Smooth fade transitions throughout
- **Loading State**: Full-screen overlay with spinner (2-second duration)
- **Validation**: Real-time IBAN and file format validation
- **File Support**: CSV files only, with drag & drop functionality

### Features
- **IBAN Validation**: Real-time validation for Revolut IBAN format (`XX##REVO##########`)
- **File Upload**: Drag & drop CSV file support with visual feedback
- **Error Handling**: Client-side error display for invalid CSV formats
- **Loading Feedback**: Professional loading overlay during conversion
- **Download**: Automatic MT940 file download upon completion
- **SEO Optimized**: Meta tags for Dutch accounting software users
- **Analytics**: Privacy-first Simple Analytics integration

### Docker Support
- Containerized application
- Docker Compose configuration available
- Production-ready deployment

### Accounting Software Compatibility
Compatible with popular Dutch accounting platforms:
- Exact Online
- Moneybird  
- e-Boekhouden.nl
- SnelStart

## Development Commands

### Local Development
```bash
pip install -r requirements.txt
python app.py
```

### Docker
```bash
docker-compose up
```

### Testing
- Manual testing with Revolut CSV exports
- Validation testing for various error scenarios
- UI/UX testing across devices

## File Structure
- `app.py` - Main Flask application
- `revolut.py` - Revolut CSV parser
- `mt940.py` - MT940 file writer
- `templates/upload.html` - Web interface
- `requirements.txt` - Python dependencies
- `Dockerfile` - Container configuration
- `docker-compose.yml` - Multi-container setup

## Known Limitations
- Only processes completed transactions from Revolut
- Missing counterparty IBAN for received transactions (Revolut limitation)
- Designed specifically for Revolut CSV format
- Fee transactions are split into separate entries for accounting accuracy