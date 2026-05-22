<div align="center">

<img width="100%" src="https://capsule-render.vercel.app/api?type=waving&color=gradient&customColorList=8,12,20,24&height=200&section=header&text=ai-commit&fontSize=72&fontColor=ffffff&animation=fadeIn&desc=AI-powered%20git%20commit%20messages%20%E2%80%94%20fast%2C%20clean%2C%20conventional&descSize=17&descAlignY=70"/>

<br/>

<p>
<img src="https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white"/>
<img src="https://img.shields.io/badge/CLI-4D4D4D?style=for-the-badge&logo=gnubash&logoColor=white"/>
<img src="https://img.shields.io/badge/Multi--LLM-412991?style=for-the-badge&logo=openai&logoColor=white"/>
<img src="https://img.shields.io/badge/Arabic-006C35?style=for-the-badge"/>
<img src="https://img.shields.io/badge/MIT-000000?style=for-the-badge"/>
</p>

<p>
<img src="https://img.shields.io/github/stars/kasimmj/ai-commit?style=social"/>
<img src="https://img.shields.io/github/forks/kasimmj/ai-commit?style=social"/>
</p>

**Stop writing `fix stuff` commits.**
`ai-commit` reads your staged diff and generates a clean, conventional commit message in under a second.

```bash
$ git add .
$ ai-commit
✨ Generated commit message:

  feat(auth): add refresh-token rotation with audit log

  - Rotate refresh tokens on every use
  - Persist token family for compromise detection
  - Log all rotations to security_audit table

Accept this message? [Y/n/edit/regen]
```

[Install](#-install) • [Usage](#-usage) • [Configuration](#-configuration) • [Why?](#-why-ai-commit)

</div>

---

## ⚡ Install

### Via pip (recommended)
```bash
pip install ai-commit
```

### Via curl
```bash
curl -fsSL https://raw.githubusercontent.com/kasimmj/ai-commit/main/install.sh | bash
```

### Via git clone
```bash
git clone https://github.com/kasimmj/ai-commit
cd ai-commit && pip install -e .
```

---

## 🚀 Usage

### Basic
```bash
git add .
ai-commit
```

### Choose a model
```bash
ai-commit --model gpt-4o-mini       # OpenAI
ai-commit --model claude-haiku-4    # Anthropic
ai-commit --model llama3.2          # Local via Ollama
```

### Commit in Arabic
```bash
ai-commit --lang ar
# → "feat(auth): إضافة دورة تجديد رموز التحديث"
```

### Generate without committing
```bash
ai-commit --dry-run
```

### Auto-accept (CI / scripts)
```bash
ai-commit --yes
```

### Install as a pre-commit hook
```bash
ai-commit --install-hook
```

Now `git commit` (without `-m`) opens with the AI message pre-filled in your editor.

---

## ⚙️ Configuration

Create `~/.ai-commit.toml`:

```toml
[default]
model = "gpt-4o-mini"
language = "en"
emoji = true
max_diff_lines = 500

[providers.openai]
api_key_env = "OPENAI_API_KEY"
base_url = "https://api.openai.com/v1"

[providers.anthropic]
api_key_env = "ANTHROPIC_API_KEY"

[providers.ollama]
base_url = "http://localhost:11434"

[prompts]
# Customize the system prompt
style = "conventional"   # conventional | gitmoji | plain
length = "concise"       # concise | detailed
```

Env vars override:
```bash
AI_COMMIT_MODEL=claude-haiku-4 ai-commit
```

---

## 💡 Why ai-commit?

| Without ai-commit | With ai-commit |
|-------------------|----------------|
| `fix stuff` | `fix(api): handle 429 from upstream gracefully` |
| `wip` | `wip(dashboard): export CSV partial — handle pagination next` |
| `updates` | `chore(deps): bump axios 1.6.0 → 1.7.2 for ReDoS fix` |
| `asdfasdf` | `refactor(payments): extract Stripe client into adapter` |

You spend **3 seconds** instead of **90 seconds**, and your `git log` actually tells the story of your project.

---

## 🧠 How it works

1. Reads `git diff --cached` (your staged changes)
2. Detects the most-changed file types and scope
3. Sends a focused prompt to the chosen model
4. Parses the response into a conventional commit format
5. Shows you the result, lets you accept / edit / regenerate / cancel

The prompt is designed for **fast, cheap models** (Haiku, GPT-4o-mini, llama3.2:3b). You don't need GPT-4 for a commit message.

---

## 🔒 Privacy

- Diffs are sent to the model you choose
- **Use a local model** (Ollama) for zero data leaving your machine
- Secrets in the diff are auto-redacted (regex patterns: API keys, tokens, passwords) before sending

---

## 📜 License

[MIT](LICENSE) © 2026 [Kasim Mohammed](https://github.com/kasimmj)

---

<div align="center">

**Star ⭐ if you've ever committed `fix bug` and regretted it.**

<img src="https://capsule-render.vercel.app/api?type=waving&color=gradient&customColorList=8,12,20,24&height=100&section=footer"/>

</div>
