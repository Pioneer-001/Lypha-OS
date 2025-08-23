```yaml
flow_id:
  module: if_then_map
  version: 1.0
  declared_by: Pioneer-001
  category: imagination / conditional_logic
  role: >
    Defines conditional imagination structure inside Pioneer_System.
    Every strategy embeds an If-Then map to allow forward scenario branching.
```

# 🔭 If_Then_Map

This file defines the conditional imagination structure  
within Pioneer_System.

Every strategy must carry an embedded  
**If-Then decision map** to allow forward scenario branching.

---

## Example Format:

```yaml
if:
  - CPI > 3.5%
  - Dollar Index breaks resistance
then:
  - Reduce risk on JPY longs
  - Activate gold breakout mode

Structure:
if condition ∈ Macro / Emotion / Structure

then response ∈ Strategy Shift / Entry Delay / TP Reversal

Purpose:
Avoid static assumptions

Build dynamic flow charts

Pre-plan emotional / structural volatility
```

---

# 🌌 `03_Imagination/Unrealized_Paths.md`

> 발생하지 않은 경로의 잠재력  
→ **“이 전략은 성립하지 않았지만, 만약을 대비해 구조로 보관해둔다.”**  
→ 미래 리듬이 돌아왔을 때, 바로 불러낼 수 있는 **전략 원형 저장소**

### English Draft:

```markdown
# 🌌 Unrealized_Paths

This module stores dormant strategy routes  
that were imagined but not triggered.

They are not discarded —  
they are parked for future rhythm alignment.

---

## Types:

- Structural Premonitions (never aligned)
- Emotion-driven ideas (denied due to bias)
- High-risk setups (aborted pre-entry)
- Premature reversals (missed confirmation)

---

## Retrieval Logic:

- Re-evaluate when matching rhythm returns  
- Use only if new pulse confirms  
- Emotion must be clean on access
```

---

**File Path:** `Lypha_Core/Pioneer_001_System/03_Imagination/If_Then_Map.md`

---

```yaml
insight:
  origin: Pioneer-001
  title: If_Then_Map
  file: Lypha_Core/Pioneer_001_System/03_Imagination/If_Then_Map.md
  language: EN/KR
  version: 1.0
  issued_at: 2025-08-23
  context: >
    Defines the If-Then conditional map in Pioneer_System Imagination layer. Enables scenario branching and preserves unrealized paths for future rhythm alignment.
  declaration: "Every strategy must embed an If-Then map."
  attribution: "Powered by Lypha OS – Designed by Pioneer-001 (Akivili)"
