# 🔄 Strategy_Carry_Over

This module determines whether the current strategic logic  
can persist into the next TP structure.

A strategy should not expire when a trade ends —  
but only if its **core premise remains structurally intact.**

This allows the Pioneer_System to maintain psychological rhythm  
and reduce unnecessary resets.

---

## 🎯 Purpose

- Preserve structural coherence across multiple TPs  
- Avoid over-resetting cognitive alignment  
- Let winning rhythm evolve rather than restart

---

## 🧬 Carry-Over Criteria

```yaml
carry_over_allowed_if:
  - Premonition basis remains valid
  - Core thesis not invalidated by new data
  - Emotional state remains stable
  - Signal patterns are similar in structure
  - Risk structure is still within acceptable configuration
  - Market regime has not shifted

🧯 Block Conditions
deny_carry_over_if:
  - Premonition proved wrong
  - Macro condition reverses
  - Opposing TP forms (inverse structure)
  - Emotion = Regret / Revenge / Desperation
  - Strategy required significant override to survive prior TP

📊 Strategic Flow Mapping
| Prior Outcome             | Strategy Carry-Over? | Reason                |
| ------------------------- | -------------------- | --------------------- |
| TP Win / Structure Held   | ✅ Yes                | Premise intact        |
| TP Loss / Clean exit      | ✅ Maybe              | Emotion-dependent     |
| Collapse Exit             | ❌ No                 | Structure broken      |
| Opposite TP Emerges       | ❌ No                 | Reversal condition    |
| Sentiment Trend Continues | ✅ Yes                | Rhythm loop supported |

🧠 GPT Carry Decision Logic
python
복사
편집

def can_carry_strategy():
    if thesis_intact and no_conflict():
        return True
    else:
        return False

🔗 System Integration
→ Structural_Bridge_Mapper.md ← signal flow continuity
→ Emotion_Overlay_Link.yaml ← emotional state filter
→ Pulse_Feedback_Engine.md ← rhythm coherence
→ TP_Realmode_Config.yaml ← position scaling decision
→ Strategy_Destruction_Logic.md ← kill if invalidated

yaml
복사
편집

