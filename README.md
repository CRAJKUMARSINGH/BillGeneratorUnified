# 🚀 BillGenerator Unified - Enhanced Edition

**One Codebase, Five Variants, All Features, Zero Duplication**

## ✨ Features

### Core Features (All Variants)
- ✅ Excel Upload Mode
- ✅ Online Entry Mode
- ✅ Multiple Document Generation
- ✅ PDF & HTML Export
- ✅ Professional Templates

### Advanced Features
- 🔄 **Batch Processing** (V04, SmartBillFlow)
- 📊 **Analytics Dashboard** (SmartBillFlow)
- 🎨 **Custom Templates** (V04, SmartBillFlow)
- ⚡ **Advanced PDF** (V01, V04, SmartBillFlow)
- 🔌 **API Access** (SmartBillFlow)

## 🛡️ Security & Configuration

### Environment Variables
The application now supports configuration via environment variables for enhanced security. To use this feature:

1. Copy the `.env.example` file to `.env`:
   ```bash
   cp .env.example .env
   ```

2. Edit the `.env` file to set your configuration values:
   ```env
   # Application Settings
   APP_NAME=MyBillGenerator
   APP_VERSION=2.0.0
   APP_MODE=Production
   
   # Feature Toggles
   FEATURE_EXCEL_UPLOAD=true
   FEATURE_ONLINE_ENTRY=true
   FEATURE_BATCH_PROCESSING=true
   FEATURE_ANALYTICS=false
   
   # UI Settings
   BRANDING_TITLE="My Company Bill Generator"
   BRANDING_ICON="🏢"
   BRANDING_COLOR="#2196F3"
   
   # Processing Settings
   PROCESSING_MAX_FILE_SIZE_MB=100
   PROCESSING_ENABLE_CACHING=true
   
   # Security Settings (Backend)
   JWT_SECRET_KEY=your_super_secret_random_key
   DATABASE_URL=sqlite:///billgenerator.db
   
   # CORS Settings
   CORS_ORIGINS=http://localhost:3000,https://yourdomain.com
   
   # Rate Limiting Settings
   RATE_LIMIT_DEFAULT=1000 per hour
   RATE_LIMIT_STORAGE=memory://
   
   # Redis Settings (for caching)
   REDIS_URL=redis://localhost:6379/0
   ```

3. The application will automatically load these values, overriding the default configuration.

### Security Best Practices
- Never commit `.env` files to version control (already in `.gitignore`)
- Use strong, randomly generated secrets for production
- Regularly rotate secrets and API keys
- Limit permissions for environment variables to authorized users only
- Set specific CORS origins for production deployments
- Adjust rate limits based on expected traffic patterns

## 🚀 Quick Start

### Windows (Easy)
```bash
LAUNCH.bat
```

### Python (Any Variant)
```bash
# V01 - Standard
python launchers/launch_v01.py

# V04 - With Batch Processing
python launchers/launch_v04.py

# SmartBillFlow - All Features
python launchers/launch_smartbillflow.py
```

## 📊 Variant Comparison

| Feature | V01 | V02 | V03 | V04 | SmartBillFlow |
|---------|-----|-----|-----|-----|---------------|
| Excel Upload | ✓ | ✓ | ✓ | ✓ | ✓ |
| Online Entry | ✓ | ✓ | ✓ | ✓ | ✓ |
| **Batch Processing** | ✗ | ✗ | ✗ | **✓** | **✓** |
| Advanced PDF | ✓ | ✗ | ✗ | ✓ | ✓ |
| Custom Templates | ✗ | ✗ | ✗ | ✓ | ✓ |
| Analytics | ✗ | ✗ | ✗ | ✗ | ✓ |
| API Access | ✗ | ✗ | ✗ | ✗ | ✓ |

## 🔒 Enterprise Security Features

### API Security
- **JWT Authentication**: Secure token-based authentication for all API endpoints
- **Rate Limiting**: Prevent API abuse with configurable request limits
- **CORS Protection**: Controlled cross-origin resource sharing
- **Input Validation**: Structured validation with Pydantic
- **Password Hashing**: Secure password storage using PBKDF2 SHA256

### Data Protection
- **Environment Variables**: All secrets stored securely outside code
- **SQL Injection Prevention**: Parameterized queries throughout
- **XSS Protection**: Sanitized user inputs and outputs
- **CSRF Protection**: Secure form handling

