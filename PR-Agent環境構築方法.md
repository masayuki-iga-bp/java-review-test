# PR-Agent(現Qodo Merge)

## はじめに

PR-Agent（現Qodo Merge）は、PRのレビューを自動化するツールです。主な使用方法は以下の2つです：

1. **GitHub Actions（推奨）** - PRが作成/更新されると自動的にレビュー
2. **ローカルCLI実行** - 開発者が手動でレビューを実行

このドキュメントでは、両方の設定方法を説明します。

---

## 方法1: GitHub Actions（推奨）

### 1-1. GitHub Secretsの設定

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

### 1-2. ワークフローファイルの確認

`.github/workflows/pr-agent.yml` が既に作成されています。このファイルにより、PRの作成/更新時に自動的にレビューが実行されます。

### 1-3. 動作確認

1. 新しいPRを作成
2. GitHub Actionsが自動的に実行される
3. PR画面にレビューコメントが投稿される

---

## 方法2: ローカルCLI実行

ローカルで手動実行する場合の手順です。

### 2-1. PR-Agentのインストール

```bash
pip install pr-agent
```

### 2-2. GitHub Personal Access Tokenの取得

PR-AgentでGitHubのプルリクエストを読み取るために、Personal Access Tokenが必要です。

### 手順
1. GitHubにログイン
2. 右上のプロフィールアイコンをクリック → **Settings**
3. 左メニューの下部 → **Developer settings**
4. **Personal access tokens** → **Tokens (classic)**
5. **Generate new token (classic)** をクリック
6. トークンの設定：
   - **Note**: 用途を記入（例：PR-Agent）
   - **Expiration**: 有効期限を選択
   - **Select scopes**: 以下を選択
     - ✅ `repo` (Full control of private repositories)
     - ✅ `read:org` (組織のリポジトリの場合)
7. **Generate token** をクリック
8. 生成されたトークンをコピー（この画面を離れると二度と表示されません）

### 2-3. 設定ファイルの作成

#### configuration.toml（必須）

プロジェクトのルートディレクトリに`configuration.toml`ファイルを作成します：

```toml
[config]
model = "azure/gpt-5.2"
model_turbo = "azure/gpt-5.2"
fallback_models = ["azure/gpt-5.2"]
custom_model_max_tokens = 128000

[azure_openai]
api_type = "azure"
api_base = "https://aoairg-sub-aoai.openai.azure.com"
api_version = "2025-04-01"
deployment_id = "gpt-5.2"
api_key = "your-azure-openai-api-key-here"

[github]
user_token = "ghp_your_github_token_here"

[pr_reviewer]
model = "azure/gpt-5.2"
model_turbo = "azure/gpt-5.2"

[pr_description]
model = "azure/gpt-5.2"

[pr_code_suggestions]
model = "azure/gpt-5.2"
```

#### .secrets.toml（オプション）

機密情報を分離したい場合は`.secrets.toml`も作成できます：

```toml
[github]
user_token = "ghp_your_github_token_here"

[azure_openai]
api_type = "azure"
api_base = "https://aoairg-sub-aoai.openai.azure.com/v1"
api_key = "your-azure-openai-api-key-here"
api_version = "2025-04-01"
```

#### 設定項目の説明

#### GitHub設定
- **user_token**: GitHub Personal Access Token（上記手順で取得）

#### Azure OpenAI設定
- **api_type**: "azure"を指定
- **api_base**: Azure OpenAIのエンドポイントURL（標準形式）
- **api_key**: Azure OpenAIのAPIキー
- **api_version**: APIバージョン（2025-04-01）
- **deployment_id**: デプロイメント名（例: gpt-5.2）

#### モデル設定
- **model**: 使用するAzureモデル（azure/デプロイメント名）
- **custom_model_max_tokens**: モデルの最大トークン数（128000）

#### 設定手順
1. **GitHub Personal Access Token**を上記手順で取得
2. **Azure OpenAI**の情報をAzureポータルから確認：
   - エンドポイントURL（例: `https://your-resource.openai.azure.com`）
   - APIキー
   - デプロイメント名
3. `configuration.toml`に上記情報を記入

**注意**: 設定ファイルにはAPIキーとトークンが含まれるため、`.gitignore`に追加してください。

### 2-4. ローカル実行

設定ファイルを作成後、以下のコマンドでPRをレビューします：

```bash
python -m pr_agent.cli --pr_url=https://github.com/owner/repo/pull/番号 review
```

#### 主なコマンド

- `review` - PRのレビューとコード改善提案を生成
- `describe` - PRの説明とタイトルを自動生成
- `improve` - コード改善提案を生成
- `ask "質問内容"` - PRについて質問

#### 実行例

```bash
# PRのレビュー
python -m pr_agent.cli --pr_url=https://github.com/masayuki-iga-bp/java-review-test/pull/4 review

# PRの説明を生成
python -m pr_agent.cli --pr_url=https://github.com/masayuki-iga-bp/java-review-test/pull/4 describe

# PRについて質問
python -m pr_agent.cli --pr_url=https://github.com/masayuki-iga-bp/java-review-test/pull/4 ask "このPRのテストカバレッジは十分ですか？"
```

---

## トラブルシューティング（ローカル実行時）

### 設定ファイルが読み込まれない

**症状**: `'DynaBox' object has no attribute 'user_token'`

**解決方法**:
- カレントディレクトリがプロジェクトルートであることを確認
- `configuration.toml`にGitHub tokenが記載されているか確認

### モデルエラー

**症状**: `Model azure/gpt-5.2 is not defined`

**解決方法**:
- `configuration.toml`に`custom_model_max_tokens = 128000`を追加

### API接続エラー

**解決方法**:
- Azure OpenAIのエンドポイントURL、APIキー、デプロイメント名を確認
- api_base は標準形式（`https://your-resource.openai.azure.com`）を使用
- api_type は `"azure"` を指定

### 認証エラー

**解決方法**:
- GitHub Personal Access Tokenの有効期限を確認
- Azure OpenAIのAPIキーが正しいか確認

### ローカル実行が動作しない場合

ローカルCLI実行で問題が発生する場合は、**GitHub Actionsでの実行を推奨**します。GitHub Actionsは公式にサポートされている実行環境で、ローカル実行よりも安定して動作します。

---

## 参考情報

- [PR-Agent公式ドキュメント](https://github.com/Codium-ai/pr-agent)
- [Qodo Merge（PR-Agentの新名称）](https://www.qodo.ai/products/qodo-merge/)

**注意**: ローカル実行時のAzure OpenAI統合は環境により動作が不安定な場合があります。本番環境ではGitHub Actionsの使用を推奨します。


