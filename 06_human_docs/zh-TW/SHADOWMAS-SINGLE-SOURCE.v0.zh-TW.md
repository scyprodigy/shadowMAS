# SHADOWMAS-SINGLE-SOURCE.v0.zh-TW.md

## 0. 這份文件是幹嘛的

這份文件是 shadowMAS 給人類先讀的單一入口。

它不是要取代所有正式文件，而是要讓後續的人先搞懂：

- shadowMAS 是什麼
- 為什麼要這樣設計
- 現在已經定到哪裡
- 哪些還沒定
- 正式英文文件放哪裡
- 應該從哪裡切入
- 不要誤把什麼當成真相

你可以把它當成：
- 導航腦
- 中文總覽
- 設計理由總整理
- onboarding 入口
- 後續人類理解用的主文件

原則上：
- agent 先讀英文 formal docs
- 人類先讀這份中文單一入口
- 想深入再去追其他文件

---

## 1. shadowMAS 是什麼

shadowMAS 不是單純 prompt 技巧，也不是 giant prompt，更不是會到處亂讀 repo 的聊天機器人。

它是：

**一個治理導向、記憶感知、可 mergeback 的人機協作系統。**

它的目標是幫你做這些事：
- 收斂多個 session / 多個 agent 的結果
- 管理哪些東西算正式真相、哪些只是草稿、哪些只是快取
- 建立最小 packet / handoff / review 規格
- 幫多個專案提供共通治理層
- 讓人類最後仍保有決策權
- 讓 agent 不要亂擴張、亂覆寫、亂遍歷

---

## 2. 它不是什麼

shadowMAS 不是：
- 產品本體
- 一定要先有 UI 的平台
- 一定要先有 DB 的系統
- 一個超大萬能 system prompt
- 一個直接覆寫專案業務真相的中央暴君
- 一堆框架拼湊出來的炫技平台

---

## 3. 為什麼要和產品專案硬分離

### 定案
**shadowMAS 必須和產品專案硬分離。**

### 理由
因為產品專案就算沒有 shadowMAS，也必須還能：
- 開發
- 測試
- 部署
- 上雲
- 維運

如果 shadowMAS 跟產品專案混在一起，後面很容易變成：
- 規則污染
- 資料夾混亂
- 不知道哪個是產品真相，哪個是治理真相
- agent 把治理檔案誤當業務檔案

### 正確做法
**系統抽離，產物回寫。**

也就是：
- shadowMAS 自己活在自己的 root / repo
- 再把需要的 entry/index/truth-priority/change-impact 等產物回寫到專案 repo

---

## 4. 為什麼文件系統會比 DB 還亂

資料庫天生有：
- schema
- relation
- constraint
- query
- index
- migration

但文件系統如果只有：
- 資料夾
- 檔名
- 一堆 Markdown

那它就缺：
- 強制 schema
- 強制關聯
- 強制 read order
- 強制 impact map
- 強制 promotion gate

所以文件一多，就容易變成：
**一堆孤島真相碎片。**

### shadowMAS 的解法
不是叫 agent 全遍歷。

而是做成：
- entry layer
- truth layer
- change layer
- machine-readable registry

也就是：
**docs-as-code + machine-readable registry**

---

## 5. 現在定下來的權重模型

### 權重模型
- 治理層最高：MAS
- 業務層最高：Project Canonical Truth
- Shared Core 在中間共享，但不直接覆寫 project domain facts

### 這代表什麼
MAS 很高，但**不是來直接改掉專案的業務真相**。

例如：
- 欄位定義
- API 契約
- 業務角色
- ERD
- Prisma schema

這些仍由專案自己的 canonical truth 說了算。

### 為什麼這樣設計
因為如果中央治理系統可以直接壓掉每個專案的業務真相，會很危險。

正確做法是：
- MAS 管治理、記憶、promotion、review、routing
- 專案管自己的業務正式真相

---

## 6. 三層 prompt / rule 分工

目前方向：

### A. Shared Core
所有專案都共用的鐵律，例如：
- 先收斂後實作
- 未定不可假裝已定
- 不要盲目遍歷 repo
- 最小必要變更
- 顯式列出衝突與缺口

### B. Project Execution
某個專案自己的執行規則，例如：
- repo 結構
- truth priority
- 資料模型
- API 契約
- 實作落點
- 命名與權限細節

### C. shadowMAS Governance
MAS 自己的治理規則，例如：
- packet
- handoff
- memory plane
- promotion / invalidation
- routing
- write-back boundary

### 為什麼不 flatten 成一個 prompt
因為 giant prompt 會把：
- 真相
- 規則
- 任務
- 技能
- 審查
- 治理

