---
name: acad-regions-solids
description: Regions, 3D solids, and surfaces - boolean operations, extrusion, revolution, sweep, loft, mass properties, sectioning, and Brep sub-entity access
---

# AutoCAD Regions and 3D Solids

Use this skill when creating or manipulating regions (2D enclosed areas), 3D solids, surfaces, and bodies. Covers boolean operations, solid primitives, extrusion/revolution/sweep/loft, mass properties, sectioning, and sub-entity access via the Brep API.

## Region Creation from Closed Curves

Regions are 2D enclosed areas created from closed curve boundaries. `Region.CreateFromCurves` accepts a `DBObjectCollection` of curves that form one or more closed loops (curves must meet end-to-end within tolerance).

```csharp
using (Transaction tr = db.TransactionManager.StartTransaction())
{
    BlockTableRecord btr = (BlockTableRecord)tr.GetObject(
        db.CurrentSpaceId, OpenMode.ForWrite);

    // Build a closed polyline boundary
    Polyline pline = new Polyline();
    pline.AddVertexAt(0, new Point2d(0, 0), 0, 0, 0);
    pline.AddVertexAt(1, new Point2d(100, 0), 0, 0, 0);
    pline.AddVertexAt(2, new Point2d(100, 50), 0, 0, 0);
    pline.AddVertexAt(3, new Point2d(0, 50), 0, 0, 0);
    pline.Closed = true;
    btr.AppendEntity(pline);
    tr.AddNewlyCreatedDBObject(pline, true);

    // Create region from closed curves
    DBObjectCollection curves = new DBObjectCollection();
    curves.Add(pline);
    DBObjectCollection regions = Region.CreateFromCurves(curves);

    foreach (DBObject obj in regions)
    {
        Region region = (Region)obj;
        btr.AppendEntity(region);
        tr.AddNewlyCreatedDBObject(region, true);
    }
    tr.Commit();
}
```

Multiple open curves that together close a loop also work:

```csharp
DBObjectCollection curves = new DBObjectCollection();
curves.Add(line1);   // Line from (0,0) to (100,0)
curves.Add(arc1);    // Arc from (100,0) to (100,50)
curves.Add(line2);   // Line from (100,50) to (0,0)
DBObjectCollection regions = Region.CreateFromCurves(curves);
```

## Region Boolean Operations

```csharp
Region regionA = /* ... */;
Region regionB = /* ... */;

// Union -- merges both regions
regionA.BooleanOperation(BooleanOperationType.BoolUnite, regionB);
// regionA now contains the union; regionB becomes a null region

// Subtract -- removes regionB from regionA
regionA.BooleanOperation(BooleanOperationType.BoolSubtract, regionB);

// Intersect -- keeps only the overlap
regionA.BooleanOperation(BooleanOperationType.BoolIntersect, regionB);
```

## Region Properties

- `Area` (double, get-only) -- enclosed area
- `Perimeter` (double, get-only) -- total boundary length
- `Normal` (Vector3d, get-only) -- plane normal
- `IsNull` (bool, get-only) -- true if zero area (e.g., after a boolean that produces nothing)
- `Bounds` (Extents3d?, get-only) -- axis-aligned bounding box

## Solid3d Primitives

All primitives are created centered at the world origin. Use `TransformBy` to position them.

```csharp
// Box
Solid3d box = new Solid3d();
box.CreateBox(100, 50, 25);  // length, width, height

// Sphere
Solid3d sphere = new Solid3d();
sphere.CreateSphere(25);  // radius

// Cylinder (frustum with equal radii)
Solid3d cyl = new Solid3d();
cyl.CreateFrustum(50, 15, 15, 15);  // height, xRadius, yRadius, topRadius

// Cone (frustum with topRadius = 0)
Solid3d cone = new Solid3d();
cone.CreateFrustum(50, 20, 20, 0);  // height, xRadius, yRadius, topRadius

// Torus
Solid3d torus = new Solid3d();
torus.CreateTorus(40, 10);  // majorRadius, minorRadius

// Wedge
Solid3d wedge = new Solid3d();
wedge.CreateWedge(100, 50, 25);  // length, width, height

// Pyramid (truncated: add 4th param for topRadius)
Solid3d pyramid = new Solid3d();
pyramid.CreatePyramid(50, 4, 20);  // height, sides, radius
```

