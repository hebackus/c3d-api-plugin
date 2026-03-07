---
name: acad-jigs
description: EntityJig, DrawJig, interactive entity placement, live preview dragging, Sampler, Update, WorldDraw, Editor.Drag, JigPromptOptions, multi-step jigs, cursor types
---

# AutoCAD Jigs

Use this skill when implementing interactive entity placement with live preview, drag-based input acquisition, or custom drawing feedback during user input in AutoCAD plugins.

## Overview

Jigs provide real-time visual feedback while the user moves the cursor. AutoCAD offers two jig base classes:

- **EntityJig** -- drives a single `Entity` that AutoCAD draws automatically each frame.
- **DrawJig** -- gives full control over what is drawn via `WorldDraw` / `ViewportDraw`, useful when previewing multiple entities or non-entity graphics.

Both follow the same loop: AutoCAD repeatedly calls `Sampler()` to read input, then `Update()` (EntityJig) or `WorldDraw()` (DrawJig) to refresh the preview, until the user accepts or cancels.

## EntityJig

Subclass `Autodesk.AutoCAD.EditorInput.EntityJig` and pass the entity to the base constructor. Override two methods:

```csharp
using Autodesk.AutoCAD.DatabaseServices;
using Autodesk.AutoCAD.EditorInput;
using Autodesk.AutoCAD.Geometry;

public class CircleJig : EntityJig
{
    private Point3d _center;
    private double _radius;

    public CircleJig(Circle circle)
        : base(circle)
    {
        _center = circle.Center;
        _radius = circle.Radius;
    }

    protected override SamplerStatus Sampler(JigPrompts prompts)
    {
        var opts = new JigPromptPointOptions("\nSpecify radius point: ")
        {
            BasePoint = _center,
            UseBasePoint = true,
            CursorType = CursorType.RubberBand
        };

        PromptPointResult result = prompts.AcquirePoint(opts);

        if (result.Status != PromptStatus.OK)
            return SamplerStatus.Cancel;

        double newRadius = _center.DistanceTo(result.Value);

        // Return NoChange when value hasn't moved -- prevents flicker
        if (Math.Abs(newRadius - _radius) < Tolerance.Global.EqualPoint)
            return SamplerStatus.NoChange;

        _radius = newRadius;
        return SamplerStatus.OK;
    }

    protected override bool Update()
    {
        ((Circle)Entity).Radius = _radius;
        return true;  // return false to abort the jig
    }
}
```

### Sampler()

`Sampler()` acquires one input value per call. Available acquisition methods on `JigPrompts`:

| Method | Returns | Use for |
|--------|---------|---------|
| `AcquirePoint(JigPromptPointOptions)` | `PromptPointResult` | Pick a point |
| `AcquireDistance(JigPromptDistanceOptions)` | `PromptDoubleResult` | Drag a distance |
| `AcquireAngle(JigPromptAngleOptions)` | `PromptDoubleResult` | Drag an angle |
| `AcquireString(JigPromptStringOptions)` | `PromptStringResult` | Type a string |

**Critical:** Always compare the new value against the previous value and return `SamplerStatus.NoChange` when they are equal. Omitting this check causes display flicker because AutoCAD redraws every frame even when nothing changed.

### SamplerStatus Enum

| Value | Meaning |
|-------|---------|
| `OK` | New value acquired -- call `Update()` and redraw |
| `NoChange` | Value unchanged -- skip redraw (prevents flicker) |
| `Cancel` | User pressed Escape or right-clicked -- end jig |

### Update()

`Update()` applies the sampled values to the entity. Return `true` to continue, `false` to abort. AutoCAD draws the entity automatically after `Update()` returns `true`.

### Running an EntityJig

```csharp
public void RunCircleJig()
{
    var doc = Application.DocumentManager.MdiActiveDocument;
    var db = doc.Database;
    var ed = doc.Editor;

    var circle = new Circle(Point3d.Origin, Vector3d.ZAxis, 1.0);
    var jig = new CircleJig(circle);

    PromptResult result = ed.Drag(jig);

    if (result.Status != PromptStatus.OK)
        return;

    using (var tr = db.TransactionManager.StartTransaction())
    {
        var btr = (BlockTableRecord)tr.GetObject(
            db.CurrentSpaceId, OpenMode.ForWrite);
        btr.AppendEntity(circle);
        tr.AddNewlyCreatedDBObject(circle, true);
        tr.Commit();
    }
}
```

## DrawJig

Subclass `Autodesk.AutoCAD.EditorInput.DrawJig` when you need to draw custom graphics or preview multiple entities. Override `Sampler()` and `WorldDraw()`.

