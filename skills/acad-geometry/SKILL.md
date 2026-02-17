---
name: acad-geometry
description: Points, vectors, matrices, lines, arcs, curves, planes, bounds, tolerance - construction, transforms, intersections, and common recipes
---

# AutoCAD Geometry (Autodesk.AutoCAD.Geometry)

Use this skill when working with geometric primitives - points, vectors, matrices, lines, arcs, curves, planes, and bounding boxes. These types are used throughout both AutoCAD and Civil 3D APIs.

## Points

### Point2d (struct)
- Constructors: `Point2d(double x, double y)`, `Point2d(double[] xy)`
- Static: `Point2d.Origin`
- Properties: `X`, `Y` (double, get-only), indexer `[int i]`
- Key methods: `GetDistanceTo(Point2d)`, `GetVectorTo(Point2d)`, `GetAsVector()`, `TransformBy(Matrix2d)`, `RotateBy(double angle, Point2d origin)`, `Mirror(Line2d)`, `ScaleBy(double, Point2d)`, `Add(Vector2d)`, `Subtract(Vector2d)`, `MultiplyBy(double)`, `DivideBy(double)`, `IsEqualTo(Point2d)`, `IsEqualTo(Point2d, Tolerance)`, `ToArray()`
- Operators: `Point2d + Vector2d -> Point2d`, `Point2d - Vector2d -> Point2d`, `Point2d - Point2d -> Vector2d`, `Matrix2d * Point2d -> Point2d`, `Point2d * double -> Point2d`, `double * Point2d -> Point2d`, `Point2d / double -> Point2d`, `==`, `!=`

```csharp
Point2d p1 = new Point2d(100.0, 200.0);
Point2d p2 = new Point2d(300.0, 400.0);
double dist = p1.GetDistanceTo(p2);
Vector2d dir = p1.GetVectorTo(p2);
Point2d mid = p1 + dir * 0.5;   // midpoint via vector math
Point2d rotated = p1.RotateBy(Math.PI / 4, Point2d.Origin);
```

### Point3d (struct)
- Constructors: `Point3d(double x, double y, double z)`, `Point3d(double[] xyz)`, `Point3d(PlanarEntity plane, Point2d point)`
- Static: `Point3d.Origin`
- Properties: `X`, `Y`, `Z` (double, get-only), indexer `[int i]`
- Key methods: `DistanceTo(Point3d)` (NOTE: not GetDistanceTo like Point2d!), `GetVectorTo(Point3d)`, `GetAsVector()`, `TransformBy(Matrix3d)`, `RotateBy(double angle, Vector3d axis, Point3d centerPoint)`, `ScaleBy(double, Point3d)`, `Add(Vector3d)`, `Subtract(Vector3d)`, `MultiplyBy(double)`, `DivideBy(double)`, `Convert2d(PlanarEntity)`, `OrthoProject(Plane)`, `Project(Plane, Vector3d)`, `Mirror(Plane)`, `IsEqualTo(Point3d)`, `IsEqualTo(Point3d, Tolerance)`, `ToArray()`
- Operators: same pattern as Point2d but with Vector3d/Matrix3d

```csharp
Point3d p1 = new Point3d(100.0, 200.0, 0.0);
Point3d p2 = new Point3d(300.0, 400.0, 0.0);
double dist = p1.DistanceTo(p2);    // Note: DistanceTo, not GetDistanceTo
Vector3d dir = p1.GetVectorTo(p2).GetNormal();
Point3d rotated = p1.RotateBy(Math.PI / 2, Vector3d.ZAxis, Point3d.Origin);
Point2d flat = p1.Convert2d(new Plane());  // project to XY plane
```

## Vectors

