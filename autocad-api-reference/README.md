# AutoCAD 2026 .NET API Reference

**Complete API documentation and class index for AutoCAD 2026**

## What's Included

### 1. **HTML Documentation** (Doxygen-generated)
📍 **Location:** `C:\Users\youth\Documents\C3D PLugins\ac3d_netapi2docs\docs\AutoCAD_2026\html\`
- **Browse:** Open `index.html` in your browser (just opened!)
- **Complete** class documentation with inheritance diagrams
- **Searchable** interface
- **Generated from:** Decompiled reference assemblies

### 2. **Class Index** (1,248 types across 28 namespaces)
📍 **Location:** `CLASS_INDEX.md` (this directory)
- **Quick lookup** of all classes organized by namespace
- **Breakdown by type:** Classes, Interfaces, Enums, Structs
- **Top namespaces:**
  - `Autodesk.AutoCAD.DatabaseServices`: 561 types
  - `Autodesk.AutoCAD.Internal`: 158 types
  - `Autodesk.AutoCAD.Windows.Data`: 110 types
  - `Autodesk.AutoCAD.GraphicsInterface`: 86 types
  - `Autodesk.AutoCAD.Geometry`: 42 types

### 3. **C# Source Code** (3,958 files)
📍 **Location:** `C:\Users\youth\Documents\C3D PLugins\ac3d_netapi2docs\src\AutoCAD_2026\`
- **Decompiled** from reference assemblies
- **Searchable** via IDE or file explorer
- **Clean** - stripped of implementation details
- **All API signatures** preserved

### 4. **Claude Skill**
📍 **Access:** `/autocad-class-reference` in Claude Code

**NEW Skill:**
- Quick class lookups for all 1,248 AutoCAD types
- Common patterns and examples
- Entity creation, database access, user input

## Key Namespaces

### Core Database (561 types)
`Autodesk.AutoCAD.DatabaseServices`
- Entity classes: Line, Arc, Circle, Polyline, Text, etc.
- Database: Database, Transaction, BlockTable, LayerTable
- Object management: ObjectId, DBObject, Entity

### Geometry (42 types)
`Autodesk.AutoCAD.Geometry`
- Points: Point2d, Point3d
- Vectors: Vector2d, Vector3d
- Primitives: Line2d, CircularArc3d, Plane
- Transforms: Matrix2d, Matrix3d

### Editor Input (28 types)
`Autodesk.AutoCAD.EditorInput`
- Editor: Main editor interface
- Prompts: PromptEntityOptions, PromptPointOptions
- Selection: SelectionFilter, PromptSelectionResult

### Runtime (31 types)
`Autodesk.AutoCAD.Runtime`
- Attributes: CommandMethod, LispFunction
- Exceptions: Exception, ErrorStatus

### Graphics (86 types)
`Autodesk.AutoCAD.GraphicsInterface`
- Drawing: Drawable, WorldDraw, ViewportDraw
- Rendering: SubEntityTraits, GraphicsKernel

## How to Use

### Quick Class Lookup
1. **Use the Class Index:** Open `CLASS_INDEX.md`
2. **Search by namespace:** Find your class
3. **Invoke skill:** `/autocad-class-reference` for common patterns

### Detailed Documentation
1. **Open HTML docs:** Browse to `ac3d_netapi2docs/docs/AutoCAD_2026/html/index.html`
2. **Search:** Use the search box
3. **Navigate:** Click through namespaces

### Source Code Exploration
1. **Open in IDE:** Load `ac3d_netapi2docs/src/AutoCAD_2026/` in Visual Studio
2. **Search:** Use find in files
3. **Browse:** Navigate class hierarchies

## Common Tasks

### Create an Entity
```csharp
using (Transaction tr = db.TransactionManager.StartTransaction())
{
    BlockTableRecord btr = /* get model space */;
    Line line = new Line(new Point3d(0,0,0), new Point3d(100,100,0));
    btr.AppendEntity(line);
    tr.AddNewlyCreatedDBObject(line, true);
    tr.Commit();
}
```

### Get User Input
```csharp
Editor ed = Application.DocumentManager.MdiActiveDocument.Editor;
PromptPointResult ppr = ed.GetPoint("Select point: ");
if (ppr.Status == PromptStatus.OK)
{
    Point3d pt = ppr.Value;
}
```

### Iterate Entities
```csharp
BlockTableRecord btr = /* get model space */;
foreach (ObjectId objId in btr)
{
    Entity ent = tr.GetObject(objId, OpenMode.ForRead) as Entity;
    if (ent is Line line)
    {
        // Process line
    }
}
```

## Statistics

- **Total Types:** 1,248
- **Namespaces:** 28
- **C# Files:** 3,958
- **HTML Pages:** Generated for all types

## Cross-References

- **Civil 3D API:** See `../api-reference/` for Civil 3D classes
- **Skills Directory:** `../skills/`
- **Main Plugin:** `../plugin.json`

---

**Generated:** 2026-02-15
**AutoCAD Version:** 2026
**API Coverage:** Complete .NET managed API surface (acdbmgd, acmgd, accoremgd)
