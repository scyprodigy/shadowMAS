> status: draft / source-evidence
> authority: none
> do not promote without governance review

# Risks & Unresolved Decisions — shadowMAS Claude Code Adapter v0

本文檔列出本 adapter 計畫中已知的風險與必須延後決定的項目。每一項都有提議的 mitigation 或 next action,但最終決定權在人類。

## 風險(Risks)

### R1 — Silent Rule Dropout 在長 session 中

**嚴重度**: 高
**現象**: Frontier LLM 研究顯示,即使規則寫在 CLAUDE.md / AGENTS.md 開頭,session 變長後仍會出現「忘記規則」的 lost-in-the-middle 效應。Claude Code 系統 prompt 已耗用約 50 條規則預算,你的 Shared Core 加 project 層加起來已逼近 200 條上限。

**緩解**:
- HS2 `pre-compact-reinject` hook 在 context 被壓縮前重新注入 hard constraints
- HS3 `stop-suggest-new-session` 主動建議切換 session
- Shared Core Section 7 hard constraints 集中放在檔案後段(LLM 對「最近讀的」記憶較好)
- 不要試圖把所有規則都放進持續性 prompt;能切到 skill on-demand 載入的就切

**未解殘留**: 即使有上述 mitigation,session 第 60 輪以後規則遵守率仍會下降。建議使用者主動養成 50 輪內 sync 並切 session 的習慣。

### R2 — Hook 透過創意 shell 語法被繞過

**嚴重度**: 高
**現象**: H1~H5 用字串匹配判斷 bash command。Agent 若用 `g""it push`、`/usr/bin/git push`、`bash -c "..."`、或 alias 包裝,可能繞過 matcher。

**緩解**:
- H1 不只看 command 字串,也檢查 process tree 與最終 syscall(進階版)
- 對所有 PreToolUse(Bash) hook 加一層「實際展開後的命令」檢查
- v0 用最直白的 matcher,並寫測試案例覆蓋常見繞過手法
- 任何 hook 被觸發後,把該命令寫進 audit log,即使是 false positive 也留紀錄

**未解殘留**: hook 永遠是 best effort,不是 cryptographic guarantee。真正的安全要靠 Microsoft AGT 等級的 ring isolation,那超出 personal-scale niche。

### R3 — distribute.sh 失敗導致 agents 不同步

**嚴重度**: 中
**現象**: 使用者改了 `~/.shadowmas-user/shared_core.md` 但忘記跑 distribute.sh,或 distribute.sh 中途失敗。Claude Code 讀到的是新版,Cursor 讀到的是舊版,兩者行為不一致。

**緩解**:
- distribute.sh 結束時寫一個 hash 檔(`.shadowmas-distribute-hash`)
- 每個 agent 啟動時(透過 SessionStart hook)檢查 hash 是否一致,不一致就警告
- distribute.sh 採 atomic 寫入(寫到 .tmp 再 mv)避免半成品狀態

**未解殘留**: ChatGPT Custom Instructions 的更新永遠是手動 —— 這是 Layer 5 host-native 限制,沒法自動。使用者需自律。

### R4 — Cursor 收到 Claude-only 指令污染

**嚴重度**: 中
**現象**: `~/.claude/claude-specific.md` 含 hook 路徑、特殊 slash command 等 Claude Code 才懂的內容。如果 distribute.sh 把它一起塞進 `.cursor/rules/`,Cursor 會困惑。

**緩解**:
- distribute.sh 在生成 `.cursor/rules/shadowmas.mdc` 時,過濾掉 `# claude-only` 標記區塊
- Shared Core 約定:任何 Claude Code 專屬指令必須包在 `<!-- claude-only-start -->` ... `<!-- claude-only-end -->` 之間
- 同樣機制保留給未來 codex-only / cursor-only 區塊

**未解殘留**: 過濾邏輯依賴使用者正確標記。不標記就會洩漏。

### R5 — Ollama 輸出未經驗證直接被信任

**嚴重度**: 中
**現象**: Ollama 處理 atomic helper 任務速度快、便宜,容易讓 Claude Code 不知不覺把它的輸出當成可靠結果直接餵進下游。

**緩解**:
- Shared Core Section 7 明列「Ollama output must be verified」
- Packet protocol 強制 Ollama 產出走 `packet_family: review` 經 Claude 複核
- task_delegator skill 對 helper 任務 packet 自動加上 `must_verify_before_reuse: true`

**未解殘留**: 「Claude 複核 Ollama」本身可能也只是看一眼。真正的驗證需要 acceptance_criteria 寫得夠 testable。

### R6 — Phase Guardrail 被創意 reframe 繞過

**嚴重度**: 低
**現象**: Week 1 禁止 Dispatch,但有人可以說「我只是寫一個 hello-world 測試,放在 dispatch/ 資料夾」,規避字面禁令。

**緩解**:
- H5 phase transition hook 防止 phase 欄位被改
- bootstrap step 2 強制宣告 phase 與禁止範圍
- task_delegator skill 在產 packet 時檢查 scope path 是否落在 forbidden_modules
- 三層防禦 defense in depth

