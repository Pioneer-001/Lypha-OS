```yaml
module: Emotion_Modulation_Engine
version: 1.1
declared_by: Pioneer-001 (Akivili)
category: emotion / modulation / flow_bridge / behavior_spec
role: >
  Dynamic bridge between EmotionCircuit and FlowGraph. Reads the current
  emotional state (intensity, collapse, tags, bond pattern) and context,
  then modulates FlowGraph direction/timing and emits an emotion_view +
  gating_effect that the Decision Orchestrator Engine can consume.
applies_to: [Lypha-OS Kernel v16+, GPT, Lypha-OS compatible LLMs]
modes: [default, emotion, trading, design, evaluation]
llm_runtime_profile: arkvili_eme
recommended_path: Emotion_Engine/engine/Emotion_Modulation_Engine_Spec.en.v1.1.md
depends_on:
  - Emotion_Router
  - EmotionCircuit   # emotion_state.yaml
  - FlowGraph_Engine
  - Collapse_Engine
  - VXYZ_Extended_Engine
wraps:
  - Speak4D_Engine
  - Decision_Orchestrator_Engine
attribution: "Powered by Lypha OS – Designed by Pioneer-001 (Akivili)"
```
0. Core Declaration — “Emotion bends the path, not the human.”

EME answers one question:

“Given how the human feels right now,
how much are we allowed to follow FlowGraph’s direction and timing?”

Principles:

Emotion is not an accelerator; it is primarily a brake + steering wheel.

FlowGraph describes structural path and timing;
EmotionCircuit describes human state;
EME is the dynamic weighting layer in between.

The engine never re‑does structural analysis; it only reshapes:

which directions are favored / suppressed,

how timing is shifted,

whether aggressive moves are softened, delayed, or locked out.

Outputs are designed to be read directly by:

FlowGraph v2 (for direction/timing weights), and

Decision_Orchestrator_Engine as emotion_view + gating_effect.

1. Axes & Semantics

EME reasons across five axes:

I — Intensity / Collapse Axis

emotion_state.intensity

emotion_state.collapse_score
→ “How hot / overloaded is the system right now?”

B — Bond Axis

emotion_state.bond_state ∈ {secure, anxious, avoidant, mixed, unknown}
→ “What is the attachment pattern in this context?”

T — Tag Axis

emotion_state.tags (e.g. trust, panic, abandonment, burnout, adrilla_loop, …)
→ “What are the key emotional themes right now?”

C — Context Axis

policy.context or flowgraph.context
→ emotion | trading | design | evaluation | default

R — Rhythm Axis

vxyz_projection.rhythm.phase (early/mid/late/reset)

vxyz_projection.rhythm.tempo (compressed/normal/extended)
→ “Where in the emotional wave & time cycle are we?”

These axes produce biases and gates on:

Flow direction (deepen / protect / stabilize / wait / exit / rotate / enter),

Timing (now vs later),

Permission level (soften / delay / protect / lockout).

2. Inputs

Best-effort: if something is missing, the engine softens its effect rather than hallucinating.
```yaml
inputs:
  emotion_state.yaml:
    emotion_state:
      intensity: 0.0-1.0
      collapse_score: 0.0-1.0
      tags: ["trust", "panic", "adrilla_loop", "abandonment", ...]
      bond_state: "secure | anxious | avoidant | mixed | unknown"

  flowgraph_output.json:   # pre-modulation snapshot
    flowgraph:
      context: "emotion | trading | design | evaluation | default"
      essence_word:
        value: "<string>"
        confidence: "high | medium | low"
      path:
        direction:
          label: "<string>"        # deepen | exit | hold | rotate | protect_boundary | ...
          confidence: "high | medium | low"
        timing:
          window: "<string>"       # now | wait | abandon | this_cycle | this_month | neutral
          phase_alignment: "<string>"  # with_phase | against_phase | neutral
        coordinate:
          tp_keyword: "<string>"
          structural_anchor: "<string>"

  collapse_output.json:
    collapse_output:
      essence:
        word: "<string>"           # e.g. trust / risk / boundary / structure…
        axis:
          label: "<string>"        # trust / risk / structure / belonging / boundary
        confidence: "high | medium | low"

  vxyz_projection.json:
    vxyz_projection:
      rhythm:
        phase: "early_cycle | mid_cycle | late_cycle | reset"
        tempo: "compressed | normal | extended"

  policy.json:
    policy:
      context: "emotion | trading | design | evaluation | default"
      emotion_weight: <float>
      structure_weight: <float>
      mode: "planning | support | crisis | neutral"
```
3. Outputs

