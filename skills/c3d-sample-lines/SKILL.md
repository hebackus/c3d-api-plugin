---
name: c3d-sample-lines
description: Sample lines, sample line groups, section views, section network discovery for gravity and pressure pipe labeling in cross-section workflows
---

# Civil 3D Sample Lines and Section Views

Use this skill when working with sample line groups, sample lines, section views, or when labeling gravity/pressure pipe networks in cross-section views.

## Object Hierarchy

```
Alignment
  └── SampleLineGroup (via GetSampleLineGroupIds())
        └── SampleLine (via GetSampleLineIds())
              ├── .Station — chainage at which this sample line cuts
              ├── GetSectionIds()   → Section objects (one per sampled source)
              └── GetSectionViewIds() → SectionView objects (one per view at this station)
```

## Accessing Sample Line Groups

```csharp
CivilDocument civilDoc = CivilApplication.ActiveDocument;
ObjectIdCollection alignmentIds = civilDoc.GetAlignmentIds();

foreach (ObjectId alignId in alignmentIds)
{
    Alignment alignment = tr.GetObject(alignId, OpenMode.ForRead) as Alignment;
    ObjectIdCollection slgIds = alignment.GetSampleLineGroupIds();

    foreach (ObjectId slgId in slgIds)
    {
        SampleLineGroup slg = tr.GetObject(slgId, OpenMode.ForRead) as SampleLineGroup;
        ed.WriteMessage("Group: {0}\n", slg.Name);

        ObjectIdCollection sampleLineIds = slg.GetSampleLineIds();
        ed.WriteMessage("  Sample lines: {0}\n", sampleLineIds.Count);
    }
}
```

## Iterating Sample Lines

```csharp
SampleLineGroup slg = tr.GetObject(slgId, OpenMode.ForRead) as SampleLineGroup;

foreach (ObjectId slId in slg.GetSampleLineIds())
{
    SampleLine sl = tr.GetObject(slId, OpenMode.ForRead) as SampleLine;

    double station = sl.Station; // chainage value along the alignment

    ObjectIdCollection sectionIds     = sl.GetSectionIds();     // Section objects
    ObjectIdCollection sectionViewIds = sl.GetSectionViewIds(); // SectionView objects
}
```

## Section Types — Gravity vs. Pressure

Each `SampleLine` holds one `Section` per sampled source (surface, gravity network, pressure network, etc.). Cast to the appropriate subtype:

```csharp
foreach (ObjectId sectionId in sampleLine.GetSectionIds())
{
    Section section = tr.GetObject(sectionId, OpenMode.ForRead) as Section;

    if (section is SectionPipeNetwork gravitySection)
    {
        // Gravity pipe network section
        ObjectId networkId = gravitySection.SourceId; // links to Network
    }
    else if (section is SectionPressurePipeNetwork pressureSection)
    {
        // Pressure pipe network section
        ObjectId networkId = pressureSection.SourceId; // links to PressurePipeNetwork
    }
    // Other types: SectionSurface, etc.
}
```

**`SourceId`** is the key link from a `Section` back to the model object (network, surface, etc.) that was sampled.

## Finding the Section Network ID for Label Creation

Before creating labels in a section view, you must find the `Section` object (`SectionPipeNetwork` or `SectionPressurePipeNetwork`) that corresponds to your chosen network. This ID is required by all section label `Create()` methods as the `sectionNetworkId` parameter:

```csharp
// Gravity
ObjectId sectionPipeNetworkId = ObjectId.Null;
foreach (ObjectId sectionId in sampleLine.GetSectionIds())
{
    Section section = tr.GetObject(sectionId, OpenMode.ForRead) as Section;
    if (section is SectionPipeNetwork sn && sn.SourceId == targetNetworkId)
    {
        sectionPipeNetworkId = sectionId; // this is the sectionNetworkId for labels
        break;
    }
}

// Pressure
ObjectId sectionPressureNetworkId = ObjectId.Null;
foreach (ObjectId sectionId in sampleLine.GetSectionIds())
{
    Section section = tr.GetObject(sectionId, OpenMode.ForRead) as Section;
    if (section is SectionPressurePipeNetwork spn && spn.SourceId == pressureNetworkId)
    {
        sectionPressureNetworkId = sectionId;
        break;
    }
}
```

If `sectionNetworkId` is `ObjectId.Null`, the network is not sampled at this sample line — skip it.

## Creating Section Labels

Once you have a `sectionViewId` and `sectionNetworkId`, create labels for individual parts:

