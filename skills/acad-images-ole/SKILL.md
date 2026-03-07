---
name: acad-images-ole
description: Raster images, image definitions, image clipping, OLE objects, PDF/DWF/DGN underlays, wipeouts, image adjustment, underlay layer filtering
---

# AutoCAD Images, Underlays, and OLE Objects

Use this skill when inserting or manipulating raster images, PDF/DWF/DGN underlays, OLE embedded objects, or wipeout masking entities in AutoCAD drawings.

## Raster Image Definition

Every raster image requires a `RasterImageDef` stored in the `ACAD_IMAGE_DICT` dictionary. The definition holds the source file path and resolution; multiple `RasterImage` entities can reference the same definition.

```csharp
public static ObjectId GetOrCreateImageDef(Database db, Transaction tr,
    string imagePath, string dictKey)
{
    ObjectId imageDictId = RasterImageDef.GetImageDictionary(db);
    if (imageDictId.IsNull)
        imageDictId = RasterImageDef.CreateImageDictionary(db);

    DBDictionary imageDict = (DBDictionary)tr.GetObject(
        imageDictId, OpenMode.ForWrite);

    if (imageDict.Contains(dictKey))
        return imageDict.GetAt(dictKey);

    RasterImageDef imageDef = new RasterImageDef();
    imageDef.SourceFileName = imagePath;
    imageDef.Load();  // reads file to get resolution and pixel dimensions

    ObjectId defId = imageDict.SetAt(dictKey, imageDef);
    tr.AddNewlyCreatedDBObject(imageDef, true);
    return defId;
}
```

### RasterImageDef Properties

- `SourceFileName` (string, get/set) — stored file path (absolute or relative)
- `ActiveFileName` (string, get) — resolved path AutoCAD actually found
- `Size` (Vector2d, get) — pixel dimensions (width, height)
- `ResolutionMMPerPixel` (Vector2d, get/set) — resolution in mm per pixel
- `ResolutionUnits` (ResolutionUnit, get/set) — None=0, Centimeter=1, Inch=2
- `IsLoaded` (bool, get) — true if image data is loaded in memory
- `IsEmbedded` (bool, get) — true if image data is embedded in the DWG

### RasterImageDef Methods

- `Load()` — load image data from file into memory
- `Unload()` — release image data from memory
- `Embed()` — embed image data into the drawing file
- `GetImageDictionary(Database db)` → ObjectId — get the image dictionary (static)
- `CreateImageDictionary(Database db)` → ObjectId — create the image dictionary (static)

## RasterImageDefReactor

A `RasterImageDefReactor` keeps an image definition alive while `RasterImage` entities reference it. Without a reactor, the definition can be purged prematurely.

```csharp
RasterImageDefReactor reactor = new RasterImageDefReactor();
reactor.ImageDefId = imageDefId;
btr.AppendEntity(reactor);
tr.AddNewlyCreatedDBObject(reactor, true);

rasterImage.ReactorId = reactor.ObjectId;
```

## Inserting a Raster Image

```csharp
public static ObjectId InsertRasterImage(Database db, ObjectId imageDefId,
    Point3d insertionPt, double widthInDrawingUnits)
{
    using (Transaction tr = db.TransactionManager.StartTransaction())
    {
        BlockTableRecord btr = (BlockTableRecord)tr.GetObject(
            db.CurrentSpaceId, OpenMode.ForWrite);
        RasterImageDef imageDef = (RasterImageDef)tr.GetObject(
            imageDefId, OpenMode.ForRead);

        RasterImage image = new RasterImage();
        image.SetDatabaseDefaults();
        image.ImageDefId = imageDefId;

        // U/V vectors represent FULL width and height in drawing units
        Vector2d pixelSize = imageDef.Size;
        double height = widthInDrawingUnits * (pixelSize.Y / pixelSize.X);

        image.Orientation = new CoordinateSystem3d(insertionPt,
            Vector3d.XAxis * widthInDrawingUnits,
            Vector3d.YAxis * height);

        btr.AppendEntity(image);
        tr.AddNewlyCreatedDBObject(image, true);

        // Attach reactor to keep definition alive
        RasterImageDefReactor reactor = new RasterImageDefReactor();
        reactor.ImageDefId = imageDefId;
        btr.AppendEntity(reactor);
        tr.AddNewlyCreatedDBObject(reactor, true);
        image.ReactorId = reactor.ObjectId;

        // Associate image with its definition for xref-style tracking
        image.AssociateRasterDef(imageDef);

        tr.Commit();
        return image.ObjectId;
    }
}
```

