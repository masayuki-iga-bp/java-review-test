# PR-Agent 自動レビューシステム セットアップガイド

## 📖 このドキュメントについて

**ゼロから同じ環境を構築できる完全ガイドです。**

- プログラミング知識不要
- 手順通りに進めれば必ず動作します
- 所要時間: 30分

---

## 🎯 完成すると何ができるか

プルリクエスト（PR）を作成すると、**AIが自動的にコードレビュー**してくれます。

**レビュー内容:**
- セキュリティの問題
- パフォーマンスの問題
- バグの可能性
- コード品質の改善提案

すべて日本語で表示されます。

---

## 📋 必要なもの

以下のいずれかが必要です：

### Option A: OpenAI API（推奨・すぐ使える）
- ✅ OpenAIアカウント
- ✅ APIキー（有料・$5チャージで十分）
- ✅ インターネット接続のみ

### Option B: Azure OpenAI（企業向け）
- Azure OpenAIリソース
- ネットワーク設定権限（管理者が必要）

**初めての方はOption Aを推奨します。**

---

## 🏗️ プロジェクト作成（0からの場合）

既存のJavaプロジェクトがある場合は、このセクションをスキップしてください。

### 方法1: Gradleで新規作成（推奨）

```bash
# 新しいディレクトリを作成して移動
mkdir my-java-project
cd my-java-project

# Gradleプロジェクトを初期化
gradle init
```

**以下の質問に答えます:**

| 質問 | 選択肢 | 説明 |
|------|--------|------|
| type of build | `application` | アプリケーションを作成 |
| language | `Java` | Java を選択 |
| target Java version | `21` | Java 21 |
| Project name | `(そのままEnter)` | ディレクトリ名が使われる |
| application structure | `Single application` | 単一アプリ |
| build script DSL | `Groovy` | Groovy（標準） |
| test framework | `JUnit Jupiter` | JUnit 5 |
| Generate new APIs | `no` | そのままEnter |

**完了すると以下の構造が作成されます:**

```
my-java-project/
├── app/
│   └── src/
│       ├── main/java/    ← Javaコードをここに書く
│       └── test/java/    ← テストコードをここに書く
├── gradle/
├── gradlew
├── gradlew.bat
├── build.gradle
└── settings.gradle
```

### 方法2: GitHubで新規リポジトリ作成

```bash
# GitHubに新しいリポジトリを作成（Web UIで）
# 1. GitHub.com → New repository
# 2. Repository name を入力（例: my-java-project）
# 3. "Add a README file" をチェック
# 4. Create repository

# ローカルにクローン
git clone https://github.com/your-username/my-java-project.git
cd my-java-project

# Gradleプロジェクトを初期化（上記と同じ手順）
gradle init
```

### ✅ プロジェクト作成完了の確認

以下のコマンドが成功すればOK:

```bash
# ビルドテスト
./gradlew build

# 成功すると "BUILD SUCCESSFUL" と表示される
```

---

## 🚀 セットアップ手順

### ステップ1: OpenAI APIキーを取得

1. https://platform.openai.com にアクセス
2. サインアップ/ログイン
3. 画面右上のアイコン → **API keys** をクリック
4. **+ Create new secret key** をクリック
5. 名前を入力（例: `pr-agent-key`）
6. **Create secret key** をクリック
7. **表示されたキーをコピー**（後で使います）
   - `sk-proj-` で始まる長い文字列
   - ⚠️ 二度と表示されないので必ずコピー

8. **課金設定**（重要）
   - 画面左メニュー → **Settings** → **Billing**
   - **Add payment method** でクレジットカード登録
   - **Add to credit balance** で $5 チャージ
   - ✅ これがないとAPIが動作しません

---

### ステップ2: GitHub Secretsに登録

1. GitHubリポジトリページを開く
2. 上部メニューの **Settings** をクリック
3. 左メニューの **Secrets and variables** → **Actions** をクリック
4. **New repository secret** をクリック
5. 以下を入力：
   - **Name**: `OPENAI_API_KEY`
   - **Secret**: （ステップ1でコピーしたキー）
6. **Add secret** をクリック

✅ これで設定完了です。

**💡 重要:** APIキーはリポジトリごとに設定が必要です。複数のプロジェクトで使う場合、同じAPIキーの値を各リポジトリに設定できます。

---

### ステップ3: ワークフローファイルを作成