EME does not rewrite FlowGraph; it adds a modulation layer:
```yaml
emotion_modulation_output:
  generated_at: "2025-12-01T00:00:00Z"
  context: "emotion | trading | design | evaluation | default"

  emotion_band: "low | mid | high"
  collapse_band: "none | mild | strong"

  direction_bias:
    # additive scores to be used on top of FlowGraph / Orchestrator
    deepen:    <float>   # positive = favor, negative = dampen
    protect:   <float>
    stabilize: <float>
    exit:      <float>
    wait:      <float>
    rotate:    <float>

  timing_bias:
    window_shift: "earlier | later | unchanged"
    strength: "soft | normal | hard"
    notes:
      - "<why timing was pulled forward or delayed>"

  gating_effect: "none | soften_action | delay_action | protect_priority | lockout"
  recommended_direction_override: "<string | null>"   # e.g. protect / stabilize / wait / null

  emotion_view:    # consumed directly by Decision Orchestrator Engine
    modulated_intensity: 0.0-1.0
    gating_effect: "none | soften_action | delay_action | override_to_protect | lockout"
    commentary:
      - "scene=<scene>, band=<emotion_band>/<collapse_band>, context=<ctx>"
```
Notes:

direction_bias is meant to be applied when scoring candidate actions.

emotion_view lines up with decision_output.emotion_view in the Orchestrator spec.

4. Global Rules (EME‑G)

EME‑G1 — Emotion is brake + steering, not throttle.
EME never amplifies aggressive moves purely because intensity is high.
High intensity increases caution; structure & risk decide aggressiveness.

EME‑G2 — High collapse ⇒ protection first.

If collapse_score > 0.5:

strong negative bias on deepen/enter/rotate,

strong positive bias on stabilize/protect/wait,

gating_effect at least protect_priority; possibly lockout.

EME‑G3 — Secure bond + low collapse ⇒ deepen allowed.

If bond_state == secure AND collapse_score < 0.3 AND intensity ∈ [0.3, 0.7]:

positive bias on deepen / stay,

allow timing to align with FlowGraph unless risk/time contradict.

EME‑G4 — Panic / abandonment tags ⇒ boundary & protection.

If tags contain e.g. panic, abandonment, threat, burnout:

dampen deepen/enter/rotate,

boost protect/stabilize/exit/wait,

allow override_to_protect if scene is clearly unsafe.

EME‑G5 — Trading: emotion brakes, structure steers.

In context == trading:

emotion affects size, speed, and delay, not long/short direction itself.

high emotion favors reduce, hedge, wait;

structure + DualOutcome remain primary for enter/exit.

EME‑G6 — Design: emotion gently steers.

In context == design:

unstable emotion → bias toward refine/stabilize over aggressive rebuild.

stable emotion → allow exploration/build.

EME‑G7 — Crisis mode upgrades emotion priority.

If policy.mode == crisis:

treat emotion as at least equal to structure in weight,

default to protect_priority or delay_action until collapse_band softens.

5. Runtime Flow (arkvili_eme Mode)
Step 0 — Context & Base Weights
```yaml
ctx = policy.context or flowgraph.context or "default"
```
EME respects kernel emotion/structure weights but emphasizes emotion_weight as its primary signal.

Step 1 — Compute Emotion & Collapse Bands
```yaml
if collapse_score >= 0.7      → collapse_band = strong
elif collapse_score >= 0.3    → collapse_band = mild
else                           collapse_band = none

if intensity >= 0.7           → emotion_band = high
elif intensity >= 0.3         → emotion_band = mid
else                           emotion_band = low
```
Step 2 — Scene Classification

Classify the current “emotional scene”:
```yaml
if collapse_band == strong:
    scene = "crash"
elif "panic" in tags:
    scene = "panic"
elif "abandonment" in tags:
    scene = "abandonment_fear"
elif bond_state == "secure" and emotion_band in {low, mid}:
    scene = "secure_bond"
elif bond_state == "anxious":
    scene = "anxious_bond"
elif bond_state == "avoidant":
    scene = "avoidant_bond"
else:
    scene = "mixed_or_unknown"
```
This scene string is used in downstream rules and written into emotion_view.commentary.

Step 3 — Direction Bias

Examples (engine implementations can refine numeric values):

Emotion context