### Vector2d (struct)
- Constructors: `Vector2d(double x, double y)`, `Vector2d(double[] xy)`
- Static: `Vector2d.XAxis`, `Vector2d.YAxis`
- Properties: `X`, `Y`, `Angle`, `Length`, `LengthSqrd` (all get-only)
- Key methods: `GetNormal()`, `GetNormal(Tolerance)`, `GetAngleTo(Vector2d)`, `GetPerpendicularVector()`, `DotProduct(Vector2d)`, `RotateBy(double)`, `Mirror(Vector2d)`, `Negate()`, `Add(Vector2d)`, `Subtract(Vector2d)`, `MultiplyBy(double)`, `DivideBy(double)`, `IsParallelTo(Vector2d)`, `IsPerpendicularTo(Vector2d)`, `IsCodirectionalTo(Vector2d)`, `IsUnitLength()`, `IsZeroLength()`, `IsEqualTo(Vector2d)` (all comparison methods have Tolerance overloads)
- Operators: `+`, unary `-`, binary `-`, `*` (Matrix2d, double), `/`

### Vector3d (struct)
- Constructors: `Vector3d(double x, double y, double z)`, `Vector3d(double[] xyz)`, `Vector3d(PlanarEntity plane, Vector2d vector2d)`
- Static: `Vector3d.XAxis`, `Vector3d.YAxis`, `Vector3d.ZAxis`
- Properties: `X`, `Y`, `Z`, `Length`, `LengthSqrd`, `LargestElement` (all get-only)
- Key methods: all of Vector2d's methods plus `CrossProduct(Vector3d)`, `GetAngleTo(Vector3d)`, `GetAngleTo(Vector3d, Vector3d referenceVector)`, `Convert2d(PlanarEntity)`, `AngleOnPlane(PlanarEntity)`, `ProjectTo(Vector3d planeNormal, Vector3d projectDirection)`, `OrthoProjectTo(Vector3d planeNormal)`

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

### Matrix3d (struct)
- Constructor: `Matrix3d(double[] data)` (16 elements, row-major)
- Static: `Matrix3d.Identity`
- Properties: `Translation` (Vector3d), `CoordinateSystem3d`, indexer `[int row, int column]`
- Factory methods (all static):
  - `Matrix3d.Displacement(Vector3d vector)`
  - `Matrix3d.Rotation(double angle, Vector3d axis, Point3d center)`
  - `Matrix3d.Scaling(double scaleAll, Point3d center)`
  - `Matrix3d.Mirroring(Point3d point)`, `Mirroring(Plane plane)`, `Mirroring(Line3d line)`
  - `Matrix3d.WorldToPlane(Vector3d normal)`, `WorldToPlane(Plane plane)`
  - `Matrix3d.PlaneToWorld(Vector3d normal)`, `PlaneToWorld(Plane plane)`
  - `Matrix3d.Projection(Plane projectionPlane, Vector3d projectDir)`
  - `Matrix3d.AlignCoordinateSystem(Point3d fromOrigin, Vector3d fromXAxis, Vector3d fromYAxis, Vector3d fromZAxis, Point3d toOrigin, Vector3d toXAxis, Vector3d toYAxis, Vector3d toZAxis)`
- Methods: `Inverse()`, `Transpose()`, `PreMultiplyBy(Matrix3d)`, `PostMultiplyBy(Matrix3d)`, `GetDeterminant()`, `GetScale()`, `IsSingular()`, `IsScaledOrtho()`, `IsUniscaledOrtho()`, `IsEqualTo(Matrix3d)` (with Tolerance overloads)
- Operators: `Matrix3d * Matrix3d -> Matrix3d`, `==`, `!=`

### Matrix2d (struct)
- Same pattern as Matrix3d but 2D
- Factory methods: `Displacement(Vector2d)`, `Rotation(double angle, Point2d center)`, `Scaling(double, Point2d)`, `Mirroring(Line2d)`, `Mirroring(Point2d)`, `AlignCoordinateSystem(Point2d fromOrigin, Vector2d fromE0, Vector2d fromE1, Point2d toOrigin, Vector2d toE0, Vector2d toE1)`

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