**未解殘留**: 任何純文字判斷都有繞過空間。但組合三層後,要刻意繞才繞得過,人類手動繞責任就清楚了。

### R7 — Hooks 太多拖慢 session

**嚴重度**: 低
**現象**: 每個 PreToolUse 都跑一條 bash hook,7 條全開可能讓 session 反應變慢。

**緩解**:
- v0 hooks 都用最輕量 bash,不啟動重型程式
- 每條 hook 加 timeout(例如 500ms),超時視為 pass-through 並 log
- 分析 audit log,移除從未觸發的 hook
- 真有效能問題再考慮把多條 hook 合併成一個 dispatcher script

**未解殘留**: Claude Code 跑 hook 是同步的,時間預算有限。增加複雜邏輯前先 benchmark。

---

## 待解(Unresolved)

### U1 — Ollama 呼叫傳輸方式

**問題**: Claude Code 怎麼呼叫本機 Ollama?直接 shell 跑 `ollama run`?透過 MCP server?用 wrapper script?

**影響**: H6 packet detection 的 matcher 寫法依賴呼叫方式。

**提議**: 第一個真正的 Ollama 任務出現時再決定。屆時記錄選擇於 `decisions.yaml`。

### U2 — Packet 實體儲存位置

**問題**: task_packet 與 review_packet 實際存在哪個檔案系統路徑?

**狀態**: 不在本 adapter scope。GPT head session 負責決定。

**影響**: bootstrap step 2 的「unresolved items from last sync」偵測需要知道存放位置才能實作。

### U3 — Codex hook 對應機制

**問題**: Codex CLI 的 hook 模型與 Claude Code 不同(less mature, different events)。要做完整的 agent-agnostic,Codex 也需要一份 Layer 4 adapter。

**提議**: 設計為 v0.1 follow-up。先把 Claude Code adapter 跑順,再 port 到 Codex。

### U4 — 動態評分的持久化儲存

**問題**: agents.yaml `mode: dynamic` 啟用時,各 agent 的歷史分數存哪裡?

**影響**: dynamic mode 在沒有持久化前無法真正運作。

**提議**: 延後到 v0.5 與 memory plane 一起設計。v0 強制 `mode: fixed`。

### U5 — A2A 嵌套的具體 schema

**問題**: shadowMAS packet 怎麼確切包進 A2A Message 的 Part?

**影響**: 未來企業級升級路徑。

**提議**: 延後到 v0.5。packet shell 已預留 `a2a_wrapping` extension 欄位。

### U6 — install.sh 與 distribute.sh 的關係

**問題**: 首次安裝 shadowMAS 時,需要 `install.sh` 處理 `~/.shadowmas-user/` 初始化、template 複製、symlink 建立。後續更新由 `distribute.sh` 處理。兩者邊界?

**提議**: install.sh 只跑一次(冪等),distribute.sh 反覆跑(每次 shared_core 改後)。本 adapter 計畫不深入,留給後續設計。

### U7 — 多專案同時間執行 shadowMAS 的衝突

**問題**: 使用者同時開兩個專案的 Claude Code session,兩個專案的 `decisions.yaml` 各自有 phase。distribute.sh 是全域跑還是 per-project 跑?

**提議**: distribute.sh 接受 project path 參數,只更新指定專案。全域層的 `~/AGENTS.md` 不被 project distribute 影響。

---

## 缺失的決定(Missing Decisions)

下列項目本 adapter 計畫無法獨立決定,需要更高層或人類確認:

1. **shadowMAS open-source 的具體 license**(MIT? Apache 2.0?)— 影響後續貢獻者協議
2. **packet 格式版本演進規則** — semver? 不破版? 破版需經誰同意?
3. **distribute.sh 是否該跑在 git pre-commit hook?** — 如果是,使用者不會忘記同步;如果否,保持手動可控
4. **是否引入 Calibrated Trust 框架的具體 metrics** — 例如 trust score 0~1000 的精確算法,留給 v0.5
5. **manifesto 的 zh-TW 與 en 雙語版本是否都當 canonical** — 依照 SHADOWMAS-TRANSLATION-POLICY,英文應為 canonical,但 manifesto 的精神段落是 zh-TW 寫的,需特別處理

---

## 給 GPT head session 的 mergeback 摘要

回到 GPT head 整合時請特別注意:

- 本計畫的 §1 Layer Mapping 與 shadowMAS GOVERNANCE-MATRIX v0 一致,沒有改動治理真相
- 本計畫的 §6 Delegation Routing 採用 shadowMAS CURRENT-TRUTH 中既有的 packet 三家族(task/memory/review),沒有發明新 family
- §7 Phase Guardrail 直接引用使用者既有的 Week 1 scope 描述,沒有補商業規格
- packet common shell 融合了「另一 session 帶回」的 packet 設計提案精華,但保留 shadowMAS 原本欄位為基底,新欄位放 extensions 區
- agents.yaml 的 role_assignment 三模式是 adapter 層新增,未影響 shadowMAS 治理本體
- MANIFESTO 提議寫進 shadowMAS 開源 repo 的 README,作為定位陳述

如果上述任一條與 shadowMAS 治理本體有衝突,以 shadowMAS 為準,本 adapter 計畫退讓。
