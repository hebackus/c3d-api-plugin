---
name: acad-mleaders
description: Multileaders - creation, leader lines and vertices, MText and Block content, dogleg/landing settings, MLeaderStyle configuration
---

# AutoCAD Multileaders (MLeader)

Use this skill when creating or modifying multileader objects - leaders with text, block, or tolerance content.

## MLeader Structure

```
MLeader
├── Leader 0
│   ├── LeaderLine 0 (vertices: first → ... → last/arrow)
│   └── LeaderLine 1
├── Leader 1
│   └── LeaderLine 0
└── Content (MText, Block, or Tolerance - shared across all leaders)
```

An MLeader contains one or more **Leaders** (collections of leader lines pointing to the same content side). Each Leader contains one or more **LeaderLines**, each with multiple **Vertices**. The **first vertex** is the landing/connection point near content; the **last vertex** is the arrow tip.

## Creating an MLeader with MText Content

```csharp
using (Transaction tr = db.TransactionManager.StartTransaction())
{
    BlockTableRecord btr = (BlockTableRecord)tr.GetObject(
        db.CurrentSpaceId, OpenMode.ForWrite);

    MLeader mleader = new MLeader();
    mleader.SetDatabaseDefaults();

    // Set content type
    mleader.ContentType = ContentType.MTextContent;

    // Create MText content
    MText mt = new MText();
    mt.Contents = "Label Text";
    mt.TextHeight = 2.5;
    mleader.MText = mt;

    // Add a leader with one leader line
    int leaderIdx = mleader.AddLeader();
    int lineIdx = mleader.AddLeaderLine(leaderIdx);

    // Add vertices (last = arrow tip, first = near content)
    mleader.AddFirstVertex(lineIdx, new Point3d(200, 200, 0));
    mleader.AddLastVertex(lineIdx, new Point3d(100, 100, 0));

    // Set text location
    mleader.TextLocation = new Point3d(210, 200, 0);

    btr.AppendEntity(mleader);
    tr.AddNewlyCreatedDBObject(mleader, true);
    tr.Commit();
}
```

## Creating an MLeader with Block Content

```csharp
MLeader mleader = new MLeader();
mleader.SetDatabaseDefaults();
mleader.ContentType = ContentType.BlockContent;
mleader.BlockContentId = blockDefId;  // ObjectId of BlockTableRecord
mleader.BlockPosition = new Point3d(200, 200, 0);
mleader.BlockScale = new Scale3d(1.0);
mleader.BlockRotation = 0.0;
mleader.BlockColor = Color.FromColorIndex(ColorMethod.ByLayer, 256);
mleader.BlockConnectionType = BlockConnectionType.ConnectExtents;
// or BlockConnectionType.ConnectBase

int leaderIdx = mleader.AddLeader();
int lineIdx = mleader.AddLeaderLine(leaderIdx);
mleader.AddFirstVertex(lineIdx, new Point3d(200, 200, 0));
mleader.AddLastVertex(lineIdx, new Point3d(100, 100, 0));
```

## MLeader Properties

**Content properties:**
- `ContentType` (ContentType, get/set) - NoneContent=0, BlockContent=1, MTextContent=2, ToleranceContent=3
- `MText` (MText, get/set) - the MText content object
- `TextLocation` (Point3d, get/set) - text position
- `TextHeight` (double, get/set)
- `TextColor` (Color, get/set)
- `TextStyleId` (ObjectId, get/set)
- `TextAlignmentType` (TextAlignmentType, get/set) - LeftAlignment=0, CenterAlignment=1, RightAlignment=2
- `TextAngleType` (TextAngleType, get/set) - InsertAngle=0, HorizontalAngle=1, AlwaysRightReadingAngle=2
- `TextAttachmentType` (TextAttachmentType, get/set) - see enum below
- `TextAttachmentDirection` (TextAttachmentDirection, get/set) - AttachmentHorizontal=0, AttachmentVertical=1
- `EnableFrameText` (bool, get/set)
- `EnableAnnotationScale` (bool, get/set)

