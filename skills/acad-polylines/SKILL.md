---
name: acad-polylines
description: Polyline, Polyline2d, Polyline3d — vertices, bulges, area, type conversion
---

# AutoCAD Polylines

Use this skill when creating, reading, or modifying polylines — lightweight polylines (Polyline / LWPOLYLINE), 2D polylines (Polyline2d), 3D polylines (Polyline3d), vertex manipulation, bulge values, and curve extraction.

## Polyline (Lightweight / LWPOLYLINE)

### Creating a Polyline

```csharp
Polyline polyline = new Polyline();
polyline.Layer = layerName;

for (int i = 0; i < points.Count; i++)
{
    Point2d pt = points[i];
    double bulge = i < bulges.Count ? bulges[i] : 0.0;
    polyline.AddVertexAt(i, pt, bulge, 0.0, 0.0);
    // AddVertexAt(index, point, bulge, startWidth, endWidth)
}

polyline.ColorIndex = 256;  // ByLayer
// or: polyline.Color = Color.FromRgb(255, 0, 255);

BlockTableRecord ms = (BlockTableRecord)tr.GetObject(
    bt[BlockTableRecord.ModelSpace], OpenMode.ForWrite);
ms.AppendEntity(polyline);
tr.AddNewlyCreatedDBObject(polyline, true);
```

### Polyline Properties

- `NumberOfVertices` (int, get-only) — vertex count
- `Closed` (bool, get/set) — adds segment from last to first vertex (does not duplicate vertex)
- `Length` (double, get-only) — total length
- `Area` (double, get-only) — enclosed area (closed polylines only)
- `Normal` (Vector3d, get/set) — plane normal (typically ZAxis)
- `Elevation` (double, get/set) — Z value for all vertices (LWPOLYLINE is 2D; Z comes from this)
- `Thickness` (double, get/set) — extrusion thickness
- `ConstantWidth` (double, get/set) — uniform width (0 = no width)
- `Plinegen` (bool, get/set) — generate linetype across vertices
- `HasBulges` (bool, get-only) — any arc segments present
- `HasWidth` (bool, get-only) — any non-zero widths present
- `IsOnlyLines` (bool, get-only) — all segments are straight (no arcs)
- `Layer` (string, get/set) — layer name
- `Color` (Color, get/set) — entity color
- `ColorIndex` (int, get/set) — ACI color (256 = ByLayer, 0 = ByBlock)

### Reading Vertices

```csharp
Polyline pline = tr.GetObject(entityId, OpenMode.ForRead) as Polyline;

int count = pline.NumberOfVertices;
for (int i = 0; i < count; i++)
{
    Point2d pt = pline.GetPoint2dAt(i);      // 2D vertex in OCS
    Point3d pt3d = pline.GetPoint3dAt(i);    // 3D vertex (applies Elevation)
    double bulge = pline.GetBulgeAt(i);      // arc curvature to next vertex
    double startW = pline.GetStartWidthAt(i);
    double endW = pline.GetEndWidthAt(i);
}
```

### Modifying Vertices

```csharp
pline.UpgradeOpen();  // or open ForWrite initially

// Move a vertex
pline.SetPointAt(2, new Point2d(10.0, 20.0));

// Change arc curvature
pline.SetBulgeAt(2, 0.5);

// Change width at a vertex
pline.SetStartWidthAt(2, 0.0);
pline.SetEndWidthAt(2, 1.0);

// Insert a new vertex at index 3
pline.AddVertexAt(3, new Point2d(15.0, 25.0), 0.0, 0.0, 0.0);

// Remove vertex at index 3
pline.RemoveVertexAt(3);
```

## Bulge Values

The bulge value at vertex `i` defines the arc from vertex `i` to vertex `i+1`:

```
bulge = tan(includedAngle / 4)
```

| Bulge | Meaning |
|-------|---------|
| `0.0` | Straight segment |
| `> 0` | Counter-clockwise arc |
| `< 0` | Clockwise arc |
| `1.0` | Semicircle (180°) CCW |
| `-1.0` | Semicircle (180°) CW |
| `0.4142` | 90° arc CCW |
| `-0.4142` | 90° arc CW |

### Calculating Bulge

```csharp
// From included angle (radians)
double bulge = Math.Tan(includedAngle / 4.0);

// Back to angle
double angle = 4.0 * Math.Atan(Math.Abs(bulge));  // always positive
```

## Polyline as Curve

Polyline inherits from `Curve`. All Curve methods are available.

### Curve Methods

```csharp
// Point at a given distance along the curve
Point3d pt = pline.GetPointAtDist(50.0);

// Distance to a point on the curve
double dist = pline.GetDistAtPoint(pt);

// Closest point on curve to an arbitrary point
Point3d closest = pline.GetClosestPointTo(testPoint, false);
// second param: extend curve if needed

// Tangent direction at a point
Vector3d tangent = pline.GetFirstDerivative(pline.GetParameterAtPoint(pt));
```

