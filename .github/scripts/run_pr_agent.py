#!/usr/bin/env python3
"""
PR-Agent wrapper script to ensure proper environment variable handling
for Azure OpenAI with non-standard model names.
"""
import os
import sys
import subprocess

# Explicitly set environment variables as strings
os.environ['OPENAI_API_TYPE'] = str('azure')
os.environ['OPENAI_API_VERSION'] = str('2024-10-01-preview')

# Use gpt-4o as model name (tiktoken compatible) while actual deployment is set via DEPLOYMENT_ID
# Force model configuration
os.environ['CONFIG__MODEL'] = str('gpt-4o')
os.environ['CONFIG__MODEL_TURBO'] = str('gpt-4o')
os.environ['PR_REVIEWER__MODEL'] = str('gpt-4o')

# Azure credentials (already set by GitHub Actions but ensure they're strings)
if 'AZURE_OPENAI_API_KEY' in os.environ:
    os.environ['OPENAI_KEY'] = str(os.environ['AZURE_OPENAI_API_KEY'])
if 'AZURE_OPENAI_API_BASE' in os.environ:
    os.environ['OPENAI_API_BASE'] = str(os.environ['AZURE_OPENAI_API_BASE'])
if 'AZURE_OPENAI_DEPLOYMENT_ID' in os.environ:
    os.environ['OPENAI_DEPLOYMENT_ID'] = str(os.environ['AZURE_OPENAI_DEPLOYMENT_ID'])

print("=== Python Wrapper Environment ===")
print(f"OPENAI_API_TYPE: {os.environ.get('OPENAI_API_TYPE')}")
print(f"OPENAI_API_VERSION: {os.environ.get('OPENAI_API_VERSION')}")
print(f"OPENAI_API_BASE: {os.environ.get('OPENAI_API_BASE', 'NOT SET')}")
print(f"OPENAI_DEPLOYMENT_ID: {os.environ.get('OPENAI_DEPLOYMENT_ID', 'NOT SET')}")
print(f"CONFIG__MODEL: {os.environ.get('CONFIG__MODEL')}")
print(f"PR_REVIEWER__MODEL: {os.environ.get('PR_REVIEWER__MODEL')}")
print("================================\n")

# Get PR URL from command line
if len(sys.argv) < 2:
    print("Error: PR URL required as argument")
    sys.exit(1)

pr_url = sys.argv[1]

# Run PR-Agent
print(f"Running PR-Agent for: {pr_url}\n")
result = subprocess.run(
    ['python', '-m', 'pr_agent.cli', '--pr_url', pr_url, 'review'],
    env=os.environ.copy()
)

sys.exit(result.returncode)
