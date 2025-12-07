from typing import Dict, Any, Optional, Callable, TypeVar, Type
from abc import ABC, abstractmethod
import threading
import time
import logging
from dataclasses import dataclass
from enum import Enum

T = TypeVar('T')

class ServiceLifetime(Enum):
    TRANSIENT = "transient"
    SINGLETON = "singleton"
    SCOPED = "scoped"

@dataclass
class ServiceDescriptor:
    service_type: Type
    implementation_type: Type
    lifetime: ServiceLifetime
    factory: Optional[Callable[[], Any]] = None
    instance: Optional[Any] = None

class DIContainer:
    def __init__(self):
        self._services: Dict[Type, ServiceDescriptor] = {}
        self._singletons: Dict[Type, Any] = {}
        self._scoped_instances: Dict[str, Dict[Type, Any]] = {}
        self._lock = threading.RLock()
        self.logger = logging.getLogger(__name__)
        
    def register_transient(self, service_type: Type[T], implementation_type: Type[T]) -> 'DIContainer':
        """Register transient service (new instance each time)"""
        with self._lock:
            descriptor = ServiceDescriptor(
                service_type=service_type,
                implementation_type=implementation_type,
                lifetime=ServiceLifetime.TRANSIENT
            )
            self._services[service_type] = descriptor
            self.logger.debug(f"Registered transient: {service_type.__name__}")
        return self
        
    def register_singleton(self, service_type: Type[T], implementation_type: Type[T]) -> 'DIContainer':
        """Register singleton service (single instance for container lifetime)"""
        with self._lock:
            descriptor = ServiceDescriptor(
                service_type=service_type,
                implementation_type=implementation_type,
                lifetime=ServiceLifetime.SINGLETON
            )
            self._services[service_type] = descriptor
            self.logger.debug(f"Registered singleton: {service_type.__name__}")
        return self
        
    def register_singleton_instance(self, service_type: Type[T], instance: T) -> 'DIContainer':
        """Register singleton instance"""
        with self._lock:
            descriptor = ServiceDescriptor(
                service_type=service_type,
                implementation_type=type(instance),
                lifetime=ServiceLifetime.SINGLETON,
                instance=instance
            )
            self._services[service_type] = descriptor
            self._singletons[service_type] = instance
            self.logger.debug(f"Registered singleton instance: {service_type.__name__}")
        return self
        
    def register_scoped(self, service_type: Type[T], implementation_type: Type[T]) -> 'DIContainer':
        """Register scoped service (single instance per scope)"""
        with self._lock:
            descriptor = ServiceDescriptor(
                service_type=service_type,
                implementation_type=implementation_type,
                lifetime=ServiceLifetime.SCOPED
            )
            self._services[service_type] = descriptor
            self.logger.debug(f"Registered scoped: {service_type.__name__}")
        return self
        
    def register_factory(self, service_type: Type[T], factory: Callable[[], T]) -> 'DIContainer':
        """Register service with factory function"""
        with self._lock:
            descriptor = ServiceDescriptor(
                service_type=service_type,
                implementation_type=type(None),
                lifetime=ServiceLifetime.TRANSIENT,
                factory=factory
            )
            self._services[service_type] = descriptor
            self.logger.debug(f"Registered factory: {service_type.__name__}")
        return self
        
    def resolve(self, service_type: Type[T]) -> T:
        """Resolve service instance"""
        with self._lock:
            if service_type not in self._services:
                raise ValueError(f"Service {service_type.__name__} not registered")
                
            descriptor = self._services[service_type]
            
            # Check for existing singleton
            if descriptor.lifetime == ServiceLifetime.SINGLETON:
                if service_type in self._singletons:
                    return self._singletons[service_type]
                    
            # Create new instance
            instance = self._create_instance(descriptor)
            
            # Store singleton
            if descriptor.lifetime == ServiceLifetime.SINGLETON:
                self._singletons[service_type] = instance
                
            return instance
            
    def _create_instance(self, descriptor: ServiceDescriptor) -> Any:
        """Create instance of service"""
        try:
            if descriptor.factory:
                return descriptor.factory()
                
            if descriptor.instance:
                return descriptor.instance
                
            # Try to create instance with dependency injection
            implementation_type = descriptor.implementation_type
            
            # Get constructor parameters
            import inspect
            sig = inspect.signature(implementation_type.__init__)
            
            # Resolve constructor dependencies
            kwargs = {}
            for param_name, param in sig.parameters.items():
                if param_name == 'self':
                    continue
                    
                if param.annotation != inspect.Parameter.empty:
                    dependency_type = param.annotation
                    if dependency_type in self._services:
                        kwargs[param_name] = self.resolve(dependency_type)
                        
            return implementation_type(**kwargs)
            
        except Exception as e:
            self.logger.error(f"Failed to create instance of {descriptor.service_type.__name__}: {e}")
            raise
            
    def create_scope(self) -> 'DIScope':
        """Create new dependency injection scope"""
        return DIScope(self)
        
    def get_service_info(self) -> Dict[str, Any]:
        """Get information about registered services"""
        with self._lock:
            services_info = {}
            
            for service_type, descriptor in self._services.items():
                services_info[service_type.__name__] = {
                    'lifetime': descriptor.lifetime.value,
                    'implementation': descriptor.implementation_type.__name__,
                    'has_factory': descriptor.factory is not None,
                    'is_singleton_cached': service_type in self._singletons
                }
                
            return {
                'total_services': len(self._services),
                'singleton_instances': len(self._singletons),
                'services': services_info
            }

