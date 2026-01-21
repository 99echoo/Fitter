# Testing Guide

This guide explains how to run tests for the Fitter backend AI services.

## Prerequisites

1. Python 3.11+ installed and configured
2. Poetry dependencies installed: `cd backend && poetry install`
3. API keys configured (see [API_SETUP.md](./API_SETUP.md))
4. PostgreSQL database running (for integration tests)

## Test Structure

```
backend/tests/
├── conftest.py              # Shared fixtures
├── unit/                    # Unit tests (planned)
├── integration/             # Integration tests (planned)
├── e2e/                     # End-to-end tests (planned)
└── fixtures/                # Test data
    ├── sample_clothing.jpg
    ├── sample_face.jpg  (TO BE ADDED)
    └── sample_body.jpg  (TO BE ADDED)
```

## Test Markers

Tests are organized with pytest markers:

- `@pytest.mark.unit` - Fast unit tests with all external dependencies mocked
- `@pytest.mark.integration` - Integration tests with mocked AI services
- `@pytest.mark.e2e` - End-to-end tests with real AI API calls
- `@pytest.mark.requires_api` - Tests that need valid API keys

## Running Tests

### Quick Start

```bash
cd backend

# Run all fast tests (unit + integration, no real API calls)
poetry run pytest -m "not e2e and not requires_api"

# Run with coverage report
poetry run pytest -m "not e2e" --cov=app --cov-report=term --cov-report=html
```

### By Test Type

```bash
# Unit tests only (fastest, ~5 seconds)
poetry run pytest tests/unit -m unit -v

# Integration tests only (medium, ~30 seconds)
poetry run pytest tests/integration -m integration -v

# E2E tests with REAL APIs (slow, ~5 minutes, costs $$$)
poetry run pytest tests/e2e -m "e2e and requires_api" -v --maxfail=1
```

### By Module

```bash
# Test specific unit folder
poetry run pytest tests/unit -v

# Test specific API endpoint
poetry run pytest tests/integration/test_try_on_api.py -v
```

### With Verbosity

```bash
# Minimal output
poetry run pytest -q

# Standard output
poetry run pytest -v

# Detailed output with print statements
poetry run pytest -v -s

# Show local variables on failure
poetry run pytest -v -l
```

## Quick API Verification

Before running full test suite, use quick verification scripts:

```bash
cd backend

# Test OpenAI GPT-Image API
poetry run python scripts/test_gpt_image.py

# Test Kling AI Image-to-Video API
poetry run python scripts/test_kling_ai.py
```

These scripts:
- Initialize services
- Make minimal API calls
- Display detailed success/error messages
- Help diagnose configuration issues

## Test Data Preparation

### For Unit & Integration Tests

No special setup needed. Tests use:
- In-memory SQLite database
- Temporary files (created automatically)
- Mocked AI services

### For E2E Tests (Real APIs)

You need actual test images:

1. **Face Photo** (`tests/fixtures/sample_face.jpg`):
   - Clear, frontal face
   - 512x512 or 1024x1024 pixels
   - JPEG format
   - Appropriate for testing

2. **Body Photo** (`tests/fixtures/sample_body.jpg`):
   - Full body, standing straight
   - 1024x1024 pixels
   - JPEG format
   - Appropriate for testing

3. **Clothing Photo** (`tests/fixtures/sample_clothing.jpg`):
   - ✅ Already included (from Amazon Fashion dataset)

**Important**: Do not use photos with sensitive personal information.

## Test Coverage

### Current Implementation

- ✅ Test infrastructure (pytest, fixtures, markers)
- ✅ Sample test data (clothing image)
- ⚠️  Unit tests (TO BE IMPLEMENTED - see `backend/tests/unit/`)
- ⚠️  Integration tests (TO BE IMPLEMENTED - see `backend/tests/integration/`)
- ⚠️  E2E tests (TO BE IMPLEMENTED - see `backend/tests/e2e/`)

### Coverage Goals

- Overall: > 75%
- Service modules: > 85%
- Router modules: > 80%

### Generating Coverage Reports

```bash
# Terminal report
poetry run pytest --cov=app --cov-report=term

# HTML report (opens in browser)
poetry run pytest --cov=app --cov-report=html
open htmlcov/index.html

# XML report (for CI/CD)
poetry run pytest --cov=app --cov-report=xml
```

## CI/CD Integration

### GitHub Actions Example

```yaml
name: Backend Tests

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest

    services:
      postgres:
        image: postgres:15
        env:
          POSTGRES_PASSWORD: fitter_password
          POSTGRES_DB: fitter_test
        ports:
          - 5432:5432

    steps:
      - uses: actions/checkout@v3

      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.11'

      - name: Install Poetry
        run: pip install poetry

      - name: Install dependencies
        run: cd backend && poetry install

      - name: Run unit tests
        run: cd backend && poetry run pytest tests/unit -m unit

      - name: Run integration tests
        run: cd backend && poetry run pytest tests/integration -m integration

      # E2E tests skipped in CI (cost concerns)
      # Run manually or in scheduled jobs
```

## Troubleshooting

### Common Issues

**Import errors**
```bash
# Ensure you're in the backend directory
cd backend

# Reinstall dependencies
poetry install
```

**Database connection errors**
```bash
# Check PostgreSQL is running
docker-compose up -d postgres

# Or use docker directly
docker run -d -p 5432:5432 -e POSTGRES_PASSWORD=fitter_password postgres:15
```

**API key errors in tests**
- Unit/Integration tests should NOT require real API keys (they're mocked)
- If you see API errors, check the test is properly marked with `@pytest.mark.unit`

**Test isolation issues**
- Each test should be independent
- Check fixtures are properly scoped
- Use `--tb=short` for cleaner tracebacks

### Debugging Tests

```bash
# Run unit tests with debugging
poetry run pytest tests/unit -v -s

# Drop into debugger on failure
poetry run pytest --pdb

# Show local variables on failure
poetry run pytest -v -l
```

## Best Practices

### Writing Tests

1. **Use descriptive names**: `test_generate_try_on_success` not `test_1`
2. **One assertion per test**: Focus on single behavior
3. **Arrange-Act-Assert**: Clear test structure
4. **Mock external dependencies**: Don't hit real APIs in unit tests
5. **Clean up resources**: Use fixtures for setup/teardown

### Running Tests

1. **Run fast tests frequently**: `pytest -m unit` during development
2. **Run full suite before commits**: Catch integration issues
3. **Run E2E tests sparingly**: They're slow and cost money
4. **Monitor test duration**: Keep unit tests < 5s, integration < 30s

### Test Data

1. **Use realistic data**: But not real user data
2. **Keep fixtures small**: Minimal data for each test
3. **Version control test files**: Include in git (except large files)
4. **Document requirements**: Explain what test data represents

## Performance Benchmarks

### Expected Runtimes

- Unit tests: < 5 seconds (all unit tests combined)
- Integration tests: < 30 seconds (with mocked AI)
- E2E tests: 2-5 minutes (with real APIs)

### Cost per E2E Run

- Image generation: $0.15
- Video generation: $0.125
- **Total**: ~$0.28 per full workflow test

## Additional Resources

- [pytest documentation](https://docs.pytest.org/)
- [pytest-asyncio](https://pytest-asyncio.readthedocs.io/)
- [Coverage.py](https://coverage.readthedocs.io/)
- [Testing Best Practices](https://testdriven.io/blog/testing-best-practices/)

## Support

If tests fail:
1. Check error messages and tracebacks
2. Verify environment configuration
3. Review test isolation
4. Check API status if E2E tests fail
5. Create an issue with reproduction steps