### Line2d / Line3d (infinite lines)
- Constructors: `Line2d()`, `Line2d(Point2d p1, Point2d p2)`, `Line2d(Point2d point, Vector2d direction)` (same pattern for Line3d)
- Inherited from LinearEntity2d/3d: `Direction` (Vector2d/3d), `PointOnLine` (Point2d/3d)
- Methods (from LinearEntity): `IntersectWith(LinearEntity)` -> `Point2d[]`/`Point3d[]`, `IsParallelTo(LinearEntity)`, `IsPerpendicularTo(LinearEntity)`, `IsColinearTo(LinearEntity)`, `GetPerpendicularLine(Point2d)`/`GetPerpendicularPlane(Point3d)`, `Overlap(LinearEntity)`, `GetLine()`
- Line3d additional: `IntersectWith(PlanarEntity)`, `IsParallelTo(PlanarEntity)`, `IsPerpendicularTo(PlanarEntity)`

### LineSegment2d / LineSegment3d (bounded segments)
- Constructors: `LineSegment2d(Point2d p1, Point2d p2)`, `LineSegment2d(Point2d point, Vector2d direction)` (same for 3d)
- Properties: `StartPoint`, `EndPoint`, `MidPoint` (Point2d/3d), `Length` (double)
- Methods: `GetBisector()` -> Line2d/Plane, `BaryComb(double blendCoefficient)` -> Point, `Set(...)` (multiple overloads)
- Inherits all LinearEntity methods (IntersectWith, IsParallelTo, etc.)

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

### CircularArc2d
- Constructors: `CircularArc2d(Point2d center, double radius)`, `CircularArc2d(Point2d center, double radius, double startAngle, double endAngle, Vector2d referenceVector, bool isClockWise)`, `CircularArc2d(Point2d startPoint, Point2d pointOnArc, Point2d endPoint)` (3-point), `CircularArc2d(Point2d startPoint, Point2d endPoint, double bulge, bool bulgeFlag)`
- Properties: `Center` (get/set), `Radius` (get/set), `StartAngle`, `EndAngle` (get), `IsClockWise` (get), `StartPoint`, `EndPoint`, `ReferenceVector` (get/set)
- Methods: `IntersectWith(LinearEntity2d)` -> `Point2d[]`, `IntersectWith(CircularArc2d)` -> `Point2d[]`, `GetTangent(Point2d)` -> `Line2d`, `IsInside(Point2d)`, `SetAngles(double, double)`, `SetToComplement()`

### CircularArc3d
- Constructors: `CircularArc3d(Point3d center, Vector3d normal, double radius)`, `CircularArc3d(Point3d center, Vector3d normal, Vector3d referenceVector, double radius, double startAngle, double endAngle)`, `CircularArc3d(Point3d startPoint, Point3d pointOnArc, Point3d endPoint)` (3-point)
- Properties: same as 2d plus `Normal` (Vector3d, get)
- Methods: same as 2d plus `IntersectWith(PlanarEntity)`, `ClosestPointToPlane(PlanarEntity)`, `ProjectedIntersectWith(LinearEntity3d, Vector3d)`, `GetPlane()`

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

## Elliptical Arcs

### EllipticalArc2d / EllipticalArc3d
- Constructors: `EllipticalArc2d(Point2d center, Vector2d majorAxis, Vector2d minorAxis, double majorRadius, double minorRadius)`, with optional `double startAngle, double endAngle`, `EllipticalArc2d(CircularArc2d)` (convert from circle)
- Properties: `Center` (get/set), `MajorRadius`/`MinorRadius` (get/set), `MajorAxis`/`MinorAxis` (get), `StartAngle`, `EndAngle` (get), `StartPoint`, `EndPoint`, `IsClockWise` (2d only)
- Methods: `IntersectWith(LinearEntity)`, `IsCircular()`, `IsInside(Point)`, `SetAngles(double, double)`, `SetAxes(Vector, Vector)`
- 3d adds: `Normal`, `GetPlane()`, `IntersectWith(PlanarEntity)`, `ClosestPointToPlane(PlanarEntity)`

