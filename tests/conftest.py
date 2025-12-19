import asyncio
import os
import sys
from dotenv import load_dotenv
from pathlib import Path


# Add parent directory to path to import adk_travel_agent module
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

def pytest_configure(config):
    set_env_vars_on_local_run()

def set_env_vars_on_local_run():
    """Load environment variables from .env.test for local testing.
    In CI/CD, environment variables should already be set."""
    env_test_path = Path(__file__).parent.parent / '.env.test'
    if env_test_path.exists():
        load_dotenv(env_test_path)