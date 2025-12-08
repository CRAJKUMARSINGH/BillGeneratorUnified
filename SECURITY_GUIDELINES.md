# Security Guidelines for BillGenerator Unified

This document outlines the security measures implemented in BillGenerator Unified and best practices for maintaining a secure deployment.

## 🔐 Environment Variable Management

### Implementation
The application now uses `python-dotenv` to manage configuration through environment variables, following security best practices:

1. **Environment Variable Loading**: Configuration values can be overridden using environment variables
2. **.env File Support**: Local development configuration through `.env` files
3. **.gitignore Protection**: `.env` files are excluded from version control

### Configuration Hierarchy
1. Environment variables (highest priority)
2. Configuration files (fallback)
3. Hardcoded defaults (lowest priority)

### Supported Environment Variables

#### Application Settings
- `APP_NAME` - Application name
- `APP_VERSION` - Application version
- `APP_MODE` - Application mode (Development/Production)

#### Feature Toggles
- `FEATURE_EXCEL_UPLOAD` - Enable Excel upload feature
- `FEATURE_ONLINE_ENTRY` - Enable online entry feature
- `FEATURE_BATCH_PROCESSING` - Enable batch processing
- `FEATURE_ADVANCED_PDF` - Enable advanced PDF features
- `FEATURE_ANALYTICS` - Enable analytics dashboard
- `FEATURE_CUSTOM_TEMPLATES` - Enable custom templates
- `FEATURE_API_ACCESS` - Enable API access

#### UI Settings
- `UI_THEME` - UI theme
- `UI_SHOW_DEBUG` - Show debug information
- `BRANDING_TITLE` - Application title
- `BRANDING_ICON` - Application icon
- `BRANDING_COLOR` - Branding color

#### Processing Settings
- `PROCESSING_MAX_FILE_SIZE_MB` - Maximum file size limit
- `PROCESSING_ENABLE_CACHING` - Enable caching
- `PROCESSING_PDF_ENGINE` - PDF engine to use
- `PROCESSING_AUTO_CLEAN_CACHE` - Auto-clean cache on startup

## 🔒 Security Best Practices

### 1. Environment Variable Security
```
# DO: Use .env files for local development
cp .env.example .env
# Edit .env with your values

# DON'T: Commit .env files to version control
# (Already protected by .gitignore)
```

### 2. Secret Management
For production deployments:
- Use system environment variables instead of `.env` files
- Rotate secrets regularly
- Limit access permissions to environment variables
- Use strong, randomly generated secrets

### 3. File Upload Security
The application includes built-in security measures:
- File type validation
- File size limits
- Content scanning for malicious patterns
- Secure temporary file handling
- Filename sanitization

### 4. Input Sanitization
- User inputs are sanitized to prevent XSS attacks
- HTML tags are stripped from text inputs
- Dangerous patterns are removed from user data

## 🛡️ Future Security Enhancements

### Password Hashing
When implementing user authentication:
```python
from werkzeug.security import generate_password_hash, check_password_hash

# Hash passwords during registration
hashed_password = generate_password_hash(password, method='pbkdf2:sha256')

# Verify passwords during login
if check_password_hash(hashed_password, password):
    # Password is correct
```

### Database Security
When adding database functionality:
- Use environment variables for database credentials
- Implement proper connection pooling
- Use parameterized queries to prevent SQL injection
- Encrypt sensitive data at rest

## 📋 Security Checklist

### For Developers
- [ ] Never hardcode secrets in source code
- [ ] Always use environment variables for configuration
- [ ] Test environment variable overrides
- [ ] Verify .gitignore includes .env files
- [ ] Document all environment variables

### For Deployments
- [ ] Set environment variables in the deployment environment
- [ ] Remove or secure .env files in production
- [ ] Use strong, unique secrets for production
- [ ] Regularly audit environment variable permissions
- [ ] Monitor for security updates to dependencies

## 🆘 Incident Response

If a security vulnerability is discovered:
1. Immediately rotate affected secrets
2. Review logs for unauthorized access
3. Update vulnerable code
4. Deploy security patches
5. Notify affected parties if necessary

## 📚 Additional Resources

- [OWASP Security Guidelines](https://owasp.org)
- [Python Security Best Practices](https://security.openstack.org/guidelines/dg_using-annotations-for-security.html)
- [Environment Variable Security](https://12factor.net/config)