**Block properties:**
- `BlockContentId` (ObjectId, get/set)
- `BlockPosition` (Point3d, get/set)
- `BlockConnectionType` (BlockConnectionType, get/set) - ConnectExtents=0, ConnectBase=1
- `BlockRotation` (double, get/set)
- `BlockScale` (Scale3d, get/set)
- `BlockColor` (Color, get/set)

**Leader line appearance:**
- `LeaderLineType` (LeaderType, get/set) - InVisibleLeader=0, StraightLeader=1, SplineLeader=2
- `LeaderLineColor` (Color, get/set)
- `LeaderLineTypeId` (ObjectId, get/set) - linetype
- `LeaderLineWeight` (LineWeight, get/set)
- `ArrowSymbolId` (ObjectId, get/set) - arrow block
- `ArrowSize` (double, get/set)

**Leader configuration:**
- `EnableDogleg` (bool, get/set)
- `DoglegLength` (double, get/set)
- `EnableLanding` (bool, get/set)
- `LandingGap` (double, get/set)
- `ExtendLeaderToText` (bool, get/set)

**Counts (read-only):**
- `LeaderCount` (int, get)
- `LeaderLineCount` (int, get)

**Other:**
- `MLeaderStyle` (ObjectId, get/set)
- `Scale` (double, get/set)
- `Normal` (Vector3d, get)

## Leader and LeaderLine Management

```csharp
// Add leaders and lines
int leaderIdx = mleader.AddLeader();
int lineIdx = mleader.AddLeaderLine(leaderIdx);
// or: int lineIdx = mleader.AddLeaderLine(new Point3d(x, y, z)); // adds to default leader

// Get all leader/line indexes
ArrayList leaderIndexes = mleader.GetLeaderIndexes();
ArrayList lineIndexes = mleader.GetLeaderLineIndexes(leaderIdx);

// Get parent leader of a line
int parentLeader = mleader.GetLeaderIndex(lineIdx);

// Remove
mleader.RemoveLeaderLine(lineIdx);
mleader.RemoveLeader(leaderIdx);
```

## Vertex Management

```csharp
// Add vertices
mleader.AddFirstVertex(lineIdx, connectionPoint);  // near content
mleader.AddLastVertex(lineIdx, arrowPoint);         // arrow tip

// Get/set vertices
Point3d first = mleader.GetFirstVertex(lineIdx);
Point3d last = mleader.GetLastVertex(lineIdx);
mleader.SetFirstVertex(lineIdx, newPoint);
mleader.SetLastVertex(lineIdx, newPoint);

// Middle vertices
int count = mleader.VerticesCount(lineIdx);
Point3d pt = mleader.GetVertex(lineIdx, 1);  // 0-indexed
mleader.SetVertex(lineIdx, 1, newPoint);

// Remove vertices
mleader.RemoveFirstVertex(lineIdx);
mleader.RemoveLastVertex(lineIdx);
```

## Per-Leader and Per-Line Overrides

```csharp
// Dogleg per leader
mleader.SetDogleg(leaderIdx, new Vector3d(1, 0, 0));
Vector3d dogDir = mleader.GetDogleg(leaderIdx);
mleader.SetDoglegLength(leaderIdx, 5.0);
double dogLen = mleader.GetDoglegLength(leaderIdx);

// Per-line leader appearance overrides
mleader.SetLeaderLineType(lineIdx, LeaderType.SplineLeader);
mleader.SetLeaderLineColor(lineIdx, Color.FromColorIndex(ColorMethod.ByAci, 1));
mleader.SetLeaderLineWeight(lineIdx, LineWeight.LineWeight050);
mleader.SetArrowSymbolId(lineIdx, arrowBlockId);
mleader.SetArrowSize(lineIdx, 3.0);

// Read overrides
LeaderType lt = mleader.GetLeaderLineType(lineIdx);
Color lc = mleader.GetLeaderLineColor(lineIdx);
```

## Text Attachment (per direction)

```csharp
// Set attachment type for specific leader direction
mleader.SetTextAttachmentType(
    TextAttachmentType.AttachmentMiddle,
    LeaderDirectionType.LeftLeader);

TextAttachmentType att = mleader.GetTextAttachmentType(
    LeaderDirectionType.RightLeader);
```

## Block Attributes

