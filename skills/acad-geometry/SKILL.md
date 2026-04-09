---
name: acad-geometry
description: Points, vectors, matrices, curves, planes — transforms, intersections, recipes
---

# AutoCAD Geometry (Autodesk.AutoCAD.Geometry)

Use this skill when working with geometric primitives - points, vectors, matrices, lines, arcs, curves, planes, and bounding boxes. These types are used throughout both AutoCAD and Civil 3D APIs.

## Points

### Point2d (struct)

```csharp
Point2d p1 = new Point2d(100.0, 200.0);
Point2d p2 = new Point2d(300.0, 400.0);
double dist = p1.GetDistanceTo(p2);
Vector2d dir = p1.GetVectorTo(p2);
Point2d mid = p1 + dir * 0.5;   // midpoint via vector math
Point2d rotated = p1.RotateBy(Math.PI / 4, Point2d.Origin);
```

### Point3d (struct)

```csharp
Point3d p1 = new Point3d(100.0, 200.0, 0.0);
Point3d p2 = new Point3d(300.0, 400.0, 0.0);
double dist = p1.DistanceTo(p2);    // Note: DistanceTo, not GetDistanceTo
Vector3d dir = p1.GetVectorTo(p2).GetNormal();
Point3d rotated = p1.RotateBy(Math.PI / 2, Vector3d.ZAxis, Point3d.Origin);
Point2d flat = p1.Convert2d(new Plane());  // project to XY plane
```

## Vectors

### Vector2d / Vector3d (structs)

```csharp
Vector3d v1 = new Vector3d(1.0, 0.0, 0.0);
Vector3d v2 = new Vector3d(0.0, 1.0, 0.0);
double angle = v1.GetAngleTo(v2);           // pi/2
Vector3d cross = v1.CrossProduct(v2);        // (0, 0, 1)
double dot = v1.DotProduct(v2);              // 0.0
Vector3d unit = new Vector3d(3, 4, 0).GetNormal();  // (0.6, 0.8, 0)
Vector3d perp = v1.GetPerpendicularVector(); // perpendicular in arbitrary direction
bool parallel = v1.IsParallelTo(v2);         // false
```

## Transformations

### Matrix3d / Matrix2d (structs)

```csharp
// Rotate entity 45 degrees around a point
Point3d center = new Point3d(100, 100, 0);
Matrix3d rot = Matrix3d.Rotation(Math.PI / 4, Vector3d.ZAxis, center);
entity.TransformBy(rot);

// Mirror across a line (defined by two points)
Line3d mirrorLine = new Line3d(new Point3d(0, 0, 0), new Point3d(1, 1, 0));
Matrix3d mir = Matrix3d.Mirroring(mirrorLine);

// Scale from base point
Matrix3d scl = Matrix3d.Scaling(2.0, new Point3d(0, 0, 0));

// Compose transforms (apply scaling THEN rotation)
Matrix3d combined = rot * scl;  // right-to-left order
entity.TransformBy(combined);

// Move entity by displacement
Matrix3d move = Matrix3d.Displacement(new Vector3d(50, 100, 0));
```

## Lines & Segments

### Lines and Segments

```csharp
// Find intersection of two lines
Line2d lineA = new Line2d(new Point2d(0, 0), new Point2d(10, 10));
Line2d lineB = new Line2d(new Point2d(0, 10), new Point2d(10, 0));
Point2d[] intersections = lineA.IntersectWith(lineB);
if (intersections != null && intersections.Length > 0)
    ed.WriteMessage("Intersection at: {0}\n", intersections[0]);

// Segment midpoint and length
LineSegment3d seg = new LineSegment3d(
    new Point3d(0, 0, 0), new Point3d(100, 0, 0));
Point3d mid = seg.MidPoint;    // (50, 0, 0)
double len = seg.Length;        // 100.0
```

## Arcs & Circles

### CircularArc2d / CircularArc3d

