---
name: acad-events-overrules
description: Database events, document events, application events, editor events, ObjectOverrule, DrawableOverrule, TransformOverrule, GripOverrule, overrule registration and filtering
---

# AutoCAD Events and Overrules

Use this skill when subscribing to database, document, application, or editor events, or when overriding default entity behavior via ObjectOverrule, DrawableOverrule, TransformOverrule, or GripOverrule.

## Database Events

Database events fire when objects are added, modified, or erased. Subscribe via the `Database` object.

```csharp
Database db = HostApplicationServices.WorkingDatabase;

db.ObjectAppended += OnObjectAppended;
db.ObjectErased += OnObjectErased;
db.ObjectModified += OnObjectModified;
db.ObjectOpenedForModify += OnObjectOpenedForModify;
```

### ObjectAppended

Fires after a new object is added to the database (after `AddNewlyCreatedDBObject`).

```csharp
private void OnObjectAppended(object sender, ObjectEventArgs e)
{
    ObjectId id = e.DBObject.ObjectId;
    // e.DBObject is the newly added object — read-only at this point
}
```

### ObjectErased

Fires when an object is erased or unerased. Check `e.Erased` to distinguish.

```csharp
private void OnObjectErased(object sender, ObjectErasedEventArgs e)
{
    if (e.Erased)
    {
        // Object was erased
    }
    else
    {
        // Object was unerased (undo)
    }
}
```

### ObjectModified / ObjectOpenedForModify

`ObjectOpenedForModify` fires when opened for write (before changes). `ObjectModified` fires after modification and close. Both use `ObjectEventArgs` with `e.DBObject`.

## Document Events

Subscribe via individual `Document` objects. Also: `CommandFailed`, `LispWillStart`, `LispEnded`.

```csharp
Document doc = Application.DocumentManager.MdiActiveDocument;

doc.CommandWillStart += OnCommandWillStart;
doc.CommandEnded += OnCommandEnded;
doc.CommandCancelled += OnCommandCancelled;
```

### DocumentLockModeChanged

Fires when the document lock mode changes (e.g., entering or leaving a command context).

```csharp
doc.LockModeChanged += OnLockModeChanged;

private void OnLockModeChanged(object sender, DocumentLockModeChangedEventArgs e)
{
    string commandName = e.GlobalCommandName;
    DocumentLockMode currentMode = e.CurrentMode;
    // Veto the lock change: e.Veto();
}
```

## DocumentCollection Events

Subscribe via `Application.DocumentManager`. Also: `DocumentToBeActivated`, `DocumentToBeDeactivated`, `DocumentCreateStarted`, `DocumentLockModeWillChange`.

```csharp
DocumentCollection docMgr = Application.DocumentManager;

docMgr.DocumentCreated += OnDocumentCreated;
docMgr.DocumentToBeDestroyed += OnDocumentToBeDestroyed;
docMgr.DocumentActivated += OnDocumentActivated;
docMgr.DocumentBecameCurrent += OnDocumentBecameCurrent;
```

### Typical Document Lifecycle Handler

```csharp
private void OnDocumentCreated(object sender, DocumentCollectionEventArgs e)
{
    // Subscribe to per-document events on the new document
    e.Document?.Database.ObjectModified += OnObjectModified;
}

private void OnDocumentToBeDestroyed(object sender, DocumentCollectionEventArgs e)
{
    // Unsubscribe per-document events before it closes
    e.Document?.Database.ObjectModified -= OnObjectModified;
}
```

## Application Events

Global events on the `Application` class or `SystemVariableChanged` on `Application`.

```csharp
Application.SystemVariableChanged += OnSysVarChanged;
Application.Idle += OnIdle;
Application.QuitWillStart += OnQuitWillStart;
```

### SystemVariableChanged

```csharp
private void OnSysVarChanged(object sender, SystemVariableChangedEventArgs e)
{
    if (e.Name == "CLAYER" && e.Changed)
    {
        // Current layer changed — update UI
    }
}
```

### Idle

Fires when AutoCAD is idle (no commands running). Useful for deferred processing.

```csharp
private void OnIdle(object sender, EventArgs e)
{
    Application.Idle -= OnIdle;  // unsubscribe to avoid repeated firing
    ProcessDeferredWork();
}
```

## Editor Events

Subscribe via `Editor` for selection and input monitoring.

