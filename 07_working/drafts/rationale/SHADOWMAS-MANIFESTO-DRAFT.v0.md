> status: draft / source-evidence
> authority: none
> do not promote without governance review

# shadowMAS — MANIFESTO

> shadowMAS is a governance protocol, not a framework.
> It defines the legal form of communication between agents,
> without prescribing how agents are implemented.
> Like a shadow, it conforms to every system's shape,
> but the boundary is always there.

---

## The Shadow Doctrine(影子教義)

Shadow 本身也是系統,系統本身就不是完美的。Shadow 隨著真實的需求與數據不斷改變跟迭代,但是因為精簡的駭客精神以及心理學認知專家的考量,讓 Shadow 的彈性達到盡量大。

Shadow 本身是朝著統一協定去沒錯,但是她跟 Unix 一樣,她可以被改造、可以被外接。他是最小核心可動,但不是最終版本。他是一即全的最小根基。

Shadow 不屬於任何人,Shadow 屬於所有人,他可以是任何形體,但他跟大道一樣,永遠代表本質本身。

---

## Positioning(定位)

**We are not another A2A.**
**We are Unix for multi-agent workstations.**

| Layer | Dominant Standard (2026) | Who it serves |
|---|---|---|
| Agent transport (enterprise) | **Google A2A** (v1.2, 150+ orgs, Linux Foundation) | cross-org agent-to-agent over HTTPS / JSON-RPC |
| Agent governance (enterprise) | **Microsoft AGT** (DID + IATP + SRE + compliance) | corporate agent fleets, OWASP Top 10, EU AI Act |
| Agent-to-tool | **MCP** (Anthropic) | single agent calling tools |
| Skill / config format | **SKILL.md + AGENTS.md** (Linux Foundation) | cross-tool reusable instructions |
| **Personal-scale MAS governance** | **shadowMAS** | **one developer, multiple coding agents, own laptop** |

shadowMAS 填的是上述四層沒服務到的縫隙。A2A 假設你有 HTTP endpoint 與 OAuth;AGT 假設你有 DID 與 compliance team;MCP 是 single-agent 範疇;SKILL.md 只定義單一 skill 不定義協作。

shadowMAS 假設:**你是一個人,電腦裡有 Claude Code + Cursor + Codex + Ollama,想讓他們協作不踩彼此、不綁任何廠商、不需要上雲。**

### 與 A2A 的關係

Not a competitor. shadowMAS packet 的 common shell 設計允許未來嵌套進 A2A Message 的 Parts 欄位。個人規模先用 shadowMAS,長大要上企業級時可以包成 A2A message payload,零改寫。

```
A2A Message
  └── Part (type: data)
      └── shadowMAS packet (common shell + payload)
```

---

## Calibrated Trust(校準信任)—— 治理哲學支柱

借用 2026 年 agent production 領域的 Calibrated Trust 框架:

- **Under-trust** → agent 閒置、產能浪費、開發者倦怠
- **Over-trust** → 催化災難、approval gates 在第 4 天變成 rubber-stamping
- **Calibrated trust** → 人類理解界線、agent 在驗證過的範圍內運作

shadowMAS hook 不是「替代人類判斷」,是「在 rubber-stamping 出現時仍保留 deterministic 攔截」。固定閘門 + 隨機抽驗 + 強制攔截三層組合,對應三種信任失效模式。

研究提醒:
- approval rate 在人類看了 3 天後會升到 99.7%,並不代表品質提升,是注意力疲乏
- 一個產品最重要的是它的長期有效性,不是當下的熱鬧

shadowMAS 的 hook 設計,是為了讓信任校準在 session 100、專案 100 後依然有效。

---

## Core Principles(五句一即全)

1. **最小核心可動,最大彈性可變。** 格式固定、內容可擴展。
2. **不綁任何廠商。** Agent 可替換、模式可切換、分發點都是通用標準。
3. **Packet 是最小單位,也是全部。** 格式對了,shadowMAS 的核心就在。其他都是擴展。
4. **治理不跨級。** T-layer 邊界不能被任何 agent 或 hook 繞過。
5. **人類是最後一公里。** 不是第一公里、不是每公里、是關鍵公里。

---

## What Shadow Is NOT

- 不是產品應用本身
- 不是另一個 agent 框架
- 不是 A2A 或 AGT 的替代品
- 不是企業合規工具
- 不是封閉協議
- 不是一次性完整解
- 不是某人的專屬系統

## What Shadow IS

- 一份 packet 格式規範
- 一組檔案位置約定
- 一套 hook 攔截哲學
- 一個可被任何人改寫的最小根基
- 一個邊界清楚、形體可變的治理影子

---

## License and Ownership

MIT or equivalent permissive. Owned by no one, usable by anyone, forkable by everyone.

The shadow belongs to all who cast it.
