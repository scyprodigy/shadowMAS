> status: draft / source-evidence
> authority: none
> do not promote without governance review

# SHADOWMAS-CLAUDE-CODE-ADAPTER-PLAN.v0

> Layer 4 Runtime Adapter 設計書 — RideDispatch + shadowMAS v0
> Scope: Claude Code 作為 L2 決策樞紐時的 prompt 分層、skills 呼叫、hooks 攔截、delegation 規則
> Out of scope: shadowMAS 治理真相修改、RideDispatch 商業規格、Week 1 實際程式碼

---

## 執行摘要(zh-TW)

shadowMAS 在 2026 年的定位不是跟 Google A2A 或 Microsoft Agent Governance Toolkit 競爭,而是在他們服務不到的 niche 活下來:**個人或小團隊在自己電腦上用任意 coding agent 組合時的最小治理契約**。A2A 是企業資料中心的 TCP/IP,AGT 是企業 agent fleet 的 Kubernetes,shadowMAS 是**個人工作站時代的 Unix** —— 小、可駭、不綁廠商、形體可變但邊界恆定。本計畫書把這個定位具體化為八章節:層級映射、prompt 組裝、session bootstrap、skills 政策、hooks 政策、delegation 路由、當前階段護欄、輸出格式。

本計畫採三層檔案分離(`shadowmas/` 治理本體 read-only、`~/.shadowmas-user/` 使用者私人層、`{project}/.shadowmas/` 專案 domain 層),以 AGENTS.md 當跨工具入口(Codex/Cursor/Gemini/Copilot 原生支援),`~/.claude/CLAUDE.md` symlink 到 `~/AGENTS.md` 做單一真相,Shared Core 透過 `distribute.sh` 一鍵分發,Ollama 走呼叫端 system prompt 注入。Agent 角色採**可切換模式**(dynamic / fixed / self_claim),由使用者依場景切換而非依心情。Hook 採三類檢查(固定閘門 / 隨機抽驗 / 強制性攔截)對應 Calibrated Trust 框架,避免 rubber-stamping。Packet 採融合版共用 shell,欄位設計允許未來嵌套進 A2A Message 的 Parts。

---

## 1. Layer Mapping(層級映射)

每個協作元件都必須對應到 shadowMAS 的 L / T / R 三軸,並明確可做與不可做。這避免任何單一元件僭越治理邊界。

### 1.1 主映射表

| 元件 | L-layer | T-layer | R-layer 參與 | 可決策? | 可寫入? | 可 promote? | 絕對禁止 |
|---|---|---|---|---|---|---|---|
| 人類(你/老闆) | L1 | T0 | N/A | 是(最終) | 是 | 是 | — |
| GPT head session | L1/L2 | T1 | 否 | 是(範圍內) | 是(packet) | 否(僅 propose) | 動本地 hook 細節、改 shadowMAS 治理真相 |
| Claude Code session | L2(主)/L3(受限) | T1 | 是(呼叫 hook) | 是(範圍內) | 是(packet/patch) | 否(僅 propose) | 改 shadowMAS 真相、補商業規格、跨任務 scope |
| Codex CLI session | L2 或 L3(視指派) | T1 或 T4 | 是 | 視 role | 是 | 否 | 同上 |
| Cursor | L3 | T4 | 部分(1.7+ hooks) | 否 | 是(受 packet 限) | 否 | 自行決策、補規格、改架構 |
| Ollama(本地小模型) | R 或 T5/低風險 T4 | T5 | 是 | 否 | 是(暫時) | 否 | 安全/schema/auth/架構任何決策 |
| Hooks(Claude Code) | — | — | R | 否 | 否(僅攔截/記錄) | 否 | 充當 truth source |
| Skills(SKILL.md) | Layer 4 | — | R 支援 | 否 | 否 | 否 | 充當 canonical truth |
| `shadowmas/` repo | — | T2 | — | — | read-only for agents | — | 被 agent 直接改 |
| `~/.shadowmas-user/` | — | T2 | — | — | 人類手動改 | — | 被 agent 直接改 |
| `{project}/.shadowmas/` | — | T2 | — | — | 人類手動改 | — | 被 agent 直接改 |
| `{project}/AGENTS.md` | — | T2(投影) | — | — | 由 distribute.sh 產出 | — | 被 agent 直接改 |
| session memory / context | — | T5 | R | 否 | 是(session 內) | 否 | 充當 truth |
| Cache(任何) | — | T5 | R | 否 | 是(暫時) | 否 | 充當 truth,或 survive session |