```csharp
// Create arc through 3 points
CircularArc3d arc = new CircularArc3d(
    new Point3d(0, 0, 0),
    new Point3d(50, 50, 0),
    new Point3d(100, 0, 0));
double radius = arc.Radius;
Point3d center = arc.Center;

// Full circle
CircularArc2d circle = new CircularArc2d(
    new Point2d(100, 100), 50.0);

// Find arc-line intersections
Line3d testLine = new Line3d(center, Vector3d.XAxis);
Point3d[] hits = arc.IntersectWith(testLine);
```

## Curves (Abstract Base)

### CurveCurveIntersector2d / CurveCurveIntersector3d
For finding intersections between ANY two curves:

```csharp
// 2D intersection
CurveCurveIntersector2d cci = new CurveCurveIntersector2d(curve1, curve2);
// Optional: with tolerance or restricted intervals
// new CurveCurveIntersector2d(curve1, curve2, Tolerance tolerance)
// new CurveCurveIntersector2d(curve1, curve2, Interval range1, Interval range2)

for (int i = 0; i < cci.NumberOfIntersectionPoints; i++)
{
    Point2d pt = cci.GetIntersectionPoint(i);
    double[] parms = cci.GetIntersectionParameters(i);  // [param1, param2]
    bool tangent = cci.IsTangential(i);
    bool transversal = cci.IsTransversal(i);
}

// Check for overlaps (collinear segments)
int overlapCount = cci.OverlapCount;   // property on 2d, method on 3d
```

Note: CurveCurveIntersector3d requires a `Vector3d planeNormal` parameter in all constructors (for projection direction).

## Planes & Bounds

### Extents2d / Extents3d (axis-aligned bounding boxes)
**Namespace:** `Autodesk.AutoCAD.DatabaseServices` (NOT `Autodesk.AutoCAD.Geometry` — easy to get wrong)

These are used very commonly:

```csharp
// Extents3d is used by Entity.GeometricExtents
Extents3d ext = entity.GeometricExtents;
Point3d minPt = ext.MinPoint;
Point3d maxPt = ext.MaxPoint;

// Build extents from points
Extents3d bounds = new Extents3d();
bounds.AddPoint(new Point3d(0, 0, 0));
bounds.AddPoint(new Point3d(100, 200, 0));

// Merge extents
bounds.AddExtents(otherExtents);
```

## Tolerance

```csharp
// Global tolerance (used by default for all comparisons)
Tolerance defaultTol = Tolerance.Global;

// Custom tolerance for specific comparisons
Tolerance customTol = new Tolerance(1e-6, 1e-6);  // (equalVector, equalPoint)

// Use with comparison methods
bool equal = p1.IsEqualTo(p2, customTol);
bool parallel = v1.IsParallelTo(v2, customTol);
```

Properties: `EqualPoint` (double), `EqualVector` (double) - both get-only.

## UCS / OCS / WCS Coordinate Conversion