## Image Clipping

Clip boundaries are specified in image pixel coordinates (origin at bottom-left corner of the image).

```csharp
// Rectangular clip — exactly 2 points (lower-left, upper-right)
Point2dCollection rectPts = new Point2dCollection();
rectPts.Add(new Point2d(100, 100));   // lower-left in pixels
rectPts.Add(new Point2d(400, 300));   // upper-right in pixels
rasterImage.SetClipBoundary(ClipBoundaryType.Rectangle, rectPts);
rasterImage.IsClipped = true;

// Polygonal clip — 3+ vertices, first and last must match to close
Point2dCollection polyPts = new Point2dCollection();
polyPts.Add(new Point2d(50, 50));
polyPts.Add(new Point2d(300, 50));
polyPts.Add(new Point2d(300, 250));
polyPts.Add(new Point2d(150, 300));
polyPts.Add(new Point2d(50, 50));  // close
rasterImage.SetClipBoundary(ClipBoundaryType.Poly, polyPts);
rasterImage.IsClipped = true;

// Reset clip to full image
rasterImage.SetClipBoundaryToWholeImage();
rasterImage.IsClipped = false;

// Read existing clip boundary
ClipBoundary clip = rasterImage.GetClipBoundary();
// clip.ClipPoints — 2 points for rectangle, N+1 for polygon
```

### Converting Drawing Coordinates to Pixel Coordinates

```csharp
// Use the inverse of PixelToModelTransform to convert WCS points to pixels
Matrix3d pixelToModel = rasterImage.PixelToModelTransform;
Matrix3d modelToPixel = pixelToModel.Inverse();

Point3d wcsPoint = new Point3d(50.0, 25.0, 0.0);
Point3d pixelPoint = wcsPoint.TransformBy(modelToPixel);
Point2d clipPt = new Point2d(pixelPoint.X, pixelPoint.Y);
```

## RasterImage Properties

- `ShowImage` (bool, get/set) — show or hide image raster data
- `IsClipped` (bool, get/set) — enable or disable clipping
- `ClipInverted` (bool, get/set) — invert clip region (show outside, hide inside)
- `ImageTransparency` (bool, get/set) — honor transparent pixels
- `Orientation` (CoordinateSystem3d, get/set) — origin, U-vector (width), V-vector (height)
- `ImageDefId` (ObjectId, get/set) — link to the RasterImageDef
- `ReactorId` (ObjectId, get/set) — link to the RasterImageDefReactor
- `Brightness` (sbyte, get/set) — 0 to 100, default 50
- `Contrast` (sbyte, get/set) — 0 to 100, default 50
- `Fade` (sbyte, get/set) — 0 to 100, default 0
- `PixelToModelTransform` (Matrix3d, get) — transform from pixel space to WCS

### RasterImage Methods

- `SetClipBoundary(ClipBoundaryType type, Point2dCollection pts)` — set clip boundary
- `SetClipBoundaryToWholeImage()` — reset clip to full image extents
- `GetClipBoundary()` → ClipBoundary — read existing clip boundary
- `AssociateRasterDef(RasterImageDef def)` — bind image to its definition for reactor tracking

## RasterVariables

Drawing-wide image display settings stored in the named object dictionary.

```csharp
ObjectId rvId = RasterVariables.GetRasterVariables(db);
if (rvId.IsNull)
    rvId = RasterVariables.CreateRasterVariables(db);

RasterVariables rv = (RasterVariables)tr.GetObject(rvId, OpenMode.ForWrite);
rv.ImageFrame = ImageFrameType.DisplayedNotPlotted;
// ImageFrameType: None=0, DisplayedAndPlotted=1, DisplayedNotPlotted=2
rv.ImageQuality = ImageQualityType.High;  // Draft=0, High=1
rv.UserScale = 1.0;
```

## PDF Underlay

PDF underlays use a definition/reference pair: `PdfDefinition` + `PdfReference`. The definition lives in the `ACAD_PDFDEFINITIONS` named dictionary.

