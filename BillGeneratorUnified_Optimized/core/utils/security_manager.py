import os
import re
import hashlib
import magic
import logging
from typing import Dict, List, Optional, Any, Union, BinaryIO
from dataclasses import dataclass
from pathlib import Path
import tempfile
import threading
from datetime import datetime

@dataclass
class SecurityScanResult:
    is_safe: bool
    threats_detected: List[str]
    file_type: str
    file_size: int
    checksum: str
    scan_time: datetime
    risk_level: str  # LOW, MEDIUM, HIGH, CRITICAL

@dataclass
class SecurityPolicy:
    max_file_size: int = 100 * 1024 * 1024  # 100MB
    allowed_extensions: List[str] = None
    blocked_patterns: List[str] = None
    scan_for_malware: bool = True
    validate_checksum: bool = True
    quarantine_suspicious: bool = True

class SecurityManager:
    def __init__(self, policy: SecurityPolicy = None):
        self.policy = policy or SecurityPolicy()
        self.quarantine_dir = Path("quarantine")
        self.quarantine_dir.mkdir(exist_ok=True)
        
        # Initialize default allowed extensions
        if self.policy.allowed_extensions is None:
            self.policy.allowed_extensions = [
                '.pdf', '.doc', '.docx', '.xls', '.xlsx', '.txt', '.csv', 
                '.jpg', '.jpeg', '.png', '.gif', '.zip', '.rar', '.7z'
            ]
            
        # Initialize default blocked patterns
        if self.policy.blocked_patterns is None:
            self.policy.blocked_patterns = [
                r'<script[^>]*>.*?</script>',  # Script tags
                r'javascript:',  # JavaScript URLs
                r'vbscript:',  # VBScript URLs
                r'onload\s*=',  # Event handlers
                r'onerror\s*=',  # Error handlers
                r'eval\s*\(',  # eval() functions
                r'document\.write',  # Document write
                r'exec\s*\(',  # exec functions
                r'system\s*\(',  # System calls
                r'shell_exec\s*\(',  # Shell exec
                r'\.exe',  # Executable files
                r'\.bat',  # Batch files
                r'\.cmd',  # Command files
                r'\.scr',  # Screensaver files
                r'\.vbs',  # VBScript files
                r'\.js',  # JavaScript files (if not allowed)
            ]
            
        self.logger = logging.getLogger(__name__)
        self.scan_cache: Dict[str, SecurityScanResult] = {}
        self.lock = threading.RLock()
        
        # Compile regex patterns
        self.blocked_regex = [re.compile(pattern, re.IGNORECASE | re.DOTALL) 
                             for pattern in self.policy.blocked_patterns]
        
    def scan_file(self, file_path: Union[str, Path, BinaryIO], 
                  filename: str = None) -> SecurityScanResult:
        """Scan file for security threats"""
        with self.lock:
            # Handle different input types
            if isinstance(file_path, (str, Path)):
                file_path = Path(file_path)
                if not file_path.exists():
                    raise FileNotFoundError(f"File not found: {file_path}")
                    
                filename = filename or file_path.name
                file_size = file_path.stat().st_size
                
                # Calculate checksum
                checksum = self._calculate_checksum(file_path)
                
                # Check cache first
                cache_key = f"{filename}:{checksum}"
                if cache_key in self.scan_cache:
                    return self.scan_cache[cache_key]
                    
                # Read file content
                with open(file_path, 'rb') as f:
                    content = f.read()
                    
            else:  # BinaryIO
                content = file_path.read()
                filename = filename or "unknown_file"
                file_size = len(content)
                checksum = hashlib.sha256(content).hexdigest()
                
                # Check cache
                cache_key = f"{filename}:{checksum}"
                if cache_key in self.scan_cache:
                    return self.scan_cache[cache_key]
                    
            # Perform security checks
            scan_result = self._perform_security_scan(
                content, filename, file_size, checksum
            )
            
            # Cache result
            self.scan_cache[cache_key] = scan_result
            
            # Handle suspicious files
            if not scan_result.is_safe and self.policy.quarantine_suspicious:
                self._quarantine_file(content, filename, scan_result)
                
            self.logger.info(f"Security scan completed for {filename}: "
                           f"Risk Level: {scan_result.risk_level}, "
                           f"Threats: {len(scan_result.threats_detected)}")
            
            return scan_result
            
    def _perform_security_scan(self, content: bytes, filename: str, 
                              file_size: int, checksum: str) -> SecurityScanResult:
        """Perform comprehensive security scan"""
        threats_detected = []
        risk_level = "LOW"
        
        # 1. File size check
        if file_size > self.policy.max_file_size:
            threats_detected.append(f"File size ({file_size} bytes) exceeds maximum allowed ({self.policy.max_file_size} bytes)")
            risk_level = "HIGH"
            
        # 2. File extension check
        file_ext = Path(filename).suffix.lower()
        if file_ext not in self.policy.allowed_extensions:
            threats_detected.append(f"File extension '{file_ext}' not in allowed list")
            risk_level = "MEDIUM"
            
        # 3. Content-based threat detection
        try:
            content_str = content.decode('utf-8', errors='ignore')
            
            # Check for blocked patterns
            for pattern in self.blocked_regex:
                matches = pattern.findall(content_str)
                if matches:
                    threats_detected.append(f"Suspicious pattern detected: {pattern.pattern}")
                    risk_level = "HIGH"
                    
            # Check for suspicious strings
            suspicious_strings = [
                'base64_decode', 'eval(', 'exec(', 'system(', 'shell_exec',
                'document.cookie', 'window.location', 'alert(', 'confirm(',
                'prompt(', 'setTimeout(', 'setInterval('
            ]
            
            for suspicious in suspicious_strings:
                if suspicious in content_str.lower():
                    threats_detected.append(f"Suspicious string found: {suspicious}")
                    if risk_level == "LOW":
                        risk_level = "MEDIUM"
                        
        except UnicodeDecodeError:
            # Binary file - skip string-based checks
            pass
            
        # 4. File type verification
        try:
            detected_type = magic.from_buffer(content, mime=True)
            
            # Check for executable files
            if detected_type.startswith('application/x-executable') or detected_type.startswith('application/x-msdownload'):
                threats_detected.append(f"Executable file detected: {detected_type}")
                risk_level = "CRITICAL"
                
            # Check for suspicious MIME types
            suspicious_mime_types = [
                'application/x-msdos-program', 'application/x-msdownload',
                'application/x-executable', 'application/x-sh'
            ]
            
            if detected_type in suspicious_mime_types:
                threats_detected.append(f"Suspicious MIME type: {detected_type}")
                risk_level = "CRITICAL"
                
        except Exception as e:
            self.logger.warning(f"Could not determine file type: {e}")
            detected_type = "unknown"
            
        # 5. Header analysis
        header_threats = self._analyze_file_header(content)
        threats_detected.extend(header_threats)
        if header_threats and risk_level == "LOW":
            risk_level = "MEDIUM"
            
        # 6. Entropy analysis (for encrypted/packed content)
        entropy = self._calculate_entropy(content)
        if entropy > 7.5:  # High entropy indicates possible encryption/packing
            threats_detected.append(f"High entropy content detected: {entropy:.2f}")
            if risk_level in ["LOW", "MEDIUM"]:
                risk_level = "HIGH"
                
        # Determine final safety
        is_safe = len(threats_detected) == 0
        
        return SecurityScanResult(
            is_safe=is_safe,
            threats_detected=threats_detected,
            file_type=detected_type,
            file_size=file_size,
            checksum=checksum,
            scan_time=datetime.now(),
            risk_level=risk_level
        )
        
    def _analyze_file_header(self, content: bytes) -> List[str]:
        """Analyze file header for threats"""
        threats = []
        
        if len(content) < 4:
            return threats
            
        # Check for executable signatures
        executable_signatures = [
            b'MZ',  # Windows PE
            b'\x7fELF',  # Linux ELF
            b'\xca\xfe\xba\xbe',  # Java class
            b'\xfe\xed\xfa\xce',  # Mach-O binary
            b'\xfe\xed\xfa\xcf',  # Mach-O binary (64-bit)
        ]
        
        for sig in executable_signatures:
            if content.startswith(sig):
                threats.append(f"Executable signature detected: {sig.hex()}")
                break
                
        return threats
        
    def _calculate_entropy(self, content: bytes) -> float:
        """Calculate Shannon entropy of content"""
        if not content:
            return 0.0
            
        # Count byte frequencies
        byte_counts = {}
        for byte in content:
            byte_counts[byte] = byte_counts.get(byte, 0) + 1
            
        # Calculate entropy
        entropy = 0.0
        content_len = len(content)
        
        for count in byte_counts.values():
            probability = count / content_len
            entropy -= probability * (probability.bit_length() - 1)
            
        return entropy
        
    def _calculate_checksum(self, file_path: Path) -> str:
        """Calculate SHA-256 checksum"""
        sha256_hash = hashlib.sha256()
        with open(file_path, "rb") as f:
            for chunk in iter(lambda: f.read(4096), b""):
                sha256_hash.update(chunk)
        return sha256_hash.hexdigest()
        
    def _quarantine_file(self, content: bytes, filename: str, 
                        scan_result: SecurityScanResult):
        """Move suspicious file to quarantine"""
        try:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            quarantine_name = f"{timestamp}_{filename}_{scan_result.checksum[:8]}.quarantine"
            quarantine_path = self.quarantine_dir / quarantine_name
            
            with open(quarantine_path, 'wb') as f:
                f.write(content)
                
            # Create metadata file
            metadata = {
                'original_filename': filename,
                'quarantine_time': scan_result.scan_time.isoformat(),
                'risk_level': scan_result.risk_level,
                'threats_detected': scan_result.threats_detected,
                'file_size': scan_result.file_size,
                'checksum': scan_result.checksum
            }
            
            metadata_path = quarantine_path.with_suffix('.meta')
            with open(metadata_path, 'w') as f:
                import json
                json.dump(metadata, f, indent=2)
                
            self.logger.warning(f"File quarantined: {filename} -> {quarantine_path}")
            
        except Exception as e:
            self.logger.error(f"Failed to quarantine file {filename}: {e}")
            
    def validate_path(self, file_path: Union[str, Path]) -> bool:
        """Validate file path against directory traversal"""
        try:
            path = Path(file_path).resolve()
            
            # Check for directory traversal
            if '..' in str(path):
                return False
                
            # Check if path is within allowed directories
            # Add your allowed directories here
            allowed_dirs = [Path.cwd(), Path.temp_dir()]
            
            return any(
                str(path).startswith(str(allowed_dir))
                for allowed_dir in allowed_dirs
            )
            
        except Exception:
            return False
            
    def sanitize_filename(self, filename: str) -> str:
        """Sanitize filename for safe storage"""
        # Remove dangerous characters
        dangerous_chars = ['..', '/', '\\', ':', '*', '?', '"', '<', '>', '|']
        sanitized = filename
        
        for char in dangerous_chars:
            sanitized = sanitized.replace(char, '_')
            
        # Limit length
        if len(sanitized) > 255:
            name, ext = os.path.splitext(sanitized)
            sanitized = name[:255-len(ext)] + ext
            
        return sanitized
        
    def get_security_report(self) -> Dict[str, Any]:
        """Get comprehensive security report"""
        with self.lock:
            total_scans = len(self.scan_cache)
            safe_files = sum(1 for result in self.scan_cache.values() if result.is_safe)
            suspicious_files = total_scans - safe_files
            
            risk_distribution = {}
            for result in self.scan_cache.values():
                risk_distribution[result.risk_level] = risk_distribution.get(result.risk_level, 0) + 1
                
            quarantine_count = len(list(self.quarantine_dir.glob("*.quarantine")))
            
            return {
                'total_files_scanned': total_scans,
                'safe_files': safe_files,
                'suspicious_files': suspicious_files,
                'quarantined_files': quarantine_count,
                'risk_distribution': risk_distribution,
                'scan_cache_size': len(self.scan_cache),
                'policy': {
                    'max_file_size': self.policy.max_file_size,
                    'allowed_extensions': self.policy.allowed_extensions,
                    'scan_for_malware': self.policy.scan_for_malware,
                    'quarantine_suspicious': self.policy.quarantine_suspicious
                }
            }
            
    def clear_scan_cache(self):
        """Clear scan cache"""
        with self.lock:
            self.scan_cache.clear()
            self.logger.info("Security scan cache cleared")

# Global security manager instance
security_manager = SecurityManager()

def get_security_manager() -> SecurityManager:
    """Get the global security manager instance"""
    return security_manager