### Positioning Primitives

```csharp
Solid3d box = new Solid3d();
box.CreateBox(100, 50, 25);

// Move then rotate
Matrix3d move = Matrix3d.Displacement(new Vector3d(200, 300, 0));
Matrix3d rot = Matrix3d.Rotation(Math.PI / 4, Vector3d.ZAxis, new Point3d(200, 300, 0));
box.TransformBy(rot * move);  // right-to-left: move first, then rotate
```

## Solid3d from Extrusion

```csharp
// Extrude a region by height with optional taper
Region region = /* closed boundary region */;
Solid3d solid = new Solid3d();
solid.Extrude(region, 30.0, 0.0);  // height, taperAngle (radians)
// Positive taper = narrows; negative = widens
```

### Extrude Along a Path

```csharp
Region profile = /* cross-section region */;
ObjectId pathId = /* path curve ObjectId (Line, Arc, Polyline, Spline) */;

Solid3d solid = new Solid3d();
solid.ExtrudeAlongPath(profile, pathId, 0.0);  // taperAngle
```

## Solid3d from Revolution

```csharp
Region profile = /* profile region -- must be entirely on one side of axis */;
Point3d axisPoint = new Point3d(0, 0, 0);
Vector3d axisDir = Vector3d.YAxis;

Solid3d solid = new Solid3d();
solid.Revolve(profile, axisPoint, axisDir, 2 * Math.PI);  // full revolution
```

## Solid3d from Sweep

```csharp
Entity profileEntity = /* closed curve or region (must be in database) */;
Entity pathEntity = /* path curve (must be in database) */;

SweepOptions sweepOpts = new SweepOptions();
// Optional: sweepOpts.Align, sweepOpts.Bank, sweepOpts.BasePoint,
//           sweepOpts.ScaleFactor, sweepOpts.TwistAngle

Solid3d solid = new Solid3d();
solid.CreateSweptSolid(profileEntity, pathEntity, sweepOpts);
```

## Solid3d from Loft

```csharp
Entity[] crossSections = new Entity[] { profile1, profile2, profile3 };

LoftOptions loftOpts = new LoftOptions();
// Optional: loftOpts.Ruled, loftOpts.Closed, loftOpts.StartDraftAngle,
//           loftOpts.EndDraftAngle, loftOpts.StartDraftMagnitude

Solid3d solid = new Solid3d();
solid.CreateLoftedSolid(crossSections, null, null, loftOpts);
// Parameters: crossSections, guideCurves (Entity[]), pathEntity (Entity), options

// With guide curves:
solid.CreateLoftedSolid(crossSections, new Entity[] { guide1 }, null, loftOpts);
```

## Solid3d Boolean Operations

```csharp
Solid3d solidA = /* first solid */;
Solid3d solidB = /* second solid */;

// Union -- solidB is erased from the database
solidA.BooleanOperation(BooleanOperationType.BoolUnite, solidB);

// Subtract -- solidB carved out of solidA; solidB erased
solidA.BooleanOperation(BooleanOperationType.BoolSubtract, solidB);

// Intersect -- only overlap remains; solidB erased
solidA.BooleanOperation(BooleanOperationType.BoolIntersect, solidB);
```

### Practical Example: Box with Cylindrical Hole

