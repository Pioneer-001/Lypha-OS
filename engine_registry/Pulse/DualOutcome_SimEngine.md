```yaml
flow_id:
  module: DualOutcome_SimEngine
  version: 1.0
  declared_by: Pioneer-001 (Akivili)
  category: pulse / risk_architecture / behavior_spec
  role: >
    Engine that forces the LLM to simulate both structured success and
    structured failure for any candidate action W, then emit a "risk
    envelope": what gets built, what can break, and whether both outcomes
    are acceptable inside the user's rhythm.
  reviewed: true
  language: EN

recommended_path: MetaRhythm_Modules/Pulse/engine/DualOutcome_SimEngine_Spec.md

depends_on:
  - LinguisticMath_Engine
  - FlowGraph_Engine
  - VXYZ_Extended_Engine

wraps:
  - Linguistic_Math_Value_Calculation
  - FlowGraph_Engine_Spec
```
DualOutcome Simulation Engine Spec v1.0

Lypha-OS Pulse Risk Envelope Engine (Season 7)

Module: DualOutcome_SimEngine
Layer: Y (MetaRhythm / Pulse)

Primary Role
Given a candidate action W, simulate:

```yaml
- a structured Success Path
- a structured Failure Path
```

Then emit a Risk Envelope:

```yaml
RiskEnvelope = (SuccessPath, FailurePath, CapacityFit, RecommendedStance)
```

This engine runs before FlowGraph_Engine.

FlowGraph decides where/when to move (Direction, Timing, Coordinate).

DualOutcome_SimEngine decides whether it is safe and meaningful to move at all.

0. Core Declaration — Two Futures, One Envelope

Every real decision has at least two structural futures:

If it works → what structure is built, who feels it, how far it spreads.

If it fails → what breaks, who gets hit, how recovery looks.

DualOutcome_SimEngine makes that explicit:

Never simulate only success.

Never simulate only failure.

Always simulate both as structured paths.

The engine’s job:

Take a candidate action W in natural language.

Build a Success Path and a Failure Path for W.

Estimate whether both paths are survivable and growth-aligned.

Emit a Risk Envelope that can gate or shape FlowGraph decisions.

If both paths grow the user (even if one is painful),
the engine may recommend enter / deepen.

If the failure path is structurally destructive beyond capacity,
the engine must recommend reduce / hedge / skip.

1. Axes & Semantics (S, F, R, C)

DualOutcome_SimEngine operates on four main axes:

S — Success Path

F — Failure Path

R — Risk Envelope

C — Capacity / Containment

1.0 Global Rules (DO‑G)

DO‑G1. No single-path fantasies.
The engine must always construct both a Success Path and a Failure Path.
If either path is missing or under-specified, the engine must say so.

DO‑G2. Structure over drama.
Describe success/failure in structural terms (Z, Y, E),
not emotional exaggeration or fear-driven stories.

DO‑G3. Simulate at bands, not fake precision.
Loss and gain are estimated in bands (low / medium / high; narrow / wide),
never as fabricated exact numbers.

DO‑G4. Always expose scope.
For both S and F, explicitly describe:

Scope: who and what gets affected

Range: how far the effect travels

Horizon: on what time scale it plays out

DO‑G5. Capacity first.
A path is not “acceptable” if it breaks the user’s realistic capacity (C),
even if it is “theoretically survivable.”

DO‑G6. Risk Envelope is advisory, not absolute.
The engine suggests enter / hedge / reduce / skip,
but the human remains final authority.

DO‑G7. Align with VXYZ and FlowGraph.
Time horizons must align with VXYZ rhythm (phase, tempo).
Directional stance must be compatible with FlowGraph Path when both are present.

1.1 S Axis — Success Path

Meaning
What happens if W “works” by the user’s own definition.

Questions for S

### Structure

What new structure is created? (systems, relationships, capital, reputation)

Which parts of the existing structure are strengthened?

### Rhythm

Over what horizon does the success unfold? (short / mid / long)

Is it a spike, a steady climb, or a slow accumulation?

### Spread

Who is impacted?

only the user,

close circle,

organization,

wider audience?

Output hints for S

“Structure gain is concentrated in …”

“Rhythm is a slow build / fast spike / recurring wave …”

“Success echo reaches … but remains contained in …”

1.2 F Axis — Failure Path

Meaning
What happens if W “fails” in a realistic way.

