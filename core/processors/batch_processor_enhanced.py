"""
Enhanced Batch Processor with Parallel Processing for BillGeneratorUnified
Combines the features of the original batch processor with parallel processing capabilities
"""

import os
import time
import threading
from pathlib import Path
from typing import List, Dict, Any, Optional, Callable
from dataclasses import dataclass, field
from concurrent.futures import ThreadPoolExecutor, Future, as_completed
import logging
from queue import Queue, Empty
import psutil
import streamlit as st
from datetime import datetime
import shutil

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@dataclass
class BatchConfig:
    """Configuration for batch processing"""
    max_workers: int = 4
    batch_size: int = 100
    timeout_seconds: float = 300.0
    retry_attempts: int = 3
    retry_delay: float = 1.0
    progress_callback: Optional[Callable[[int, int], None]] = None
    use_enhanced_pdf: bool = True


@dataclass
class BatchJob:
    """Represents a batch job"""
    job_id: str
    items: List[Any]
    processor: Callable[[Any], Any]
    config: BatchConfig
    status: str = "pending"
    results: List[Any] = field(default_factory=list)
    errors: List[Exception] = field(default_factory=list)
    start_time: float = 0.0
    end_time: float = 0.0
    processed_count: int = 0


@dataclass
class ProcessingResult:
    """Result of processing a single file"""
    filename: str
    status: str
    html_files: List[str] = field(default_factory=list)
    pdf_files: List[str] = field(default_factory=list)
    output_folder: str = ""
    error: str = ""
    processing_time: float = 0.0
    macro_sheet: Dict[str, Any] = field(default_factory=dict)  # NEW: Store macro sheet result