### 1.2 關鍵原則

`owner` 與 `writable_by` 永遠分離。shadowMAS 治理本體對 agent 是 read-only,只有人類可改 —— 這不是技術限制,是 T-layer 不跨級的治理原則落地。任何 agent 在任何時刻嘗試寫入 `shadowmas/` 或 `~/.shadowmas-user/`,hook 硬擋。

---

## 2. Prompt Composition Plan(Prompt 組裝計畫)

### 2.1 三層分離檔案結構

```
shadowmas/                                  ← 開源治理本體(read-only for agents)
├── 01_truth/                               ← shadowMAS 治理真相
│   ├── SHADOWMAS-CURRENT-TRUTH.v0.en.md
│   ├── SHADOWMAS-PROMPT-LAYERING-CONTRACT.v0.en.md
│   ├── SHADOWMAS-GOVERNANCE-MATRIX.v0.en.md
│   ├── SHADOWMAS-CHANGE-IMPACT-MAP.v0.en.md
│   └── SHADOWMAS-TRANSLATION-POLICY.v0.en.md
├── 02_packets/
│   └── packet_common_shell.v0.yaml         ← 融合版 packet shell
├── bin/
│   ├── distribute.sh                       ← 一鍵分發
│   └── install.sh                          ← 首次裝配
├── templates/
│   ├── shared_core.template.md
│   ├── project_execution.template.md
│   ├── agents.template.yaml
│   └── claude-code-settings.template.json
└── MANIFESTO.md

~/.shadowmas-user/                          ← 使用者私人層(跨專案)
├── shared_core.md                          ← 個人 L1 行為準則
├── agents.yaml                             ← agent registry
├── preferences.md                          ← 個人偏好(zh-TW 對話等)
└── outputs/                                ← distribute.sh 產出
    ├── chatgpt_custom.txt                  ← 手動貼 ChatGPT Custom Instructions
    └── ollama_system.txt                   ← Ollama 呼叫端 load

(分發到全域路徑,agent 自動讀取:)
~/AGENTS.md                                 ← Codex/Cursor/Gemini/Copilot 入口
~/.claude/CLAUDE.md                         → symlink to ~/AGENTS.md
~/.claude/claude-specific.md                ← Claude Code 專屬指令(hook 路徑等)

{project}/                                  ← 商業專案(RideDispatch)
├── .shadowmas/
│   ├── project_execution.md                ← 專案 domain truth
│   └── decisions.yaml                      ← 專案禁令/ADR
├── AGENTS.md                               ← distribute.sh 產出,專案層入口
├── CLAUDE.md                               → symlink to AGENTS.md
├── .cursor/
│   └── rules/
│       └── shadowmas.mdc                   ← distribute.sh 產出(Cursor 1.7+)
├── .claude/
│   ├── settings.json                       ← hook 配置
│   ├── skills/                             ← SKILL.md 格式(跨工具通用)
│   │   ├── bootstrap-interview/
│   │   ├── core-reasoning/
│   │   ├── system-analyst/
│   │   └── task-delegator/
│   └── hooks/                              ← hook 實際 shell script
└── ...專案其他檔案...
```

### 2.2 單一真相流(Single Source of Truth Flow)

每一份「看起來重複」的檔案,都有唯一上游。