```csharp
using Autodesk.AutoCAD.EditorInput;
using Autodesk.AutoCAD.Geometry;
using Autodesk.AutoCAD.GraphicsInterface;

public class CrosshairJig : DrawJig
{
    private Point3d _point;
    private readonly double _size;

    public CrosshairJig(double size)
    {
        _size = size;
        _point = Point3d.Origin;
    }

    public Point3d PickedPoint => _point;

    protected override SamplerStatus Sampler(JigPrompts prompts)
    {
        var opts = new JigPromptPointOptions("\nSpecify point: ")
        {
            CursorType = CursorType.Crosshair
        };

        PromptPointResult result = prompts.AcquirePoint(opts);

        if (result.Status != PromptStatus.OK)
            return SamplerStatus.Cancel;

        if (result.Value.IsEqualTo(_point))
            return SamplerStatus.NoChange;

        _point = result.Value;
        return SamplerStatus.OK;
    }

    protected override bool WorldDraw(WorldDraw draw)
    {
        // Draw a crosshair at the cursor position
        var geo = draw.Geometry;

        geo.WorldLine(
            new Point3d(_point.X - _size, _point.Y, _point.Z),
            new Point3d(_point.X + _size, _point.Y, _point.Z));

        geo.WorldLine(
            new Point3d(_point.X, _point.Y - _size, _point.Z),
            new Point3d(_point.X, _point.Y + _size, _point.Z));

        return true;  // return true = handled; false = let AutoCAD draw defaults
    }
}
```

### WorldDraw vs ViewportDraw

- `WorldDraw()` draws in world coordinates, visible in all viewports. Return `true` if drawing is complete, `false` to also invoke `ViewportDraw()`.
- `ViewportDraw()` draws per-viewport. Override it for viewport-specific graphics (rare in jig usage).

### WorldGeometry Drawing Methods

Common methods available on `WorldDraw.Geometry`:

| Method | Description |
|--------|-------------|
| `WorldLine(Point3d from, Point3d to)` | Draw a line segment |
| `Polyline(Point3dCollection, Vector3d, IntPtr)` | Draw a polyline |
| `Circle(Point3d center, double radius, Vector3d normal)` | Draw a circle |
| `Text(...)` | Draw text |
| `Draw(Drawable)` | Draw an existing entity |

### Running a DrawJig

```csharp
var jig = new CrosshairJig(5.0);
PromptResult result = ed.Drag(jig);

if (result.Status == PromptStatus.OK)
{
    Point3d picked = jig.PickedPoint;
    // Use the picked point
}
```

## Editor.Drag()

`Editor.Drag(Jig)` starts the jig loop and blocks until the user completes or cancels. Returns a `PromptResult` whose `Status` property indicates the outcome.

### DragStatus Enum

The `PromptResult.Status` returned by `Drag()` maps to standard `PromptStatus` values:

| Value | Meaning |
|-------|---------|
| `PromptStatus.OK` | User accepted (clicked or pressed Enter) |
| `PromptStatus.Cancel` | User cancelled (Escape or right-click) |
| `PromptStatus.Keyword` | User entered a keyword |
| `PromptStatus.None` | No input / empty response |

## Prompt Options

### JigPromptPointOptions

```csharp
var opts = new JigPromptPointOptions("\nSpecify insertion point: ");
opts.UseBasePoint = true;
opts.BasePoint = new Point3d(0, 0, 0);
opts.CursorType = CursorType.RubberBand;
opts.UserInputControls =
    UserInputControls.Accept3dCoordinates |
    UserInputControls.NullResponseAccepted;
opts.Keywords.Add("Rotate");
opts.Keywords.Add("Scale");
```

### JigPromptDistanceOptions

```csharp
var opts = new JigPromptDistanceOptions("\nSpecify offset distance: ");
opts.BasePoint = _center;
opts.UseBasePoint = true;
opts.DefaultValue = 10.0;
```

### JigPromptAngleOptions

```csharp
var opts = new JigPromptAngleOptions("\nSpecify rotation angle: ");
opts.BasePoint = _insertionPoint;
opts.UseBasePoint = true;
opts.DefaultValue = 0.0;
```

## Cursor Types

Set via `JigPromptPointOptions.CursorType`:

| CursorType | Appearance |
|------------|------------|
| `Crosshair` | Standard crosshair (default) |
| `RubberBand` | Line from `BasePoint` to cursor |
| `EntitySelect` | Pick box for entity selection |
| `Invisible` | Hidden cursor |

`RubberBand` requires `UseBasePoint = true` and a valid `BasePoint`.

## Multi-Step Jigs

For entities that need multiple inputs (e.g., pick insertion point, then set rotation), track the current step and branch in `Sampler()` / `Update()`.

