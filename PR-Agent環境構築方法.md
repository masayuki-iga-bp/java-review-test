# PR-Agent(現Qodo Merge)

## はじめに

PR-Agent（現Qodo Merge）は、PRのレビューを自動化するツールです。

GitHub Actionsワークフローにより、PRが作成・更新されると自動的にレビューが実行されます。

**特徴:**
- ✅ ユーザーによるインストール不要
- ✅ GitHub Secretsの設定のみ
- ✅ 完全自動化

---

## GitHub Actionsでの実行

GitHub Actionsのワークフローが自動的にPR-Agentをインストール・実行します。

### 1. GitHub Secretsの設定

リポジトリにAzure OpenAIの認証情報を登録します。

1. GitHubリポジトリページで **Settings** → **Secrets and variables** → **Actions**
2. **New repository secret** をクリック
3. 以下のSecretsを追加：

| Secret名 | 値 | 説明 |
|---------|-----|------|
| `AZURE_OPENAI_API_BASE` | `https://your-resource.openai.azure.com` | Azure OpenAIエンドポイント |
| `AZURE_OPENAI_API_KEY` | `your-api-key` | Azure OpenAI APIキー |
| `AZURE_OPENAI_API_VERSION` | `2025-04-01` | APIバージョン |
| `AZURE_OPENAI_DEPLOYMENT_ID` | `gpt-5.2` | デプロイメント名 |

**注意**: `GITHUB_TOKEN`は自動的に提供されるため、設定不要です。

### 2. ワークフローファイルの確認

`.github/workflows/pr-agent.yml` が既に作成されています。このファイルにより、PRの作成/更新時に自動的にレビューが実行されます。

### 3. 動作確認

1. 新しいPRを作成
2. GitHub Actionsが自動的に実行される
3. PR画面にレビューコメントが投稿される

---

## 参考情報

- [PR-Agent公式ドキュメント](https://github.com/Codium-ai/pr-agent)
- [Qodo Merge（PR-Agentの新名称）](https://www.qodo.ai/products/qodo-merge/)