```csharp
Solid3d box = new Solid3d();
box.CreateBox(100, 100, 50);
btr.AppendEntity(box);
tr.AddNewlyCreatedDBObject(box, true);

Solid3d hole = new Solid3d();
hole.CreateFrustum(60, 15, 15, 15);  // cylinder
btr.AppendEntity(hole);
tr.AddNewlyCreatedDBObject(hole, true);

box.BooleanOperation(BooleanOperationType.BoolSubtract, hole);
// hole is erased; box has a cylindrical hole through it
```

## Solid3d Properties and Mass Properties

- `Area` (double, get-only) -- total surface area
- `IsNull` (bool, get-only) -- true if zero volume
- `NumChanges` (int, get-only) -- modification counter

```csharp
Solid3d solid = (Solid3d)tr.GetObject(solidId, OpenMode.ForRead);

double volume = solid.MassProperties.Volume;
Point3d centroid = solid.MassProperties.Centroid;
double[] momentsOfInertia = solid.MassProperties.MomentsOfInertia.ToArray();
double[] productsOfInertia = solid.MassProperties.ProductsOfInertia.ToArray();
double[] radiiOfGyration = solid.MassProperties.RadiiOfGyration.ToArray();
double[] principalMoments = solid.MassProperties.PrincipalMoments.ToArray();
Vector3d[] principalDirs = solid.MassProperties.PrincipalDirections;
```

## Solid3d Sectioning and Slicing

### Sectioning (creates a Region cross-section)

```csharp
Solid3d solid = (Solid3d)tr.GetObject(solidId, OpenMode.ForWrite);
Plane sectionPlane = new Plane(new Point3d(0, 0, 25), Vector3d.ZAxis);

Entity sectionEntity = solid.GetSection(sectionPlane);
if (sectionEntity != null)
{
    btr.AppendEntity(sectionEntity);
    tr.AddNewlyCreatedDBObject(sectionEntity, true);
}
```

### Slicing (cuts the solid in two)

```csharp
Plane slicePlane = new Plane(new Point3d(50, 0, 0), Vector3d.XAxis);

// true = keep both halves; returns the other half as a new Solid3d
Solid3d otherHalf = solid.Slice(slicePlane, true);
if (otherHalf != null)
{
    btr.AppendEntity(otherHalf);
    tr.AddNewlyCreatedDBObject(otherHalf, true);
}

// false = discard the negative side
solid.Slice(slicePlane, false);
```

## SubEntity Access via Brep API

The Brep (Boundary Representation) API provides access to faces, edges, and vertices. Hierarchy: Complex -> Shell -> Face -> BoundaryLoop -> Edge -> Vertex.

```csharp
using Autodesk.AutoCAD.BoundaryRepresentation;

Solid3d solid = (Solid3d)tr.GetObject(solidId, OpenMode.ForRead);
using (Brep brep = new Brep(solid))
{
    // Faces
    foreach (Face face in brep.Faces)
    {
        ExternalBoundedSurface surf = face.Surface;
        double faceArea = face.GetArea();

        foreach (BoundaryLoop loop in face.Loops)
        {
            foreach (Edge edge in loop.Edges)
            {
                ExternalCurve3d curve = edge.Curve;
                Point3d startPt = curve.StartPoint;
                Point3d endPt = curve.EndPoint;
            }
        }
    }

    // Edges and vertices directly
    foreach (Edge edge in brep.Edges)
    {
        Point3d pt1 = edge.Vertex1.Point;
        Point3d pt2 = edge.Vertex2.Point;
    }

    foreach (Vertex vertex in brep.Vertices)
        Point3d pt = vertex.Point;

    // Topology counts (LINQ methods, not properties)
    int faceCount = brep.Faces.Count();
    int edgeCount = brep.Edges.Count();

    // Shells
    foreach (Shell shell in brep.Shells)
        ShellType type = shell.ShellType;  // ShellIn or ShellOut
}
```

## Body and Surface Entities

Surface entities are open surfaces (area but no volume). They cannot participate in solid boolean operations.

