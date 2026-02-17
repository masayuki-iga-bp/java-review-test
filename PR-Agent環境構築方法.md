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

---

### ステップ3: ワークフローファイルを確認

このリポジトリには既に設定済みのファイルがあります：

```
.github/workflows/pr-agent-openai.yml  ✅ OpenAI版（有効）
.github/workflows/pr-agent.yml.disabled  ⚠️ Azure版（無効化済み）
```

**何もする必要はありません。**

---

### ステップ4: 動作確認

#### 4-1. 新しいブランチを作成

```bash
git checkout -b feature/test-pr-agent
```

#### 4-2. テスト用のコード変更を追加

任意のファイルを編集（例: README.mdに1行追加）

```bash
git add -A
git commit -m "PR-Agent動作テスト"
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


