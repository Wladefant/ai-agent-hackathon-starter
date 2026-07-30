#!/usr/bin/env python
"""
Pre-flight Check Script
Verifies that the environment is set up correctly before running the main pipeline.
Comprehensive validation of all prerequisites.
"""
import sys
import os
from pathlib import Path
import json
import argparse
from typing import List, Tuple

# Ensure UTF-8 output on consoles that default to cp1252 (Windows PowerShell).
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")
    sys.stderr.reconfigure(encoding="utf-8")

# Exit codes
EXIT_SUCCESS = 0
EXIT_ENV_ERROR = 1
EXIT_CONFIG_ERROR = 2
EXIT_INPUT_ERROR = 3


class PreflightChecker:
    """Validates pipeline prerequisites."""
    
    def __init__(self, project_name: str = None):
        self.project_name = project_name
        self.errors: List[str] = []
        self.warnings: List[str] = []
        self.checks_passed = 0
        self.checks_failed = 0
    
    def _pass(self, message: str):
        """Record a passed check."""
        self.checks_passed += 1
        print(f"  ✅ {message}")
    
    def _fail(self, message: str):
        """Record a failed check."""
        self.checks_failed += 1
        self.errors.append(message)
        print(f"  ❌ {message}")
    
    def _warn(self, message: str):
        """Record a warning."""
        self.warnings.append(message)
        print(f"  ⚠️  {message}")

    def check_python_version(self) -> bool:
        """Checks if the Python version is 3.8 or higher."""
        version = sys.version_info
        if version.major >= 3 and version.minor >= 8:
            self._pass(f"Python version {version.major}.{version.minor}.{version.micro}")
            return True
        else:
            self._fail(f"Python {version.major}.{version.minor} found, but 3.8+ required")
            return False

    def check_virtual_environment(self) -> bool:
        """Checks if the virtual environment exists and is activated."""
        venv_path = Path(".venv")
        
        if not venv_path.exists():
            self._fail("Virtual environment not found. Run: python -m venv .venv")
            return False
        
        if os.environ.get("VIRTUAL_ENV"):
            self._pass("Virtual environment activated")
            return True
        else:
            self._warn("Virtual environment exists but not activated. Run: .\\.venv\\Scripts\\Activate.ps1")
            return True

    def check_required_packages(self) -> bool:
        """Check if required packages are installed."""
        required = {
            "openpyxl": "openpyxl",
            "pandas": "pandas", 
            "pymupdf": "fitz",
            "python-docx": "docx"
        }
        missing = []
        
        for package, import_name in required.items():
            try:
                __import__(import_name)
            except ImportError:
                missing.append(package)
        
        if missing:
            self._fail(f"Missing packages: {', '.join(missing)}. Run: pip install -r requirements.txt")
            return False
        
        self._pass(f"All required packages installed ({len(required)} checked)")
        return True

    def check_input_files(self) -> bool:
        """Checks if there are any supported files in the inputs directory."""
        supported_extensions = ['.pdf', '.docx', '.xlsx', '.vsdx', '.md', '.txt', '.pptx']
        input_path = Path("inputs")
        
        if not input_path.exists():
            self._fail("Input directory 'inputs/' does not exist")
            return False
        
        # Check for project subfolder if specified
        if self.project_name:
            project_path = input_path / self.project_name
            if not project_path.exists():
                self._fail(f"inputs/{self.project_name}/ folder not found")
                return False
            
            files = [p for p in project_path.rglob("*") if p.suffix.lower() in supported_extensions]
            if not files:
                self._fail(f"No supported documents in inputs/{self.project_name}/")
                return False
            
            self._pass(f"Found {len(files)} document(s) in inputs/{self.project_name}/")
            return True
            
        files = [p for p in input_path.rglob("*") if p.suffix.lower() in supported_extensions]
        if not files:
            self._fail("No supported documents found in 'inputs/'")
            return False
        
        self._pass(f"Found {len(files)} supported documents")
        return True

    def check_config_file(self) -> bool:
        """Checks if the config.json file is valid."""
        config_file = Path("config.json")
        
        if not config_file.exists():
            self._fail("Configuration file 'config.json' not found")
            return False
        
        try:
            with open(config_file, 'r') as f:
                config = json.load(f)
            
            # Validate required sections
            required_sections = ["models", "validation_thresholds", "file_paths"]
            missing = [s for s in required_sections if s not in config]
            
            if missing:
                self._fail(f"config.json missing sections: {', '.join(missing)}")
                return False
            
            self._pass("config.json is valid")
            return True
            
        except json.JSONDecodeError as e:
            self._fail(f"Invalid JSON in config.json: {e}")
            return False

    def check_output_folders(self) -> bool:
        """Ensure output folders exist or can be created."""
        folders = ["output/extracted", "output/generated_docs", "output/test_cases", "output/validation", "output/traceability", "output/remediation"]
        
        for folder in folders:
            path = Path(folder)
            if not path.exists():
                try:
                    path.mkdir(parents=True, exist_ok=True)
                except Exception as e:
                    self._fail(f"Cannot create {folder}/ folder: {e}")
                    return False
        
        self._pass("All output folders ready")
        return True

    def check_scripts_exist(self) -> bool:
        """Check that essential scripts exist."""
        essential_scripts = [
            "scripts/extract.py",
            "scripts/generate_context.py",
            "scripts/extract_requirements.py",
            "scripts/remediate_requirements_unified.py",
        ]
        
        missing = [s for s in essential_scripts if not Path(s).exists()]
        
        if missing:
            self._fail(f"Missing essential scripts: {', '.join(missing)}")
            return False
        
        self._pass(f"All essential scripts present ({len(essential_scripts)} checked)")
        return True

    def check_agents_exist(self) -> bool:
        """Check that agent files exist."""
        agents = [
            ".github/agents/orchestrator.agent.md",
            ".github/agents/context_generator.agent.md",
            ".github/agents/requirements_extractor.agent.md",
            ".github/agents/requirements_validator.agent.md",
            ".github/agents/test_case_generator.agent.md",
            ".github/agents/test_case_validator.agent.md",
        ]
        
        missing = [a for a in agents if not Path(a).exists()]
        
        if missing:
            self._warn(f"Missing agent files: {', '.join(missing)}")
        else:
            self._pass(f"All agent files present ({len(agents)} checked)")
        
        return True

    def check_existing_excel_files(self) -> bool:
        """Check that existing Excel files have required columns."""
        files_to_check = [
            ("output/generated_docs/extracted_requirements.xlsx", ["REQ_ID", "Title", "Description"]),
            ("output/test_cases/generated_test_cases.xlsx", ["TC_ID"]),
        ]
        
        for file_path, required_cols in files_to_check:
            path = Path(file_path)
            if path.exists():
                try:
                    import openpyxl
                    wb = openpyxl.load_workbook(path)
                    ws = wb.active
                    headers = [str(cell.value).strip() if cell.value else "" for cell in ws[1]]
                    
                    missing = [col for col in required_cols if col not in headers]
                    if missing:
                        self._warn(f"{file_path} missing columns: {', '.join(missing)}")
                    else:
                        self._pass(f"{file_path} has valid structure")
                except Exception as e:
                    self._warn(f"Cannot validate {file_path}: {e}")
        
        return True

    def run_all_checks(self) -> int:
        """Run all preflight checks and return exit code."""
        print("=" * 60)
        print("PREFLIGHT CHECKS")
        print("=" * 60)
        
        if self.project_name:
            print(f"Project: {self.project_name}")
        print("")
        
        checks = [
            ("Python Version", self.check_python_version),
            ("Virtual Environment", self.check_virtual_environment),
            ("Required Packages", self.check_required_packages),
            ("Configuration", self.check_config_file),
            ("Input Files", self.check_input_files),
            ("Output Folders", self.check_output_folders),
            ("Essential Scripts", self.check_scripts_exist),
            ("Agent Files", self.check_agents_exist),
            ("Existing Files", self.check_existing_excel_files),
        ]
        
        for name, check_fn in checks:
            print(f"\n{name}:")
            try:
                check_fn()
            except Exception as e:
                self._fail(f"Check failed with error: {e}")
        
        # Summary
        print("\n" + "=" * 60)
        print("SUMMARY")
        print("=" * 60)
        print(f"  Passed: {self.checks_passed}")
        print(f"  Failed: {self.checks_failed}")
        print(f"  Warnings: {len(self.warnings)}")
        
        if self.checks_failed > 0:
            print("\n❌ PREFLIGHT FAILED - Fix errors before running pipeline")
            print("\nErrors to fix:")
            for err in self.errors:
                print(f"  • {err}")
            return EXIT_ENV_ERROR
        
        if self.warnings:
            print("\n⚠️  PREFLIGHT PASSED WITH WARNINGS")
            return EXIT_SUCCESS
        
        print("\n✅ PREFLIGHT PASSED - Ready to run pipeline")
        return EXIT_SUCCESS


def main():
    parser = argparse.ArgumentParser(description="Run preflight checks before pipeline execution")
    parser.add_argument("--project", "-p", default=None, help="Project name to validate")
    args = parser.parse_args()
    
    checker = PreflightChecker(project_name=args.project)
    exit_code = checker.run_all_checks()
    sys.exit(exit_code)


if __name__ == "__main__":
    main()