### Block Insertion Jig (Position + Rotation)

```csharp
public class BlockInsertJig : EntityJig
{
    private Point3d _position;
    private double _rotation;
    private int _step;  // 0 = position, 1 = rotation

    public BlockInsertJig(BlockReference blockRef)
        : base(blockRef)
    {
        _position = blockRef.Position;
        _rotation = blockRef.Rotation;
        _step = 0;
    }

    public int Step
    {
        get => _step;
        set => _step = value;
    }

    protected override SamplerStatus Sampler(JigPrompts prompts)
    {
        switch (_step)
        {
            case 0:
                return SamplePosition(prompts);
            case 1:
                return SampleRotation(prompts);
            default:
                return SamplerStatus.Cancel;
        }
    }

    private SamplerStatus SamplePosition(JigPrompts prompts)
    {
        var opts = new JigPromptPointOptions("\nSpecify insertion point: ")
        {
            CursorType = CursorType.Crosshair
        };

        PromptPointResult result = prompts.AcquirePoint(opts);
        if (result.Status != PromptStatus.OK)
            return SamplerStatus.Cancel;

        if (result.Value.IsEqualTo(_position))
            return SamplerStatus.NoChange;

        _position = result.Value;
        return SamplerStatus.OK;
    }

    private SamplerStatus SampleRotation(JigPrompts prompts)
    {
        var opts = new JigPromptAngleOptions("\nSpecify rotation angle: ")
        {
            BasePoint = _position,
            UseBasePoint = true,
            DefaultValue = 0.0
        };

        PromptDoubleResult result = prompts.AcquireAngle(opts);
        if (result.Status != PromptStatus.OK)
            return SamplerStatus.Cancel;

        if (Math.Abs(result.Value - _rotation) < Tolerance.Global.EqualPoint)
            return SamplerStatus.NoChange;

        _rotation = result.Value;
        return SamplerStatus.OK;
    }

    protected override bool Update()
    {
        var blockRef = (BlockReference)Entity;

        switch (_step)
        {
            case 0:
                blockRef.Position = _position;
                break;
            case 1:
                blockRef.Rotation = _rotation;
                break;
        }

        return true;
    }
}
```

### Running a Multi-Step Jig

Call `Editor.Drag()` once per step, advancing the step counter between calls:

```csharp
public static void InsertBlockWithJig(
    Database db, Editor ed, ObjectId blockDefId)
{
    using (var tr = db.TransactionManager.StartTransaction())
    {
        var btr = (BlockTableRecord)tr.GetObject(
            db.CurrentSpaceId, OpenMode.ForWrite);

        var blockRef = new BlockReference(Point3d.Origin, blockDefId);
        var jig = new BlockInsertJig(blockRef);

        // Step 0: pick position
        jig.Step = 0;
        PromptResult res = ed.Drag(jig);
        if (res.Status != PromptStatus.OK)
            return;

        // Step 1: pick rotation
        jig.Step = 1;
        res = ed.Drag(jig);
        if (res.Status != PromptStatus.OK)
            return;

        // Commit the entity
        btr.AppendEntity(blockRef);
        tr.AddNewlyCreatedDBObject(blockRef, true);
        tr.Commit();
    }
}
```

## Common Patterns

### Line Jig (Start + End)

```csharp
public class LineJig : EntityJig
{
    private Point3d _startPoint;
    private Point3d _endPoint;

    public LineJig(Line line, Point3d startPoint)
        : base(line)
    {
        _startPoint = startPoint;
        _endPoint = startPoint;
    }

    protected override SamplerStatus Sampler(JigPrompts prompts)
    {
        var opts = new JigPromptPointOptions("\nSpecify end point: ")
        {
            BasePoint = _startPoint,
            UseBasePoint = true,
            CursorType = CursorType.RubberBand
        };

        PromptPointResult result = prompts.AcquirePoint(opts);
        if (result.Status != PromptStatus.OK)
            return SamplerStatus.Cancel;

        if (result.Value.IsEqualTo(_endPoint))
            return SamplerStatus.NoChange;

        _endPoint = result.Value;
        return SamplerStatus.OK;
    }

    protected override bool Update()
    {
        var line = (Line)Entity;
        line.StartPoint = _startPoint;
        line.EndPoint = _endPoint;
        return true;
    }
}
```

### Move Jig (Displace Existing Entity)