```csharp
// Read/write attributes on block content
AttributeReference attRef = mleader.GetBlockAttribute(attDefId);
string val = attRef.TextString;

attRef.TextString = "New Value";
mleader.SetBlockAttribute(attDefId, attRef);
```

## Movement

```csharp
// Move entire MLeader
mleader.MoveMLeader(new Vector3d(50, 50, 0), MoveType.MoveAllPoints);
```

**MoveType enum:** MoveAllPoints=0, MoveAllExceptArrowHeaderPoints=1, MoveContentAndDoglegPoints=2

## Other Methods

- `GetContentGeomExtents()` → `Extents3d` - bounding box of content
- `ConnectionPoint(Vector3d direction)` → `Point3d` - calculate connection point
- `ConnectionPoint(Vector3d direction, TextAttachmentDirection)` → `Point3d`
- `HasContent()` → bool
- `PostMLeaderToDb(Database db)` - post to database

## MLeaderStyle

```csharp
// Create a new style
MLeaderStyle style = new MLeaderStyle();
// or copy: new MLeaderStyle(existingStyle);

style.Name = "My Leader Style";
style.ContentType = ContentType.MTextContent;
style.TextHeight = 2.5;
style.TextStyleId = textStyleId;
style.TextColor = Color.FromColorIndex(ColorMethod.ByLayer, 256);
style.TextAlignmentType = TextAlignmentType.LeftAlignment;
style.TextAlignAlwaysLeft = false;
style.TextAngleType = TextAngleType.HorizontalAngle;
style.EnableFrameText = false;

// Leader line settings
style.LeaderLineType = LeaderType.StraightLeader;
style.LeaderLineColor = Color.FromColorIndex(ColorMethod.ByBlock, 0);
style.ArrowSymbolId = ObjectId.Null;  // default arrow
style.ArrowSize = 3.0;
style.EnableDogleg = true;
style.DoglegLength = 8.0;
style.EnableLanding = true;
style.LandingGap = 2.0;
style.ExtendLeaderToText = true;

// Block content defaults
style.BlockId = blockId;
style.BlockConnectionType = BlockConnectionType.ConnectExtents;
style.BlockScale = new Scale3d(1.0);
style.EnableBlockScale = false;
style.EnableBlockRotation = false;

// Workflow
style.Scale = 1.0;
style.BreakSize = 2.0;
style.MaxLeaderSegmentsPoints = 2;
style.FirstSegmentAngleConstraint = AngleConstraint.DegreesAny;
style.SecondSegmentAngleConstraint = AngleConstraint.DegreesAny;
style.DrawLeaderOrderType = DrawLeaderOrderType.DrawLeaderHeadFirst;
style.DrawMLeaderOrderType = DrawMLeaderOrderType.DrawContentFirst;

// Text attachment per direction
style.SetTextAttachmentType(
    TextAttachmentType.AttachmentMiddleOfTop, LeaderDirectionType.LeftLeader);
style.SetTextAttachmentType(
    TextAttachmentType.AttachmentMiddleOfTop, LeaderDirectionType.RightLeader);
style.TextAttachmentDirection = TextAttachmentDirection.AttachmentHorizontal;

// Post to database
ObjectId styleId = style.PostMLeaderStyleToDb(db, "My Leader Style");
tr.AddNewlyCreatedDBObject(style, true);
```

**MLeaderStyle properties** mirror MLeader properties and serve as defaults. Notable additions:
- `Name` (string, get/set)
- `TextAlignAlwaysLeft` (bool, get/set)
- `DefaultMText` (MText, get/set) - template MText
- `EnableBlockScale` (bool, get/set)
- `EnableBlockRotation` (bool, get/set)
- `BreakSize` (double, get/set)
- `MaxLeaderSegmentsPoints` (int, get/set)
- `FirstSegmentAngleConstraint` / `SecondSegmentAngleConstraint` (AngleConstraint, get/set)
- `DrawLeaderOrderType` (DrawLeaderOrderType, get/set)
- `DrawMLeaderOrderType` (DrawMLeaderOrderType, get/set)

## Enums

