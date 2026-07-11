---
name: c3d-subassembly-patterns
description: Stock-subassembly pattern catalog — need→file index, worked DrawImplement recipes, point/link/shape code reference, mined from Autodesk's 120 VB stock subassemblies
---

# Subassembly Patterns & Recipe Catalog

Use this skill when authoring a coded Civil 3D subassembly and you want a worked pattern to copy:
a lookup of "which stock subassembly already solves this," a `DrawImplement` recipe for a specific
shape (median, daylight, overlay, marked-point join, conditional), or the canonical point/link/shape
code list. It is the companion to `c3d-custom-subassemblies` (the API/mechanics skill) — start there
for the SATemplate lifecycle, targets API, `.atc` registration, and build/deploy.

**Source corpus:** Autodesk ships 120 production VB.NET subassemblies at
`…\AutoCAD <ver>\C3D\Sample\Civil 3D API\C3DStockSubassemblies\Subassemblies\` (plus `SATemplate.vb`,
`Utilities.vb`, `CodesSpecific.vb`). This catalog is mined from them. **Version-skew caveat:** the
installed sample is Civil 3D **2027**; this project targets **2026**. Patterns are stable across both,
but verify any unusual API member against `api_combined_2026.db` before relying on it.

Our working C# implementations live in `CSharp/GpdSubassemblies/` — `LaneGpd.cs`,
`DaylightToSurfaceGpd.cs`, `OdotGuardrailMgs.cs`, `OdotCurbType2B6.cs` — all on `SubassemblyBase` (our
C# port of `SATemplate.vb`). Recipes below use that base and the `SaUtilities`/`Codes` helpers.

## Reading params vs. targets — the one rule that bites

Two different accessors, and mixing them up silently freezes every parameter at its default:

| You are reading… | Use | Returns | Proven in |
|---|---|---|---|
| A **scalar param** (double/long/string/bool) | **indexer** `cs.ParamsDouble[name].Value` | the value | `SubassemblyBase.GetDouble/GetInt/GetString` |
| A **target** (surface/alignment/offset/elevation) | **collection method** `cs.ParamsSurface.Value(name)` | `ObjectId` / `WidthOffsetTarget` / `SlopeElevationTarget` | `DaylightToSurfaceGpd`, `OdotGuardrailMgs` |
| A **marked point** | **collection method** `cs.ParamsPoint.Value(name)` → `ParamPoint`, then `.Station/.Offset/.Elevation` | a `ParamPoint` | stock `LinkToMarkedPoint.vb` (no C# example yet — verify) |

- `cs.ParamsDouble.Add(name, default)` is a **SETTER** — only call it in `GetInputParametersImplement`
  (declare) and in `Set*` helpers (write computed output back). Reading with `Add(name,d).Value`
  overwrites the user's edit with the default every section. Symptom: "subassembly ignores all params
  and Left/Right." Always read scalars through `GetInt/GetDouble/GetString`.
- **DB-invisibility trap (verification):** every param/target collection inherits a generic
  `ParamCollectionBase<T>` whose members do **not** reflect into `api_combined_2026.db`
  (`ParamSurfaceCollection`/`ParamOffsetTargetCollection` show "No members"; `ParamDoubleCollection`
  shows only `Add`). So `code-verifier`/DB lookups will **false-positive** on `.Value(name)`,
  `[name].Value`, `GetDistanceToAlignment`, `GetElevation`. These are verified by the shipping VB
  stock samples and our own code — **do not "fix" them away.**

## Stock-Subassembly Lookup Index

"I need X → study/copy this stock file." All paths under `…\C3DStockSubassemblies\Subassemblies\`.

| Need | Best stock file | Nearest C# example |
|---|---|---|
| Plain fixed-slope lane | `BasicLane.vb` | `LaneGpd.cs` |
| Crowned two-slope lane | `CrownedLane.vb` | — |
| Broken-back inside/outside slopes | `LaneBrokenBack.vb` | — |
| Parabolic lane | `LaneParabolic.vb` | — |
| Lane driven by superelevation (alignment SE) | `LaneInsideSuper.vb` / `LaneOutsideSuper.vb` | — |
| Lane with full axis-of-rotation control | `LaneSuperelevationAOR.vb` | Recipe R5 |
| Multi-layer pavement (pave/base/subbase stack) | `ShoulderMultiLayer.vb` | — |
| Basic curb / curb+gutter | `BasicCurb.vb` / `BasicCurbAndGutter.vb` | `OdotCurbType2B6.cs` |
| Fully parametric curb+gutter (11 dims, SE, subbase) | `UrbanCurbGutterGeneral.vb` | `OdotCurbType2B6.cs` |
| Sidewalk with offset targets | `UrbanSidewalk.vb` | — |
| Basic / multi-layer shoulder | `BasicShoulder.vb` / `ShoulderMultiLayer.vb` | — |
| V-ditch / channel with lining | `Channel.vb` | — |
| Cut ditch that ties to a surface | `BasicSideSlopeCutDitch.vb` | `DaylightToSurfaceGpd.cs` |
| Simple daylight to surface (cut/fill auto) | `DaylightStandard.vb` | `DaylightToSurfaceGpd.cs` |
| Daylight chaining several surfaces + benches | `DaylightMultipleSurface.vb` | Recipe R4 |
| Daylight constrained to min/max width or offset | `DaylightMinWidth.vb` / `DaylightMaxOffset.vb` | — |
| Daylight to right-of-way / fixed offset | `DaylightToROW.vb` / `DaylightToOffset.vb` | — |
| **Depressed median, symmetric left+right** | `MedianDepressed.vb` | Recipe R1 |
| Raised median (crown / constant slope) | `MedianRaisedWithCrown.vb` | — |
| Median with integrated barrier | `MedianConstantSlopeWithBarrier.vb` | — |
| Barrier / noise wall (closed trapezoid) | `BasicBarrier.vb` / `SimpleNoiseBarrier.vb` | `OdotGuardrailMgs.cs` (AddClosedRect) |
| Guardrail | `BasicGuardrail.vb` | `OdotGuardrailMgs.cs` |
| Retaining wall (tapered / vertical / tie-to-ditch) | `RetainWallVertical.vb` / `RetainWallTieToDitch.vb` | — |
| Pavement mill / level / mill+level overlay | `Overlay_Mill_Level_Crown.vb` | — |
| Widen existing pavement, match existing slope | `OverlayWidenMatchSlope1.vb` | — |
| **Mark a point** for a later subassembly to find | `MarkPoint.vb` | Recipe R2 |
| **Link to a marked point** (join two roadways) | `LinkToMarkedPoint.vb` | Recipe R2 |
| Generic link to offset+elevation target | `LinkWidthAndSlope.vb` / `LinkOffsetAndElevation.vb` | `OdotGuardrailMgs.cs` |
| Link sloping to a surface | `LinkSlopeToSurface.vb` | `DaylightToSurfaceGpd.cs` |
| **Conditional** cut-vs-fill gate (no geometry) | `ConditionalCutOrFill.vb` | Recipe R3 |
| Conditional on target found/not-found | `ConditionalHorizontalTarget.vb` | — |
| Trench + pipe | `TrenchPipe1.vb` | `OdotCurbType2B6.cs` (underdrain) |
| Strip topsoil / pavement removal | `StrippingTopSoil.vb` | — |

## Pattern by Category

Shared scaffold for every stock SA: inherit `SATemplate`; override
`GetLogicalNamesImplement` (targets), `GetInputParametersImplement` (params),
`GetOutputParametersImplement` (computed outputs), `DrawImplement` (geometry). Origin = attachment
point at (0,0); `flip = -1` on Left mirrors all horizontal offsets; build **Points → Links → Shapes**
and tag each with codes.

| Category | Attachment | Targets | Geometry signature | Notable |
|---|---|---|---|---|
| **Lanes / SE** | single, flip by side | OffsetTarget (width), ElevationTarget (edge) | 4–10 pts, layered links, 1–4 shapes | reads alignment cross-slope via `Alignment.GetCrossSlopeAtStation`; AOR via `SetAxisOfRotation*` |
| **Curbs/Gutters** | single, at EOP | optional offset/elev | 4–6 pts, curb-face/gutter/back links, 1–2 shapes | dimension-driven; subbase shape conditional on depth |
| **Shoulders** | single | OffsetTarget (width) | cumulative-depth point stacks; many shapes | multi-layer stacking accumulates `−depth` down the attachment line |
| **Ditches/Channels** | single; cut ties to surface | Surface, sometimes elev/offset | foreslope→bottom→backslope; lining shapes | `IsAboveSurface` then `IntersectSurface`; re-check cut/fill at ditch edge |
| **Daylight** | single (hinge) | Surface (1 or many) | hinge→slope→intersection point | multi-slope flat/medium/steep by height limit; optional rounding via `SampleSection`/`GetRoundingCurve` |
| **Medians** | **centerline, symmetric — no side param** | optional MarkedPoint | mirrored point pairs about x=0 | draws both sides from one origin; depressed variant needs a prior `MarkPoint` |
| **Barriers/Walls/Rails** | single, flip by side | Surface/elev for walls | closed trapezoid (8 pts → 1 shape) | `AddClosedRect` helper pattern |
| **Overlays** | single | Surface (existing road) + edge OffsetTargets | samples existing surface, builds mill/level/overlay layers | `SampleSection` between crown & edge; min-mill-depth clearance negotiation |
| **Generic links** | single | any | 1–N links, no shape | the primitives; `LinkWidthAndSlope` is the target-read reference |
| **Conditional** | single | Surface/offset | **emits no geometry** | `RecordError(StopProcessingConditional, …)` halts downstream SAs when test fails |

## Worked Recipes

All recipes target our `SubassemblyBase`. Read scalars with `GetInt/GetDouble/GetString`; never throw —
call `SaUtilities.RecordWarning`. Add codes from `Codes.cs`.

### R1 — Median dual-insert (symmetric, single center origin)

Medians attach at the centerline and draw **both** sides from one origin — there is no `Side`/flip
param. Mirror each point about x=0. (Stock: `MedianDepressed.vb`.)

```csharp
protected override void DrawImplement(CorridorState cs)
{
    double halfWidth = GetDouble(cs, "Width", 16.0) / 2.0;   // total median width
    double depth     = GetDouble(cs, "Depth", 0.5);          // depressed ditch depth
    double slope     = GetDouble(cs, "Slope", 0.25);         // each side falls toward center

    // Symmetric points about the centerline (x = 0). Origin is the median CL top.
    var pLeftTop  = cs.Points.Add(-halfWidth, 0.0, "");      pLeftTop.Codes.TryAdd(Codes.ETW);
    var pRightTop = cs.Points.Add( halfWidth, 0.0, "");      pRightTop.Codes.TryAdd(Codes.ETW);
    var pBottom   = cs.Points.Add( 0.0, -depth, "");         pBottom.Codes.TryAdd(Codes.FlowlineDitch);

    cs.Links.Add(pLeftTop,  pBottom, Codes.Top);             // left fall
    cs.Links.Add(pBottom,   pRightTop, Codes.Top);           // right fall
}
```

### R2 — Marked-point join (link two roadways)

One subassembly drops a named mark; another retrieves it and links to it. Marked-point names are
**upper-cased** in the stock samples — normalize. (Stock: `MarkPoint.vb` + `LinkToMarkedPoint.vb`.)

```csharp
// --- Producer: drop a mark at the attachment point (in its DrawImplement) ---
var mp = cs.ParamsPoint.Add(markName.ToUpperInvariant());   // ParamPoint
double wx = 0, wy = 0, wz = 0;
cs.SoeToXyz(alignId, cs.CurrentStation, origin.Offset, origin.Elevation, ref wx, ref wy, ref wz);
mp.SetPoint(wx, wy, wz);

