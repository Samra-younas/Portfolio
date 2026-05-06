# Test Suite for Flask Portfolio App

This document explains how to run and understand the test suite for the Flask backend.

## Test Coverage

The test suite (`test_app.py`) provides comprehensive coverage for:

### Endpoints Tested
- **`/health`** - Basic health check endpoint
- **`/api/chat`** - Main chat API endpoint with Anthropic integration

### Test Categories

#### 1. Health Endpoint Tests (`TestHealthEndpoint`)
- ✅ Successful health check returns 200 status
- ✅ Returns correct JSON structure with "ok" status

#### 2. Chat Endpoint Tests (`TestChatEndpoint`)
- ✅ Successful chat request with valid messages
- ✅ Proper Anthropic API integration
- ✅ Correct response format and content
- ✅ API parameter validation (model, max_tokens, system prompt)

#### 3. Error Handling Tests (`TestChatEndpointErrors`)
- ✅ Missing/empty messages validation (400 error)
- ✅ Invalid JSON handling (400 error)
- ✅ Anthropic authentication errors (401 error)
- ✅ Rate limit errors (429 error)
- ✅ General exception handling (500 error)

#### 4. Configuration Tests (`TestAppConfiguration`)
- ✅ Flask app initialization
- ✅ CORS configuration
- ✅ System prompt validation

## Running Tests

### Install Test Dependencies
```bash
pip install -r requirements.txt
```

### Run All Tests
```bash
pytest
```

### Run with Verbose Output
```bash
pytest -v
```

### Run Specific Test Class
```bash
pytest test_app.py::TestChatEndpoint -v
```

### Run Specific Test Method
```bash
pytest test_app.py::TestChatEndpoint::test_chat_endpoint_success -v
```

### Run with Coverage Report
```bash
pip install pytest-cov
pytest --cov=app --cov-report=html
```

## Test Structure

### Fixtures Used
- **`client`**: Flask test client for making HTTP requests
- **`mock_anthropic_client`**: Mocked Anthropic API client for isolated testing

### Mocking Strategy
- The Anthropic API client is mocked to avoid actual API calls during testing
- This ensures tests are fast, reliable, and don't consume API credits
- Mock responses simulate real API behavior for comprehensive testing

### Test Data
- Uses realistic message formats
- Tests both valid and invalid input scenarios
- Covers edge cases and error conditions

## Test Metrics

- **Total Tests**: 12 test methods
- **Test Classes**: 4 organized test classes
- **Coverage Areas**: Endpoints, error handling, configuration, system integration
- **Mock Coverage**: Complete Anthropic API integration testing

## Best Practices Implemented

1. **Isolation**: Each test is independent and doesn't rely on others
2. **Clear Naming**: Test methods describe exactly what they test
3. **Comprehensive Coverage**: Tests happy paths, error paths, and edge cases
4. **Proper Fixtures**: Uses pytest fixtures for clean setup/teardown
5. **Mocking**: External dependencies are properly mocked
6. **Assertions**: Clear, specific assertions with meaningful error messages

## Adding New Tests

When adding new features to `app.py`, follow this pattern:

1. Add test methods to appropriate test classes
2. Use existing fixtures where possible
3. Mock external dependencies
4. Test both success and failure scenarios
5. Include edge cases and boundary conditions

Example:
```python
def test_new_feature_success(self, client, mock_anthropic_client):
    """Test successful new feature call."""
    # Setup mock
    # Make request
    # Assert response
    pass
```