全部混成一團，後面幾乎不可維護。

---

## 7. T / O / R 三層骨架

### T-layer：真相 / 記憶 / 狀態治理層
- T0 Human Authority
- T1 Delegated Decision Authority
- T2 Approved Truth Artifacts
- T3 Approved Shared Memory
- T4 Execution Feed
- T5 Ephemeral / Cache / Session State

### O-layer / L-layer：角色責任層
- L1 / O-L1 Human + high-level governance
- L2 / O-L2 delegated planning
- L3 / O-L3 execution
- L4 / O-L4 mergeback / sync

### R-layer：執行基底層
目前已承認需要，但還沒最後定死。
它會承接：
- queue
- retry
- timeout
- lock
- backpressure
- concurrency

### 為什麼要拆三層
因為：
- 誰做事（O/L）
- 什麼算真相（T）
- 底下怎麼跑（R）

這三件事不能混。

---

## 8. 為什麼 packet 很重要

shadowMAS 不可能只靠自然語言聊天長期運作。

所以現在已收斂出最小 packet 方向：
- `task_packet`
- `memory_packet`
- `review_packet`

### 格式
先用 YAML。

### 為什麼用 YAML
- 人類可讀
- agent 好吸收
- diff 友善
- 比 JSON 更適合治理型文本交換

### packet 的用途
- 明確任務邊界
- 明確 review 面
- 明確 memory 失效與 promotion
- 讓 session handoff 與 runtime contract 分開

---

## 9. 為什麼 supervision / risk / budget / prompt policy 要拆開

因為如果混在一起，後面自動化一定出事。

### supervision
人在不在旁邊

### risk
做壞了傷害多大

### execution budget
這次允許花多少 token / hop / retry

### prompt policy
這次規則怎麼載入，few-shot 要不要開

這四件事彼此相關，但不是同一件事。

---

## 10. 記憶架構為什麼先走最小版

目前方向不是直接引 Letta / MemGPT / LangGraph。

### 原則
**先自建最小 memory-plane harness。**

### 最小三層
- `session_log`
- `working_memory`
- `shared_memory`

### 為什麼不直接上大框架
因為現在需要的是：
- 清楚
- 可控
- 可 debug
- 少依賴
- 高約束
- 最小落地

不是先把記憶框架裝滿。

---

## 11. 為什麼依賴要少

### 可直接用
- `tree-sitter`
- `pydantic` / `jsonschema`
- `typer` / `click`
- `PyYAML`
- `Chroma`（v0）

### 先不要引
- DSPy runtime
- LangGraph
- Letta / MemGPT
- CrewAI / AutoGen
- heavy orchestration framework

### 理由
因為 v0 要的是：
- text-first
- local-first
- inspectable
- schema-first
- minimal dependencies

不是套件炫技。

---

## 12. 為什麼 DSPy 不直接引，但要學它的思想

DSPy 最值錢的地方不是框架本體，  
而是 **Signature** 的思想：

> 每個 agent / task 的輸入輸出都應顯式定義，不要靠模糊自然語言默契。

這一點其實已經滲進現在的設計了，因為：
- packet family
- shared field
- handoff schema
- common shell

都在往這個方向靠。

所以現在的決策是：
**自己做 signature schema，不拉 DSPy 框架。**

---

## 13. 為什麼向量庫先 Chroma，之後才 Qdrant

### v0：Chroma
因為它最符合：
- 本地
- 輕
- 快起
- 容易持久化

### v1 之後：Qdrant
等需要：
- 更強 filter
- 更清楚的 collections
- 更大的 scale
- 更複雜的 retrieval

再升。

---

## 14. 為什麼本地模型主力改成 Linux / WSL 側

前面曾經討論過 Windows 版 Ollama 方便，但最後設計往 Linux / WSL 主力收斂。

### 原因
因為你的真資料都在 Linux 側：
- repo
- DB
- Docker
- 未來上雲路徑

如果 Ollama 在 Windows 側，會多出：
- 跨側讀檔
- 路徑轉換
- DB 取用複雜度
- 腳本耦合度上升

### 所以現在的結論
shadowMAS v0 的本地模型主力部署方向：
**Linux / WSL side primary**

### 模型基線
- `qwen3:8b`
- `mxbai-embed-large`

---

## 15. Prompt / Context Compression 為什麼不能忽略

它不是 foundation，但對某些場景不是 optional，而是預設應該開。

### 預設啟用場景
- 長篇背景
- 多 session merge 前
- 大段歷史摘要
- RAG context 太長
- 小模型上送前的精簡

### 禁用場景
- packet YAML
- JSON schema
- API 契約
- migration
- 欄位字典欄位級內容
- code patch / diff

