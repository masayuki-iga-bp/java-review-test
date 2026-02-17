#!/usr/bin/env python3
"""
PR-Agent wrapper script to ensure proper environment variable handling
for Azure OpenAI with non-standard model names.
"""
import os
import sys
import subprocess

# 環境変数を取得
api_key = os.environ.get('AZURE_OPENAI_API_KEY', '')
api_base = os.environ.get('AZURE_OPENAI_API_BASE', '')
deployment_id = os.environ.get('AZURE_OPENAI_DEPLOYMENT_ID', 'gpt-5.2')
github_token = os.environ.get('GITHUB_TOKEN', '')

# 重要：/openai/v1 サフィックスを削除（litellmが自動追加するため）
if api_base.endswith('/openai/v1'):
    api_base = api_base.rstrip('/openai/v1')
    print(f"⚠️  Removed /openai/v1 from api_base")

# API versionを安定版に変更
api_version = '2024-10-01-preview'

print(f"=== Configuration ===")
print(f"API Base: {api_base}")
print(f"API Version: {api_version}")
print(f"Deployment ID: {deployment_id}")

# 重要：azure/ プレフィックスを使用してモデル名を構築
model_name = f"azure/{deployment_id}"

# 環境変数設定（litellm用）
os.environ['OPENAI_API_KEY'] = str(api_key)
os.environ['OPENAI_API_TYPE'] = 'azure'
os.environ['OPENAI_API_BASE'] = str(api_base)
os.environ['OPENAI_API_VERSION'] = str(api_version)
os.environ['AZURE_API_KEY'] = str(api_key)
os.environ['AZURE_API_BASE'] = str(api_base)
os.environ['AZURE_API_VERSION'] = str(api_version)

# PR-Agent用の設定（dynaconf形式）
os.environ['CONFIG__MODEL'] = str(model_name)
os.environ['CONFIG__MODEL_TURBO'] = str(model_name)
os.environ['PR_REVIEWER__MODEL'] = str(model_name)
os.environ['OPENAI__KEY'] = str(api_key)
os.environ['OPENAI__API_TYPE'] = 'azure'
os.environ['OPENAI__API_BASE'] = str(api_base)
os.environ['OPENAI__API_VERSION'] = str(api_version)
os.environ['OPENAI__DEPLOYMENT_ID'] = str(deployment_id)

# GitHub token設定
os.environ['GITHUB_TOKEN'] = str(github_token)
os.environ['CONFIG__GITHUB__USER_TOKEN'] = str(github_token)

# デバッグ情報
print(f"Model Name: {model_name}")
print(f"Environment variables set for litellm and PR-Agent")
print("=" * 40)

# PR-Agent実行
if len(sys.argv) < 2:
    print("Error: PR URL required as argument")
    sys.exit(1)

pr_url = sys.argv[1]
print(f"Running PR-Agent for: {pr_url}\n")

try:
    result = subprocess.run(
        ['python', '-m', 'pr_agent.cli', '--pr_url', pr_url, 'review'],
        env=os.environ,
        timeout=300
    )
    sys.exit(result.returncode)
except subprocess.TimeoutExpired:
    print("ERROR: PR-Agent timed out after 5 minutes", file=sys.stderr)
    sys.exit(1)
except Exception as e:
    print(f"ERROR: {e}", file=sys.stderr)
    import traceback
    traceback.print_exc()
    sys.exit(1)