```csharp
Editor ed = doc.Editor;

ed.SelectionAdded += OnSelectionAdded;
ed.SelectionRemoved += OnSelectionRemoved;
ed.PointMonitor += OnPointMonitor;
```

### SelectionAdded

Fires when entities are added to the current selection set.

```csharp
private void OnSelectionAdded(object sender, SelectionAddedEventArgs e)
{
    ObjectId[] addedIds = e.AddedObjects.GetObjectIds();
    // Inspect or veto selection:
    // e.Remove(index) to reject specific entities
}
```

### PointMonitor

Fires continuously as the cursor moves. Use sparingly — it runs on every mouse move.

```csharp
private void OnPointMonitor(object sender, PointMonitorEventArgs e)
{
    Point3d currentPoint = e.Context.ComputedPoint;

    // Get entities under the cursor
    FullSubentityPath[] paths = e.Context.GetPickedEntities();

    // Append to tooltip
    e.AppendToolTipText("Custom tooltip text");
}
```

## ObjectOverrule

Override fundamental object operations: Open, Close, Erase, DeepClone.

```csharp
public class MyObjectOverrule : ObjectOverrule
{
    public override void Erase(DBObject dbObject, bool erasing)
    {
        if (erasing)
        {
            // Prevent erase by throwing ErrorStatus.NotAllowedForThisProxy
        }
        base.Erase(dbObject, erasing);
    }

    // Also overridable: Open, Close, DeepClone
}
```

## DrawableOverrule

Customize how entities are drawn. Override `WorldDraw` and/or `ViewportDraw`.

```csharp
public class MyDrawableOverrule : DrawableOverrule
{
    public override bool WorldDraw(Drawable drawable, WorldDraw wd)
    {
        // Cast to the specific entity type
        Circle circle = drawable as Circle;
        if (circle == null) return base.WorldDraw(drawable, wd);

        // Draw default geometry first
        bool result = base.WorldDraw(drawable, wd);

        // Add custom graphics — draw a crosshair at center
        double r = circle.Radius * 0.5;
        Point3d c = circle.Center;
        wd.Geometry.WorldLine(
            new Point3d(c.X - r, c.Y, c.Z), new Point3d(c.X + r, c.Y, c.Z));
        wd.Geometry.WorldLine(
            new Point3d(c.X, c.Y - r, c.Z), new Point3d(c.X, c.Y + r, c.Z));

        return result;
    }

    public override int SetAttributes(Drawable drawable, DrawableTraits traits)
    {
        int flags = base.SetAttributes(drawable, traits);
        traits.Color = 1;  // force red
        return flags;
    }

    // ViewportDraw — override for per-viewport / view-dependent graphics
    // vd.Context.IsPlotGeneration is true when printing
}
```

## TransformOverrule

Control how entities respond to move, rotate, scale, and mirror operations.

```csharp
public class MyTransformOverrule : TransformOverrule
{
    public override void TransformBy(Entity entity, Matrix3d transform)
    {
        // Example: restrict movement to X axis only
        Vector3d delta = Point3d.Origin.TransformBy(transform) - Point3d.Origin;
        if (Math.Abs(delta.Y) > Tolerance.Global.EqualPoint)
        {
            Matrix3d xOnly = Matrix3d.Displacement(new Vector3d(delta.X, 0, 0));
            base.TransformBy(entity, xOnly);
            return;
        }
        base.TransformBy(entity, transform);
    }

    // Also overridable: Explode
}
```

## GripOverrule

Define custom grip points and stretch behavior for entities.

```csharp
public class MyGripOverrule : GripOverrule
{
    public override void GetGripPoints(Entity entity,
        GripDataCollection grips, double curViewUnitSize,
        int gripSize, Vector3d curViewDir, GetGripPointsFlags bitFlags)
    {
        base.GetGripPoints(entity, grips, curViewUnitSize,
            gripSize, curViewDir, bitFlags);

        // Add a custom grip at midpoint of a line
        Line line = entity as Line;
        if (line != null)
        {
            GripData grip = new GripData();
            grip.GripPoint = line.StartPoint +
                (line.EndPoint - line.StartPoint) * 0.5;
            grips.Add(grip);
        }
    }

    public override void MoveGripPointsAt(Entity entity,
        GripDataCollection grips, Vector3d offset, MoveGripPointsFlags bitFlags)
    {
        base.MoveGripPointsAt(entity, grips, offset, bitFlags);
    }
}
```

## Overrule Registration

### AddOverrule / RemoveOverrule

