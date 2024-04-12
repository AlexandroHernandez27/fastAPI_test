from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


def customer_loan_test():
    # Create customer
    customer_data = {"full_name": "Omar Cornelio", "email": "omar_cornelio@example.com"}
    response = client.post("/v1/customers/create_customer", json=customer_data)
    assert response.status_code == 201, f"Expected status 201, got {response.status_code}. Response: {response.json()}"
    customer = response.json()
    uuid = customer['id']

    # Create loan
    loan_data = {"amount": 1000, "customer_id": "existing-id"}
    response = client.post("/v1/loans/create_loan", json=loan_data)
    assert response.status_code == 201, f"Expected status 201, got {response.status_code}"
    loan = response.json()
    loan_id = loan['customer_id']

    # Get customer
    response = client.get(f"/v1/customers/get_customer/{uuid}")
    assert response.status_code == 200, f"Expected status 200, got {response.status_code}. Response: {response.json()}"

    # Get loan
    response = client.get(f"/v1/loans/get_loan/{loan_id}")
    assert response.status_code == 200, "Expected status 200"

    # Ger all customers
    response = client.get("/v1/customers/get_customers")
    assert response.status_code == 200, f"Expected status 200, got {response.status_code}"

    # Get all loans
    response = client.get("/v1/loans/get_loans")
    assert response.status_code == 200, f"Expected status 200, got {response.status_code}"

    # Update customer
    customer_data_updated = {"full_name": "Omar Munguía"}
    response = client.put(f"/v1/customers/update_customer/{uuid}", json=customer_data_updated)
    assert response.status_code == 200, f"Expected status 200, got {response.status_code}. Response: {response.json()}"

    # Update loan
    customer_data_updated = {"amount": 5000000}
    response = client.put(f"/v1/loans/update_loan/{loan_id}", json=customer_data_updated)
    assert response.status_code == 200, f"Expected status 200, got {response.status_code}. Response: {response.json()}"

    # Delete loan
    response = client.delete(f"/v1/customers/delete_customer/{uuid}")
    assert response.status_code == 204, f"Expected status 204, got {response.status_code}. Response: {response.text}"

    # Delete customer
    response = client.delete(f"/v1/loans/delete_loan/{loan_id}")
    assert response.status_code == 204, f"Expected status 204, got {response.status_code}. Response: {response.text}"

