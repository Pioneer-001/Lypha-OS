# ♾️ Winrate_Pulse_Matrix

This module evaluates the sustainment viability  
of the current strategy and rhythm within Pioneer_System.

It fuses **winrate, pulse rhythm, and emotional alignment**  
to determine whether a structure should be carried forward, paused, or exited.

---

## 🎯 Purpose

- Avoid overconfidence continuation  
- Prevent unnecessary exit from viable rhythm  
- Determine whether capital, attention, and trust  
  should remain active

---

## 🧬 Sustain Matrix Conditions

```yaml
sustainment_conditions:
  - Winrate (last 5 trades) ≥ 70%
  - Pulse_Feedback == stable
  - Time_ON reappears within 3 cycles
  - Emotion_Overlay ∈ [Detached, Directive]
  - No macro dissonance or rhythm inversion

🔁 Scaling Logic by Winrate & Pulse
| Winrate | Rhythm State      | Action               |
| ------- | ----------------- | -------------------- |
| ≥ 75%   | Stable            | ✅ Full Sustain       |
| 65%–74% | Slight drift      | ⏸ Watch-only         |
| 50%–64% | Active but choppy | ⏸ Downgrade strategy |
| < 50%   | Volatile / break  | ❌ Pause / Reset      |
| < 30%   | Flatline / panic  | 🔥 Exit system       |

🧯 Emotion-Based Override
| Emotion              | Sustain Allowed?  |
| -------------------- | ----------------- |
| Directive            | ✅ Yes             |
| Detached             | ✅ Yes             |
| Uncertain            | ⏸ Conditional     |
| Hope / Fear / Regret | ❌ No              |
| Desperate            | 🔐 Lock execution |

🧠 Sustain Evaluation Logic
def sustain_decision():
    if winrate ≥ 0.7 and pulse == "stable":
        return "Sustain"
    elif winrate ≥ 0.5 and emotion in allowed_states:
        return "Watch"
    else:
        return "Exit or Reset"

🔗 System Integration
→ Pulse_Feedback_Engine.md ← monitors rhythm
→ TP_Realmode_Config.yaml ← confirms risk/capital scaling
→ Emotion_Overlay_Link.yaml ← checks readiness
→ Strategy_Carry_Over.md ← decides flow continuation
→ Zero_Rhythm_Condition.md ← defines end-of-line