class EnhancedBatchProcessor:
    """Enhanced batch processor with parallel processing capabilities"""
    
    def __init__(self, config: Optional[BatchConfig] = None):
        self.config = config or BatchConfig()
        self.active_jobs: Dict[str, BatchJob] = {}
        self.job_queue: Queue = Queue()
        self.executor: Optional[ThreadPoolExecutor] = None
        self.futures: Dict[str, Future] = {}
        self.lock = threading.RLock()
        self.logger = logging.getLogger(__name__)
        
        # Resource monitoring
        self.max_memory_percent = 80.0
        self.max_cpu_percent = 90.0
        
        # Statistics
        self.stats = {
            'total_jobs': 0,
            'completed_jobs': 0,
            'failed_jobs': 0,
            'total_items_processed': 0,
            'average_processing_time': 0.0
        }
        
        # Start worker thread
        self.worker_thread = threading.Thread(target=self._job_processor, daemon=True)
        self.worker_thread.start()
        
    def submit_batch(self, items: List[Any], processor: Callable[[Any], Any],
                    job_id: str = "", config: Optional[BatchConfig] = None) -> str:
        """Submit batch job for processing"""
        if job_id is None:
            job_id = f"batch_{int(time.time() * 1000)}"
            
        job_config = config or self.config
        
        job = BatchJob(
            job_id=job_id,
            items=items,
            processor=processor,
            config=job_config,
            status="queued",
            results=[],
            errors=[],
            start_time=time.time()
        )
        
        with self.lock:
            self.active_jobs[job_id] = job
            self.job_queue.put(job)
            self.stats['total_jobs'] += 1
            
        self.logger.info(f"Batch job submitted: {job_id} ({len(items)} items)")
        return job_id
        
    def _job_processor(self):
        """Background thread for processing jobs"""
        while True:
            try:
                # Get job from queue
                job = self.job_queue.get(timeout=1.0)
                
                # Check system resources (disabled for testing)
                # if not self._check_resources():
                #     self.logger.warning("Insufficient resources, waiting...")
                #     time.sleep(5.0)
                #     self.job_queue.put(job)  # Re-queue job
                #     continue
                    
                # Process job
                self._process_job(job)
                
            except Empty:
                continue
            except Exception as e:
                self.logger.error(f"Job processor error: {e}")
                
    def _process_job(self, job: BatchJob):
        """Process individual batch job"""
        try:
            job.status = "processing"
            self.logger.info(f"Processing job: {job.job_id}")
            
            # Create thread pool for this job
            with ThreadPoolExecutor(max_workers=job.config.max_workers) as executor:
                # Submit items in batches
                batch_futures = {}
                
                for i in range(0, len(job.items), job.config.batch_size):
                    batch = job.items[i:i + job.config.batch_size]
                    future = executor.submit(self._process_batch, batch, job)
                    batch_futures[future] = i
                    
                # Collect results
                for future in as_completed(batch_futures, timeout=job.config.timeout_seconds):
                    try:
                        batch_results = future.result()
                        if isinstance(batch_results, list):
                            job.results.extend(batch_results)
                            job.processed_count += len(batch_results)
                        else:
                            job.results.append(batch_results)
                            job.processed_count += 1
                        
                        # Update progress
                        if job.config.progress_callback:
                            job.config.progress_callback(job.processed_count, len(job.items))
                            
                    except Exception as e:
                        job.errors.append(e)
                        self.logger.error(f"Batch processing error: {e}")
                        
            job.status = "completed" if not job.errors else "completed_with_errors"
            job.end_time = time.time()
            
            # Update statistics
            with self.lock:
                self.stats['completed_jobs'] += 1
                self.stats['total_items_processed'] += job.processed_count
                
                # Update average processing time
                processing_time = job.end_time - job.start_time
                total_completed = self.stats['completed_jobs']
                current_avg = self.stats['average_processing_time']
                self.stats['average_processing_time'] = (
                    (current_avg * (total_completed - 1) + processing_time) / total_completed
                )
                
            self.logger.info(f"Job completed: {job.job_id} - "
                           f"{job.processed_count}/{len(job.items)} items processed")
                           
        except Exception as e:
            job.status = "failed"
            job.end_time = time.time()
            job.errors.append(e)
            
            with self.lock:
                self.stats['failed_jobs'] += 1
                
            self.logger.error(f"Job failed: {job.job_id} - {e}")
            
    def _process_batch(self, batch: List[Any], job: BatchJob) -> List[Any]:
        """Process a batch of items with retry logic"""
        results = []
        
        for item in batch:
            success = False
            last_error = None
            
            for attempt in range(job.config.retry_attempts):
                try:
                    result = job.processor(item)
                    results.append(result)
                    success = True
                    break
                    
                except Exception as e:
                    last_error = e
                    if attempt < job.config.retry_attempts - 1:
                        time.sleep(job.config.retry_delay * (2 ** attempt))  # Exponential backoff
                        
            if not success:
                job.errors.append(last_error or Exception("Unknown error"))
                
        return results
        
    def _check_resources(self) -> bool:
        """Check if system resources are available"""
        try:
            # Check memory
            memory = psutil.virtual_memory()
            if memory.percent > self.max_memory_percent:
                self.logger.debug(f"Memory usage high: {memory.percent}%")
                return False
                
            # Check CPU - only check if we have a reasonable threshold
            if self.max_cpu_percent < 100:  # Only check if threshold is set reasonably
                cpu_percent = psutil.cpu_percent(interval=0.1)
                if cpu_percent > self.max_cpu_percent:
                    self.logger.debug(f"CPU usage high: {cpu_percent}%")
                    return False
                
            return True
            
        except Exception as e:
            self.logger.debug(f"Resource check failed: {e}")
            return True  # Assume resources are available if check fails
            
    def get_job_status(self, job_id: str) -> Optional[Dict[str, Any]]:
        """Get status of a specific job"""
        with self.lock:
            job = self.active_jobs.get(job_id)
            if not job:
                return None
                
            return {
                'job_id': job.job_id,
                'status': job.status,
                'total_items': len(job.items),
                'processed_count': job.processed_count,
                'progress_percent': (job.processed_count / len(job.items)) * 100 if job.items else 0,
                'errors_count': len(job.errors),
                'start_time': job.start_time,
                'end_time': job.end_time,
                'duration': (job.end_time or time.time()) - job.start_time,
                'results': job.results
            }
            
    def get_all_jobs(self) -> List[Dict[str, Any]]:
        """Get status of all jobs"""
        with self.lock:
            jobs = []
            for job_id in self.active_jobs.keys():
                status = self.get_job_status(job_id)
                if status is not None:
                    jobs.append(status)
            return jobs
            
    def get_active_jobs(self) -> List[Dict[str, Any]]:
        """Get status of active jobs"""
        with self.lock:
            jobs = []
            for job_id, job in self.active_jobs.items():
                if job.status in ['queued', 'processing']:
                    status = self.get_job_status(job_id)
                    if status is not None:
                        jobs.append(status)
            return jobs
            
    def cancel_job(self, job_id: str) -> bool:
        """Cancel a job"""
        with self.lock:
            job = self.active_jobs.get(job_id)
            if not job or job.status in ['completed', 'failed']:
                return False
                
            job.status = "cancelled"
            job.end_time = time.time()
            
            # Cancel associated futures if any
            if job_id in self.futures:
                self.futures[job_id].cancel()
                del self.futures[job_id]
                
            self.logger.info(f"Job cancelled: {job_id}")
            return True
            
    def cleanup_completed_jobs(self, max_age_hours: int = 24):
        """Clean up completed jobs older than specified hours"""
        current_time = time.time()
        max_age_seconds = max_age_hours * 3600
        
        with self.lock:
            jobs_to_remove = []
            
            for job_id, job in self.active_jobs.items():
                if (job.status in ['completed', 'failed', 'cancelled'] and 
                    job.end_time and 
                    current_time - job.end_time > max_age_seconds):
                    jobs_to_remove.append(job_id)
                    
            for job_id in jobs_to_remove:
                del self.active_jobs[job_id]
                if job_id in self.futures:
                    del self.futures[job_id]
                    
            if jobs_to_remove:
                self.logger.info(f"Cleaned up {len(jobs_to_remove)} old jobs")
                
    def get_statistics(self) -> Dict[str, Any]:
        """Get processing statistics"""
        with self.lock:
            active_count = sum(
                1 for job in self.active_jobs.values()
                if job.status in ['queued', 'processing']
            )
            
            return {
                'total_jobs': self.stats['total_jobs'],
                'completed_jobs': self.stats['completed_jobs'],
                'failed_jobs': self.stats['failed_jobs'],
                'active_jobs': active_count,
                'total_items_processed': self.stats['total_items_processed'],
                'average_processing_time': self.stats['average_processing_time'],
                'success_rate': (
                    (self.stats['completed_jobs'] - len([j for j in self.active_jobs.values() if 'error' in j.status])) /
                    max(1, self.stats['completed_jobs'])
                ) * 100
            }
            
    def configure_resource_limits(self, max_memory_percent: float = 80.0, 
                                 max_cpu_percent: float = 90.0):
        """Configure resource limits"""
        self.max_memory_percent = max_memory_percent
        self.max_cpu_percent = max_cpu_percent
        
        self.logger.info(f"Resource limits updated: Memory={max_memory_percent}%, CPU={max_cpu_percent}%")
        
    def shutdown(self):
        """Shutdown the processor"""
        self.logger.info("Shutting down parallel batch processor")
        
        # Cancel all active jobs
        with self.lock:
            for job_id in list(self.active_jobs.keys()):
                self.cancel_job(job_id)
                
        # Shutdown executor if running
        if self.executor:
            self.executor.shutdown(wait=True)


