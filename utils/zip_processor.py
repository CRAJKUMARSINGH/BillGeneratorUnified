from core.utils.zip_processor import ZipProcessor, ZipConfig

# Configure ZIP processing
config = ZipConfig(
    compression_level=6,      # 0-9 compression level
    max_memory_mb=100,        # Memory limit
    max_file_size_mb=50       # Max individual file size
)

# Create ZIP with progress tracking
with ZipProcessor(config) as processor:
    def progress_callback(progress, status):
        print(f"Progress: {progress}% - {status}")
    
    processor.set_progress_callback(progress_callback)
    
    # From file paths
    zip_data, metrics = processor.create_zip_from_files(file_list)
    
    # From in-memory data
    data_dict = {"file1.txt": "content", "file2.html": "<html>...</html>"}
    zip_data, metrics = processor.create_zip_from_data(data_dict)