| 終端 agent 讀到的檔 | 真正的來源 | 如何同步 |
|---|---|---|
| Claude Code 讀 `~/.claude/CLAUDE.md` | `~/AGENTS.md` | symlink,無需分發 |
| Claude Code 讀 `~/AGENTS.md` | `~/.shadowmas-user/shared_core.md` | `distribute.sh` 產出 |
| Codex 讀 `~/AGENTS.md` | 同上 | 同上 |
| Cursor 讀 `.cursor/rules/shadowmas.mdc` | `~/.shadowmas-user/shared_core.md` + project 層 | `distribute.sh` 產出 |
| 任何 agent 讀 `{project}/AGENTS.md` | `{project}/.shadowmas/project_execution.md` | `distribute.sh` 產出 |
| Ollama 收到 system prompt | `~/.shadowmas-user/outputs/ollama_system.txt` | 呼叫端程式 load |
| ChatGPT 人類貼 Custom Instructions | `~/.shadowmas-user/outputs/chatgpt_custom.txt` | 人類手動貼(Layer 5 限制) |

改一次 `shared_core.md` → 跑一次 `distribute.sh` → 全 agent 同步。100 個專案、N 個 agent,分發目標都是全域路徑,成本不隨數量膨脹。

### 2.3 長度紀律(對應 Silent Rule Dropout 研究)

研究顯示 frontier LLM 可靠遵守約 150~200 條指令,Claude Code 系統 prompt 已耗用約 50 條。因此:

- `~/AGENTS.md` ≤ 200 行
- `{project}/AGENTS.md` ≤ 200 行
- 合計單 session 上限 ≤ 400 行的 persistent context
- 超過就切 skill(on-demand 載入,不佔每輪 context)

重要規則放檔案前段,避免 lost-in-the-middle。

---

## 3. Claude Code Session Bootstrap(開場協議)

Claude Code 進入 RideDispatch 時的固定啟動序列。**不做 repo 全盤 traversal。**

### 3.1 啟動序列(每 session 一次)

```
Step 1. 讀取持續性上下文(SessionStart hook 自動注入 + 啟動時讀檔):
  - ~/AGENTS.md                                    (Shared Core,永遠在)
  - ~/.claude/claude-specific.md                   (Claude-only 補充)
  - {project}/AGENTS.md                            (專案 domain truth)
  - {project}/.shadowmas/decisions.yaml            (專案禁令)

Step 2. 宣告當前狀態(agent 主動輸出,給人類確認):
  - 當前專案: RideDispatch
  - 當前 phase: Week 1 (minimal order creation loop)
  - 已讀 truth 檔: [列表]
  - 偵測到的 unresolved questions from last session (若有 sync 紀錄)
  - 本 session 可行動範圍: [依 phase guardrail]
  - 本 session 禁止範圍: [依 phase guardrail]

Step 3. 等待人類明確任務指令。
  - 不主動開始工作
  - 不主動 traverse repo
  - 不主動讀檔除非任務需要

Step 4. 人類下達任務後:
  - 先 scope_identify
  - 再 feynman_explain(zh-TW)
  - 再 list_options(≤4, 含 tradeoff)
  - 等 user_chooses
  - 再 decompose_tasks
  - 等 user_confirms
  - 收到 "produce" 才真正產出

Step 5. 動作前檢查(hook 自動執行,agent 也要自律):
  - 要讀檔? 該檔在 scope 內嗎?
  - 要編輯? 該檔在 scope 內嗎? 是受保護檔案嗎?
  - 要跑 bash? 在 bash 白名單嗎?
  - 要派 task 給其他 agent? packet 格式合規嗎?
```

### 3.2 Decided / Pending / Undefined 三色標記

Agent 在 Step 2 和任何 status 指令下,必須輸出這三色:

- **Decided**: 已經由人類確認,可以執行
- **Pending**: 已經進入討論,等人類 decide
- **Undefined**: 尚未被任何人提出,不可假設

**「Undefined 不是 Decided」** 是 Shared Core 裡的硬原則。agent 看到空白不能腦補。

---

## 4. Skills Invocation Policy(Skills 呼叫政策)

SKILL.md 格式 2026 年跨 30+ 工具通用(Claude Code / Codex / Cursor / Gemini CLI / Copilot / Windsurf / ...)。你現有四個 skill 只要格式對就全工具可用。

### 4.1 逐 skill 政策