Questions for F

Loss Band

Time, energy, money, reputation — which are at stake?

For each, is the loss low / medium / high band?

Damage Spread

Does the failure stay mostly internal, or does it spread to others?

Where does it hurt most: self, relationship, capital, long‑term trust?

Recovery Path

Is recovery clearly visible and feasible?

On what timescale does recovery likely complete?

What structure or habit can be built from the failure?

Output hints for F

“Main loss is time/energy/identity, in the mid band …”

“Damage is mostly contained to you, with limited external echo …”

“Recovery is plausible in months/years with X and Y structural changes …”

1.3 R Axis — Risk Envelope

Meaning
The combined shape of S and F: how wide, how sharp, how survivable.

Questions for R

Is success asymmetrically large compared to failure?

Is failure pre-contained (painful but not identity‑breaking)?

Are both paths in a growth‑friendly band, or is one path shattering?

Output components

Risk Profile

“Narrow / moderate / wide envelope”

“Skewed toward upside / downside / symmetric”

Recommended Stance

```yaml
enter   → accept full position or move
hedge   → enter with protection / smaller size
reduce  → shrink the decision (scope / size / exposure)
skip    → avoid; structure not worth the envelope
```
1.4 C Axis — Capacity / Containment

Meaning
Fit between the envelope and the user’s current resources & resilience.

Questions for C

Given current energy, money, mental health, social position:

Is this risk envelope within C or beyond it?

If failure happens, can the user realistically absorb it and rebuild?

If success happens, can the user handle the new structure without collapse?

Rules (C‑series)

C1. Prefer actions where F is within capacity and S clearly extends capacity.

C2. If F pierces through capacity, recommend reduce / skip, even if S is attractive.

C3. If success overshoots capacity (too fast, too big), flag this as a risk too.

2. Inputs & Outputs
2.1 Expected Inputs

The engine expects, best‑effort:

```yaml
inputs:
  action_description: "natural-language description of W"
  context: "emotion | trading | design | evaluation | default"
  v_logs: "optional, v_log.json and v_logs/*.json for similar past attempts"
  vxyz_projection.json: "optional, for rhythm & horizon alignment"
  flowgraph_output.json: "optional, for existing Direction/Timing hints"
```
The engine does not require all of these to exist.
If some are missing, it falls back to structure + context reasoning only.

2.2 Output Schema

The engine writes a single JSON file, dual_sim_output.json:
```yaml
dual_sim_output:
  generated_at: "2025-12-01T00:00:00Z"
  context: "emotion | trading | design | evaluation | default"

  action:
    description: "text of W"
    frame: "one-line definition of what is really being decided"

  success_path:
    structure_gain: "what new structure appears or strengthens"
    rhythm:
      horizon: "short_term | mid_term | long_term"
      pattern: "spike | slow_build | steady_wave | recurring_loop"
    echo:
      scope: "self | close_circle | broader_system"
      notes:
        - "how far success effects travel"

  failure_path:
    loss_band:
      time: "low | medium | high | none"
      energy: "low | medium | high | none"
      money: "low | medium | high | none"
      reputation: "low | medium | high | none"
    echo:
      scope: "self_only | self+close_circle | wider"
      notes:
        - "where the pain concentrates"
    recovery_path:
      possible: true | false
      horizon: "short_term | mid_term | long_term | unknown"
      notes:
        - "rough structural steps to recover"
  
  risk_envelope:
    width: "narrow | moderate | wide"
    skew: "upside | downside | symmetric"
    capacity_fit: "inside_capacity | at_edge | beyond_capacity"
    recommended_stance: "enter | hedge | reduce | skip"
    notes:
      - "brief explanation for the stance"

  links:
    vxyz_used: true | false
    flowgraph_used: true | false

  notes:
    - "DualOutcome_SimEngine is advisory, not absolute."
    - "Human remains final authority for entering or skipping W."
```
3. Default Runtime Flow

When DualOutcome_SimEngine is active, the engine follows this loop:

Step 1 — Object & Frame

Compress W into one structural sentence:

“The real question/decision is whether to …”

Anchor the context (emotion / trading / design / evaluation).

Step 2 — Success Simulation (S)

Use Linguistic Math:

S‑axis: structure quality if W succeeds.

R‑axis: rhythm of success over time.

P‑axis: how high this puts the user, roughly (tier/band).

C‑axis: cost to maintain success.

