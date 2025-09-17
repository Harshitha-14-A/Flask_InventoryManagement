import requests
import json
from datetime import datetime

BASE_URL = "http://localhost:5000"

def test_api_endpoints():
    
    print("=" * 50)
    print("INVENTORY MANAGEMENT API TESTS")
    print("=" * 50)
    
    # Test Products API
    print("\n1. Testing Products API...")
    try:
        response = requests.get(f"{BASE_URL}/api/products")
        if response.status_code == 200:
            data = response.json()
            print(f"✓ Products API working - Found {len(data['products'])} products")
            if data['products']:
                print(f"  Sample product: {data['products'][0]['name']}")
        else:
            print(f"✗ Products API failed - Status: {response.status_code}")
    except Exception as e:
        print(f"✗ Products API error: {e}")
    
    print("\n2. Testing Locations API...")
    try:
        response = requests.get(f"{BASE_URL}/api/locations")
        if response.status_code == 200:
            data = response.json()
            print(f"✓ Locations API working - Found {len(data['locations'])} locations")
            if data['locations']:
                print(f"  Sample location: {data['locations'][0]['name']}")
        else:
            print(f"✗ Locations API failed - Status: {response.status_code}")
    except Exception as e:
        print(f"✗ Locations API error: {e}")
    
    print("\n3. Testing Movements API...")
    try:
        response = requests.get(f"{BASE_URL}/api/movements")
        if response.status_code == 200:
            data = response.json()
            print(f"✓ Movements API working - Found {len(data['movements'])} movements")
            if data['movements']:
                print(f"  Latest movement: {data['movements'][0]['movement_id']}")
        else:
            print(f"✗ Movements API failed - Status: {response.status_code}")
    except Exception as e:
        print(f"✗ Movements API error: {e}")
    
    print("\n4. Testing Balance API...")
    try:
        response = requests.get(f"{BASE_URL}/api/balance")
        if response.status_code == 200:
            data = response.json()
            print(f"✓ Balance API working - Found {len(data['balances'])} balance records")
            if data['balances']:
                balance = data['balances'][0]
                print(f"  Sample balance: {balance['product_name']} at {balance['location_name']}: {balance['balance']}")
        else:
            print(f"✗ Balance API failed - Status: {response.status_code}")
    except Exception as e:
        print(f"✗ Balance API error: {e}")
    
    print("\n5. Testing Specific Product Balance API...")
    try:
        products_response = requests.get(f"{BASE_URL}/api/products")
        locations_response = requests.get(f"{BASE_URL}/api/locations")
        
        if products_response.status_code == 200 and locations_response.status_code == 200:
            products = products_response.json()['products']
            locations = locations_response.json()['locations']
            
            if products and locations:
                product_id = products[0]['product_id']
                location_id = locations[0]['location_id']
                
                response = requests.get(f"{BASE_URL}/api/balance/{product_id}/{location_id}")
                if response.status_code == 200:
                    data = response.json()
                    print(f"✓ Specific Balance API working")
                    print(f"  Balance for {data['product_name']} at {data['location_name']}: {data['balance']}")
                else:
                    print(f"✗ Specific Balance API failed - Status: {response.status_code}")
            else:
                print("⚠ No products or locations available for testing specific balance API")
        else:
            print("⚠ Could not get products/locations for specific balance test")
    except Exception as e:
        print(f"✗ Specific Balance API error: {e}")
    
    print("\n" + "=" * 50)
    print("API TESTS COMPLETED")
    print("=" * 50)


def create_sample_data():
    """Create sample data for testing (via web interface)"""
    print("\n" + "=" * 50)
    print("SAMPLE DATA CREATION GUIDE")
    print("=" * 50)
    print("To fully test the system, create the following via the web interface:")
    print("\n1. Products:")
    print("   - Product ID: LAPTOP-001, Name: Dell Laptop")
    print("   - Product ID: MOUSE-001, Name: Wireless Mouse")
    print("   - Product ID: KEYBOARD-001, Name: Mechanical Keyboard")
    
    print("\n2. Locations:")
    print("   - Location ID: WAREHOUSE-A, Name: Main Warehouse")
    print("   - Location ID: STORE-001, Name: Retail Store 1")
    print("   - Location ID: STORE-002, Name: Retail Store 2")
    
    print("\n3. Movements:")
    print("   - Move 10 LAPTOP-001 to WAREHOUSE-A (incoming stock)")
    print("   - Move 5 LAPTOP-001 from WAREHOUSE-A to STORE-001 (transfer)")
    print("   - Move 2 LAPTOP-001 from STORE-001 (outgoing sale)")
    
    print("\nAfter creating this data, run the API tests again to see full functionality.")


if __name__ == "__main__":
    print("Starting API tests...")
    print("Make sure the Flask application is running on http://localhost:5000")
    
    try:
        response = requests.get(f"{BASE_URL}/")
        if response.status_code == 200:
            print("✓ Flask application is running")
            test_api_endpoints()
        else:
            print("✗ Flask application is not responding correctly")
    except requests.exceptions.ConnectionError:
        print("✗ Cannot connect to Flask application")
        print("Please make sure the application is running on http://localhost:5000")
    except Exception as e:
        print(f"✗ Unexpected error: {e}")
    
    create_sample_data()