#### `bootstrap-interview`
- **觸發條件**: Project Knowledge 空、使用者說 "new project" / "從頭描述" / `{project}/.shadowmas/project_execution.md` 不存在
- **允許輸出**: 結構化訪談問題、初步系統架構草稿、decisions.yaml 草稿
- **禁止輸出**: 程式碼、直接產 production artifact、宣稱任何決策為 final
- **支援哪個 tier**: L2 決策 agent 使用(Claude Code / Codex / GPT head)
- **人類確認前後**: **只能在人類確認前使用**。用來幫人類把模糊想法變成明確規格。產出是 proposal,不是 truth

#### `core-reasoning`
- **觸發條件**: 多選項抉擇、對話品質下滑、task 即將派給下線、review 回包要評估、偵測到 context drift
- **允許輸出**: 選項分析(≤4 + tradeoff)、反駁點、驗證清單、session 切換建議
- **禁止輸出**: 直接做決策(只能 list 選項)、補未說的事實
- **支援哪個 tier**: L1 / L2 都可用
- **人類確認前後**: **確認前主用**(幫人類想清楚)。確認後用於審查下線回包

#### `system-analyst`
- **觸發條件**: 討論模組設計、API 規劃、phase transition、ERD、tech stack 決策、多模組任務拆解
- **允許輸出**: 架構圖文字描述、phase gate 檢查清單、模組邊界草案、ADR 候選
- **禁止輸出**: 直接宣告 phase 已完成、commit schema、自己做架構 final call
- **支援哪個 tier**: L2(Claude Code 主)
- **人類確認前後**: **兩端都可**。確認前幫人類畫系統地圖,確認後做 phase gate

#### `task-delegator`
- **觸發條件**: Claude Code 已決定要把任務派給 Cursor / Ollama / 其他 agent
- **允許輸出**: 合規的 task_packet YAML(依 §6 delegation routing 的欄位)
- **禁止輸出**: 跳過 packet 直接下指令、省略 acceptance_criteria / stop_conditions、自創 packet 欄位
- **支援哪個 tier**: L2 決策 agent
- **人類確認前後**: **確認後**。packet 產出即意味著派工,這是執行層動作

### 4.2 Skills 紀律三原則

1. **One skill, one job.** 不做 mega-skill。
2. **Skills 不是 truth source.** 呼叫 skill 只是載入推理模板,產出還是要經 review。
3. **Skills 可被 SessionStart hook 建議但不強制呼叫.** AI 看情況判斷。但如果動作需要某 skill(例如派工要用 task-delegator),hook 會檢查產出格式,不符就擋。

---

## 5. Hooks Policy(Hook 政策)

Hook = 動作最後一公尺的柵欄。Claude 自律靠 skill 和 prompt,但自律會被 context drift 和 rubber-stamping 侵蝕。hook 是 deterministic 的,不會忘。

### 5.1 三類檢查架構(對應 Calibrated Trust)

| 類別 | 觸發方式 | 目的 | 例子 |
|---|---|---|---|
| **固定閘門** | 特定事件必觸發 | 高風險動作必審 | git push、schema change、第一層目錄 |
| **隨機抽驗** | 機率觸發(5~20%) | 防 rubber-stamping、抽測 agent 自律 | 普通編輯後隨機跑 lint、隨機要求 agent 自述 scope |
| **強制性攔截** | PreToolUse 擋住不讓動 | 絕對禁區 | .env、secrets、`shadowmas/` 本體寫入 |

v0 先實作**固定閘門 + 強制性攔截**。隨機抽驗在 v0.5。

### 5.2 v0 Hook 最小集(7 條全上)