```csharp
public static ObjectId InsertPdfUnderlay(Database db, string pdfPath,
    int pageNumber, Point3d insertionPt, double scale)
{
    using (Transaction tr = db.TransactionManager.StartTransaction())
    {
        BlockTableRecord btr = (BlockTableRecord)tr.GetObject(
            db.CurrentSpaceId, OpenMode.ForWrite);

        // Get or create the PDF definitions dictionary
        ObjectId pdDictId = UnderlayDefinition.GetDictionaryId(db,
            new PdfDefinition().GetType());
        if (pdDictId.IsNull)
            pdDictId = UnderlayDefinition.CreateDictionary(db,
                new PdfDefinition().GetType());

        DBDictionary pdfDict = (DBDictionary)tr.GetObject(
            pdDictId, OpenMode.ForWrite);

        PdfDefinition pdfDef = new PdfDefinition();
        pdfDef.SourceFileName = pdfPath;
        pdfDef.ItemName = pageNumber.ToString();  // 1-based page number
        ObjectId pdfDefId = pdfDict.SetAt(
            "MyPdf_Page" + pageNumber, pdfDef);
        tr.AddNewlyCreatedDBObject(pdfDef, true);

        PdfReference pdfRef = new PdfReference();
        pdfRef.SetDatabaseDefaults();
        pdfRef.DefinitionId = pdfDefId;
        pdfRef.Position = insertionPt;
        pdfRef.ScaleFactors = new Scale3d(scale, scale, scale);
        pdfRef.Rotation = 0.0;

        btr.AppendEntity(pdfRef);
        tr.AddNewlyCreatedDBObject(pdfRef, true);

        tr.Commit();
        return pdfRef.ObjectId;
    }
}
```

## DWF and DGN Underlays

DWF and DGN underlays follow the identical definition/reference pattern with swapped types:

| Format | Definition | Reference | Dictionary | ItemName |
|--------|-----------|-----------|------------|----------|
| PDF | `PdfDefinition` | `PdfReference` | `ACAD_PDFDEFINITIONS` | Page number |
| DWF | `DwfDefinition` | `DwfReference` | `ACAD_DWFDEFINITIONS` | Sheet name |
| DGN | `DgnDefinition` | `DgnReference` | `ACAD_DGNDEFINITIONS` | Model name |

## Underlay Common Properties

All underlay references inherit from `UnderlayReference`:

- `Position` (Point3d, get/set) — insertion point
- `ScaleFactors` (Scale3d, get/set) — X, Y, Z scale factors
- `Rotation` (double, get/set) — rotation angle in radians
- `DefinitionId` (ObjectId, get/set) — link to the underlay definition
- `IsOn` (bool, get/set) — visibility toggle
- `IsMonochrome` (bool, get/set) — monochrome display
- `AdjustContrast` (sbyte, get/set) — contrast (0-100)
- `AdjustFade` (sbyte, get/set) — fade (0-100)
- `IsClipped` (bool, get/set) — enable clipping
- `ClipInverted` (bool, get/set) — invert clip region
- `UnderlayLayerCount` (int, get) — number of layers in the underlay

### Underlay Clipping and Layer Filtering

```csharp
// Clip underlay — 2 points = rectangle, 3+ = polygon (in underlay space)
Point2dCollection clipPts = new Point2dCollection();
clipPts.Add(new Point2d(0, 0));
clipPts.Add(new Point2d(500, 350));
pdfRef.SetClipBoundary(clipPts);
pdfRef.IsClipped = true;

// Filter underlay layers
for (int i = 0; i < pdfRef.UnderlayLayerCount; i++)
{
    UnderlayLayer layer = pdfRef.GetUnderlayLayer(i);
    string name = layer.Name;
    layer.State = UnderlayLayerState.Off;  // On or Off
}
```

## OLE Objects (Ole2Frame)

OLE objects embed or link external documents (Excel, Word, images) in the drawing. The .NET API cannot create new OLE objects programmatically; use COM automation or `SendStringToExecute` with the `INSERTOBJ` command instead.

### Ole2Frame Properties

- `Position3d` (Point3d, get/set) — WCS coordinates of the four corners
- `Location` (Point3d, get/set) — lower-left corner of the OLE display rectangle
- `LinkPath` (string, get) — file path if linked; empty if embedded
- `Type` (Ole2Frame.ItemType, get) — Link, Embedded, or Static
- `UserType` (string, get) — display type string (e.g., "Paintbrush Bitmap")
- `OutputQuality` (OleOutputQuality, get/set) — LineArt=0, Text=1, Graphics=2, Photo=3, HighPhoto=4
- `AutoOutputQuality` (bool, get/set) — automatic plot quality selection
- `WcsWidth` (double, get/set) — width in WCS drawing units
- `WcsHeight` (double, get/set) — height in WCS drawing units
- `ScaleWidth` (double, get/set) — scale relative to original size
- `ScaleHeight` (double, get/set) — scale relative to original size
- `LockAspect` (bool, get/set) — maintain aspect ratio
- `Rotation` (double, get/set) — rotation angle in radians
- `IsLinked` (bool, get) — true if object is linked rather than embedded

