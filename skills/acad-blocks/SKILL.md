---
name: acad-blocks
description: Block definitions, references, attributes, dynamic block properties, exploding
---

# AutoCAD Blocks and Attributes

Use this skill when creating block definitions, inserting block references, working with attributes, or reading dynamic block properties.

## Block Definition (BlockTableRecord)

```csharp
using (Transaction tr = db.TransactionManager.StartTransaction())
{
    BlockTable bt = (BlockTable)tr.GetObject(
        db.BlockTableId, OpenMode.ForWrite);

    // Create a new block definition
    BlockTableRecord blockDef = new BlockTableRecord();
    blockDef.Name = "MyBlock";
    blockDef.Origin = new Point3d(0, 0, 0);
    blockDef.Comments = "A custom block";
    blockDef.Units = UnitsValue.Millimeters;
    blockDef.Explodable = true;

    ObjectId blockId = bt.Add(blockDef);
    tr.AddNewlyCreatedDBObject(blockDef, true);

    // Add entities to the block definition
    Line line = new Line(new Point3d(0, 0, 0), new Point3d(10, 10, 0));
    blockDef.AppendEntity(line);
    tr.AddNewlyCreatedDBObject(line, true);

    Circle circle = new Circle(new Point3d(5, 5, 0), Vector3d.ZAxis, 3.0);
    blockDef.AppendEntity(circle);
    tr.AddNewlyCreatedDBObject(circle, true);

    tr.Commit();
}
```

### Iterating Block Contents

```csharp
BlockTableRecord btr = (BlockTableRecord)tr.GetObject(
    blockId, OpenMode.ForRead);
foreach (ObjectId entId in btr)
{
    Entity ent = (Entity)tr.GetObject(entId, OpenMode.ForRead);
    ed.WriteMessage("Entity: {0}\n", ent.GetType().Name);
}
```

## Block Reference (Inserting a Block)

```csharp
BlockTableRecord space = (BlockTableRecord)tr.GetObject(
    db.CurrentSpaceId, OpenMode.ForWrite);

BlockReference blockRef = new BlockReference(
    new Point3d(100, 200, 0),   // insertion point
    blockDefId);                 // BlockTableRecord ObjectId

blockRef.Rotation = 0.0;                // rotation in radians
blockRef.ScaleFactors = new Scale3d(1.0); // uniform scale
blockRef.Normal = Vector3d.ZAxis;

space.AppendEntity(blockRef);
tr.AddNewlyCreatedDBObject(blockRef, true);
```

## Attributes

### Attribute Definition (in block definition)

```csharp
AttributeDefinition attDef = new AttributeDefinition(
    new Point3d(5, -5, 0),    // position
    "Default Value",           // default value
    "TAG_NAME",               // tag
    "Enter value:",           // prompt
    textStyleId);             // text style

attDef.Height = 2.5;
attDef.Invisible = false;
attDef.Constant = false;
attDef.Verifiable = false;
attDef.Preset = false;
attDef.LockPositionInBlock = false;

// MText attribute definition
attDef.IsMTextAttributeDefinition = true;
MText mtext = new MText();
mtext.Contents = "Multi\\Pline";
attDef.MTextAttributeDefinition = mtext;
attDef.UpdateMTextAttributeDefinition();

blockDef.AppendEntity(attDef);
tr.AddNewlyCreatedDBObject(attDef, true);
```

### Attribute Reference (on block insert)

```csharp
// After inserting a BlockReference, add attribute references
BlockTableRecord blockDef = (BlockTableRecord)tr.GetObject(
    blockRef.BlockTableRecord, OpenMode.ForRead);

foreach (ObjectId entId in blockDef)
{
    AttributeDefinition attDef = tr.GetObject(entId, OpenMode.ForRead)
        as AttributeDefinition;
    if (attDef == null || attDef.Constant) continue;

    AttributeReference attRef = new AttributeReference();
    attRef.SetAttributeFromBlock(attDef, blockRef.BlockTransform);
    // Position does NOT auto-update from SetAttributeFromBlock — must set manually
    attRef.Position = attDef.Position.TransformBy(blockRef.BlockTransform);
    attRef.TextString = attDef.TextString;  // or set custom value

    blockRef.AttributeCollection.AppendAttribute(attRef);
    tr.AddNewlyCreatedDBObject(attRef, true);
}
```

