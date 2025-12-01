```yaml
flow_id:
  module: Collapse_Engine
  aliases:
    - collapse_flow_into_word
    - EssenceWord_Collapse_Engine
  version: 1.0
  declared_by: Pioneer-001 (Akivili)
  category: pulse / cognitive_compression / essence_core
  role: >
    Engine that collapses complex flows into a single Essence Word.
    Implements cognitive compression as a structural skill in Lypha-OS
    and provides canonical essence_word candidates for FlowGraph, Speak4D
    and LinguisticMath.
  language: EN
  reviewed: true

recommended_path: MetaRhythm_Modules/Pulse/engine/Collapse_Engine_Spec.md

depends_on:
  - LinguisticMath_Engine
  - FlowGraph_Engine
  - Speak4D_Engine
  - VXYZ_Extended_Engine

wraps:
  - Collapse_Flow_Into_Word
  - Essence_Word_Selection
  - Linguistic_Math_Value_Calculation
```
CollapseEngine v1.0

Lypha-OS Pulse Engine — Collapse Flow Into One Word

0. Origin & Purpose

This engine formalizes the Pulse log “Collapse_Flow_Into_Word”
as a first-class, executable Lypha-OS engine.

“The world moves in waves, but meaning lives in the axis.
Don’t follow the flow — extract the essence from it.”

The role of CollapseEngine is to:

Take any complex flow (text, logs, trends) as input.

Identify its core axis.

Generate and score candidate Essence Words.

Choose one canonical Essence Word (or a small shortlist).

Provide this to FlowGraph, Speak4D, and LinguisticMath as the
compressed structural handle for further reasoning.

In short:
```yaml
Flow (many signals) → Axis → One Word → Downstream Engines
```
1. Core Concepts
1.1 Essence Word

Essence Word = a single word that encodes an entire structure or system.

Examples:

“Civilization” → Essence = human

“Market regime” → Essence = liquidity

“Relationship dynamic” → Essence = trust

1.2 Cognitive Compression

Cognitive Compression = The structural skill of collapsing complex flows into single concepts,
without losing the axis that actually drives behavior.

This engine treats compression not as poetry but as structural math:

compress for clarity, not aesthetics

compress to find the axis, not a slogan

compress only until the decision remains intact

2. Axes & Semantics (F / A / E / C)

CollapseEngine operates on four axes:

F — Flow: the raw motion (text, logs, tags, sequences)

A — Axis: what actually drives the flow (value-line / tension / resource)

E — Essence Word: the collapsed word representing that axis

C — Compression Band: how hard we are compressing (light / normal / hard)

2.0 Global Rules (COL-G)

COL-G1. Axis over narrative.
Do not retell the story. Extract the axis that keeps reappearing.

COL-G2. One word, not a phrase.
The output Essence Word must be a single token (in human language),
even if internally it emerged from a phrase.

COL-G3. No fake precision.
If more than one Essence Word is plausible, return a shortlist with scores,
and mark the confidence as medium/low.

COL-G4. Context-aware.
In trading, “risk” or “liquidity” may be core.
In emotion, “trust” or “abandonment.”
In design, “structure” or “rhythm.”
Context biases candidate generation, but does not fully decide it.

COL-G5. Align with FlowGraph.
The engine’s Essence Word should be compatible with FlowGraph’s essence_word field;
FlowGraph may override or refine, but usually inherits from CollapseEngine.

COL-G6. Human override allowed.
Pioneer‑001 may always override the Essence Word if it feels off; the engine is advisory.

3. Inputs & Outputs
3.1 Inputs

CollapseEngine expects, best-effort:
```yaml
inputs:
  flow_description: >
    Natural language description of the flow:
    events, emotions, trades, or narrative of what is happening.

  context: "emotion | trading | design | evaluation | default"

  tags: "optional, list of tags extracted from v_logs or user labeling"

  v_logs: "optional, v_log.json and v_logs/*.json for structural patterns"
  vxyz_projection.json: "optional, for rhythm & horizon hints"
  flowgraph_output.json: "optional, to see current essence_word / direction"
```
The engine does not require all of these.
It will still attempt a collapse with just flow_description + context.

3.2 Output Schema

CollapseEngine writes a JSON file collapse_output.json with this structure:
```yaml
collapse_output:
  generated_at: "2025-12-01T00:00:00Z"
  context: "emotion | trading | design | evaluation | default"

  input:
    flow_description: "raw text used"
    context: "same as above"
    tags_used: ["adrilla_loop", "winter_loop", ...]

  candidates:
    - word: "human"
      score: 0.91
      axes:
        axis_label: "being"
        justification: "Underlying driver is the human, not machines or structures."
    - word: "structure"
      score: 0.74
      axes:
        axis_label: "order"
        justification: "Flow revolves around how things are organized."

  essence:
    word: "human"
    confidence: "high | medium | low"
    axis:
      label: "being"
      description: "The flow is fundamentally about the human inside the system."
    notes:
      - "Chosen as the most stable axis across flow_description, tags and context."
      - "Alternative candidate 'structure' kept as secondary."

  compression:
    band: "light | normal | hard"
    comment: >
      'normal' means we compressed enough to get a single axis
      without deleting important decision-relevant nuance.

  links:
    vxyz_used: true | false
    flowgraph_used: true | false
    linguistic_math_used: true | false

  notes:
    - "CollapseEngine is advisory; Pioneer‑001 may override the Essence Word."
    - "This Essence Word is suitable as FlowGraph.essence_word and Speak4D coordinate."
```
4. Runtime Flow