# Global batch processor instance
batch_processor = EnhancedBatchProcessor()


def get_batch_processor() -> EnhancedBatchProcessor:
    """Get the global batch processor instance"""
    return batch_processor


class FileBatchProcessor:
    """Process individual files for batch processing"""
    
    def __init__(self, config):
        self.config = config
        self.output_base_dir = Path("output")
    
    def _create_timestamped_folder(self, filename: str) -> Path:
        """Create a timestamped folder for output files"""
        # Get current timestamp
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        
        # Clean filename (remove extension)
        clean_filename = Path(filename).stem
        
        # Create folder name: YYYYMMDD_HHMMSS_filename
        folder_name = f"{timestamp}_{clean_filename}"
        
        # Create full path
        output_folder = self.output_base_dir / folder_name
        output_folder.mkdir(parents=True, exist_ok=True)
        
        return output_folder
    
    def process_single_file(self, file, use_enhanced_pdf: bool = True) -> ProcessingResult:
        """Process a single file and save outputs to timestamped folder"""
        start_time = time.time()
        
        try:
            from core.processors.excel_processor import ExcelProcessor
            from core.generators.document_generator import DocumentGenerator
            
            # Process Excel file
            excel_processor = ExcelProcessor()
            processed_data = excel_processor.process_excel(file)
            
            # Generate documents
            doc_generator = DocumentGenerator(processed_data)
            html_documents = doc_generator.generate_all_documents()
            
            # Generate PDFs with enhanced generator if available
            if use_enhanced_pdf:
                try:
                    from core.generators.pdf_generator_enhanced import EnhancedPDFGenerator
                    print("✅ Using Enhanced PDF Generator (CSS Zoom + Disable Smart Shrinking)")
                    
                    pdf_gen = EnhancedPDFGenerator()
                    pdf_documents_bytes = pdf_gen.batch_convert(
                        html_documents,
                        zoom=1.0,
                        disable_smart_shrinking=True
                    )
                    
                    # Convert to expected format
                    pdf_documents = {f"{name}.pdf": content for name, content in pdf_documents_bytes.items()}
                    
                except Exception as e:
                    print(f"⚠️ Enhanced PDF Generator failed, using fallback: {e}")
                    pdf_documents = doc_generator.create_pdf_documents(html_documents)
            else:
                pdf_documents = doc_generator.create_pdf_documents(html_documents)
            
            # Generate Macro Scrutiny Sheet (NEW)
            macro_sheet_result = None
            try:
                from simple_scrutiny_sheet_generator import create_scrutiny_sheet_simple
                import tempfile
                
                # Create temporary paths for scrutiny sheet
                with tempfile.NamedTemporaryFile(suffix='.xlsm', delete=False) as tmp_xlsm:
                    tmp_xlsm_path = tmp_xlsm.name
                    
                with tempfile.NamedTemporaryFile(suffix='.pdf', delete=False) as tmp_pdf:
                    tmp_pdf_path = tmp_pdf.name
                
                # Template path (adjust as needed)
                template_path = "ATTACHED_ASSETS/even BILL NOTE SHEET.xlsm"
                
                if os.path.exists(template_path):
                    # Determine bill type from filename
                    filename_lower = file.name.lower()
                    if 'final' in filename_lower:
                        bill_type = "final"
                    elif 'first' in filename_lower:
                        bill_type = "first"
                    elif 'running' in filename_lower:
                        bill_type = "running"
                    else:
                        bill_type = "running"  # default
                    
                    # Create scrutiny sheet
                    macro_sheet_result = create_scrutiny_sheet_simple(
                        template_path=template_path,
                        output_path=tmp_xlsm_path,
                        processed_data=processed_data,
                        bill_type=bill_type,
                        output_pdf_path=tmp_pdf_path
                    )
                    
                    if macro_sheet_result.get('success'):
                        macro_sheet_result['output_file'] = tmp_xlsm_path
                        macro_sheet_result['pdf_file'] = tmp_pdf_path
                        print(f"✅ Macro scrutiny sheet created: {macro_sheet_result.get('sheet_name')}")
                    else:
                        print(f"⚠️ Macro scrutiny sheet failed: {macro_sheet_result.get('error', 'Unknown error')}")
                else:
                    print(f"⚠️ Template not found: {template_path}")
                    
            except Exception as e:
                print(f"⚠️ Error creating macro scrutiny sheet: {e}")
                macro_sheet_result = {'success': False, 'error': str(e)}
            
            # Create timestamped folder for this file
            output_folder = self._create_timestamped_folder(file.name)
            
            # Save HTML files
            html_folder = output_folder / "html"
            html_folder.mkdir(exist_ok=True)
            
            for doc_name, html_content in html_documents.items():
                html_file = html_folder / f"{doc_name}.html"
                html_file.write_text(html_content, encoding='utf-8')
            
            # Save PDF files
            pdf_folder = output_folder / "pdf"
            pdf_folder.mkdir(exist_ok=True)
            
            for doc_name, pdf_content in pdf_documents.items():
                pdf_file = pdf_folder / doc_name
                pdf_file.write_bytes(pdf_content)
            
            # Save Macro Scrutiny Sheet files (NEW)
            if macro_sheet_result and macro_sheet_result.get('success'):
                try:
                    # Copy XLSM file
                    xlsm_source = Path(macro_sheet_result['output_file'])
                    xlsm_dest = output_folder / f"{Path(file.name).stem}_scrutiny_sheet.xlsm"
                    shutil.copy2(xlsm_source, xlsm_dest)
                    macro_sheet_result['saved_xlsm_path'] = str(xlsm_dest)
                    
                    # Copy PDF file if it exists
                    if macro_sheet_result.get('pdf_file'):
                        pdf_source = Path(macro_sheet_result['pdf_file'])
                        pdf_dest = output_folder / f"{Path(file.name).stem}_scrutiny_sheet.pdf"
                        shutil.copy2(pdf_source, pdf_dest)
                        macro_sheet_result['saved_pdf_path'] = str(pdf_dest)
                        
                    print(f"✅ Macro scrutiny sheet files saved to output folder")
                except Exception as e:
                    print(f"⚠️ Error saving macro scrutiny sheet files: {e}")
            
            processing_time = time.time() - start_time
            
            return ProcessingResult(
                filename=file.name,
                status='success',
                html_files=list(html_documents.keys()),
                pdf_files=list(pdf_documents.keys()),
                output_folder=str(output_folder),
                processing_time=processing_time,
                macro_sheet=macro_sheet_result or {}  # NEW: Include macro sheet result
            )
            
        except Exception as e:
            processing_time = time.time() - start_time
            return ProcessingResult(
                filename=file.name,
                status='error',
                error=str(e),
                processing_time=processing_time
            )


