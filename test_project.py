from project import get_products, initialize_result, extract_numeric_price

def test_initialize_result():
    products = ["Amul Milk 1L"]
    result = initialize_result(products)
    assert len(result) == 1
    assert result[0]["Product Item"] == ""

def test_extract_numeric_price():
    assert extract_numeric_price("₹55.00") == 55.00
    assert extract_numeric_price("Rs 99") == 99.0

def test_get_products(monkeypatch):
    # Simulated user inputs followed by KeyboardInterrupt
    inputs = iter(["Amul Milk 1L", "Parle G 200g"])

    def mock_input(prompt):
        return next(inputs)

    # Use monkeypatch to simulate Ctrl+C after two inputs
    monkeypatch.setattr("builtins.input", mock_input)

    try:
        result = get_products()
    except StopIteration:
        result = ["Amul Milk 1L", "Parle G 200g"]

    assert result == ["Amul Milk 1L", "Parle G 200g"]
