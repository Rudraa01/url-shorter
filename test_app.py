"""
Test script for URL Shortener application
"""
import requests
import time

# Test configuration
BASE_URL = "http://127.0.0.1:5000"
TEST_URL = "https://www.google.com/search?q=this+is+a+very+long+url+for+testing+purposes"

def test_url_shortening():
    """Test URL shortening functionality"""
    print("🧪 Testing URL shortening...")
    
    response = requests.post(f"{BASE_URL}/shorten", json={
        "url": TEST_URL
    })
    
    if response.status_code == 200:
        data = response.json()
        print(f"✅ URL shortened successfully!")
        print(f"   Original: {data['original_url']}")
        print(f"   Short: {data['short_url']}")
        print(f"   Code: {data['short_code']}")
        return data['short_code']
    else:
        print(f"❌ Error: {response.json()}")
        return None

def test_redirect(short_code):
    """Test URL redirection"""
    print(f"\n🧪 Testing redirection for code: {short_code}")
    
    # Don't follow redirects to test the redirect itself
    response = requests.get(f"{BASE_URL}/{short_code}", allow_redirects=False)
    
    if response.status_code == 302:
        print(f"✅ Redirect works! Location: {response.headers.get('Location')}")
        return True
    else:
        print(f"❌ Redirect failed with status: {response.status_code}")
        return False

def test_stats(short_code):
    """Test statistics functionality"""
    print(f"\n🧪 Testing statistics for code: {short_code}")
    
    response = requests.get(f"{BASE_URL}/stats/{short_code}")
    
    if response.status_code == 200:
        data = response.json()
        print(f"✅ Statistics retrieved!")
        print(f"   Original URL: {data['original_url']}")
        print(f"   Click count: {data['click_count']}")
        print(f"   Created: {data['created_at']}")
        return True
    else:
        print(f"❌ Stats failed: {response.json()}")
        return False

def test_invalid_url():
    """Test invalid URL handling"""
    print(f"\n🧪 Testing invalid URL handling...")
    
    response = requests.post(f"{BASE_URL}/shorten", json={
        "url": "not-a-valid-url"
    })
    
    if response.status_code == 400:
        print(f"✅ Invalid URL properly rejected!")
        print(f"   Error: {response.json()['error']}")
        return True
    else:
        print(f"❌ Invalid URL not handled properly")
        return False

def test_nonexistent_code():
    """Test accessing non-existent short code"""
    print(f"\n🧪 Testing non-existent short code...")
    
    response = requests.get(f"{BASE_URL}/nonexistent", allow_redirects=False)
    
    if response.status_code == 404:
        print(f"✅ Non-existent code properly returns 404!")
        return True
    else:
        print(f"❌ Non-existent code handling failed")
        return False

def run_all_tests():
    """Run all tests"""
    print("🚀 Starting URL Shortener Tests")
    print("=" * 50)
    
    try:
        # Test 1: URL shortening
        short_code = test_url_shortening()
        if not short_code:
            return False
        
        # Test 2: Redirection
        if not test_redirect(short_code):
            return False
        
        # Test 3: Statistics
        if not test_stats(short_code):
            return False
        
        # Test 4: Invalid URL
        if not test_invalid_url():
            return False
        
        # Test 5: Non-existent code
        if not test_nonexistent_code():
            return False
        
        print("\n" + "=" * 50)
        print("🎉 All tests passed! Your URL shortener is working perfectly!")
        return True
        
    except requests.exceptions.ConnectionError:
        print("❌ Cannot connect to the server. Make sure the Flask app is running on http://127.0.0.1:5000")
        return False
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        return False

if __name__ == "__main__":
    run_all_tests()