**TextAttachmentType:** AttachmentTopOfTop=0, AttachmentMiddleOfTop=1, AttachmentMiddle=2, AttachmentMiddleOfBottom=3, AttachmentBottomOfBottom=4, AttachmentBottomLine=5, AttachmentBottomOfTopLine=6, AttachmentBottomOfTop=7, AttachmentAllLine=8, AttachmentCenter=9, AttachmentLinedCenter=10

**LeaderDirectionType:** UnknownLeader=0, LeftLeader=1, RightLeader=2, TopLeader=3, BottomLeader=4

**AngleConstraint:** DegreesAny=0, Degrees015=1, Degrees030=2, Degrees045=3, Degrees060=4, Degrees090=6, DegreesHorz=12

**DrawLeaderOrderType:** DrawLeaderHeadFirst=0, DrawLeaderTailFirst=1

**DrawMLeaderOrderType:** DrawContentFirst=0, DrawLeaderFirst=1

## Legacy Leader Class

The OARX guide documents the older `Leader` class (not `MLeader`). Prefer `MLeader` for new code. Use `Leader` only when working with legacy drawings that contain it.

```csharp
using (Transaction tr = db.TransactionManager.StartTransaction())
{
    BlockTableRecord btr = (BlockTableRecord)tr.GetObject(
        db.CurrentSpaceId, OpenMode.ForWrite);

    Leader leader = new Leader();
    leader.SetDatabaseDefaults();

    // Add vertices (start at arrow tip, end at annotation)
    leader.AppendVertex(new Point3d(100, 100, 0));  // arrow tip
    leader.AppendVertex(new Point3d(200, 150, 0));  // elbow
    leader.AppendVertex(new Point3d(250, 150, 0));  // near annotation

    leader.HasArrowHead = true;
    leader.IsSplined = false;

    btr.AppendEntity(leader);
    tr.AddNewlyCreatedDBObject(leader, true);

    // Attach annotation (must be added to DB first)
    MText mt = new MText();
    mt.Location = new Point3d(252, 150, 0);
    mt.Contents = "Leader Text";
    mt.TextHeight = 2.5;
    btr.AppendEntity(mt);
    tr.AddNewlyCreatedDBObject(mt, true);

    leader.Annotation = mt.ObjectId;  // attach annotation
    leader.EvaluateLeader();          // MUST call to update hook geometry

    tr.Commit();
}
```

**Leader properties:**
- `HasArrowHead` (bool, get/set)
- `IsSplined` (bool, get/set) - spline leader
- `Annotation` (ObjectId, get/set) - attached annotation object
- `AnnoType` (LeaderAnnoType, get-only) - None=0, MText=1, BlockReference=2, Tolerance=3
- `AnnoOffset` (Vector3d, get/set) - annotation offset
- `AnnoHeight` / `AnnoWidth` (double, get-only) - annotation size
- `Normal` (Vector3d, get/set)
- `NumVertices` (int, get-only)

**Leader methods:**
- `AppendVertex(Point3d)` - add vertex
- `RemoveLastVertex()` - remove last vertex
- `VertexAt(int index)` → `Point3d`
- `EvaluateLeader()` - recalculate hook line geometry (**required** after setting Annotation)

## Gotchas

- Leader/line indexes are NOT sequential integers - always use `GetLeaderIndexes()` and `GetLeaderLineIndexes()` to get valid indexes
- First vertex = connection point near content; Last vertex = arrow tip (opposite of what you might expect)
- `AddLeaderLine(Point3d)` adds a line to a default leader; `AddLeaderLine(int leaderIndex)` adds to a specific leader - different signatures do different things
- Setting `MText` property replaces the content object entirely; modify the existing `MText` object for incremental changes
- Per-line overrides (color, weight, arrow) only take effect if they differ from the MLeader's default properties
- `MLeaderStyle` must be posted to the database with `PostMLeaderStyleToDb()` before it can be assigned to an MLeader
- `MoveType.MoveAllExceptArrowHeaderPoints` keeps arrow tips fixed while moving content - useful for repositioning text without changing what the leader points to
- `TextAttachmentType` and direction interact: horizontal leaders use top/middle/bottom attachment; vertical leaders use center/lined attachment