PR-Agentを動かすための設定ファイルを作成します。

#### 3-1. ディレクトリを作成

```bash
mkdir -p .github/workflows
```

#### 3-2. ワークフローファイルを作成

`.github/workflows/pr-agent-openai.yml` というファイルを作成し、以下の内容を貼り付けます：

<details>
<summary>📄 pr-agent-openai.yml の内容（クリックして展開）</summary>

```yaml
name: PR Agent Review (OpenAI)

on:
  pull_request:
    types: [opened, reopened, synchronize]
  pull_request_review_comment:
    types: [created]
  workflow_dispatch:

jobs:
  pr-agent:
    runs-on: ubuntu-latest
    permissions:
      contents: read
      pull-requests: write
      issues: write
    
    steps:
      - name: Checkout repository
        uses: actions/checkout@v4

      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: '3.11'

      - name: Install PR-Agent
        run: |
          pip install --upgrade pr-agent
          pip install --upgrade litellm httpx openai

      - name: Test OpenAI API Connection
        env:
          OPENAI_API_KEY: ${{ secrets.OPENAI_API_KEY }}
        run: |
          echo "=== Testing OpenAI API with curl ==="
          curl -X POST https://api.openai.com/v1/chat/completions \
            -H "Content-Type: application/json" \
            -H "Authorization: Bearer ${OPENAI_API_KEY}" \
            -d '{
              "model": "gpt-4o-mini",
              "messages": [{"role": "user", "content": "Test"}],
              "max_tokens": 10
            }' \
            -w "\nHTTP Status: %{http_code}\n" \
            2>&1 | tee curl-result.log
          
          if grep -q "200" curl-result.log || grep -q "content" curl-result.log; then
            echo "✅ OpenAI API connection successful!"
          else
            echo "❌ OpenAI API connection failed"
            exit 1
          fi

      - name: Create configuration
        env:
          GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
        run: |
          cat > .pr_agent.toml << CONFIG
          [config]
          model = "gpt-4o-mini"
          model_turbo = "gpt-4o-mini"
          fallback_models = []
          language = "ja"
          
          [github]
          user_token = "${GITHUB_TOKEN}"
          
          [pr_reviewer]
          num_code_suggestions = 3
          require_tests_review = false
          require_score_review = false
          extra_instructions = "すべてのレビューコメントを日本語で記述してください。"
          
          [pr_description]
          publish_description_as_comment = true
          
          [pr_code_suggestions]
          num_code_suggestions = 3
          CONFIG
          
          echo "=== Configuration file content ==="
          cat .pr_agent.toml

      - name: Run PR-Agent Review
        env:
          OPENAI_API_KEY: ${{ secrets.OPENAI_API_KEY }}
          OPENAI__KEY: ${{ secrets.OPENAI_API_KEY }}
          GITHUB__USER_TOKEN: ${{ secrets.GITHUB_TOKEN }}
          CONFIG__MODEL: "gpt-4o-mini"
          CONFIG__LANGUAGE: "ja"
          PR_REVIEWER__EXTRA_INSTRUCTIONS: "必ず日本語でレビューコメントを記述してください。All review comments must be written in Japanese language."
        run: |
          echo "=== Environment ==="
          echo "Model: gpt-4o-mini (OpenAI)"
          echo "Language: Japanese"
          echo "=== Running PR-Agent ==="
          python -m pr_agent.cli \
            --pr_url=https://github.com/${{ github.repository }}/pull/${{ github.event.pull_request.number }} \
            review
```

</details>

**このファイルの役割:**
- PRが作成されると自動実行
- OpenAI APIを使ってコードレビュー
- レビューを日本語で投稿

#### 3-3. ファイルをコミット

```bash
git add .github/workflows/pr-agent-openai.yml
git commit -m "Add PR-Agent workflow"
git push origin main
```

✅ これでセットアップ完了です。

---

### ステップ4: 動作確認

#### 4-1. 新しいブランチを作成

```bash
git switch -c feature/test-pr-agent
```

#### 4-2. テスト用のコード変更を追加

**簡単な例: README.mdに1行追加**

```bash
echo "PR-Agent test" >> README.md
```

**Javaコードの例: 意図的に問題のあるコードを追加**

`app/src/main/java/myproject/Calculator.java` を作成：