## Curves (Abstract Base)

### Curve2d / Curve3d (abstract)
These are the base classes for all 2d/3d curve types. Key methods available on all curves:

- Properties: `StartPoint`, `EndPoint`, `HasStartPoint`, `HasEndPoint`, `BoundBlock`, `OrthoBoundBlock`
- Methods:
  - `GetInterval()` -> `Interval`, `SetInterval(Interval)`
  - `GetLength(double fromParam, double toParam)` / `GetLength(double, double, Tolerance)` (Curve3d signature: `GetLength(double, double, double tolerance)`)
  - `GetDistanceTo(Point)`, `GetDistanceTo(Curve)`
  - `GetClosestPointTo(Point)` -> `PointOnCurve`, `GetClosestPointTo(Curve)` -> `PointOnCurve[]`
  - `GetParameterOf(Point)`, `GetParameterAtLength(double datum, double length, bool direction)`
  - `EvaluatePoint(double parameter)` -> Point
  - `GetSamplePoints(int numSample)` -> `Point[]`, `GetSamplePoints(double from, double to, double approxEps)` -> `PointOnCurve[]`
  - `GetTrimmedOffset(double distance, OffsetCurveExtensionType)` (Curve3d adds `Vector3d planeNormal` param)
  - `IsClosed()`, `IsPeriodic(out double period)`, `IsLinear(out Line)`, `IsOn(Point)`, `IsOn(Point, out double param)`, `IsOn(double param)`
  - `GetSplitCurves(double param)` -> `Curve[]`, `Explode(Interval)` -> `Curve[]`
  - `GetArea(double startParam, double endParam)`
  - `GetReverseParameterCurve()`
- Curve3d additional: `IsPlanar(out Plane)`, `IsCoplanarWith(Curve3d, out Plane)`, `GetProjectedEntity(Plane, Vector3d)`, `GetOrthoProjectEntity(Plane)`, `GetProjectedClosestPointTo(Point3d, Vector3d)`, `GetNewSamplePoints(double, double, double)`

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

### CompositeCurve2d / CompositeCurve3d
For combining multiple curves into one:
- Constructor: `CompositeCurve2d(Curve2d[] curves)`, `CompositeCurve3d(Curve3d[] curves)`
- Methods: `GetCurves()` -> `Curve[]`, `GlobalToLocalParameter(double)` -> `CompositeParameter`, `LocalToGlobalParameter(CompositeParameter)` -> `double`
- CompositeCurve2d also has `SetCurves(Curve2d[])`

## Planes & Bounds

### Plane
- Constructors: `Plane()`, `Plane(Point3d origin, Vector3d normal)`, `Plane(Point3d p1, Point3d origin, Point3d p2)` (3-point), `Plane(Point3d origin, Vector3d u, Vector3d v)`, `Plane(double a, double b, double c, double d)` (equation coefficients)
- Inherited from PlanarEntity: `GetNormal()` (or just `Normal`), `GetCoordinateSystem()`
- Methods: `GetSignedDistanceTo(Point3d)`, `IntersectWith(Plane)` -> `Line3d`, `IntersectWith(BoundedPlane)` -> `LineSegment3d` (both have Tolerance overloads)

### BoundBlock2d / BoundBlock3d (oriented bounding boxes)
- Constructors: `BoundBlock2d(Point2d p1, Point2d p2)` (axis-aligned), `BoundBlock2d(Point2d basePoint, Vector2d dir1, Vector2d dir2)` (oriented)
- Properties: `BasePoint`, `Direction1`, `Direction2` (3d adds `Direction3`), `IsBox` (get/set)
- Methods: `GetMinimumPoint()`, `GetMaximumPoint()`, `Contains(Point)`, `IsDisjoint(BoundBlock)`, `Extend(Point)`, `Swell(double distance)`

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
