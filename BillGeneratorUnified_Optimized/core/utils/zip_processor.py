
                try:
                    result = future.result()
                    result['group_name'] = group_name
                    results.append(result)
                except Exception as e:
                    results.append({
                        'group_name': group_name,
                        'status': 'error',
                        'error': str(e)
                    })
                    
        return results
        
    def get_operation_status(self, operation_id: str) -> Optional[Dict]:
        """Get status of ZIP operation"""
        with self.lock:
            return self.active_operations.get(operation_id)
            
    def get_active_operations(self) -> List[Dict]:
        """Get list of active operations"""
        with self.lock:
            return [
                {**info, 'operation_id': op_id}
                for op_id, info in self.active_operations.items()
                if info['status'] == 'active'
            ]
            
    def cleanup_operation(self, operation_id: str):
        """Clean up operation resources"""
        with self.lock:
            if operation_id in self.active_operations:
                del self.active_operations[operation_id]
                
    def estimate_zip_size(self, files: List[Union[str, Path]]) -> int:
        """Estimate ZIP file size"""
        total_size = 0
        
        for file_path in files:
            file_path = Path(file_path)
            if file_path.exists():
                total_size += file_path.stat().st_size
                
        # Estimate 30-70% compression ratio
        estimated_size = int(total_size * 0.5)
        return estimated_size
        
    def __enter__(self):
        return self
        
    def __exit__(self, exc_type, exc_val, exc_tb):
        # Clean up active operations
        with self.lock:
            self.active_operations.clear()

# Global ZIP processor instance
zip_processor = ZipProcessor()

def get_zip_processor() -> ZipProcessor:
    """Get the global ZIP processor instance"""
    return zip_processor