def show_enhanced_batch_mode(config):
    """Show enhanced batch processing UI with parallel processing"""
    st.markdown("## 📦 Enhanced Batch Processing Mode")
    st.info("Process multiple Excel files in parallel with advanced features")
    
    # Configuration options
    with st.expander("⚙️ Processing Configuration", expanded=False):
        col1, col2, col3 = st.columns(3)
        
        with col1:
            max_workers = st.slider("Max Workers", 1, 8, 4)
            batch_size = st.slider("Batch Size", 10, 200, 100)
            
        with col2:
            timeout_seconds = st.slider("Timeout (seconds)", 30, 600, 300)
            retry_attempts = st.slider("Retry Attempts", 0, 5, 3)
            
        with col3:
            use_enhanced_pdf = st.checkbox("Use Enhanced PDF Generator", value=True)
            show_detailed_stats = st.checkbox("Show Detailed Statistics", value=False)
    
    uploaded_files = st.file_uploader(
        "Upload Excel Files",
        type=['xlsx', 'xls'],
        accept_multiple_files=True
    )
    
    if uploaded_files:
        st.success(f"✅ {len(uploaded_files)} files uploaded")
        
        if st.button("🚀 Process All Files in Parallel", type="primary"):
            # Configure batch processor
            batch_config = BatchConfig(
                max_workers=max_workers,
                batch_size=batch_size,
                timeout_seconds=timeout_seconds,
                retry_attempts=retry_attempts,
                use_enhanced_pdf=use_enhanced_pdf
            )
            
            # Create file processor
            file_processor = FileBatchProcessor(config)
            
            # Progress tracking
            progress_bar = st.progress(0)
            status_text = st.empty()
            stats_placeholder = st.empty()
            
            def update_progress(processed, total):
                progress = processed / total if total > 0 else 0
                progress_bar.progress(progress)
                status_text.text(f"Processing {processed}/{total} files")
                
                # Update statistics if requested
                if show_detailed_stats:
                    processor_stats = batch_processor.get_statistics()
                    stats_placeholder.json(processor_stats)
            
            # Set up progress callback
            batch_config.progress_callback = update_progress
            
            # Create processor function
            def process_file_wrapper(file):
                return file_processor.process_single_file(file, use_enhanced_pdf)
            
            # Submit batch job
            job_id = batch_processor.submit_batch(
                items=uploaded_files,
                processor=process_file_wrapper,
                config=batch_config
            )
            
            # Wait for job completion
            with st.spinner("Processing files in parallel..."):
                while True:
                    job_status = batch_processor.get_job_status(job_id)
                    if job_status and job_status['status'] in ['completed', 'completed_with_errors', 'failed']:
                        break
                    time.sleep(0.5)
            
            # Get results
            job_status = batch_processor.get_job_status(job_id)
            results = job_status.get('results', []) if job_status else []
            
            # Celebrate success with balloons! 🎈
            success_count = sum(1 for r in results if hasattr(r, 'status') and r.status == 'success')
            if success_count > 0:
                st.balloons()
                st.success(f"🎉 Successfully processed {success_count} file(s)!")
            
            # Show results
            st.markdown("### 📊 Results")
            
            # Summary metrics
            success_count = sum(1 for r in results if hasattr(r, 'status') and r.status == 'success')
            error_count = len(results) - success_count
            
            col1, col2, col3, col4 = st.columns(4)
            col1.metric("Total", len(results))
            col2.metric("Success", success_count)
            col3.metric("Errors", error_count)
            col4.metric("Avg Time", f"{job_status.get('duration', 0)/len(results):.2f}s" if results and job_status else "0s")
            
            # Detailed results with output folder information
            st.markdown("### 📁 Output Folders")
            for result in results:
                if hasattr(result, 'status') and result.status == 'success':
                    with st.expander(f"✅ {result.filename}", expanded=True):
                        st.success(f"**Output Folder:** `{result.output_folder}`")
                        st.info(f"**Processing Time:** {result.processing_time:.2f} seconds")
                        
                        col1, col2 = st.columns(2)
                        
                        with col1:
                            st.markdown("**📄 HTML Files:**")
                            for html_file in result.html_files or []:
                                st.text(f"  • {html_file}.html")
                        
                        with col2:
                            st.markdown("**📕 PDF Files:**")
                            for pdf_file in result.pdf_files or []:
                                st.text(f"  • {pdf_file}")
                        
                        st.info(f"📂 All files saved to: {result.output_folder}")
                else:
                    error_msg = getattr(result, 'error', 'Unknown error')
                    st.error(f"❌ {getattr(result, 'filename', 'Unknown file')}: {error_msg}")
            
            # Summary of all output folders
            st.markdown("---")
            st.markdown("### 📦 All Output Folders")
            output_folders = [getattr(r, 'output_folder', '') for r in results if hasattr(r, 'status') and r.status == 'success']
            if output_folders:
                st.code('\n'.join(output_folders), language='text')
            
            # Show processor statistics
            if show_detailed_stats:
                st.markdown("### 📈 Processing Statistics")
                processor_stats = batch_processor.get_statistics()
                st.json(processor_stats)
                
            # Cleanup completed jobs
            batch_processor.cleanup_completed_jobs()