### Curve Properties

- `StartPoint` (Point3d, get-only) — first vertex
- `EndPoint` (Point3d, get-only) — last vertex (or first if closed)
- `StartParam` (double, get-only) — start parameter (0.0)
- `EndParam` (double, get-only) — end parameter (NumberOfVertices for closed)
- `Area` (double, get-only) — enclosed area
- `Closed` (bool, get-only) — whether the curve is closed

### Offset and Split

```csharp
// Offset polyline by distance (positive = left, negative = right relative to direction)
DBObjectCollection offsets = pline.GetOffsetCurves(2.5);
foreach (DBObject obj in offsets)
{
    Entity offsetEnt = (Entity)obj;
    ms.AppendEntity(offsetEnt);
    tr.AddNewlyCreatedDBObject(offsetEnt, true);
}

// Split at a point
DBObjectCollection pieces = pline.GetSplitCurves(
    new Point3dCollection { splitPoint });

// Reverse direction
pline.ReverseCurve();
```

### Segment-Level Access

```csharp
for (int i = 0; i < pline.NumberOfVertices - 1; i++)
{
    SegmentType segType = pline.GetSegmentType(i);

    if (segType == SegmentType.Line)
    {
        LineSegment2d lineSeg = pline.GetLineSegment2dAt(i);
        double length = lineSeg.Length;
    }
    else if (segType == SegmentType.Arc)
    {
        CircularArc2d arcSeg = pline.GetArcSegment2dAt(i);
        double radius = arcSeg.Radius;
        Point2d center = arcSeg.Center;
    }
}
```

### SegmentType Enum

- `SegmentType.Line` — straight segment
- `SegmentType.Arc` — arc segment
- `SegmentType.Coincident` — zero-length segment (coincident vertices)
- `SegmentType.Point` — degenerate segment
- `SegmentType.Empty` — no segment

## Polyline2d (Heavy / DXF "POLYLINE")

Polyline2d vertices are separate database objects (`Vertex2d`) owned by the polyline.

### Creating Polyline2d

```csharp
Point3dCollection pts = new Point3dCollection
{
    new Point3d(0, 0, 0),
    new Point3d(10, 0, 0),
    new Point3d(10, 10, 0)
};

Polyline2d pline2d = new Polyline2d(Poly2dType.SimplePoly, pts, 0.0, false, 0.0, 0.0, null);
// (type, points, elevation, closed, defaultStartWidth, defaultEndWidth, bulges)

ms.AppendEntity(pline2d);
tr.AddNewlyCreatedDBObject(pline2d, true);
```

### Iterating Polyline2d Vertices

```csharp
Polyline2d pline2d = tr.GetObject(entityId, OpenMode.ForRead) as Polyline2d;

foreach (ObjectId vertexId in pline2d)
{
    Vertex2d vertex = tr.GetObject(vertexId, OpenMode.ForRead) as Vertex2d;
    if (vertex == null) continue;

    Point3d position = vertex.Position;
    double bulge = vertex.Bulge;
    double startWidth = vertex.StartWidth;
    double endWidth = vertex.EndWidth;
}
```

### Vertex2d Properties

- `Position` (Point3d, get/set) — vertex location
- `Bulge` (double, get/set) — arc to next vertex
- `StartWidth` (double, get/set) — width at start of segment
- `EndWidth` (double, get/set) — width at end of segment
- `Tangent` (double, get/set) — tangent direction (curve-fit)
- `VertexType` (Vertex2dType, get-only) — `SimplePoly`, `CurveFit`, `SplineFit`, etc.

### Polyline2d Properties

- `DefaultStartWidth` (double, get/set) — default start width
- `DefaultEndWidth` (double, get/set) — default end width
- `Closed` (bool, get/set)
- `Elevation` (double, get/set)
- `Normal` (Vector3d, get/set)
- `PolyType` (Poly2dType, get/set) — `SimplePoly`, `FitCurvePoly`, `CubicSplinePoly`, `QuadSplinePoly`

## Polyline3d

Polyline3d vertices are separate database objects (`PolylineVertex3d`) with full 3D coordinates.

### Creating Polyline3d

```csharp
Point3dCollection pts = new Point3dCollection
{
    new Point3d(0, 0, 0),
    new Point3d(10, 0, 5),
    new Point3d(20, 10, 10)
};

Polyline3d pline3d = new Polyline3d(Poly3dType.SimplePoly, pts, false);
ms.AppendEntity(pline3d);
tr.AddNewlyCreatedDBObject(pline3d, true);
```

### Iterating Polyline3d Vertices

