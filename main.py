"""
Main entry point for the Survey Analysis program.
"""
import argparse
import sys
import importlib.util
from data_processing import process_data
from dashboard_generator import generate_dashboard

def load_config(config_path: str):
    """Dynamically load a python configuration module."""
    if config_path == 'config' or config_path == 'config.py':
        import config
        return config
    
    spec = importlib.util.spec_from_file_location("config_module", config_path)
    if spec is None or spec.loader is None:
        raise ImportError(f"Could not load config from {config_path}")
    config_module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(config_module)
    return config_module

def validate_config(config_module):
    """Validate that required configuration fields exist."""
    required_keys = [
        'SURVEY_FILE_PATH', 'GRADES_FILE_PATH', 'OUTPUT_HTML_PATH',
        'GRADE_MAPPING', 'PROGRAM_STUDI_GROUPING', 'GROUPING_SUGGESTION_MAPPING', 'MIN_SAMPLE_SIZE'
    ]
    for key in required_keys:
        if not hasattr(config_module, key):
            raise AttributeError(f"Configuration module is missing required key: {key}")

def main():
    parser = argparse.ArgumentParser(description="Survey Analysis Dashboard Generator")
    parser.add_argument('--config', type=str, default='config.py', help="Path to the python config module.")
    args = parser.parse_args()
    
    try:
        config_module = load_config(args.config)
        validate_config(config_module)
    except Exception as e:
        print(f"Configuration Error: {e}")
        sys.exit(1)
        
    print("========================================")
    print(" Starting Survey Analysis")
    print("========================================")
    
    try:
        df = process_data(config_module.SURVEY_FILE_PATH, config_module.GRADES_FILE_PATH, config_module)
        generate_dashboard(df, config_module)
    except Exception as e:
        print(f"\n[ERROR] An error occurred during execution: {e}")
        sys.exit(1)
        
if __name__ == "__main__":
    main()