```csharp
// ── Gravity section labels ────────────────────────────────────────────────
// PipeSectionLabel.Create(sectionViewId, pipeId, sectionNetworkId, partIndex, styleId)
ObjectId pipeLabelId = PipeSectionLabel.Create(
    sectionViewId, pipeId, sectionPipeNetworkId, 0, pipeStyleId);

// StructureSectionLabel.Create(sectionViewId, structureId, sectionNetworkId, partIndex, styleId)
ObjectId structLabelId = StructureSectionLabel.Create(
    sectionViewId, structureId, sectionPipeNetworkId, 0, structureStyleId);

// ── Pressure section labels ───────────────────────────────────────────────
// All three share the same long signature
ObjectId pressurePipeLabelId = PressurePipeSectionLabel.Create(
    sectionViewId, pipeId, sectionPressureNetworkId,
    0 /* partIndex */, 0.5 /* ratio */, new Vector3d(1, 0, 0),
    labelStyleId, (DimensionAnchorOptionType)0, 0.0);

ObjectId fittingLabelId = PressureFittingSectionLabel.Create(
    sectionViewId, fittingId, sectionPressureNetworkId,
    0, 0.5, new Vector3d(1, 0, 0),
    labelStyleId, (DimensionAnchorOptionType)0, 0.0);

ObjectId appurtLabelId = PressureAppurtenanceSectionLabel.Create(
    sectionViewId, appurtId, sectionPressureNetworkId,
    0, 0.5, new Vector3d(1, 0, 0),
    labelStyleId, (DimensionAnchorOptionType)0, 0.0);
```

**Note:** If the part is not present in the section view, `Create()` throws `ArgumentException` — wrap in try/catch and treat as "not in this section".

## Detecting Existing Section Labels

Check before creating to avoid duplicates:

```csharp
// Gravity — takes sectionViewId only
ObjectIdCollection existingPipeLabels      = PipeSectionLabel.GetAvailableLabelIds(sectionViewId);
ObjectIdCollection existingStructureLabels = StructureSectionLabel.GetAvailableLabelIds(sectionViewId);

// Inspect each label's FeatureId to know which part it covers
foreach (ObjectId labelId in existingPipeLabels)
{
    PipeSectionLabel label = tr.GetObject(labelId, OpenMode.ForRead) as PipeSectionLabel;
    ObjectId featureId = label.FeatureId; // the pipe ObjectId
}

// Pressure — takes sectionViewId + partId + sectionNetworkId
// Returns label ids if part is in section; throws if part is not in section
ObjectIdCollection existingPressurePipe = PressurePipeSectionLabel.GetAvailableLabelIds(
    sectionViewId, pipeId, sectionPressureNetworkId);
```

## Label Style Selection for Section Views

```csharp
var labelStylesRoot = civilDoc.Styles.LabelStyles;

// Gravity pipe cross-section styles
var crossSectionStyles = labelStylesRoot.PipeLabelStyles.CrossSectionLabelStyles;
foreach (ObjectId styleId in crossSectionStyles) { /* pipe section styles */ }

// Gravity structure styles (same collection for all views)
var structStyles = labelStylesRoot.StructureLabelStyles.LabelStyles;

// Pressure pipe cross-section styles
var pressCrossSection = labelStylesRoot.GetPressurePipeLabelStyles().CrossingSectionLabelStyles;

// Pressure fitting and appurtenance styles (same collection for all views)
var fitStyles = labelStylesRoot.GetPressureFittingLabelStyles().LabelStyles;
var appStyles = labelStylesRoot.GetPressureAppurtenanceLabelStyles().LabelStyles;
```

## Discovering Which Networks Are Sampled in a Sample Line Group

Use this pattern to populate a "select network" list by scanning all sections:

```csharp
var sampledNetworkIds = new HashSet<ObjectId>();

foreach (ObjectId slId in slg.GetSampleLineIds())
{
    SampleLine sl = tr.GetObject(slId, OpenMode.ForRead) as SampleLine;
    if (sl == null) continue;

    foreach (ObjectId sectionId in sl.GetSectionIds())
    {
        Section section = tr.GetObject(sectionId, OpenMode.ForRead) as Section;

        // Gravity
        if (section is SectionPipeNetwork sn)
            sampledNetworkIds.Add(sn.SourceId);

        // Pressure
        if (section is SectionPressurePipeNetwork spn)
            sampledNetworkIds.Add(spn.SourceId);
    }
}
```

Then open each discovered `ObjectId` as `Network` (gravity) or `PressurePipeNetwork` (pressure).

## Gotchas

- `SampleLine.GetSectionIds()` returns one `Section` per sampled source — a section view may have multiple sections (surface, gravity network, pressure network, etc.)
- `SectionPipeNetwork.SourceId` links to the `Network`, not to the `SampleLine` or `SectionView`
- `PipeSectionLabel.Create()` throws `ArgumentException` (not returns Null) when a pipe has no crossing at that section view — always try/catch
- `PressurePipeSectionLabel.GetAvailableLabelIds()` also throws when the part is absent from the section — use the same try/catch pattern for detection
- Section label `partIndex` is 0-based; passing `0` works for single-crossing scenarios
- `sectionNetworkId` in label `Create()` is the `SectionPipeNetwork`/`SectionPressurePipeNetwork` ObjectId — NOT the model network ObjectId

## Related Skills

- `c3d-root-objects` - Accessing alignments through CivilDocument
- `c3d-pipe-networks` - Gravity and pressure pipe network part IDs used in section labels
- `c3d-label-styles` - Label style navigation for cross-section styles
- `c3d-alignments` - Alignment and profile view concepts