```csharp
public class MoveJig : EntityJig
{
    private Point3d _basePoint;
    private Point3d _currentPoint;
    private Matrix3d _lastTransform;

    public MoveJig(Entity entity, Point3d basePoint)
        : base(entity)
    {
        _basePoint = basePoint;
        _currentPoint = basePoint;
        _lastTransform = Matrix3d.Identity;
    }

    protected override SamplerStatus Sampler(JigPrompts prompts)
    {
        var opts = new JigPromptPointOptions("\nSpecify destination point: ")
        {
            BasePoint = _basePoint,
            UseBasePoint = true,
            CursorType = CursorType.RubberBand
        };

        PromptPointResult result = prompts.AcquirePoint(opts);
        if (result.Status != PromptStatus.OK)
            return SamplerStatus.Cancel;

        if (result.Value.IsEqualTo(_currentPoint))
            return SamplerStatus.NoChange;

        _currentPoint = result.Value;
        return SamplerStatus.OK;
    }

    protected override bool Update()
    {
        // Undo previous transform, apply new one
        Entity.TransformBy(_lastTransform.Inverse());

        Vector3d displacement = _currentPoint - _basePoint;
        _lastTransform = Matrix3d.Displacement(displacement);
        Entity.TransformBy(_lastTransform);

        return true;
    }
}
```

### DrawJig for Multiple Entities

```csharp
public class RectangleJig : DrawJig
{
    private Point3d _corner1;
    private Point3d _corner2;

    public RectangleJig(Point3d firstCorner)
    {
        _corner1 = firstCorner;
        _corner2 = firstCorner;
    }

    public Point3d Corner1 => _corner1;
    public Point3d Corner2 => _corner2;

    protected override SamplerStatus Sampler(JigPrompts prompts)
    {
        var opts = new JigPromptPointOptions("\nSpecify opposite corner: ")
        {
            BasePoint = _corner1,
            UseBasePoint = true,
            CursorType = CursorType.RubberBand
        };

        PromptPointResult result = prompts.AcquirePoint(opts);
        if (result.Status != PromptStatus.OK)
            return SamplerStatus.Cancel;

        if (result.Value.IsEqualTo(_corner2))
            return SamplerStatus.NoChange;

        _corner2 = result.Value;
        return SamplerStatus.OK;
    }

    protected override bool WorldDraw(WorldDraw draw)
    {
        var pts = new Point3dCollection
        {
            _corner1,
            new Point3d(_corner2.X, _corner1.Y, 0),
            _corner2,
            new Point3d(_corner1.X, _corner2.Y, 0),
            _corner1  // close the rectangle
        };

        draw.Geometry.Polyline(pts, Vector3d.ZAxis, IntPtr.Zero);
        return true;
    }
}
```

## Gotchas

- **Always check for NoChange in Sampler.** Returning `SamplerStatus.OK` every frame causes display flicker because AutoCAD redraws even when the entity has not moved. Compare new values against previous values and return `NoChange` when equal.
- **Entity must not be database-resident during jig.** The entity passed to `EntityJig` must be a transient (non-added) entity. Add it to the database only after `Drag()` returns `PromptStatus.OK`.
- **Update() must not throw.** If `Update()` throws an exception, the jig terminates and the entity is left in an inconsistent state. Validate values before applying.
- **MoveJig requires transform reversal.** When displacing an entity, undo the previous transform before applying the new one, or the displacements accumulate incorrectly.
- **Point comparison uses IsEqualTo, not ==.** `Point3d` is a struct; use `IsEqualTo()` or `DistanceTo() < tolerance` for reliable equality checks in `Sampler()`.
- **AcquireAngle returns radians.** The angle value from `AcquireAngle` is in radians, not degrees. Use it directly with `Rotation` properties (which also expect radians).
- **Keyword handling in jigs.** Check `PromptResult.Status == PromptStatus.Keyword` and read `PromptResult.StringResult` to get the keyword. Return `SamplerStatus.OK` to keep the jig alive after processing a keyword.
- **DrawJig WorldDraw must be fast.** This method is called every frame at cursor-move frequency. Avoid allocations, database reads, or expensive geometry calculations inside `WorldDraw()`.
- **No transactions inside jig methods.** Do not open transactions in `Sampler()`, `Update()`, or `WorldDraw()`. These run in a tight loop and transactions will severely degrade performance or cause errors.
- **Jig entities are not cloned.** The entity you pass to the jig constructor is the same object that gets added to the database after the jig completes. Do not dispose it between `Drag()` and `AppendEntity()`.

## Related Skills

- `acad-editor-input` -- prompt options, keyword handling, and input acquisition outside of jigs
- `acad-geometry` -- Point3d, Vector3d, Matrix3d, and transformation math used in jig calculations
- `acad-blocks` -- BlockReference creation and attribute handling for block insertion jigs
- `acad-polylines` -- polyline construction techniques used with DrawJig preview rendering