```csharp
Polyline3d pline3d = tr.GetObject(entityId, OpenMode.ForRead) as Polyline3d;

foreach (ObjectId vertexId in pline3d)
{
    PolylineVertex3d vertex = tr.GetObject(vertexId, OpenMode.ForRead) as PolylineVertex3d;
    if (vertex == null) continue;

    Point3d position = vertex.Position;
}
```

### PolylineVertex3d Properties

- `Position` (Point3d, get/set) — 3D vertex location
- `VertexType` (Vertex3dType, get-only) — `SimplePoly`, `FitVertex`, `SplineControlPoint`, `SplineFitVertex`

### Polyline3d Properties

- `Closed` (bool, get/set)
- `Length` (double, get-only) — total 3D length
- `PolyType` (Poly3dType, get/set) — `SimplePoly`, `CubicSplinePoly`, `QuadSplinePoly`

## Handling All Polyline Types

When processing an entity that could be any polyline type, use a cascade pattern:

```csharp
private static List<Point3d> GetVertices(Entity entity, Transaction tr)
{
    List<Point3d> points = new List<Point3d>();

    Polyline pline = entity as Polyline;
    if (pline != null)
    {
        for (int i = 0; i < pline.NumberOfVertices; i++)
            points.Add(pline.GetPoint3dAt(i));
    }
    else
    {
        Polyline2d pline2d = entity as Polyline2d;
        if (pline2d != null)
        {
            foreach (ObjectId vId in pline2d)
            {
                Vertex2d v = tr.GetObject(vId, OpenMode.ForRead) as Vertex2d;
                if (v != null) points.Add(v.Position);
            }
        }
        else
        {
            Polyline3d pline3d = entity as Polyline3d;
            if (pline3d != null)
            {
                foreach (ObjectId vId in pline3d)
                {
                    PolylineVertex3d v = tr.GetObject(vId, OpenMode.ForRead) as PolylineVertex3d;
                    if (v != null) points.Add(v.Position);
                }
            }
        }
    }

    return points;
}
```

## Common Recipes

### Join Polylines

```csharp
// Join contiguous polylines into one (endpoints must be within tolerance)
pline.UpgradeOpen();
pline.JoinEntities(new Entity[] { otherPline1, otherPline2 });
```

### Reverse Direction

```csharp
pline.UpgradeOpen();
pline.ReverseCurve();
```

### Convert Polyline to Point Collection

```csharp
Point3dCollection points = new Point3dCollection();
for (int i = 0; i < pline.NumberOfVertices; i++)
    points.Add(pline.GetPoint3dAt(i));
```

### Spline Fit a Polyline2d

```csharp
pline2d.UpgradeOpen();
pline2d.ConvertToPolyType(Poly2dType.CubicSplinePoly);
// Also: QuadSplinePoly, FitCurvePoly
```

## Gotchas

- Polyline (LWPOLYLINE) stores **2D vertices only** — Z comes from the `Elevation` property
- Polyline vertices are in **OCS** (object coordinate system), not WCS — convert with `Matrix3d.WorldToPlane(Normal)` if the normal is not ZAxis
- `AddVertexAt` index must be 0 to `NumberOfVertices` inclusive — index = NumberOfVertices appends
- `RemoveVertexAt` on a polyline with only 2 vertices throws — erase the entity instead
- Polyline2d and Polyline3d vertices are **separate database objects** — must open each via transaction
- DXF name `"LWPOLYLINE"` = `Polyline` class; `"POLYLINE"` = `Polyline2d` **or** `Polyline3d` — check the managed type to distinguish
- `GetOffsetCurves` returns `DBObjectCollection` — results may not be Polyline (could be individual curves for complex offsets)
- `Area` only works on closed polylines in a plane — throws for non-planar 3D polylines
- Bulge at vertex `i` defines the arc **from** vertex `i` **to** vertex `i+1` (not centered on vertex i)
- `Closed = true` adds a segment from last to first vertex — does **not** duplicate the first point
- `JoinEntities` requires contiguous endpoints within `Application.DocumentManager.MdiActiveDocument.Database.EqualPoint` tolerance
- Polyline2d `foreach` yields ObjectIds of all sub-entities including fit/spline vertices — check `VertexType` to filter
- `ConvertToPolyType` on Polyline2d is destructive — original vertices become control/fit points

## Related Skills

- `acad-geometry` — Point2d/Point3d construction, bulge math, CircularArc2d from arc segments
- `acad-editor-input` — selecting polylines with GetEntity or selection filters (DxfCode.Start `"LWPOLYLINE"`)
- `acad-layers` — setting polyline layer, reading layer properties
- `acad-hatches` — polylines as hatch boundary loops (AppendLoop with entity IDs or vertex+bulge arrays)