// --- Consumer: find the mark and link to it ---
ParamPoint? mark = null;
try { mark = cs.ParamsPoint.Value(markName.ToUpperInvariant()); } catch { }
if (mark == null)
{
    SaUtilities.RecordWarning(cs, CorridorError.NoMarkedPointFound,
        $"Marked point '{markName}' not found — is the producing subassembly upstream?",
        nameof(MySubassembly));
    return;
}
// mark.Station / mark.Offset / mark.Elevation are absolute; convert to section-relative:
var pHere  = cs.Points.Add(0.0, 0.0, "");
var pThere = cs.Points.Add(mark.Offset - origin.Offset, mark.Elevation - origin.Elevation, "");
cs.Links.Add(pHere, pThere, Codes.Top);
```

### R3 — Conditional cut/fill gate (emits no geometry)

A conditional subassembly tests a condition and, when it fails, calls
`RecordError(StopProcessingConditional, …)` to halt the subassemblies placed **after** it in the
assembly. It draws nothing. (Stock: `ConditionalCutOrFill.vb`.)

```csharp
protected override void DrawImplement(CorridorState cs)
{
    int wantCut   = GetInt(cs, "Type", 0);                  // 0 = cut, 1 = fill
    double minD   = GetDouble(cs, "MinDistance", 0.0);
    double maxD   = GetDouble(cs, "MaxDistance", SaUtilities.BigDistance);

    ObjectId surfId = ObjectId.Null;
    try { surfId = cs.ParamsSurface.Value("TargetDTM"); } catch { }
    if (surfId.IsNull) return;

    SaUtilities.GetAlignmentAndOrigin(cs, out var alignId, out var origin);
    bool isFill = cs.IsAboveSurface(surfId, alignId, origin);   // above existing ground ⇒ fill
    bool conditionMet = (wantCut == 0) ? !isFill : isFill;

    // (optional) also gate on the cut/fill depth being within [minD, maxD] …

    if (!conditionMet)
    {
        cs.LayoutModeDisplayType = CorridorLayoutModeDisplay.Conditional;
        cs.RecordError(CorridorError.StopProcessingConditional, CorridorErrorLevel.None,
            "", nameof(MyConditional), false);   // halts downstream subassemblies
    }
    // either way: no points/links/shapes
}
```

### R4 — Multi-surface daylight with benches

Chain from the inner-most surface outward; insert an optional bench between layers. (Stock:
`DaylightMultipleSurface.vb`. Single-surface baseline: `DaylightToSurfaceGpd.cs`.)

```csharp
string[] surfNames = { "Surface1", "Surface2", "Surface3" };   // registered as Surface logical names
double benchWidth  = GetDouble(cs, "BenchWidth", 0.0);
double benchSlope  = GetDouble(cs, "BenchSlope", -0.02);
double cutSlope    = GetDouble(cs, "CutSlope", 0.25);
bool   lookRight   = GetInt(cs, "Side", SaUtilities.Right) == SaUtilities.Right;