### 做法
學 LLMLingua 思想，不直接引 LLMLingua。
採：
- 句子級
- 段落級
- rule-based + small-model scoring

這些理由都應寫進中文大文件，讓後續人類理解初衷。

---

## 16. 參照與技術影子要記錄

後續不只要記「現在怎麼做」，還要記：
- 為什麼這樣做
- 參照了什麼
- 哪些東西只吸收思想，沒有直接引入
- 哪些方案被否決
- 哪些是以後再升級

也就是說：
**shadowMAS 不只要正式檔，還要有設計理由與影子軌跡。**

這些比較適合收進：
- `06_human_docs/zh-TW/decisions/`
- `06_human_docs/zh-TW/rationale/`
- 後續中文 ADR 或技術對照文件

---

## 17. 這份文件怎麼用

### 第一次接觸 shadowMAS 的人
先讀這份。

### 想要進一步深入
再去讀：
- 英文 formal truth
- prompt layering contract
- governance matrix
- packet field dictionary
- memory plane harness

### 想看更完整技術取捨
未來再讀：
- 中文 decisions
- 中文導覽
- 中文 rationale
- 中文 references
- 核心圖

---

## 18. 目前下一步

目前最值錢的正式文件順序是：

1. `01_truth/SHADOWMAS-CURRENT-TRUTH.v0.en.md`
2. `01_truth/SHADOWMAS-PROMPT-LAYERING-CONTRACT.v0.en.md`
3. `01_truth/SHADOWMAS-GOVERNANCE-MATRIX.v0.en.md`

人類導航層則以這份為單一入口，再逐步補：
- 中文 decisions
- 中文導覽
- 中文技術取捨
- 核心圖

---

## 19. 一句話總結

shadowMAS 是一個與產品專案硬分離的治理／記憶／協作系統；它用最小 packet、分層權重、repo-first truth、選擇性雙語與可追溯的中文導航腦，來避免多 agent、多 session、多文件系統最後失控。
<!-- SHADOWMAS_PRINCIPLES_PATCH:BEGIN -->
## 補丁：最高核心原則（v0）

### 1. Capability Routing 原則
不要只按模型名選模型，要按任務形狀與資料形狀做路由。

意思是：
- 不是看到 `qwen3:8b` 就先塞給它
- 不是看到 embedding 就一律一樣處理
- 而是要先看：
  - 這次任務是什麼形狀
  - 輸入資料是什麼形狀
  - 輸出要多結構化
  - 錯了的代價有多高
  - 是否需要人審或高權限決策

這條不是靈感，而是 shadowMAS 的核心設計原則之一。

### 2. Machine-first Normalization 原則
凡是 machine-first 的檔案，都要往下面這個方向收斂：
- 最小格式
- 可解析
- 低歧義
- enum 盡量固定
- 高風險欄位要有明確規範語氣
- 不要讓 agent 靠猜

目前主要屬於 machine-first 的路徑有：
- `01_truth/`
- `02_packets/`
- `03_memory/registry/`
- `04_runtime/` 裡的 formal baseline

相對地，`06_human_docs/zh-TW/` 是 human-first，
所以可以保留設計理由、參照來源、技術取捨與歷史脈絡。

### 3. Compiled Intake 原則
0 記憶 agent / 新 session 不應該一開始就遍歷整包 repo。

v0 先用「小型 canonical 組合包」進場，
也就是先讀少數關鍵檔，再按需要請求更多文件。

如果未來真的要做 intake file，
它應該是由既有 canonical 文件編譯出來的 compact artifact，
而不是再多維護一份手寫的獨立真相檔。

### 4. 目前建議的 intake pack
目前正式的 4 份 zero-memory intake pack，
以 `01_truth/SHADOWMAS-CURRENT-TRUTH.v0.en.md` 裡的定義為唯一維護來源。

這不是永久答案，但足夠當 v0 的穩定入口。

### 5. Prompt Compact / Prompt Cache 的目前位置
目前已經吸收了 prompt compact 的概念：
- 長背景壓縮
- 長歷史摘要壓縮
- RAG context 過長壓縮
- 小模型上送前濃縮

但 prompt cache 目前還沒有正式獨立成一份 v0 規格檔，
只是概念上已承認其存在，後續可再 formalize。

### 6. 為什麼這些原則一定要落檔
因為如果這些東西只留在聊天裡，
後面 session 一多、agent 一多、repo 一大，
就一定會遺漏，然後系統會開始漂。

所以這些不是備註，而是 shadowMAS 的核心約束。
<!-- SHADOWMAS_PRINCIPLES_PATCH:END -->