```csharp
// Extruded surface
ExtrudedSurface extSurf = new ExtrudedSurface();
extSurf.CreateExtrudedSurface(profileEntity, new Vector3d(0, 0, 50), new SweepOptions());

// Revolved surface
RevolvedSurface revSurf = new RevolvedSurface();
revSurf.CreateRevolvedSurface(profileEntity, axisPoint, axisDir, angle, 0.0, new RevolveOptions());

// Lofted surface
LoftedSurface loftSurf = new LoftedSurface();
loftSurf.CreateLoftedSurface(crossSections, null, null, new LoftOptions());

// Swept surface
SweptSurface sweptSurf = new SweptSurface();
sweptSurf.CreateSweptSurface(profileEntity, pathEntity, new SweepOptions());

// Planar surface from region
PlaneSurface planeSurf = new PlaneSurface();
planeSurf.CreateFromRegion(region);
```

`Body` is a lower-level entity rarely used directly. Import from SAT data with `Body.CreateFromSatFile("model.sat")`.

## 3D Coordinate Systems and Transforms for Solids

```csharp
// Align solid to a custom coordinate system
Solid3d solid = new Solid3d();
solid.CreateBox(100, 50, 25);

Point3d targetOrigin = new Point3d(500, 200, 100);
Vector3d targetX = new Vector3d(1, 1, 0).GetNormal();
Vector3d targetZ = Vector3d.ZAxis;
Vector3d targetY = targetZ.CrossProduct(targetX).GetNormal();

Matrix3d xform = Matrix3d.AlignCoordinateSystem(
    Point3d.Origin, Vector3d.XAxis, Vector3d.YAxis, Vector3d.ZAxis,
    targetOrigin, targetX, targetY, targetZ);
solid.TransformBy(xform);

// Align to current UCS
Matrix3d ucsMatrix = ed.CurrentUserCoordinateSystem;
solid.TransformBy(ucsMatrix);

// Deep copy and transform
Solid3d copy = (Solid3d)solid.Clone();
btr.AppendEntity(copy);
tr.AddNewlyCreatedDBObject(copy, true);
copy.TransformBy(Matrix3d.Scaling(2.0, Point3d.Origin));
```

## Gotchas

- `Region.CreateFromCurves` requires curves forming closed loops. Open curves or gaps return an empty collection with no error.
- `Region.CreateFromCurves` accepts a `DBObjectCollection`, not an `ObjectIdCollection`. Pass entity objects, not their IDs.
- After a boolean on regions, the second operand becomes a null region (zero area). After a boolean on solids, the second operand is **erased from the database**.
- Solid primitives are always centered at the world origin. You must `TransformBy` to position them.
- `CreateFrustum` with equal radii creates a cylinder. With `topRadius = 0` it creates a cone.
- `Extrude` taper angle is in radians. A taper that causes self-intersection throws an exception.
- `ExtrudeAlongPath` requires the path curve to be in the database (pass its `ObjectId`).
- `Revolve` requires the profile to be entirely on one side of the revolution axis.
- `CreateSweptSolid` and `CreateLoftedSolid` require all entities to already exist in the database.
- `Brep` must be disposed (`using` block). Failing to dispose leaks unmanaged ACIS resources.
- `Brep` collections use LINQ-style enumeration. Call `.Count()` (method), not `.Count` (property).
- `Solid3d.MassProperties` computes on access. Cache the result for repeated queries.
- `Solid3d.Slice` with `getNegativeSide = true` returns the other half -- you must add it to the database yourself.
- `GetSection` returns `null` if the plane does not intersect the solid. Always null-check.
- Surface entities are open surfaces, not solids. They have area but no volume and cannot participate in solid boolean operations.

## Related Skills

- `acad-geometry` -- points, vectors, matrices, planes, and coordinate system transforms used to position solids
- `acad-polylines` -- closed polylines as region boundaries and extrusion profiles
- `acad-hatches` -- solid fills and boundary loops share region-based workflows
- `acad-editor-input` -- prompting for entity selection and point picks when building solids interactively