SaUtilities.GetAlignmentAndOrigin(cs, out var alignId, out var origin);
var here = new PointInMem { Station = cs.CurrentStation, Offset = origin.Offset, Elevation = origin.Elevation };
Point prev = cs.Points.Add(0.0, 0.0, "");

foreach (var name in surfNames)
{
    ObjectId surfId = ObjectId.Null;
    try { surfId = cs.ParamsSurface.Value(name); } catch { }
    if (surfId.IsNull) continue;                              // optional surfaces may be unassigned
    if (cs.IsAboveSurface(surfId, alignId, here)) continue;   // already above this layer — skip

    IPoint? hit = null;
    try { hit = cs.IntersectSurface(surfId, alignId, here, lookRight, cutSlope); } catch { }
    if (hit == null) continue;

    var pHit = cs.Points.Add(hit.Offset - origin.Offset, hit.Elevation - origin.Elevation, "");
    pHit.Codes.TryAdd(Codes.DaylightCut);
    cs.Links.Add(prev, pHit, Codes.DaylightCut);
    prev = pHit;
    here.Offset = hit.Offset; here.Elevation = hit.Elevation;

    if (benchWidth > 0)                                       // step out a bench before the next surface
    {
        double bx = here.Offset + (lookRight ? 1 : -1) * benchWidth;
        var pBench = cs.Points.Add(bx - origin.Offset, here.Elevation + benchWidth * benchSlope - origin.Elevation, "");
        cs.Links.Add(prev, pBench, Codes.Top);
        prev = pBench; here.Offset = bx; here.Elevation += benchWidth * benchSlope;
    }
}
```

### R5 — Superelevation axis-of-rotation lane

Read the alignment cross-slope at the station, then register the lane as a potential SE pivot. (Stock:
`LaneSuperelevationAOR.vb`.)

```csharp
double width = GetDouble(cs, "Width", 12.0);
int side     = GetInt(cs, "Side", SaUtilities.Right);
double flip  = SaUtilities.GetFlip(side);

