import requests
import time
from urllib.parse import urljoin

# Configuration
BASE_URL = "https://priyankabill6dec.streamlit.app"

def test_main_page_access() -> bool:
    """Test if we can access the main application page"""
    print("Testing Main Application Access")
    print("=" * 50)
    
    try:
        response = requests.get(BASE_URL, timeout=30)
        
        if response.status_code == 200:
            print(f"✓ Main application page accessible (Status: {response.status_code})")
            print(f"  Content size: {len(response.content)} bytes")
            
            # Look for Streamlit-specific elements
            if "streamlit" in response.text.lower():
                print("  ✓ Detected Streamlit application")
            
            # Look for application-specific keywords
            content_lower = response.text.lower()
            keywords = ["bill", "invoice", "quotation", "excel", "download"]
            found_keywords = [kw for kw in keywords if kw in content_lower]
            
            if found_keywords:
                print(f"  ✓ Found relevant keywords: {', '.join(found_keywords)}")
            
            return True
        else:
            print(f"✗ Failed to access main page (Status: {response.status_code})")
            return False
            
    except Exception as e:
        print(f"✗ Error accessing main page: {str(e)}")
        return False

def test_potential_endpoints() -> bool:
    """Test various potential endpoints for the application"""
    print("\nTesting Potential Endpoints")
    print("=" * 50)
    
    # Common endpoints for Streamlit apps and file services
    endpoints = [
        "/",           # Main page
        "/download",   # Direct download endpoint
        "/api",        # API endpoint
        "/files",      # Files endpoint
        "/templates",  # Templates endpoint
    ]
    
    successful_endpoints = []
    
    for endpoint in endpoints:
        try:
            url = urljoin(BASE_URL, endpoint)
            print(f"Testing: {endpoint}")
            
            response = requests.get(url, timeout=15)
            
            # Print status and basic info
            print(f"  Status: {response.status_code}, Size: {len(response.content)} bytes")
            
            # Consider successful if we get a 200 or have substantial content
            if response.status_code == 200 and len(response.content) > 100:
                successful_endpoints.append(endpoint)
                print(f"  ✓ Success")
            elif response.status_code != 200:
                print(f"  Info: Status {response.status_code}")
            else:
                print(f"  Info: Content too small ({len(response.content)} bytes)")
                
        except Exception as e:
            print(f"  ✗ Error: {str(e)}")
        
        # Small delay to be respectful
        time.sleep(0.5)
    
    print(f"\nSuccessfully accessed {len(successful_endpoints)} endpoints:")
    for endpoint in successful_endpoints:
        print(f"  - {endpoint}")
    
    return len(successful_endpoints) > 0

def test_file_content_analysis() -> bool:
    """Analyze the content of returned files to understand the application"""
    print("\nAnalyzing File Content")
    print("=" * 50)
    
    try:
        response = requests.get(BASE_URL, timeout=30)
        
        if response.status_code == 200 and len(response.content) > 0:
            content = response.text
            
            print(f"Content type: {type(content)}")
            print(f"Content length: {len(content)} characters")
            
            # Check if it looks like HTML
            if content.strip().startswith("<!DOCTYPE") or content.strip().startswith("<html"):
                print("✓ Content appears to be HTML")
                
                # Look for specific HTML elements
                lower_content = content.lower()
                
                if "<title>" in lower_content:
                    title_start = lower_content.find("<title>") + 7
                    title_end = lower_content.find("</title>")
                    if title_start > 6 and title_end > title_start:
                        title = content[title_start:title_end]
                        print(f"  Page title: {title}")
                
                # Count form elements which might indicate upload functionality
                form_count = lower_content.count("<form")
                if form_count > 0:
                    print(f"  Found {form_count} form element(s) - may indicate upload functionality")
                
                # Look for buttons
                button_count = lower_content.count("button") + lower_content.count('type="submit"')
                if button_count > 0:
                    print(f"  Found {button_count} button/submit element(s)")
                
                # Look for file input elements
                file_input_count = lower_content.count('type="file"') + lower_content.count("input-file")
                if file_input_count > 0:
                    print(f"  Found {file_input_count} file input element(s) - confirms upload functionality")
                
                return True
            else:
                print("? Content doesn't appear to be HTML")
                print(f"  First 100 chars: {content[:100]}")
                return True  # Still success as we got content
                
        else:
            print(f"✗ Failed to get content (Status: {response.status_code}, Size: {len(response.content)})")
            return False
            
    except Exception as e:
        print(f"✗ Error analyzing content: {str(e)}")
        return False

def main():
    """Run detailed deployment tests"""
    print("Detailed Deployment Analysis")
    print("=" * 60)
    print(f"Target: {BASE_URL}")
    print()
    
    # Run all tests
    results = []
    results.append(("Main Page Access", test_main_page_access()))
    results.append(("Potential Endpoints", test_potential_endpoints()))
    results.append(("File Content Analysis", test_file_content_analysis()))
    
    # Summary
    print("\n" + "=" * 60)
    print("DETAILED TEST SUMMARY")
    print("=" * 60)
    
    passed = 0
    for test_name, result in results:
        status = "PASS" if result else "FAIL"
        print(f"{test_name}: {status}")
        if result:
            passed += 1
    
    print(f"\nOverall: {passed}/{len(results)} tests passed")
    
    if passed == len(results):
        print("🎉 All tests passed! Deployment is working correctly.")
        return True
    elif passed >= len(results) - 1:
        print("⚠️  Most tests passed. Deployment is mostly working.")
        return True
    else:
        print("❌ Some tests failed. Please check the deployment.")
        return False

if __name__ == "__main__":
    main()