### Iterating OLE Objects

```csharp
foreach (ObjectId entId in btr)
{
    Entity ent = (Entity)tr.GetObject(entId, OpenMode.ForRead);
    if (ent is Ole2Frame ole)
    {
        ed.WriteMessage("\nOLE: {0}, Linked={1}", ole.UserType, ole.IsLinked);
        if (ole.IsLinked)
            ed.WriteMessage(", Path={0}", ole.LinkPath);

        // Reposition an OLE object
        ole.UpgradeOpen();
        ole.Location = new Point3d(100, 200, 0);
        ole.WcsWidth = 50.0;
        ole.WcsHeight = 30.0;
    }
}
```

## Wipeout Entity

A `Wipeout` masks entities behind it with the background color. It inherits from `RasterImage`.

```csharp
public static ObjectId CreateWipeout(Database db, Point2dCollection boundary)
{
    using (Transaction tr = db.TransactionManager.StartTransaction())
    {
        BlockTableRecord btr = (BlockTableRecord)tr.GetObject(
            db.CurrentSpaceId, OpenMode.ForWrite);

        Wipeout wipeout = new Wipeout();
        wipeout.SetDatabaseDefaults();
        wipeout.SetFrom(boundary, Vector3d.ZAxis);

        btr.AppendEntity(wipeout);
        tr.AddNewlyCreatedDBObject(wipeout, true);

        tr.Commit();
        return wipeout.ObjectId;
    }
}

// Boundary must be a closed polygon (first point = last point)
Point2dCollection pts = new Point2dCollection();
pts.Add(new Point2d(0, 0));
pts.Add(new Point2d(100, 0));
pts.Add(new Point2d(100, 50));
pts.Add(new Point2d(0, 50));
pts.Add(new Point2d(0, 0));
```

### Wipeout Frame and Draw Order

```csharp
// Frame visibility: 0=hidden, 1=displayed+plotted, 2=displayed not plotted
Application.SetSystemVariable("WIPEOUTFRAME", 2);

// Draw order — wipeout must be behind text but in front of hidden entities
DrawOrderTable dot = (DrawOrderTable)tr.GetObject(
    btr.DrawOrderTableId, OpenMode.ForWrite);
ObjectIdCollection ids = new ObjectIdCollection { wipeoutId };
dot.MoveBelow(ids, entityAboveId);
```

## Gotchas

- `RasterImageDef.Load()` throws if the image file does not exist — verify the path or wrap in try/catch
- `Orientation` on `RasterImage` uses U and V vectors representing the FULL width and height in drawing units, NOT unit vectors — setting unit vectors produces a 1x1 unit image
- `RasterImageDefReactor` is required to prevent image definitions from being purged — always create and attach one per image entity
- `RasterImageDef.GetImageDictionary()` returns `ObjectId.Null` if no images exist yet — always check and call `CreateImageDictionary()` if null
- Image clip boundary coordinates are in pixel space (not drawing units) — use the inverse of `PixelToModelTransform` to convert from WCS
- `ClipBoundaryType.Rectangle` requires exactly 2 points (lower-left, upper-right) — `ClipBoundaryType.Poly` requires 3+ points with first = last to close
- Wipeout boundary must be a closed polygon (first = last point) — if it appears inverted, reverse the point winding order
- PDF underlay `ItemName` must be a valid page number string (e.g., "1") — invalid values throw `eInvalidValue` or `eOutOfRange`
- Underlay clip coordinates are in the underlay's own coordinate system (relative to insertion and scale), not WCS
- `Ole2Frame` cannot be created programmatically via the .NET API — use COM automation or `SendStringToExecute("INSERTOBJ\n")` to embed new OLE content
- `UnderlayDefinition.GetDictionaryId()` and `CreateDictionary()` require the concrete type (e.g., `typeof(PdfDefinition)`) to locate the correct named dictionary
- Bitonal (1-bit) raster images cannot be adjusted for brightness, contrast, or fade
- `AssociateRasterDef()` must be called AFTER the `RasterImage` is added to the database — it establishes the reactor connection between image and definition

## Related Skills

- `acad-blocks` — images and underlays inserted inside block definitions
- `acad-layers` — layer assignment for image, underlay, wipeout, and OLE entities
- `acad-geometry` — CoordinateSystem3d orientation vectors and Matrix3d transforms for image positioning
- `acad-xrefs` — underlays vs xrefs: underlays are display-only while xrefs bring full DWG geometry