// Pull the design cross-slope from the alignment's superelevation at this station.
var segType = side == SaUtilities.Left
    ? SuperelevationCrossSegmentType.LeftOutLaneCrossSlope
    : SuperelevationCrossSegmentType.RightOutLaneCrossSlope;

double slope = GetDouble(cs, "DefaultSlope", -0.02);   // fallback if SE not assigned
SaUtilities.GetAlignmentAndOrigin(cs, out var alignId, out var origin);
using (var tr = ...)   // open a read transaction on the working DB (see c3d-root-objects)
{
    var align = (Alignment)tr.GetObject(alignId, OpenMode.ForRead);
    try { slope = align.GetCrossSlopeAtStation(cs.CurrentStation, segType, true); } catch { }
}

var pCrown = cs.Points.Add(0.0, 0.0, "");                 pCrown.Codes.TryAdd(Codes.Crown);
var pEtw   = cs.Points.Add(flip * width, width * slope, ""); pEtw.Codes.TryAdd(Codes.ETW);
cs.Links.Add(pCrown, pEtw, Codes.Top);

// Declare this lane as a candidate axis-of-rotation pivot for the SE engine.
cs.SetAxisOfRotationInformation(true, slope, segType, false);
cs.SetAxisOfRotationCrownPoint(1u);   // 1-based crown point index (see gotcha)
```

## Point / Link / Shape Code Reference

Codes are string identifiers Civil 3D keys surface-extraction, QTO, and section labels on. Our
`Codes.cs` is the subset we use; the stock `CodesSpecific.vb` defines ~189. **Hard-code codes** for
consistency across the catalog; **expose a code parameter** only for generic-link subassemblies where
the user must choose (e.g. `LinkMulti`, `GenericPavementStructure`). Add to `Codes.cs` rather than
inlining strings.

| Group | Common stock codes | In `Codes.cs` |
|---|---|---|
| **Pavement top/edge** | `Crown`, `ETW`, `EPS`, `Lane`, `EOP` | `Crown`, `ETW`, `EPS`, `EOP` |
| **Layered pavement** | `Pave`/`Pave1-3`, `Base`/`Base1-4`, `SubBase`/`Subbase1-3` | `Pave`, `Pave1`, `Pave2`, `Base`, `SubBase` |
| **Subbase-level points** | `Crown_Sub`, `ETW_Sub` | `CrownSubBase`, `ETWSubBase` |
| **Surface links** | `Top`, `Datum` | `Top`, `Datum` |
| **Curb/gutter** | `Top_Curb`, `Back_Curb`, `Flowline_Gutter`, `Flange`, `Curb` | `TopCurb`, `BackCurb`, `BottomCurb`, `FlowlineGutter`, `Curb`, `CurbFace`, `CurbTop`, `CurbBack` |
| **Sidewalk** | `Sidewalk_In`, `Sidewalk_Out` | `SidewalkIn`, `SidewalkOut` |
| **Median/shoulder** | `Median`, `LMedDitch`, `EPS` | `EPSShoulder` |
| **Ditch/channel** | `Ditch_In/Out`, `Flowline_Ditch`, `Channel_Bottom` | `DitchIn`, `DitchOut`, `FlowlineDitch` |
| **Daylight/hinge** | `Daylight`, `Daylight_Cut`, `Daylight_Fill`, `Hinge_Cut`, `Hinge_Fill` | `Daylight`, `DaylightCut`, `DaylightFill`, `DaylightSub`, `HingeCut`, `HingeFill` |
| **Barrier/guardrail/rail** | `Barrier`, `Guardrail`, `Rail`, `R1-R6` | `Barrier`, `GuardrailPost`, `GuardrailRail`, `Blockout`, `TopOfRail`, `FaceOfRail`, `SlopeBreak`, `ForeslopeToe` |
| **Retaining wall** | `RWall`, `RW_Front/Top/Back`, `Footing_Bottom` | — (add as needed) |
| **Overlay/rehab** | `EOV`, `Mill`, `Level`, `Overlay` | `Overlay`, `Mill` |
| **Marked point** | `MarkedPoint` | — |
| **Trench/pipe** | `Trench`, `Trench_Bottom`, `Trench_Bedding` | `Underdrain`, `UnderdrainPipe`, `UnderdrainInvert` |

## VB → C# translation cheat sheet

When porting a stock `.vb` subassembly to C#:

| VB | C# |
|---|---|
| `Dim a(0 To 3) As Double` | `double[] a = new double[4];` |
| `Dim a(3) As Point` | `Point[] a = new Point[4];` (VB upper-bound is inclusive) |
| `12.0#` (double literal) | `12.0` |
| `If x Is Nothing` / `x = Nothing` | `if (x == null)` / `x = null` |
| bare `Catch` | `catch { }` (catch-all) — but prefer narrowing |
| `Public Module Utilities` | `public static class Utilities` |
| `Split(s, ",")` | `s.Split(',')` |
| SE crown index `nCrownPoint - 1` (VB subtracts 1 for an internal C++ array) | **Do NOT subtract 1.** `SetAxisOfRotationCrownPoint` itself takes a **1-based** point number — `(1u)` = first point, `0` = none (see gotcha) |
| `oParamsDouble.Value("W")` | scalar read → `GetDouble(cs, "W", default)` (indexer under the hood) |
| `oParamsSurface.Value("T")` | target read → `cs.ParamsSurface.Value("T")` (collection method — keep it) |

