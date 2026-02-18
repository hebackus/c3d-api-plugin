---
name: autocad-class-reference
description: Quick reference for AutoCAD .NET API classes - 1,248 types across 28 namespaces
---

# AutoCAD 2026 .NET API Class Reference

**Quick lookup for 1,248 classes across 28 namespaces**

## When to Use This Skill

- Looking for AutoCAD base classes
- Finding database entities (Line, Circle, Polyline, etc.)
- Checking geometry classes
- Finding editor/application classes
- Exploring runtime services

## Core Namespaces

### Autodesk.AutoCAD.DatabaseServices (561 types)

**Core database objects and entities**

**Key Entity Classes:**
- `Entity` - Base class for all graphical objects
- `Curve` - Base for all curve entities
- `Line`, `Arc`, `Circle`, `Ellipse`, `Spline`
- `Polyline`, `Polyline2d`, `Polyline3d`
- `BlockReference` - Block insert
- `DBText`, `MText` - Text entities
- `Hatch`, `Solid`, `Region`
- `Dimension` - Base dimension class
- `Leader`, `MLeader` - Leader entities

**Database Classes:**
- `Database` - Drawing database
- `Transaction` - Transaction management
- `TransactionManager` - Transaction factory
- `BlockTable`, `BlockTableRecord`
- `LayerTable`, `LayerTableRecord`
- `LinetypeTable`, `TextStyleTable`
- `DimStyleTable`, `RegAppTable`
- `ViewportTable`, `UcsTable`

**Object ID Collections:**
- `ObjectId` - Object identifier
- `ObjectIdCollection` - Collection of IDs
- `DBObjectCollection` - Collection of objects

### Autodesk.AutoCAD.Geometry (42 types)

**Geometric primitives and calculations**

**Key Classes:**
- `Point2d`, `Point3d` - 2D/3D points
- `Vector2d`, `Vector3d` - 2D/3D vectors
- `Matrix2d`, `Matrix3d` - Transformation matrices
- `Line2d`, `Line3d` - Geometric lines
- `LineSegment2d`, `LineSegment3d` - Line segments
- `CircularArc2d`, `CircularArc3d` - Arcs
- `Plane` - 3D plane
- `BoundBlock3d` - Bounding box
- `Extents2d`, `Extents3d` - Extents/bounds

### Autodesk.AutoCAD.ApplicationServices (various)

**Application-level access**

**Key Classes:**
- `Application` - Main application object
- `Document` - Drawing document
- `DocumentCollection` - All open documents
- `Core` - Core application services

### Autodesk.AutoCAD.EditorInput (28 types)

**Editor interaction and user input**

**Key Classes:**
- `Editor` - Command line and editor
- `PromptEntityOptions` - Prompt for entity selection
- `PromptPointOptions` - Prompt for point
- `PromptStringOptions` - Prompt for text
- `PromptKeywordOptions` - Prompt for keyword
- `SelectionFilter` - Entity filtering
- `PromptSelectionResult` - Selection results

### Autodesk.AutoCAD.Runtime (31 types)

**Runtime services and attributes**

**Key Attributes:**
- `CommandMethod` - Define commands
- `LispFunction` - Define LISP functions
- `ExtensionApplication` - Plugin initialization

**Exceptions:**
- `Exception` - Base AutoCAD exception
- `ErrorStatus` - Error codes enum

### Autodesk.AutoCAD.GraphicsInterface (86 types)

**Graphics and rendering**

**Key Classes:**
- `Drawable` - Base drawable interface
- `WorldDraw`, `ViewportDraw` - Drawing contexts
- `SubEntityTraits` - Drawing attributes

### Autodesk.AutoCAD.PlottingServices (25 types)

**Plotting and publishing**

**Key Classes:**
- `PlotEngine` - Plot engine access
- `PlotConfig` - Plot configuration
- `PlotInfo` - Plot information

## Common Patterns

### Access Database and Transaction

```csharp
using Autodesk.AutoCAD.ApplicationServices;
using Autodesk.AutoCAD.DatabaseServices;
using Autodesk.AutoCAD.Runtime;

[CommandMethod("MYCOMMAND")]
public void MyCommand()
{
    Document doc = Application.DocumentManager.MdiActiveDocument;
    Database db = doc.Database;
    Editor ed = doc.Editor;

    using (Transaction tr = db.TransactionManager.StartTransaction())
    {
        // Work with database objects
        BlockTable bt = tr.GetObject(db.BlockTableId, OpenMode.ForRead) as BlockTable;
        BlockTableRecord btr = tr.GetObject(bt[BlockTableRecord.ModelSpace],
            OpenMode.ForWrite) as BlockTableRecord;

        tr.Commit();
    }
}
```

### Create Entity

```csharp
using (Transaction tr = db.TransactionManager.StartTransaction())
{
    BlockTable bt = tr.GetObject(db.BlockTableId, OpenMode.ForRead) as BlockTable;
    BlockTableRecord btr = tr.GetObject(bt[BlockTableRecord.ModelSpace],
        OpenMode.ForWrite) as BlockTableRecord;

    // Create a line
    Line line = new Line(new Point3d(0, 0, 0), new Point3d(100, 100, 0));
    line.ColorIndex = 1; // Red

    btr.AppendEntity(line);
    tr.AddNewlyCreatedDBObject(line, true);

    tr.Commit();
}
```

### User Input

```csharp
using Autodesk.AutoCAD.EditorInput;

Editor ed = Application.DocumentManager.MdiActiveDocument.Editor;

// Prompt for point
PromptPointOptions ppo = new PromptPointOptions("\nSelect point: ");
PromptPointResult ppr = ed.GetPoint(ppo);
if (ppr.Status == PromptStatus.OK)
{
    Point3d pt = ppr.Value;
}

// Prompt for entity
PromptEntityOptions peo = new PromptEntityOptions("\nSelect entity: ");
peo.SetRejectMessage("\nMust be a line.");
peo.AddAllowedClass(typeof(Line), true);
PromptEntityResult per = ed.GetEntity(peo);
if (per.Status == PromptStatus.OK)
{
    ObjectId lineId = per.ObjectId;
}
```

## Full Class Index

See [`../../autocad-api-reference/CLASS_INDEX.md`](../../autocad-api-reference/CLASS_INDEX.md) for complete listing of all 1,248 types.

## Related Skills

For Civil 3D-specific classes, use:
- `/c3d-api:c3d-class-reference` - Civil 3D classes
- `/c3d-api:c3d-root-objects` - CivilApplication/CivilDocument

For specific AutoCAD entity and API topics, use:
- `/c3d-api:acad-tables` - Creating and modifying AutoCAD table entities
- `/c3d-api:acad-geometry` - Working with geometric types (Point3d, Vector3d, curves)
- `/c3d-api:acad-mtext` - Creating and formatting MText entities
- `/c3d-api:acad-mleaders` - Creating and configuring MLeader entities
- `/c3d-api:acad-fields` - Working with AutoCAD field expressions
- `/c3d-api:acad-dimensions` - Creating dimension entities
- `/c3d-api:acad-hatches` - Creating hatch pattern fills
- `/c3d-api:acad-blocks` - Creating and inserting block references
- `/c3d-api:acad-sheet-sets` - Reading/writing Sheet Set (.dst) files via COM

## Documentation

- **HTML Docs:** `ac3d_netapi2docs/docs/AutoCAD_2026/html/index.html`
- **Source Code:** `ac3d_netapi2docs/src/AutoCAD_2026/`