```java
package myproject;

public class Calculator {
    // 問題: JavaDocなし、例外処理なし
    public int divide(int a, int b) {
        return a / b;
    }
    
    // 問題: マジックナンバー、nullチェックなし
    public int getLength(String text) {
        if (text.length() > 100) {
            return 100;
        }
        return text.length();
    }
}
```

**変更をコミット:**

```bash
git add -A
git commit -m "Add test code for PR-Agent review"
git push -u origin feature/test-pr-agent
```

#### 4-3. プルリクエストを作成

```bash
gh pr create --title "PR-Agent動作テスト" --body "自動レビューのテストです"
```

または GitHub Web UI で:
1. リポジトリページの **Pull requests** タブ
2. **New pull request** をクリック
3. ブランチを選択してPR作成

#### 4-4. レビューが投稿されるのを待つ

1. PR画面で **Checks** タブを確認
2. 「PR Agent Review (OpenAI)」が実行される（1-2分）
3. ✅ 成功したら、PR画面に戻る
4. **Conversation** タブにレビューコメントが表示される

**成功例:**
```
github-actions commented
## PR Reviewer Guide 🔍

⏱️ Estimated effort to review: 3 🔵🔵🔵⚪⚪
🔒 Security concerns
　ハードコードされた認証情報: ...
⚡ Key issues to review
　ドキュメント不足: ...
```

---

## 🔧 トラブルシューティング

### ❌ ワークフローが失敗する

#### 問題1: "Incorrect API key provided"

**原因**: APIキーが間違っているか、課金されていない

**解決方法**:
1. OpenAI Platform → **Billing** を確認
2. クレジットが残っているか確認
3. APIキーを再作成してGitHub Secretsを更新

#### 問題2: "AsyncClient.__init__() got an unexpected keyword argument 'proxies'"

**原因**: ライブラリのバージョン不整合

**解決方法**: 既に修正済み（ワークフローに `pip install --upgrade litellm httpx openai` が含まれています）

#### 問題3: レビューコメントが投稿されない

**原因**: GitHub tokenの権限不足

**解決方法**: 既に修正済み（環境変数 `GITHUB__USER_TOKEN` が設定されています）

---

## 🌐 日本語レビューの仕組み

以下の設定により、レビューが日本語で表示されます：

```yaml
CONFIG__LANGUAGE: "ja"
PR_REVIEWER__EXTRA_INSTRUCTIONS: "必ず日本語でレビューコメントを記述してください。"
```

**既に設定済みです。何もする必要はありません。**

---

## 🏢 Azure OpenAIを使う場合（企業向け）

### 必要な追加手順

#### 1. Azure管理者にネットワーク設定を依頼

**依頼内容:**
```
Azure OpenAI リソース「[リソース名]」のネットワーク設定変更をお願いします。

変更箇所:
Azure Portal → リソース → リソース管理 → ネットワーク
→ 「すべてのネットワーク」のラジオボタンにチェック

理由: GitHub Actions (IP範囲 13.64.0.0/16) からのアクセスを許可するため
```

#### 2. GitHub Secretsを追加

| Secret名 | 例 |
|---------|-----|
| `AZURE_OPENAI_API_KEY` | `abc123...` |
| `AZURE_OPENAI_API_BASE` | `https://your-resource.openai.azure.com` |
| `AZURE_OPENAI_DEPLOYMENT_ID` | `gpt-4` |

#### 3. Azureワークフローを有効化

```bash
git mv .github/workflows/pr-agent.yml.disabled .github/workflows/pr-agent.yml
git add -A
git commit -m "Azureワークフローを有効化"
git push
```

---

## 📚 参考情報

- [PR-Agent公式ドキュメント](https://github.com/Codium-ai/pr-agent)
- [OpenAI API Documentation](https://platform.openai.com/docs)
- [GitHub Actions Documentation](https://docs.github.com/actions)

---

## ✅ チェックリスト

セットアップ完了の確認:

- [ ] OpenAI APIキーを取得した
- [ ] OpenAI アカウントに課金した（$5）
- [ ] GitHub Secretsに `OPENAI_API_KEY` を登録した
- [ ] テストPRを作成した
- [ ] レビューコメントが日本語で表示された

**すべてチェックできたら完了です！** 🎉

---

## 🆘 サポート

問題が解決しない場合:
1. GitHub Actions の実行ログを確認
2. このドキュメントのトラブルシューティングを確認
3. PR-Agent公式のIssuesを検索

**最終更新**: 2026-02-17