## Gotchas

- **Param read vs. target read** — indexer for scalars, `.Value(name)` for targets. See the rule
  table up top. This is the single most common cause of "my subassembly ignores its parameters."
- **DB-invisible accessors** — `code-verifier`/DB lookups can't see `ParamCollectionBase<T>` members;
  they will flag `.Value(name)`, `GetDistanceToAlignment`, `GetElevation` as "not found." Verify
  against the shipping VB samples / our code, not the DB.
- **Medians have no `Side`** — they draw symmetric geometry about x=0 from one center origin; don't add
  a flip param. The depressed median needs a `MarkPoint` upstream.
- **Marked-point names are upper-cased** in the stock samples — normalize with `ToUpperInvariant()`
  on both produce and consume, or the lookup misses silently.
- **SE crown-point index is 1-based** — `SetAxisOfRotationCrownPoint(1u)` means the first point;
  `0` means "no crown point," not "first." Don't pass a 0-based array index.
- **Conditional subassemblies emit no geometry** — they gate downstream SAs via
  `RecordError(CorridorError.StopProcessingConditional, …)`. Place them *before* what they guard.
- **Cut ditches re-check cut/fill at the ditch edge** — `IsAboveSurface` at the origin can differ from
  the outer edge; re-evaluate before casting the daylight slope or it points the wrong way.
- **Convert target intersection points to section-relative** — `IntersectSurface` returns absolute
  station/offset/elevation; subtract `origin.Offset`/`origin.Elevation` before `Points.Add`.
- **Version skew** — the sample is 2027; a member that compiles there may be absent in 2026. Check the
  DB. (`ParamsBool`, `SampleSection`, `SetAxisOfRotation*` are all present in 2026.)

## Related Skills

- `c3d-custom-subassemblies` — SATemplate lifecycle, targets API, `.atc` registration, build/deploy, the GpdSubassemblies scaffold (start here)
- `c3d-corridors` — assemblies, baselines, regions, applied subassemblies
- `c3d-superelevation` — reading cross-slope / axis-of-rotation from alignments
- `c3d-surfaces` — surfaces consumed by daylight/ditch/overlay intersection