## 📊 Monitoring & Observability

### Comprehensive Logging
- **File-based Logging**: Structured logs with timestamps and severity levels
- **Log Rotation**: Automatic log file rotation to prevent disk space issues
- **Source Tracking**: Precise source code location for debugging
- **Production Ready**: Minimal overhead in production environments

### Health Monitoring
- **Health Check Endpoint**: Dedicated endpoint for infrastructure monitoring
- **Performance Metrics**: Response time and resource usage tracking
- **Error Tracking**: Comprehensive error logging and monitoring
- **Security Auditing**: Authentication and authorization event logging

## 🔄 Batch Processing

Process multiple Excel files at once!

1. Launch V04 or SmartBillFlow
2. Select "Batch Processing" mode
3. Upload multiple Excel files
4. Click "Process All Files"
5. Download all generated documents

**Benefits:**
- Process 10+ files in minutes
- Consistent results across all files
- Progress tracking
- Error handling per file

## 📝 DOC Template Support

Generate documents in Microsoft Word format!

- All document templates now support DOC format generation
- Compatible with Microsoft Word and other DOC readers
- Full formatting preserved
- Batch processing includes DOC documents
- ZIP downloads include DOC files

## 🖼️ Title Image Customization

Add project information to your title images!

### Method 1: Using Configuration File
1. Place your base image as `ATTACHED_ASSETS/title.jpeg`
2. Customize the data in `config/title_config.json`
3. Run `INSERT_TITLE.bat` to add project data
4. Find the customized image in `ATTACHED_ASSETS/title_modified.jpeg`

### Method 2: Using Excel Input Files
1. Run `CUSTOMIZE_TITLE.bat` to extract data from Excel files
2. Run `INSERT_TITLE.bat` with an Excel file path to use its data
3. Or run `PROCESS_ALL_TITLES.bat` to process all Excel files
4. Run `INSERT_TITLE_FROM_INPUT.bat` to generate title images for all input files

**Features:**
- Automatically adds project name, contract no, and work order no
- Fully customizable text positions, colors, and fonts
- Text overlay with shadow for better visibility
- Preserves image quality
- Configurable through JSON settings
- Supports automatic extraction from Excel Title sheets
- Batch processing for multiple files
- Generate customized images for each input file

## 📁 Structure

```
BillGeneratorUnified/
├── core/                  # Shared code
│   ├── processors/        # Excel & batch processing
│   ├── generators/        # Document generation
│   ├── config/            # Configuration system
│   └── ui/                # User interface components
├── config/                # 5 variant configurations
├── launchers/             # Launch scripts
├── templates/             # HTML templates
├── INPUT_FILES/           # Input data
└── OUTPUT_FILES/          # Generated outputs
```

## 💡 Why This is Brilliant

### Before (5 Separate Apps)
- 14,541 lines of code
- 95% duplication
- Fix bugs 5 times
- Add features 5 times
- Test 5 times

### After (Unified System)
- 3,050 lines of code
- 5% duplication
- Fix bugs once
- Add features once
- Test once

**Result:** 79% less code, 80% less maintenance! 🎉

## 🎯 Use Cases

### V01 - Standard
Best for: Regular bill generation with PDF export

### V02 - Light
Best for: Simple, fast bill generation

### V03 - Basic
Best for: Minimal features, maximum speed

### V04 - Advanced
Best for: **Batch processing multiple files**

### SmartBillFlow - Complete
Best for: All features including analytics

## 🛠️ Installation

```bash
# Install dependencies
pip install -r requirements.txt

# Launch
LAUNCH.bat
```

## 📖 Documentation

- Configuration Guide: See `config/` folder
- API Reference: Available at `/docs/ endpoint
- User Manual: Built-in help in each mode
- Security Documentation: See `backend/README.md`
- Monitoring Guide: See `MONITORING_LOGGING_SUMMARY.md`

## 🎉 What's New

- ✅ Batch processing for multiple files
- ✅ Enhanced UI with modern design
- ✅ Progress tracking
- ✅ Better error handling
- ✅ 5 variants in one app
- ✅ Configuration-driven features
- ✅ Enterprise-grade security
- ✅ Comprehensive monitoring
- ✅ API rate limiting
- ✅ CORS protection

## 👨‍💻 Created By

**Rajkumar Singh Chauhan**

---

**BillGenerator Unified - The Smart Way to Generate Bills** 🚀