# SHADOWMAS-OPERATOR-GUIDE.v0.zh-TW.md

## 用途
這份文件是給人類操作者看的最小接手導覽。

目標不是解釋整個 shadowMAS 世界觀，
而是讓新接手者快速分清：
- 哪些是正式真相
- 哪些只是工具執行狀態
- 哪些是 working-only 草稿
- 先讀什麼
- 不要亂動什麼

## 一句話定位
shadowMAS 是一套人機協作治理系統。

它的重點不是把所有東西塞進一個大 prompt，
而是把 truth、memory、review、runtime、write-back 邊界切乾淨，
讓人和 agent 都能在最小讀取下接手工作。

## 先讀什麼
人類接手時，先從這裡開始：

1. 先讀這份 operator guide
2. 再讀 `01_truth/SHADOWMAS-CURRENT-TRUTH.v0.en.md`
3. 需要看正式 4 份 zero-memory intake pack 時，直接看 `01_truth/SHADOWMAS-CURRENT-TRUTH.v0.en.md` 裡的 intake-pack 段落
4. 需要看 layer/source 對照時，再讀 `00_entry/SHADOWMAS-LAYERING-QUICKREF.v0.en.md`
5. 需要看 runtime 載入規則時，再讀 `04_runtime/SHADOWMAS-RUNTIME-LOADING-MAP.v0.en.md`

## 資料夾閱讀規則
接手時，不需要先把每個主資料夾都讀一遍。

先記住這三類就夠：
- `01_truth/` 放正式 English canonical truth
- `06_human_docs/` 放人類 onboarding 與解釋
- `07_working/` 放 working-only 材料，可輔助工作，但不是 canonical truth

## 什麼是 tool runtime state
有些東西是工具自己的肚子，不是 shadowMAS 的正式真相。

例如：
- 例如 `~/.codex/` 這類工具私有目錄裡的 auth、cache、history、sessions、logs、sqlite state
- 其他工具自己的 cache、登入狀態、暫存檔

這些檔案：
- 可以幫工具運作
- 可以反映執行痕跡
- 不能直接當 source-of-truth

## Git 動作誰能做
憲法級規則：

- remote push 只能 human 觸發
- final merge 只能 human 觸發
- public branch promotion 只能 human 觸發

agent 最多做到：
- local branch
- local commit
- local diff
- review packet

就算自動化做完很多步，
最後仍要等 human 回來 review 與放行。

## machine-first 的實際意思
machine-first 不等於一味省 token。

真正的原則是：
依資料形狀與錯誤成本，
先保品質與可解析，
再談壓縮。

也就是：
- 該結構化的要結構化
- 該明確 enum 的不要偷省
- 高風險欄位不要靠猜
- 不是所有地方都值得硬壓成最短字串

## 什麼叫 working-only
working-only 材料只服務於：
- 當前工作流
- 暫時整理
- 待人審
- 待升格判斷

它們可以被讀，
也可以輔助決策，
但不能直接被當成：
- canonical truth
- approved shared memory

典型例子：
- lessons queue
- incoming handoff
- merged audit draft
- pre-promotion notes

## 最小接手規則
不要一進來就讀完整個 repo。

先讀最小入口，
搞懂：
- 現在碰到哪一層
- 哪裡才是正式真相
- 哪些只是 working / runtime state
- 這輪任務需不需要再去看 `04_runtime/SHADOWMAS-RUNTIME-LOADING-MAP.v0.en.md` 的載入規則

這才是 shadowMAS 要追求的「精簡但強大」。