class DIScope:
    """Dependency injection scope for managing scoped services"""
    
    def __init__(self, container: DIContainer):
        self.container = container
        self._scope_id = f"scope_{int(time.time() * 1000)}"
        self._scoped_instances: Dict[Type, Any] = {}
        self.logger = logging.getLogger(__name__)
        
    def resolve(self, service_type: Type[T]) -> T:
        """Resolve service within scope"""
        with self.container._lock:
            if service_type not in self.container._services:
                raise ValueError(f"Service {service_type.__name__} not registered")
                
            descriptor = self.container._services[service_type]
            
            # Handle scoped services
            if descriptor.lifetime == ServiceLifetime.SCOPED:
                if service_type in self._scoped_instances:
                    return self._scoped_instances[service_type]
                    
                # Create scoped instance
                instance = self.container._create_instance(descriptor)
                self._scoped_instances[service_type] = instance
                return instance
                
            # For other lifetimes, delegate to container
            return self.container.resolve(service_type)
            
    def dispose(self):
        """Dispose scope and clean up scoped instances"""
        with self.container._lock:
            # Call dispose on scoped instances if available
            for instance in self._scoped_instances.values():
                if hasattr(instance, 'dispose') and callable(getattr(instance, 'dispose')):
                    try:
                        instance.dispose()
                    except Exception as e:
                        self.logger.error(f"Error disposing scoped instance: {e}")
                        
            self._scoped_instances.clear()
            
    def __enter__(self):
        return self
        
    def __exit__(self, exc_type, exc_val, exc_tb):
        self.dispose()

# Global container instance
_container = DIContainer()

def get_container() -> DIContainer:
    """Get the global dependency injection container"""
    return _container

def configure_services(configurator: Callable[[DIContainer], None]):
    """Configure dependency injection services"""
    configurator(_container)

def resolve(service_type: Type[T]) -> T:
    """Resolve service from global container"""
    return _container.resolve(service_type)

def create_scope() -> DIScope:
    """Create new scope from global container"""
    return _container.create_scope()

# Example service interfaces
class IService(ABC):
    @abstractmethod
    def execute(self, *args, **kwargs):
        pass

class IMemoryService(IService):
    @abstractmethod
    def get_memory_usage(self) -> Dict[str, Any]:
        pass

class ICacheService(IService):
    @abstractmethod
    def get(self, key: str) -> Any:
        pass
        
    @abstractmethod
    def set(self, key: str, value: Any) -> None:
        pass

class ISecurityService(IService):
    @abstractmethod
    def scan_file(self, file_path: str) -> bool:
        pass

# Example service implementations
class MemoryService(IMemoryService):
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        
    def execute(self, *args, **kwargs):
        return self.get_memory_usage()
        
    def get_memory_usage(self) -> Dict[str, Any]:
        import psutil
        memory = psutil.virtual_memory()
        return {
            'total': memory.total,
            'available': memory.available,
            'percent': memory.percent
        }

class CacheService(ICacheService):
    def __init__(self):
        self._cache = {}
        self.logger = logging.getLogger(__name__)
        
    def execute(self, *args, **kwargs):
        pass
        
    def get(self, key: str) -> Any:
        return self._cache.get(key)
        
    def set(self, key: str, value: Any) -> None:
        self._cache[key] = value

class SecurityService(ISecurityService):
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        
    def execute(self, *args, **kwargs):
        pass
        
    def scan_file(self, file_path: str) -> bool:
        # Simplified security check
        return True

def default_service_configuration():
    """Default service configuration"""
    container = get_container()
    
    # Register services
    container.register_singleton(IMemoryService, MemoryService)
    container.register_singleton(ICacheService, CacheService)
    container.register_singleton(ISecurityService, SecurityService)
    
    return container