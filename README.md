# Simple File Test Runner

A simple Python application to test files in a folder.

## Features

- Discovers files in a specified directory
- Tests file accessibility and readability
- Counts lines and calculates file size
- Generates detailed test reports
- Exports results to JSON

## Usage

### Basic Usage

Test all files in the current directory:
```bash
python test_runner.py
```

### Test Specific Directory

```bash
python test_runner.py /path/to/directory
```

### Test Specific File Extensions

```bash
python test_runner.py --extensions .py .js .txt
```

### Custom Output File

```bash
python test_runner.py --output my_report.json
```

## Examples

```bash
# Test current directory
python test_runner.py

# Test a specific folder
python test_runner.py ./src

# Test only Python files
python test_runner.py --extensions .py

# Test multiple extensions
python test_runner.py --extensions .py .js .ts .json
```

## Output

The application provides:
- Console output with test results
- JSON report file (default: `test_report.json`)

## Exit Codes

- `0` - All tests passed
- `1` - One or more tests failed

## Requirements

- Python 3.6 or higher
- No external dependencies (uses only standard library)