```csharp
// Register — third parameter: false = end of chain, true = beginning
Overrule.AddOverrule(RXObject.GetClass(typeof(Circle)), drawOverrule, false);

// Enable the overrule system globally (required)
Overrule.Overruling = true;

// Remove when done (e.g., in IExtensionApplication.Terminate)
Overrule.RemoveOverrule(RXObject.GetClass(typeof(Circle)), drawOverrule);
```

### SetIdFilter

Restrict an overrule to specific objects by ObjectId.

```csharp
overrule.SetIdFilter(new ObjectId[] { circleId1, circleId2 });
```

### SetXDataFilter

Restrict an overrule to objects with specific XData.

```csharp
overrule.SetXDataFilter(new string[] { "MyAppName" });
```

### Toggling Overrules

`Overrule.Overruling = false` disables all overrules globally without removing them. Set back to `true` to re-enable.

## Plugin Lifecycle Example

Manage events and overrules in `IExtensionApplication.Initialize` / `Terminate`.

```csharp
public class MyPlugin : IExtensionApplication
{
    private static MyDrawableOverrule _drawOverrule;

    public void Initialize()
    {
        Application.DocumentManager.DocumentCreated += OnDocCreated;
        Application.DocumentManager.DocumentToBeDestroyed += OnDocClosing;

        _drawOverrule = new MyDrawableOverrule();
        Overrule.AddOverrule(
            RXObject.GetClass(typeof(Circle)), _drawOverrule, false);
        Overrule.Overruling = true;

        // Subscribe to the already-open document
        Document doc = Application.DocumentManager.MdiActiveDocument;
        if (doc != null)
            doc.Database.ObjectModified += OnObjectModified;
    }

    public void Terminate()
    {
        Application.DocumentManager.DocumentCreated -= OnDocCreated;
        Application.DocumentManager.DocumentToBeDestroyed -= OnDocClosing;
        if (_drawOverrule != null)
            Overrule.RemoveOverrule(
                RXObject.GetClass(typeof(Circle)), _drawOverrule);
    }

    private void OnDocCreated(object sender, DocumentCollectionEventArgs e)
        => e.Document?.Database.ObjectModified += OnObjectModified;
    private void OnDocClosing(object sender, DocumentCollectionEventArgs e)
        => e.Document?.Database.ObjectModified -= OnObjectModified;
    private static void OnObjectModified(object sender, ObjectEventArgs e) { }
}
```

## Gotchas

- **Never modify the database inside `ObjectModified` or `ObjectAppended` handlers** — the transaction is still active and re-entrant modifications crash. Defer work to `Application.Idle`.
- **Always unsubscribe events** when documents close or the plugin terminates. Leaked handlers cause null reference exceptions.
- **`PointMonitor` runs on every mouse move** — keep the handler fast. Cache results and only recalculate when the cursor moves significantly.
- **`Overrule.Overruling` is a global toggle** — `false` disables all overrules in the session, including other plugins'.
- **`ObjectErased` fires for both erase and unerase** — always check `e.Erased`. Undo triggers unerase events.
- **`SetIdFilter` references are not weak** — erased objects stay in the filter. Clear or reset when targets change.
- **`DrawableOverrule.WorldDraw` must call `base.WorldDraw`** — skipping it makes the entity disappear.
- **Thread safety** — handlers run on the main thread. Use `DocumentManager.ExecuteInApplicationContext` for cross-thread work; never access `MdiActiveDocument` from background threads.
- **`TransformOverrule.TransformBy` receives the cumulative transform** — displacement for move, rotation matrix for rotate.
- **`GripOverrule.GetGripPoints` with `GripDataCollection`** is the newer API; the older `Point3dCollection` overload lacks custom grip styling.
- **Overrule class type must match the runtime class** — `typeof(Entity)` for broad match, `typeof(Line)` for specific. Derived classes inherit parent overrules.
- **`SelectionAdded` can veto via `e.Remove(index)`** — out-of-range index corrupts the selection set silently.
- **`SystemVariableChanged` fires even when unchanged** — check `e.Changed` to filter no-ops.

## Related Skills

- `acad-database-operations` — transactions and object access patterns used in event handlers
- `acad-editor-input` — `SelectionAdded` and `PointMonitor` events extend editor interaction
- `acad-geometry` — `Point3d`, `Matrix3d`, and `Vector3d` used throughout transform and grip overrules
- `acad-blocks` — overrules can target `BlockReference` entities for custom grip and display behavior