| # | 名稱 | 事件 | matcher | 類別 | 行為 | 阻擋或僅記錄 |
|---|---|---|---|---|---|---|
| H1 | `pre-git-push` | PreToolUse | Bash (含 `git push`) | 固定閘門 | 檢查 commit message 格式、檢查 session 內是否已宣告「準備 push」 | **硬擋**(exit 2) |
| H2 | `pre-schema-edit` | PreToolUse | Edit\|Write (path 含 `prisma/schema.prisma` 或 `*/migrations/*`) | 固定閘門 | 檢查 decisions.yaml 是否已 approve schema 版本 | **硬擋** |
| H3 | `pre-root-dir-change` | PreToolUse | Bash (含 `mkdir\|rm\|mv` 且 path depth=1) | 固定閘門 | repo root 下建 / 刪 / 改名資料夾 | **硬擋** |
| H4 | `pre-sensitive-file` | PreToolUse | Edit\|Write (path 匹配 `.env*\|secrets/*\|*.key\|*.pem`) | 強制性攔截 | 敏感檔直接擋 | **硬擋** |
| H5 | `pre-phase-transition` | PreToolUse | Edit (path = `decisions.yaml` 且 diff 含 `phase:`) | 固定閘門 | 階段轉換必須人類確認 | **硬擋** |
| H6 | `pre-delegate-packet` | PreToolUse | Task 或偵測到派工 YAML | 固定閘門 | 檢查 packet 必要欄位完整、符合 common shell | **硬擋**(回訊息「請用 task-delegator skill」) |
| H7 | `post-multi-file-edit` | PostToolUse | MultiEdit 或單 session 內累積 >5 檔 | 固定閘門(advisory) | 警告範圍擴大 | **僅警告**(exit 0 + 訊息) |

### 5.3 Session Lifecycle Hooks(對應「agent 不會忘」機制)

| # | 名稱 | 事件 | 行為 |
|---|---|---|---|
| HS1 | `session-start-inject` | SessionStart | 自動把 `~/AGENTS.md` + `{project}/AGENTS.md` + `decisions.yaml` 重點注入 additionalContext |
| HS2 | `pre-compact-reinject` | PreCompact | Context 要被壓縮前,重新注入 hard constraints |
| HS3 | `stop-suggest-new-session` | Stop | 單 session 超過 X 輪或連續失敗 2 次,建議人類 `/clear` 開新 session |

這三個 hook 合起來就是你要的「強制提示不會忘記」機制。

### 5.4 Hook 的絕對邊界

Hook 可以:攔截動作、記錄、警告、要求重試、要求 agent 呼叫特定 skill。

Hook **不可以**:
- 被視為 truth source
- 自行 promote 任何產出
- 修改 agent 的推理(只能擋動作)
- 繞過人類認證去執行高風險動作

Hook 的 `exit 2` 只擋當下這一動,不會改變 agent 的中期計畫 —— 這是合規設計。

### 5.5 隨機抽驗預留(v0.5)

v0 不實作,但在 settings.json 裡保留 matcher hook,未來接上即可:

- 5% 機率:編輯後要求 agent 自述 `{編輯了什麼 / 在 scope 內嗎 / acceptance_criteria 哪幾條}`
- 10% 機率:派工 packet 送出前,跑一次 `core-reasoning` skill 做 devil's advocate
- 20% 機率:Stop hook 觸發時,要求 agent 產 session summary 存檔

---

## 6. Agent Delegation Routing(Agent 派工路由)

### 6.1 三種 role assignment 模式

```yaml
role_assignment:
  mode: dynamic | fixed | self_claim
```

**這不是依心情切換,是依場景切換。** 三種模式對應三種場景:

| 模式 | 使用場景 | 運作方式 |
|---|---|---|
| `fixed` | **專案穩定、流程已驗證** | 使用者在 agents.yaml 寫死 decision/execution/helper 指派,linear pipeline,沒有意外 |
| `dynamic` | **專案探索期、需要實驗** | 依 agent 能力標籤 + 歷史分數動態指派,失敗會調分,表現差的會被冷卻 |
| `self_claim` | **多 agent 並存、追求效率** | packet 丟出 `agent_id=null`,合格能力的 agent 自行認領,先到先得 |

切換時機應記錄在 `decisions.yaml`,避免無來由切換造成混亂。

### 6.2 Claude Code → Cursor(L3 execution)

**只允許用 task_packet,不允許自由指令。**

Packet 必要欄位(依 §8 common shell):