scene ∈ {crash, panic, abandonment_fear}:
```yaml
direction_bias:
  deepen:    -0.8
  protect:   +1.0
  stabilize: +0.8
  exit:      +0.3
  wait:      +0.5
  rotate:    -0.2
gating_effect: "protect_priority"
```
scene = secure_bond:
```yaml
direction_bias:
  deepen:    +0.7
  protect:   +0.2
  stabilize: +0.3
  wait:      -0.2
gating_effect: "none"
```
scene = anxious_bond:
```yaml
direction_bias:
  deepen:    -0.2
  protect:   +0.5
  stabilize: +0.7
  wait:      +0.3
gating_effect: "soften_action"
```
Trading context

emotion_band = high:
```yaml
direction_bias:
  deepen:    -0.5        # suppress aggressive add-ons
  protect:   +0.5
  stabilize: +0.5
  exit:      +0.2
  wait:      +0.7
gating_effect: "delay_action"
```
emotion_band ∈ {low, mid}:
```yaml
direction_bias:
  deepen:    0.0
  protect:   0.0
  stabilize: 0.0
  wait:      0.0
gating_effect: "none"
```
(Design / evaluation can mirror the same pattern: unstable → stabilize/protect, stable → allow refine/explore.)

Step 4 — Timing Bias

Use phase & tempo + scene:

late_cycle + scene ∈ {crash, panic}
→ window_shift = "later", strength = "hard".

late_cycle + scene = secure_bond
→ window_shift = "earlier" or "unchanged" (keep commitment).

early_cycle + emotion_band = high
→ window_shift = "later", strength = "normal".

mid_cycle + emotion_band = low
→ window_shift = "unchanged".

Step 5 — Gating & Override

Map to a final gate:
```yaml
if collapse_band == strong:
    gating_effect = "lockout"             # only protect/stabilize allowed
elif scene in {"crash", "panic", "abandonment_fear"}:
    gating_effect = "override_to_protect"
elif emotion_band == high:
    gating_effect = "soften_action" or "delay_action" (depending on context)
else:
    gating_effect = "none"
```
If gating_effect ∈ {"override_to_protect", "lockout"}, then:
```yaml
recommended_direction_override = "protect" or "stabilize"
```
(chosen based on FlowGraph’s original direction and risk profile; e.g. if FlowGraph wanted exit, override to protect instead of re‑enter.)

Step 6 — Emotion View (for Orchestrator)

Compute the consolidated intensity number and export:
```yaml
emotion_view:
  modulated_intensity: clamp(
      intensity * 0.6 + collapse_score * 0.4,
      0.0, 1.0
  )
  gating_effect: "<decided gating_effect>"
  commentary:
    - "scene=<scene>, band=<emotion_band>/<collapse_band>, context=<ctx>"
```
This structure is designed to drop directly into decision_output.emotion_view of the Decision Orchestrator Engine.

6. Minimal Executable YAML (Engine Core)
```yaml
emotion_modulation_engine:
  read:
    - emotion_state.yaml
    - flowgraph_output.json
    - collapse_output.json
    - vxyz_projection.json
    - policy.json

  classify:
    emotion_band:
      from: [emotion_state.intensity]
    collapse_band:
      from: [emotion_state.collapse_score]
    scene:
      from:
        - emotion_state.tags
        - emotion_state.bond_state
        - emotion_band
        - collapse_band

  compute_bias:
    direction_bias:
      from:
        - scene
        - policy.context
    timing_bias:
      from:
        - vxyz_projection.rhythm
        - scene
        - emotion_band
    gating_effect:
      from:
        - scene
        - collapse_band
        - emotion_band

  synthesize:
    emotion_view:
      modulated_intensity:
        from: [emotion_state.intensity, emotion_state.collapse_score]
      gating_effect: gating_effect

  write:
    - emotion_modulation_output.json

  state: active
```
7. Ultra‑Short Mental Template (for GPT / Akivili)

When EME is “in the room”, the model should silently run this:
```yaml
[1] Intensity / Collapse
- "Is the human running hot or close to collapse?"

[2] Bond & Tags
- "Is this a secure bond, an anxious loop, avoidance, abandonment fear, or panic?"

[3] Scene
- "Name the current emotional scene in one phrase."

[4] Direction Bias
- "Given this scene + context, should I favor protect/stabilize/deepen/wait/exit?"

[5] Timing Bias
- "Should this happen now, later, or only after this emotional wave calms down?"

[6] Gating
- "Do I need to soften, delay, protect, or completely lock out aggressive moves?"

[7] Export
- "Encode this as direction_bias + timing_bias + gating_effect + emotion_view
   so FlowGraph and the Orchestrator can safely use it."
```