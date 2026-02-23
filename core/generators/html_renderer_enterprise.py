"""
Enterprise-Grade HTML Rendering Engine
Production-ready structured HTML generation with Jinja2 templating.

Author: Senior Python Web Rendering Engineer
Standards: HTML5, Jinja2, Modular Architecture, Security Best Practices
"""

import logging
from dataclasses import dataclass, field
from enum import Enum
from pathlib import Path
from typing import Any, Dict, List, Optional, Union
from datetime import datetime
import html

import pandas as pd
from jinja2 import Environment, FileSystemLoader, select_autoescape, TemplateNotFound
from jinja2.sandbox import SandboxedEnvironment


# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


# ============================================================================
# ENUMS AND CONSTANTS
# ============================================================================

class DocumentType(Enum):
    """Supported document types."""
    FIRST_PAGE = "first_page"
    DEVIATION_STATEMENT = "deviation_statement"
    NOTE_SHEET = "note_sheet"
    EXTRA_ITEMS = "extra_items"
    CERTIFICATE_II = "certificate_ii"
    CERTIFICATE_III = "certificate_iii"


class OutputFormat(Enum):
    """Supported output formats."""
    HTML5 = "html5"
    PDF_READY = "pdf_ready"
    PRINT_READY = "print_ready"


# Template configuration
TEMPLATE_DIR = Path(__file__).parent.parent.parent / "templates"
DEFAULT_ENCODING = "utf-8"


# ============================================================================
# CUSTOM EXCEPTIONS
# ============================================================================

class HTMLRenderingError(Exception):
    """Base exception for HTML rendering errors."""
    pass


class TemplateError(HTMLRenderingError):
    """Raised when template operations fail."""
    pass


class ValidationError(HTMLRenderingError):
    """Raised when data validation fails."""
    pass


class SecurityError(HTMLRenderingError):
    """Raised when security checks fail."""
    pass


# ============================================================================
# DATA CLASSES
# ============================================================================

@dataclass
class RenderContext:
    """Context data for template rendering."""
    data: Dict[str, Any]
    document_type: DocumentType
    output_format: OutputFormat = OutputFormat.HTML5
    metadata: Dict[str, Any] = field(default_factory=dict)
    
    def __post_init__(self):
        """Validate context after initialization."""
        if not self.data:
            raise ValidationError("Render context data cannot be empty")


@dataclass
class RenderResult:
    """Result of rendering operation."""
    success: bool
    html_content: Optional[str] = None
    document_type: Optional[DocumentType] = None
    errors: List[str] = field(default_factory=list)
    warnings: List[str] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)


# ============================================================================
# SECURITY UTILITIES
# ============================================================================

class SecurityManager:
    """Manages security for HTML rendering."""
    
    @staticmethod
    def sanitize_html(content: str) -> str:
        """
        Sanitize HTML content to prevent XSS.
        
        Args:
            content: Raw HTML content
            
        Returns:
            Sanitized HTML content
        """
        if not content:
            return ""
        
        # Escape HTML entities
        return html.escape(str(content))
    
    @staticmethod
    def validate_template_name(template_name: str) -> bool:
        """
        Validate template name to prevent path traversal.
        
        Args:
            template_name: Name of template file
            
        Returns:
            True if valid, False otherwise
        """
        # Check for path traversal attempts
        if ".." in template_name or "/" in template_name or "\\" in template_name:
            return False
        
        # Check for valid extension
        if not template_name.endswith(('.html', '.htm', '.jinja2')):
            return False
        
        return True


# ============================================================================
# DATA PROCESSOR
# ============================================================================