```yaml
packet_family: task
agent_role: execution
required_capabilities: [code_edit, local_refactor]
payload:
  goal: string
  scope: [file_paths]
  out_of_scope: [file_paths or concept boundaries]
  truth_touchpoints: [reference to ~/AGENTS.md or project decisions]
  worker_plan: [step1, step2, ...]
  acceptance_criteria: [testable assertions]
  stop_conditions: [when to abort and escalate]
```

Cursor 回報必須包含(review_packet):

```yaml
packet_family: review
payload:
  files_changed: [paths]
  tests_run: [names, results]
  blockers: [list, empty if none]
  scope_exceeded: boolean
  acceptance_satisfied: [per criterion]
  notes: string
```

### 6.3 Claude Code → Ollama(R-layer helper)

只允許原子小任務,單檔或單輸出,**絕對不下放決策**。

Packet 必要欄位:

```yaml
packet_family: task
agent_role: helper
required_capabilities: [atomic_extraction | normalization | summarization]
payload:
  goal: string (single-atomic)
  input: string or file_path
  output_schema: json_schema or plain_text
  acceptance_criteria: [exact matching or structural]
  fallback: "return null if uncertain"
```

Ollama 產出必須經 Claude Code 複核後才可用於下游。絕不直接餵進 review 或 promotion 流程。

### 6.4 GPT head session → Claude Code

GPT 提供:dispatch routing 訊息、當前 phase、任務意圖、邊界。

GPT **不需要**傾倒整個 shadowMAS —— Claude Code 本地已經有 `~/AGENTS.md`。GPT 給的訊息越小越好,避免 context 浪費。

### 6.5 Claude Code → GPT head(回流)

Claude Code 產出 adapter proposal、unresolved questions、mergeback 建議。GPT 負責把這些整合進 dispatch 紀錄,決定下一輪任務。

**Claude Code 不直接寫 dispatch 檔案,只產 packet 回給 GPT。** 這保留 T-layer 不跨級原則。

---

## 7. Current Phase Guardrail(當前階段護欄)

### 7.1 RideDispatch Week 1 Scope

**允許的**:
- 前端: `/dashboard`, `/orders/create`, `/no-access`, API client skeleton, mock/real switch, typecheck/build
- 後端: `/health`, `POST /orders`, `POST /orders/force-create` 或 stable contract, stable response/error format, stable geofence blocked response, CORS/base URL

**禁止的(Week 1 硬擋)**:
- Dispatch module(任何形式)
- Station module
- Chat module
- Audit Center
- Management CRUD
- 權限 persistence
- CTI 整合
- 正式 Auth
- 正式 Audit
- Wallet
- 第一層目錄新增

### 7.2 Phase Guardrail 如何落地到 adapter

1. `{project}/.shadowmas/decisions.yaml` 裡 `current_phase: week_1_minimal_order_loop` 欄位
2. `{project}/AGENTS.md` 前段硬寫當前 phase 與禁止 scope
3. H5 `pre-phase-transition` hook 鎖住 phase 欄位修改
4. task-delegator skill 檢查 packet scope 是否落在當前 phase 允許範圍,否則拒絕產出 packet
5. Claude Code session bootstrap Step 2 必須宣告當前 phase

未來切 Week 2 時,人類手動改 `decisions.yaml` → 觸發 H5 → 確認 → distribute.sh 重跑 → 新 phase 生效。

---

## 8. Output Format(輸出格式)

### 8.1 本 adapter 計畫的 YAML 自描述

見 `adapter-plan.v0.yaml`。

### 8.2 Packet common shell

見 `packet_common_shell.v0.yaml`。

### 8.3 可貼 Claude Code 的開場 prompt

見 `bootstrap-prompt.md`。

### 8.4 風險與待解

見 `RISKS-AND-UNRESOLVED.md`。

---

## 結尾聲明

本計畫為 Layer 4 Runtime Adapter 設計草案。不修改 shadowMAS 治理真相、不補 RideDispatch 商業規格、不跨越 L2 planning 範圍。所有產出以 packet 形式丟給 GPT head session 整合,人類保有最終 merge 決定權。