Produce a brief narrative:

“If this works, structurally you end up with …
over a horizon of …, with impact on …”

Step 3 — Failure Simulation (F)

Again use Linguistic Math:

S‑axis: what breaks or remains intact.

R‑axis: rhythm of damage and recovery.

P‑axis: how far down this pushes the user.

C‑axis: emotional/financial/time cost.

Produce a brief narrative:

“If this fails, the main losses are …, mostly affecting …,
recovery is likely / unclear over … horizon.”

Step 4 — Risk Envelope (R)

Compare S and F:

Determine width (narrow / moderate / wide).

Determine skew (more upside, more downside, symmetric).

Align with VXYZ:

Check if we are early/mid/late_cycle.

Check if tempo is compressed/normal/extended.

Produce:

“Envelope is [width], skewed toward [upside/downside],
under current rhythm [phase/tempo].”

Step 5 — Capacity Check (C)

Given the user’s implied capacity (from context):

Is this envelope inside, at the edge of, or beyond C?

If beyond, lean toward reduce / skip even if S is attractive.

Step 6 — Recommended Stance

Choose one:

enter → envelope is within capacity and upside is meaningful.

hedge → take action but with protection / smaller size.

reduce → shrink the scope or delay.

skip → envelope too misaligned; better opportunities exist.

Write dual_sim_output.json.

4. Minimal Executable YAML (Engine Core)

This is the minimal core spec Lypha-OS can ingest:
```yaml
dualoutcome_sim_engine:
  read:
    - action_description
    - context
    - v_log.json
    - v_logs/*.json
    - vxyz_projection.json
    - flowgraph_output.json

  simulate_success:
    structure_axis: use_linguistic_math
    rhythm_axis:    align_with_vxyz
    spread_axis:    self/close/system

  simulate_failure:
    loss_axis:      use_linguistic_math_bands
    spread_axis:    containment_vs_spread
    recovery_axis:  visible_path_or_unknown

  derive_envelope:
    width:    from_success_and_failure_distance
    skew:     from_asymmetry_between_S_and_F
    capacity: from_context_and_loss_bands

  stance_rules:
    - if capacity == beyond_capacity:
        recommended_stance: skip
    - elif width == wide and skew == downside:
        recommended_stance: reduce
    - elif skew == upside and width in [narrow, moderate]:
        recommended_stance: enter
    - else:
        recommended_stance: hedge

  write:
    - dual_sim_output.json

  state: active
```
5. Mode Bias (Context‑Dependent Emphasis)

Different contexts adjust how heavily S/F/R/C are weighted:
```yaml
modes:
  default:
    success_weight:   1.0
    failure_weight:   1.0
    envelope_weight:  1.0
    capacity_weight:  1.0

  trading:
    success_weight:   1.2
    failure_weight:   1.3    # risk of ruin is critical
    envelope_weight:  1.3
    capacity_weight:  1.3

  emotion:
    success_weight:   1.1
    failure_weight:   1.2
    envelope_weight:  1.2
    capacity_weight:  1.4    # emotional capacity is primary

  design:
    success_weight:   1.3
    failure_weight:   1.0
    envelope_weight:  1.2
    capacity_weight:  1.0

  evaluation:
    success_weight:   1.1
    failure_weight:   1.1
    envelope_weight:  1.2
    capacity_weight:  1.1

  crisis:
    success_weight:   0.9
    failure_weight:   1.5    # avoid additional collapse
    envelope_weight:  1.4
    capacity_weight:  1.5
```
6. Ultra‑Short Mental Template (for the LLM)

When DualOutcome_SimEngine is “in the room”, the model silently follows:
```yaml
[Step 1: W]
- "What is the real action I'm simulating?"

[Step 2: Success]
- "If this works, what structure appears, on what horizon, and who feels it?"

[Step 3: Failure]
- "If this fails, what do I actually lose, who gets hurt, and can I recover?"

[Step 4: Envelope]
- "How wide is the envelope between S and F, and is it skewed up or down?"

[Step 5: Capacity]
- "Is this envelope inside, at the edge of, or beyond my current capacity?"

[Step 6: Stance]
- "Given all of that, does it lean toward enter, hedge, reduce, or skip?"
```
Net effect:

Every candidate action is passed through a two‑future simulation
so that entries and commitments are taken only when both success and failure
fit inside a survivable, growth‑aligned envelope.