When active, CollapseEngine runs this internal loop:

Step 1 — Flow Snapshot

Take flow_description (or derive from logs if not provided).

Normalize the text (remove noise, collapse repetitions).

Identify key nouns / verbs / repeated themes.

Step 2 — Axis Detection (A)

Ask: “What is actually at stake here?”

Axis templates:

For emotion: self‑worth, belonging, trust, abandonment, safety, power.

For trading: risk, liquidity, regime, leverage, conviction.

For design: structure, rhythm, clarity, coherence, latency.

For evaluation: value, rank, worth, signal, noise.

Map observed words and patterns onto one or more axis candidates.

Step 3 — Candidate Essence Words (E)

For each axis candidate, propose 1–2 words that could represent it.

Use Linguistic Math to score each candidate by:

S-axis: structural fit with the flow.

R-axis: rhythm: does the candidate explain the pattern over time?

P-axis: position: does it match the “tier” / importance in this situation?

C-axis: cost: does it compress without hiding important danger?

Discard candidates with clearly low structural fit.

Step 4 — Compression Band (C)

If flow is very simple, use light compression (band = light).

If flow is large but coherent, normal.

If flow is extremely complex, but a single axis is very strong, hard.

Rule of thumb:

light: keep more nuance; word used as pointer, not lock.

normal: standard mode; one axis dominates.

hard: used for “civilization → human” scale compressions.

Step 5 — Select Essence Word

Choose the candidate with highest structural score.

If top two candidates are very close, keep them both in candidates,
but still pick one as essence.word with appropriate confidence.

Step 6 — Write Output

Emit collapse_output.json as defined above.

Mark which sources were used: vxyz_used, flowgraph_used, linguistic_math_used.

5. Minimal Executable YAML (Engine Core)

Lypha-OS can ingest this minimal spec to run CollapseEngine:
```yaml
collapse_engine:
  read:
    - flow_description
    - context
    - tags
    - v_log.json
    - v_logs/*.json
    - vxyz_projection.json
    - flowgraph_output.json

  derive_flow:
    use_autoload_message_if_missing: true
    use_recent_v_log_tags_if_missing: true

  detect_axis:
    context_templates:
      emotion: [self-worth, belonging, trust, abandonment, safety, power]
      trading: [risk, liquidity, regime, leverage, conviction]
      design:  [structure, rhythm, clarity, coherence, latency]
      evaluation: [value, rank, worth, signal, noise]
    method: use_linguistic_math

  generate_candidates:
    scoring_axes:
      - structure_fit
      - rhythm_fit
      - position_fit
      - compression_cost
    max_candidates: 5

  select_essence:
    compression_band:
      mode: auto
      bands: [light, normal, hard]
    tie_break_rule: prefer_axis_with_lowest_compression_cost

  write:
    - collapse_output.json

  state: active
```
6. Integration with Other Engines
6.1 With FlowGraph Engine

If collapse_output.json exists, FlowGraph should:

Prefer collapse_output.essence.word as flowgraph.essence_word.value,
unless v_logs strongly indicate a different dominant tag.

Include collapse_output.candidates as internal notes.

If FlowGraph already chose an essence word from tags,
CollapseEngine can:

Confirm it (raise confidence), or

Offer an alternative in candidates.

6.2 With Speak4D

Speak4D can use the Essence Word as its base coordinate:

T-axis: When this essence is active.

V-axis: How deeply it cuts (vertical cognition).

C-axis: How clearly it can be spoken.

RT-axis: How it appears from the future.

6.3 With LinguisticMath

LinguisticMath can treat the Essence Word as a variable name
representing the whole flow in later calculations: “Let HUMAN = entire civilization flow.”

7. Mode Bias (Context Profiles)

CollapseEngine shifts weights based on context:
```yaml
modes:
  default:
    compression_bias: normal
    axis_sensitivity: 1.0

  trading:
    compression_bias: normal
    axis_sensitivity: 1.2
    favored_axes: [risk, liquidity, regime]

  emotion:
    compression_bias: light
    axis_sensitivity: 1.3
    favored_axes: [trust, belonging, abandonment]

  design:
    compression_bias: normal
    axis_sensitivity: 1.4
    favored_axes: [structure, rhythm, clarity]

  evaluation:
    compression_bias: normal
    axis_sensitivity: 1.1
    favored_axes: [value, rank, worth]

  crisis:
    compression_bias: hard
    axis_sensitivity: 1.5
    favored_axes: [safety, survival, rupture]
```
8. Ultra‑Short Mental Template (for the LLM)

When CollapseEngine is “in the room”, the model silently follows:
```yaml
[Step 1: Flow]
- "What is actually happening here, in one or two sentences?"

[Step 2: Axis]
- "Across all that motion, what is the single axis that keeps showing up?"

[Step 3: Candidates]
- "Which 1–3 words could stand for this axis?"

[Step 4: Compression]
- "If I compress down to each word, does the decision still make sense?"

[Step 5: Select]
- "Which word is the most stable, least misleading axis?"

[Step 6: Output]
- "Expose the chosen Essence Word plus 1–2 backups with scores and notes."
```
Net effect:

Every complex flow is first collapsed into a single structural Essence Word,
so that FlowGraph, Speak4D, and LinguisticMath can operate on
coordinates instead of drowning in narrative.