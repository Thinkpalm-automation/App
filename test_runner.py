"""
Simple Test Runner Application
Tests files in a specified folder and reports results
"""
import os
import sys
from pathlib import Path
from typing import List, Dict, Tuple
import json


class FileTester:
    """Tests files in a directory"""
    
    def __init__(self, test_directory: str = "."):
        self.test_directory = Path(test_directory)
        self.results: List[Dict] = []
    
    def discover_files(self, extensions: List[str] = None) -> List[Path]:
        """Discover files in the test directory"""
        if extensions is None:
            extensions = ['.py', '.js', '.ts', '.java', '.cpp', '.c', '.txt', '.json']
        
        files = []
        if not self.test_directory.exists():
            print(f"Directory {self.test_directory} does not exist")
            return files
        
        for ext in extensions:
            files.extend(self.test_directory.glob(f"**/*{ext}"))
        
        return files
    
    def test_file(self, file_path: Path) -> Dict:
        """Test a single file"""
        result = {
            'file': str(file_path),
            'exists': file_path.exists(),
            'readable': False,
            'size': 0,
            'lines': 0,
            'status': 'unknown',
            'errors': []
        }
        
        try:
            if file_path.exists():
                result['readable'] = os.access(file_path, os.R_OK)
                result['size'] = file_path.stat().st_size
                
                # Count lines
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        result['lines'] = sum(1 for _ in f)
                    result['status'] = 'passed'
                except UnicodeDecodeError:
                    result['status'] = 'warning'
                    result['errors'].append('Binary file or encoding issue')
                except Exception as e:
                    result['status'] = 'failed'
                    result['errors'].append(str(e))
            else:
                result['status'] = 'failed'
                result['errors'].append('File does not exist')
                
        except Exception as e:
            result['status'] = 'failed'
            result['errors'].append(str(e))
        
        return result
    
    def run_tests(self, extensions: List[str] = None) -> Dict:
        """Run tests on all discovered files"""
        print(f"Discovering files in {self.test_directory}...")
        files = self.discover_files(extensions)
        
        if not files:
            print("No files found to test.")
            return {'total': 0, 'results': []}
        
        print(f"Found {len(files)} file(s) to test.\n")
        
        self.results = []
        for file_path in files:
            print(f"Testing: {file_path}")
            result = self.test_file(file_path)
            self.results.append(result)
        
        # Generate summary
        summary = self.generate_summary()
        return summary
    
    def generate_summary(self) -> Dict:
        """Generate test summary"""
        total = len(self.results)
        passed = sum(1 for r in self.results if r['status'] == 'passed')
        failed = sum(1 for r in self.results if r['status'] == 'failed')
        warnings = sum(1 for r in self.results if r['status'] == 'warning')
        
        return {
            'total': total,
            'passed': passed,
            'failed': failed,
            'warnings': warnings,
            'results': self.results
        }
    
    def print_report(self, summary: Dict = None):
        """Print test report"""
        if summary is None:
            summary = self.generate_summary()
        
        print("\n" + "="*60)
        print("TEST REPORT")
        print("="*60)
        print(f"Total files tested: {summary['total']}")
        print(f"Passed: {summary['passed']} ✓")
        print(f"Failed: {summary['faled']} ✗")
        print(f"Warnings: {summary['warnings']} ⚠")
        print("="*60)
        
        if summary['failed'] > 0:
            print("\nFAILED FILES:")
            for result in summary['results']:
                if result['status'] == 'failed':
                    print(f"  - {result['file']}")
                    for error in result['errors']:
                        print(f"    Error: {error}")
        
        if summary['warnings'] > 0:
            print("\nWARNINGS:")
            for result in summary['results']:
                if result['status'] == 'warning':
                    print(f"  - {result['file']}")
                    for error in result['errors']:
                        print(f"    Warning: {error}")
        
        print("\nDETAILED RESULTS:")
        for result in summary['results']:
            status_symbol = "✓" if result['status'] == 'passed' else "✗" if result['status'] == 'failed' else "⚠"
            print(f"{status_symbol} {result['file']}")
            print(f"    Size: {result['size']} bytes")
            print(f"    Lines: {result['lines']}")
            if result['errors']:
                for error in result['errors']:
                    print(f"    {error}")
    
    def save_report(self, output_file: str = "test_report.json"):
        """Save test report to JSON file"""
        summary = self.generate_summary()
        with open(output_file, 'w') as f:
            json.dump(summary, f, indent=2)
        print(f"\nReport saved to {output_file}")


def main():
    """Main entry point"""
    import argparse
    
    parser = argparse.ArgumentParser(description='Simple File Test Runner')
    parser.add_argument(
        'directory',
        nargs='?',
        default='.',
        help='Directory to test (default: current directory)'
    )
    parser.add_argument(
        '--extensions',
        nargs='+',
        default=None,
        help='File extensions to test (e.g., --extensions .py .js .txt)'
    )
    parser.add_argument(
        '--output',
        default='test_report.json',
        help='Output file for JSON report (default: test_report.json)'
    )
    
    args = parser.parse_args()
    
    tester = FileTester(args.directory)
    summary = tester.run_tests(args.extensions)
    tester.print_report(summary)
    
    if summary['total'] > 0:
        tester.save_report(args.output)
    
    # Exit with error code if tests failed
    sys.exit(1 if summary['failed'] > 0 else 0)


if __name__ == '__main__':
    main()