AutoCAD uses three coordinate systems:
- **WCS** — World Coordinate System (absolute, fixed)
- **UCS** — User Coordinate System (current user-defined system)
- **OCS** — Object Coordinate System (per-entity, e.g. a 2D polyline's plane)

```csharp
// WCS point → current UCS point
Matrix3d ucsMatrix = ed.CurrentUserCoordinateSystem;
Point3d wcsPoint = new Point3d(100, 200, 0);
Point3d ucsPoint = wcsPoint.TransformBy(ucsMatrix.Inverse());

// UCS point → WCS point
Point3d backToWcs = ucsPoint.TransformBy(ucsMatrix);

// WCS → OCS (entity's local plane, e.g. for a 2D polyline)
// Use WorldToPlane with the entity's Normal vector
Vector3d normal = polyline.Normal;  // e.g. Vector3d.ZAxis for XY-plane poly
Matrix3d wcsToOcs = Matrix3d.WorldToPlane(normal);
Point3d ocsPoint = wcsPoint.TransformBy(wcsToOcs);

// OCS → WCS
Matrix3d ocsToWcs = Matrix3d.PlaneToWorld(normal);
Point3d wcsFromOcs = ocsPoint.TransformBy(ocsToWcs);

// Align coordinate systems (e.g. block transform from one CS to another)
Matrix3d alignXform = Matrix3d.AlignCoordinateSystem(
    Point3d.Origin,      // fromOrigin
    Vector3d.XAxis,      // fromXAxis
    Vector3d.YAxis,      // fromYAxis
    Vector3d.ZAxis,      // fromZAxis
    targetOrigin,        // toOrigin
    targetXAxis,         // toXAxis
    targetYAxis,         // toYAxis
    targetZAxis          // toZAxis
);
```

## Common Geometry Recipes

```csharp
// Offset a point along a direction by distance
Point3d OffsetPoint(Point3d pt, Vector3d dir, double dist)
{
    return pt + dir.GetNormal() * dist;
}

// Find intersection of two 2D lines
Point2d? IntersectLines(Point2d a1, Point2d a2, Point2d b1, Point2d b2)
{
    Line2d lineA = new Line2d(a1, a2);
    Line2d lineB = new Line2d(b1, b2);
    Point2d[] pts = lineA.IntersectWith(lineB);
    return pts?.Length > 0 ? pts[0] : (Point2d?)null;
}

// Project point onto a line
Point3d ProjectPointToLine(Point3d pt, Line3d line)
{
    PointOnCurve3d poc = line.GetClosestPointTo(pt);
    return poc.Point;
}

// Distance from point to line
double PointToLineDistance(Point3d pt, Line3d line)
{
    return line.GetDistanceTo(pt);
}

// Angle between two vectors (with reference for sign)
double SignedAngle(Vector3d from, Vector3d to, Vector3d refAxis)
{
    return from.GetAngleTo(to, refAxis);
}

// Check if point is on a curve within tolerance
bool IsPointOnCurve(Curve3d curve, Point3d pt)
{
    return curve.IsOn(pt);
}
```

## Gotchas

- Point2d uses `GetDistanceTo()` but Point3d uses `DistanceTo()` (no "Get" prefix) - easy source of compile errors
- `Vector3d.GetAngleTo(Vector3d)` always returns 0 to pi. Use the 3-parameter overload `GetAngleTo(Vector3d, Vector3d referenceVector)` for signed angles (0 to 2pi)
- `GetNormal()` throws `ZeroVectorException` on zero-length vectors; check `IsZeroLength()` first or use `GetNormal(Tolerance)` which returns a zero vector instead
- Point2d/Point3d are **structs** (value types) - they are copied on assignment, not referenced
- Matrix multiplication is right-to-left: `rot * scale` applies scale first, then rotation
- `Curve.GetLength()` takes **parameter** values, not station values; get the interval first with `GetInterval()`
- All angle parameters are in **radians**, not degrees
- `Line2d`/`Line3d` are infinite lines; use `LineSegment2d`/`LineSegment3d` for bounded segments
- `CircularArc2d/3d.IntersectWith()` returns `null` (not empty array) when there are no intersections - always null-check
- `CurveCurveIntersector3d` requires a `planeNormal` parameter (for projection) - use `Vector3d.ZAxis` for XY-plane intersections
- `CurveCurveIntersector2d.OverlapCount` is a **property** (no parens); `CurveCurveIntersector3d.OverlapCount()` is a **method** (requires parens) - mixing them up causes compile errors
- 2D Polyline vertices are stored in **OCS** (Object Coordinate System), not WCS. Use `Matrix3d.WorldToPlane(polyline.Normal)` to convert WCS points to OCS before comparing or inserting vertices
- `Extents2d` and `Extents3d` are in `Autodesk.AutoCAD.DatabaseServices`, not `Autodesk.AutoCAD.Geometry` - add the correct using directive
- Tolerance overloads exist for almost every comparison method - use them when default global tolerance is too tight or too loose

## Related Skills

- `acad-polylines` — polyline vertices, bulge arcs, and OCS vertex coordinate conversion