### Reading Attribute Values

```csharp
foreach (ObjectId attId in blockRef.AttributeCollection)
{
    AttributeReference attRef = (AttributeReference)tr.GetObject(
        attId, OpenMode.ForRead);
    ed.WriteMessage("Tag: {0}, Value: {1}\n",
        attRef.Tag, attRef.TextString);
}
```

### Writing Attribute Values

```csharp
foreach (ObjectId attId in blockRef.AttributeCollection)
{
    AttributeReference attRef = (AttributeReference)tr.GetObject(
        attId, OpenMode.ForWrite);
    if (attRef.Tag == "TITLE")
        attRef.TextString = "New Title";
}
```

## Dynamic Block Properties

```csharp
if (blockRef.IsDynamicBlock)
{
    // Get the original (non-anonymous) block name
    BlockTableRecord dynBtr = (BlockTableRecord)tr.GetObject(
        blockRef.DynamicBlockTableRecord, OpenMode.ForRead);
    string originalName = dynBtr.Name;

    // Read and write dynamic properties
    DynamicBlockReferencePropertyCollection props =
        blockRef.DynamicBlockReferencePropertyCollection;

    foreach (DynamicBlockReferenceProperty prop in props)
    {
        string name = prop.PropertyName;
        object val = prop.Value;
        bool readOnly = prop.ReadOnly;
        bool show = prop.Show;
        bool visible = prop.VisibleInCurrentVisibilityState;
        short typeCode = prop.PropertyTypeCode;
        DynamicBlockReferencePropertyUnitsType units = prop.UnitsType;
        string desc = prop.Description;

        // Get allowed values (for constrained properties)
        object[] allowedValues = prop.GetAllowedValues();

        ed.WriteMessage("  {0} = {1} (type: {2})\n", name, val, typeCode);
    }

    // Set a dynamic property value
    foreach (DynamicBlockReferenceProperty prop in props)
    {
        if (prop.PropertyName == "Distance" && !prop.ReadOnly)
        {
            prop.Value = 500.0;  // set new value
            break;
        }
    }
}
```

## Gotchas

- `BlockReference.Name` returns the anonymous block name for dynamic blocks (e.g., "*U42"); use `DynamicBlockTableRecord` to get the original name
- Attribute references must be added AFTER the block reference is added to the space - call `AppendEntity` and `AddNewlyCreatedDBObject` on the block ref first
- `SetAttributeFromBlock(attDef, blockRef.BlockTransform)` is essential - it positions the attribute correctly based on the block's transform; without it, attributes appear at the wrong location
- `Constant` attributes have fixed values and are NOT included in `AttributeCollection` on the block reference
- When iterating block definition entities to find AttributeDefinitions, not every entity is an AttDef - always check for null after cast
- `BlockTableRecord.ModelSpace` and `PaperSpace` are string constants for the standard space names, not references to the blocks themselves
- `ExplodeToOwnerSpace()` adds exploded entities to the parent and erases the block reference; cannot be undone without transaction rollback
- `ConvertToStaticBlock()` on a dynamic block reference permanently freezes the current state - the reference can no longer access dynamic properties
- Dynamic block property `Value` is typed as `object` - cast to the appropriate type (double, string, Point3d, etc.) based on `PropertyTypeCode`
- `GetBlockReferenceIds(true, false)` returns only direct references; use `(false, true)` to include nested references and force validity checks

## Related Skills

- `acad-layers` — block references and entities within blocks inherit layer properties
- `acad-editor-input` — selecting block references with GetEntity or selection filters (DxfCode.Start `"INSERT"`)
- `acad-mleaders` — block references as MLeader block content