class DataProcessor:
    """Processes and validates data for rendering."""
    
    @staticmethod
    def safe_float(value: Any, default: float = 0.0) -> float:
        """
        Safely convert value to float.
        
        Args:
            value: Value to convert
            default: Default value if conversion fails
            
        Returns:
            Float value
        """
        if pd.isna(value) or value is None or value == '':
            return default
        try:
            return float(value)
        except (ValueError, TypeError):
            return default
    
    @staticmethod
    def safe_string(value: Any, default: str = "") -> str:
        """
        Safely convert value to string.
        
        Args:
            value: Value to convert
            default: Default value if conversion fails
            
        Returns:
            String value
        """
        if pd.isna(value) or value is None:
            return default
        return str(value).strip()
    
    @staticmethod
    def format_currency(value: float, decimals: int = 2) -> str:
        """
        Format value as currency.
        
        Args:
            value: Numeric value
            decimals: Number of decimal places
            
        Returns:
            Formatted currency string
        """
        if value == 0:
            return ""
        return f"{value:,.{decimals}f}"
    
    @staticmethod
    def format_date(date_value: Any, format_str: str = "%d/%m/%Y") -> str:
        """
        Format date value.
        
        Args:
            date_value: Date value (datetime, string, or timestamp)
            format_str: Output format string
            
        Returns:
            Formatted date string
        """
        if pd.isna(date_value) or date_value is None:
            return ""
        
        try:
            if isinstance(date_value, pd.Timestamp):
                return date_value.strftime(format_str)
            elif isinstance(date_value, datetime):
                return date_value.strftime(format_str)
            elif isinstance(date_value, str):
                # Try to parse string date
                parsed_date = pd.to_datetime(date_value)
                return parsed_date.strftime(format_str)
            else:
                return str(date_value)
        except Exception as e:
            logger.warning(f"Failed to format date {date_value}: {e}")
            return str(date_value)
    
    @staticmethod
    def number_to_words(num: int) -> str:
        """
        Convert number to words (Indian numbering system).
        
        Args:
            num: Integer number
            
        Returns:
            Number in words
        """
        ones = ['', 'One', 'Two', 'Three', 'Four', 'Five', 'Six', 'Seven', 'Eight', 'Nine']
        teens = ['Ten', 'Eleven', 'Twelve', 'Thirteen', 'Fourteen', 'Fifteen', 
                 'Sixteen', 'Seventeen', 'Eighteen', 'Nineteen']
        tens = ['', '', 'Twenty', 'Thirty', 'Forty', 'Fifty', 'Sixty', 'Seventy', 'Eighty', 'Ninety']
        
        if num == 0:
            return 'Zero'
        
        if num < 10:
            return ones[num]
        elif num < 20:
            return teens[num - 10]
        elif num < 100:
            return tens[num // 10] + ('' if num % 10 == 0 else ' ' + ones[num % 10])
        elif num < 1000:
            return ones[num // 100] + ' Hundred' + ('' if num % 100 == 0 else ' ' + DataProcessor.number_to_words(num % 100))
        elif num < 100000:
            return DataProcessor.number_to_words(num // 1000) + ' Thousand' + ('' if num % 1000 == 0 else ' ' + DataProcessor.number_to_words(num % 1000))
        elif num < 10000000:
            return DataProcessor.number_to_words(num // 100000) + ' Lakh' + ('' if num % 100000 == 0 else ' ' + DataProcessor.number_to_words(num % 100000))
        elif num < 1000000000:
            return DataProcessor.number_to_words(num // 10000000) + ' Crore' + ('' if num % 10000000 == 0 else ' ' + DataProcessor.number_to_words(num % 10000000))
        else:
            return str(num)  # For very large numbers



# ============================================================================
# TEMPLATE MANAGER
# ============================================================================

class TemplateManager:
    """Manages Jinja2 templates with caching and security."""
    
    def __init__(
        self,
        template_dir: Union[str, Path] = TEMPLATE_DIR,
        enable_sandbox: bool = True,
        enable_cache: bool = True
    ):
        """
        Initialize template manager.
        
        Args:
            template_dir: Directory containing templates
            enable_sandbox: Use sandboxed environment for security
            enable_cache: Enable template caching
        """
        self.template_dir = Path(template_dir)
        self.enable_sandbox = enable_sandbox
        self.enable_cache = enable_cache
        
        # Validate template directory
        if not self.template_dir.exists():
            raise TemplateError(f"Template directory not found: {self.template_dir}")
        
        # Initialize Jinja2 environment
        if enable_sandbox:
            self.env = SandboxedEnvironment(
                loader=FileSystemLoader(str(self.template_dir)),
                autoescape=select_autoescape(['html', 'htm', 'xml']),
                enable_async=False
            )
        else:
            self.env = Environment(
                loader=FileSystemLoader(str(self.template_dir)),
                autoescape=select_autoescape(['html', 'htm', 'xml']),
                enable_async=False
            )
        
        # Register custom filters
        self._register_filters()
        
        # Template cache
        self._cache = {} if enable_cache else None
        
        logger.info(
            f"TemplateManager initialized: "
            f"dir={self.template_dir}, sandbox={enable_sandbox}, cache={enable_cache}"
        )
    
    def _register_filters(self):
        """Register custom Jinja2 filters."""
        self.env.filters['currency'] = DataProcessor.format_currency
        self.env.filters['date_format'] = DataProcessor.format_date
        self.env.filters['safe_float'] = DataProcessor.safe_float
        self.env.filters['safe_string'] = DataProcessor.safe_string
        self.env.filters['number_to_words'] = DataProcessor.number_to_words
    
    def get_template(self, template_name: str):
        """
        Get template by name with caching.
        
        Args:
            template_name: Name of template file
            
        Returns:
            Jinja2 Template object
        """
        # Validate template name
        if not SecurityManager.validate_template_name(template_name):
            raise SecurityError(f"Invalid template name: {template_name}")
        
        # Check cache
        if self.enable_cache and template_name in self._cache:
            return self._cache[template_name]
        
        # Load template
        try:
            template = self.env.get_template(template_name)
            
            # Cache template
            if self.enable_cache:
                self._cache[template_name] = template
            
            logger.debug(f"Loaded template: {template_name}")
            return template
            
        except TemplateNotFound:
            raise TemplateError(f"Template not found: {template_name}")
        except Exception as e:
            raise TemplateError(f"Failed to load template {template_name}: {e}")
    
    def render_template(
        self,
        template_name: str,
        context: Dict[str, Any]
    ) -> str:
        """
        Render template with context data.
        
        Args:
            template_name: Name of template file
            context: Context data for rendering
            
        Returns:
            Rendered HTML string
        """
        try:
            template = self.get_template(template_name)
            html_content = template.render(**context)
            logger.debug(f"Rendered template: {template_name}")
            return html_content
        except Exception as e:
            logger.error(f"Failed to render template {template_name}: {e}")
            raise TemplateError(f"Template rendering failed: {e}")
    
    def list_templates(self) -> List[str]:
        """
        List all available templates.
        
        Returns:
            List of template names
        """
        templates = []
        for file_path in self.template_dir.glob("*.html"):
            templates.append(file_path.name)
        return sorted(templates)


# ============================================================================
# HTML RENDERER
# ============================================================================

class HTMLRenderer:
    """
    Enterprise-grade HTML renderer with Jinja2 templating.
    """
    
    # Document type to template mapping
    TEMPLATE_MAP = {
        DocumentType.FIRST_PAGE: "first_page.html",
        DocumentType.DEVIATION_STATEMENT: "deviation_statement.html",
        DocumentType.NOTE_SHEET: "note_sheet.html",
        DocumentType.EXTRA_ITEMS: "extra_items.html",
        DocumentType.CERTIFICATE_II: "certificate_ii.html",
        DocumentType.CERTIFICATE_III: "certificate_iii.html",
    }
    
    def __init__(
        self,
        template_dir: Union[str, Path] = TEMPLATE_DIR,
        enable_sandbox: bool = True,
        enable_cache: bool = True,
        validate_output: bool = True
    ):
        """
        Initialize HTML renderer.
        
        Args:
            template_dir: Directory containing templates
            enable_sandbox: Use sandboxed environment for security
            enable_cache: Enable template caching
            validate_output: Validate rendered HTML
        """
        self.template_manager = TemplateManager(
            template_dir=template_dir,
            enable_sandbox=enable_sandbox,
            enable_cache=enable_cache
        )
        self.validate_output = validate_output
        self.data_processor = DataProcessor()
        self.security_manager = SecurityManager()
        
        logger.info(
            f"HTMLRenderer initialized: "
            f"validate={validate_output}"
        )
    
    def render_document(
        self,
        document_type: DocumentType,
        data: Dict[str, Any],
        output_format: OutputFormat = OutputFormat.HTML5
    ) -> RenderResult:
        """
        Render a single document.
        
        Args:
            document_type: Type of document to render
            data: Data for rendering
            output_format: Output format
            
        Returns:
            RenderResult with rendered HTML or errors
        """
        result = RenderResult(success=False, document_type=document_type)
        
        try:
            # Get template name
            template_name = self.TEMPLATE_MAP.get(document_type)
            if not template_name:
                result.errors.append(f"No template mapping for document type: {document_type}")
                return result
            
            # Prepare render context
            context = self._prepare_context(data, document_type, output_format)
            
            # Render template
            html_content = self.template_manager.render_template(template_name, context)
            
            # Validate output if enabled
            if self.validate_output:
                validation_errors = self._validate_html(html_content)
                if validation_errors:
                    result.warnings.extend(validation_errors)
            
            # Success
            result.success = True
            result.html_content = html_content
            result.metadata = {
                'template': template_name,
                'output_format': output_format.value,
                'content_length': len(html_content)
            }
            
            logger.info(f"Successfully rendered document: {document_type.value}")
            
        except Exception as e:
            error_msg = f"Failed to render document {document_type.value}: {e}"
            logger.error(error_msg)
            result.errors.append(error_msg)
        
        return result
    
    def render_all_documents(
        self,
        data: Dict[str, Any],
        include_extra_items: bool = True,
        output_format: OutputFormat = OutputFormat.HTML5
    ) -> Dict[str, RenderResult]:
        """
        Render all document types.
        
        Args:
            data: Data for rendering
            include_extra_items: Include extra items document
            output_format: Output format
            
        Returns:
            Dictionary mapping document names to RenderResults
        """
        results = {}
        
        # Define documents to render
        document_types = [
            DocumentType.FIRST_PAGE,
            DocumentType.DEVIATION_STATEMENT,
            DocumentType.NOTE_SHEET,
            DocumentType.CERTIFICATE_II,
            DocumentType.CERTIFICATE_III,
        ]
        
        # Add extra items if requested and data available
        if include_extra_items and self._has_extra_items(data):
            document_types.append(DocumentType.EXTRA_ITEMS)
        
        # Render each document
        for doc_type in document_types:
            result = self.render_document(doc_type, data, output_format)
            results[doc_type.value] = result
        
        # Log summary
        success_count = sum(1 for r in results.values() if r.success)
        logger.info(
            f"Rendered {success_count}/{len(results)} documents successfully"
        )
        
        return results
    
    def _prepare_context(
        self,
        data: Dict[str, Any],
        document_type: DocumentType,
        output_format: OutputFormat
    ) -> Dict[str, Any]:
        """
        Prepare context data for template rendering.
        
        Args:
            data: Raw data
            document_type: Document type
            output_format: Output format
            
        Returns:
            Prepared context dictionary
        """
        # Base context
        context = {
            'data': data,
            'document_type': document_type.value,
            'output_format': output_format.value,
            'current_date': datetime.now().strftime('%d/%m/%Y'),
            'current_datetime': datetime.now(),
        }
        
        # Add utility functions
        context['safe_float'] = self.data_processor.safe_float
        context['safe_string'] = self.data_processor.safe_string
        context['format_currency'] = self.data_processor.format_currency
        context['format_date'] = self.data_processor.format_date
        context['number_to_words'] = self.data_processor.number_to_words
        
        return context
    
    def _validate_html(self, html_content: str) -> List[str]:
        """
        Validate rendered HTML.
        
        Args:
            html_content: HTML content to validate
            
        Returns:
            List of validation errors/warnings
        """
        warnings = []
        
        # Basic validation checks
        if not html_content:
            warnings.append("HTML content is empty")
            return warnings
        
        # Check for DOCTYPE
        if '<!DOCTYPE' not in html_content:
            warnings.append("Missing DOCTYPE declaration")
        
        # Check for basic HTML structure
        if '<html' not in html_content.lower():
            warnings.append("Missing <html> tag")
        
        if '<head' not in html_content.lower():
            warnings.append("Missing <head> tag")
        
        if '<body' not in html_content.lower():
            warnings.append("Missing <body> tag")
        
        # Check for charset
        if 'charset' not in html_content.lower():
            warnings.append("Missing charset declaration")
        
        return warnings
    
    def _has_extra_items(self, data: Dict[str, Any]) -> bool:
        """
        Check if data contains extra items.
        
        Args:
            data: Data dictionary
            
        Returns:
            True if extra items exist
        """
        extra_items = data.get('extra_items_data')
        if isinstance(extra_items, pd.DataFrame):
            return not extra_items.empty
        elif isinstance(extra_items, list):
            return len(extra_items) > 0
        return False


# ============================================================================
# CONVENIENCE FUNCTIONS
# ============================================================================

def render_document(
    document_type: DocumentType,
    data: Dict[str, Any],
    **kwargs
) -> RenderResult:
    """
    Convenience function to render a single document.
    
    Args:
        document_type: Type of document to render
        data: Data for rendering
        **kwargs: Additional arguments for HTMLRenderer
        
    Returns:
        RenderResult
    """
    renderer = HTMLRenderer(**kwargs)
    return renderer.render_document(document_type, data)


def render_all_documents(
    data: Dict[str, Any],
    **kwargs
) -> Dict[str, RenderResult]:
    """
    Convenience function to render all documents.
    
    Args:
        data: Data for rendering
        **kwargs: Additional arguments for HTMLRenderer
        
    Returns:
        Dictionary of RenderResults
    """
    renderer = HTMLRenderer(**kwargs)
    return renderer.render_all_documents(data)
