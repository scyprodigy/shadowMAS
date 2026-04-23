# SHADOWMAS-SINGLE-SOURCE.v0.zh-TW.md

## 0. 這份文件是幹嘛的

這份文件是 shadowMAS 給人類先讀的單一入口。

它不是正式英文 truth 的替代品，  
而是讓你先快速看懂：

- shadowMAS 是什麼
- 它在解什麼痛點
- 為什麼要這樣設計
- 目前已定到哪裡
- 哪些還沒定
- 接下來應該讀哪裡

原則上：
- agent 先讀英文 formal docs
- 人類先讀這份中文單一入口
- 要做實作或治理判斷時，再回英文 canonical truth

---

## 1. 一句話講 shadowMAS

**shadowMAS 是一個與產品專案硬分離的治理／記憶／協作系統。**

它不是產品本體，  
也不是 giant prompt，  
而是用來管理：

- 多 agent / 多 session 協作
- truth / draft / cache 的邊界
- memory / promotion / invalidation
- review / mergeback / write-back 邊界
- machine-first packet / registry contract

---

## 2. shadowMAS 在解什麼痛點

shadowMAS 主要在解五種會隨著 AI 協作變大而失控的問題：

### A. authority confusion
誰能決定、誰只能執行、誰能 promotion、誰只能暫存，常常會混掉。

### B. truth confusion
執行輸出、暫存結果、快取、session 記憶，很容易被誤當成正式真相。

### C. giant prompt collapse
shared rule、governance、project truth、runtime adapter、host-native constraints 被壓成一團，後面幾乎不可維護。

### D. intake chaos
新 session / 0 記憶 agent 一上來就遍歷整個 repo，最後讀不完、讀不準、也不知道哪些才重要。

### E. mergeback contamination
治理系統和產品 repo 混在一起，最後不清楚哪個是 product truth、哪個是 governance truth。

---

## 3. 它不是什麼

shadowMAS 不是：
- 產品本體
- 一個超大萬能 system prompt
- 盲目全 repo 遍歷機器人
- 直接覆寫專案業務真相的中央暴君
- 一定要先有 UI 的平台
- 一定要先有 DB 的系統
- 另一個泛用 agent framework 的包裝版本

---

## 4. 為什麼一定要和產品專案硬分離

### 定案
**shadowMAS 必須和產品專案硬分離。**

### 原因
因為產品專案就算沒有 shadowMAS，也必須還能：
- 開發
- 測試
- 部署
- 維運

如果兩者混在一起，後面很容易出現：
- 規則污染
- 資料夾混亂
- governance truth 與 project truth 混淆
- agent 誤把治理檔案當業務檔案

### 正確做法
**系統抽離，產物回寫。**

也就是：
- shadowMAS 活在自己的 root / repo
- 再把需要的 entry / index / truth-priority / change-impact / handoff / review 產物回寫到專案 repo

---

## 5. 為什麼要 machine-first

shadowMAS 不只需要人類可讀，  
也需要 machine-stable。

### human-facing 的用途
- onboarding
- 導航
- 設計理由
- review 理解
- 歷史脈絡

### machine-first 的用途
- packet
- registry
- routing
- validation
- automation surface

### 這代表什麼
凡是 machine-first 的東西，都要往下面收斂：
- 最小格式
- 可解析
- 低歧義
- 明確欄位
- 穩定 contract

所以 shadowMAS 不會只靠聊天長期運作，  
而是要靠 packet / registry / validator / CI 規則把邊界釘住。

---

## 6. 目前的核心分層

### Shared Core
跨專案可重用的行為鐵律。

### Project Execution
單一專案自己的 repo truth、資料模型、API、命名、實作落點。

### shadowMAS Governance
shadowMAS 自己的治理規則，例如：
- packet
- memory plane
- promotion / invalidation
- review
- mergeback
- write-back boundary

### 為什麼不 flatten 成 giant prompt
因為 giant prompt 會把：
- 真相
- 任務
- 規則
- 治理
- 技能
- runtime 限制

全部混成一團，最後不可維護。

---

## 7. T / L / R 三層骨架

### T-layer
真相 / 記憶 / 狀態治理層
- T0 Human Authority
- T1 Delegated Decision Authority
- T2 Approved Truth Artifacts
- T3 Approved Shared Memory
- T4 Execution Feed
- T5 Ephemeral / Cache / Session State

### L-layer
角色責任層
- L1 Human + high-level governance
- L2 delegated planning
- L3 execution
- L4 mergeback / sync

### R-layer
執行基底層
- queue
- retry
- timeout
- lock
- backpressure
- concurrency

### 為什麼要拆開
因為：
- 誰做事
- 什麼算真相
- 底下怎麼跑

這三件事不是同一件事，不能混。

---

## 8. 為什麼 intake 不應該靠 blind traversal

shadowMAS v0 不鼓勵 0 記憶 agent 一上來就遍歷整個 repo。

正確方向是：
- 先吃小型 canonical intake pack
- 再按需要擴讀
- 如果未來真的做 intake artifact，也應該由 canonical 文件**編譯產生**
- 不要再多養一份手寫真相

這是為了降低：
- intake 漂移
- truth 選錯
- 新 session 接手成本
- 大 repo 下的混亂讀取

---

## 9. 為什麼 packet 很重要

shadowMAS 不可能長期只靠自然語言聊天。

目前最小 packet 方向是：
- `task_packet`
- `memory_packet`
- `review_packet`

目前預設 codec：
- YAML

packet 的價值在於：
- 任務邊界清楚
- memory promotion / invalidation 可明寫
- review 面可被縮成最小必要 surface
- handoff 可從聊天語氣中抽離

---

## 10. 記憶為什麼先走最小版

目前方向不是先塞滿記憶框架，  
而是先把記憶治理 contract 定清楚。

### 目前最小 memory-plane
- `session_log`
- `working_memory`
- `shared_memory`

### 重點不是先做最大
而是先定：
- 什麼是 session 記憶
- 什麼是工作記憶
- 什麼有資格升成 shared memory
- promotion / invalidation 怎麼治理
- retrieval 為什麼不能直接當 truth

所以這條路不是否定記憶的重要性，  
而是先定治理，再決定 storage 與框架。

---

## 11. 這個專案現在最值得記住的事

### 已定
- shadowMAS 與 product repo 硬分離
- English formal docs 是 canonical truth
- zh-TW 文件是人類導航與設計理由主入口
- giant prompt 路線不可取
- blind full-repo traversal 不可當作 default intake
- machine-first packet / registry 是必要方向
- human final authority 不可消失

### 還沒最終定死
- R-layer 最終 runtime substrate
- 最終 promotion gate 細則
- file-status registry 的最終 schema
- write-back automation contract
- memory-plane 更細緻的 store strategy
- contract versioning 與 CI validator 的正式落檔方式

---

## 12. 第一次接觸 shadowMAS，建議怎麼讀

先讀：
1. `01_truth/SHADOWMAS-CURRENT-TRUTH.v0.en.md`
2. `01_truth/SHADOWMAS-PROMPT-LAYERING-CONTRACT.v0.en.md`
3. `01_truth/SHADOWMAS-GOVERNANCE-MATRIX.v0.en.md`

再用這份中文單一入口補：
- 為什麼這樣設計
- 這些規則在解什麼痛點
- 哪些是正式 truth、哪些只是理解輔助

---

## 13. 一句話總結

shadowMAS 不是在做「更多 agent 工具」。  
它在做的是：

**當 agent 開始跨 session、跨工具、跨 repo、跨角色工作時，怎麼讓 truth、authority、memory、promotion、mergeback 不失控。**
