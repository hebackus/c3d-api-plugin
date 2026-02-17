---
name: acad-tables
description: Tables - creation, cell content (text, blocks, fields), formatting, row/column operations, merging, table styles, data linking
---

# AutoCAD Tables

Use this skill when creating or modifying Table objects - creating tables, setting cell content (text, blocks, fields), formatting cells, inserting/deleting rows and columns, merging cells, and managing table styles.

## Table Creation

`Table` inherits from `BlockReference`. Insert it into model/paper space like any other entity.

```csharp
using Autodesk.AutoCAD.DatabaseServices;
using Autodesk.AutoCAD.Geometry;

Database db = HostApplicationServices.WorkingDatabase;
using (Transaction tr = db.TransactionManager.StartTransaction())
{
    BlockTableRecord btr = (BlockTableRecord)tr.GetObject(
        db.CurrentSpaceId, OpenMode.ForWrite);

    Table table = new Table();
    table.TableStyle = db.Tablestyle;  // current table style
    table.Position = new Point3d(0, 0, 0);

    // Set size first, then dimensions
    table.SetSize(5, 3);  // 5 rows, 3 columns (includes title + header rows)
    table.SetRowHeight(8.0);           // uniform row height
    table.SetColumnWidth(40.0);        // uniform column width

    // Set individual column widths
    table.Columns[0].Width = 20.0;
    table.Columns[1].Width = 50.0;
    table.Columns[2].Width = 30.0;

    // Populate cells (row 0 = title, row 1 = header, rows 2+ = data)
    table.Cells[0, 0].TextString = "My Table Title";
    table.Cells[1, 0].TextString = "Name";
    table.Cells[1, 1].TextString = "Description";
    table.Cells[1, 2].TextString = "Value";
    table.Cells[2, 0].TextString = "Item A";
    table.Cells[2, 1].TextString = "First item";
    table.Cells[2, 2].TextString = "100";

    table.GenerateLayout();

    btr.AppendEntity(table);
    tr.AddNewlyCreatedDBObject(table, true);
    tr.Commit();
}
```

## Cell Content

Access cells via `table.Cells[row, column]` which returns a `Cell` object.

**Setting text:**
```csharp
table.Cells[2, 0].TextString = "Hello";

// Read text back
string text = table.Cells[2, 0].TextString;

// Get text with specific format option
string formatted = table.Cells[2, 0].GetTextString(FormatOption.ForExpression);
```

**Setting a block reference in a cell:**
```csharp
BlockTable bt = (BlockTable)tr.GetObject(db.BlockTableId, OpenMode.ForRead);
ObjectId blockId = bt["MyBlockName"];

table.Cells[2, 1].BlockTableRecordId = blockId;

// Access via Contents collection for multi-content cells
table.Cells[2, 1].Contents[0].BlockTableRecordId = blockId;
table.Cells[2, 1].Contents[0].IsAutoScale = true;   // auto-fit block to cell
table.Cells[2, 1].Contents[0].Scale = 1.0;           // or set explicit scale
table.Cells[2, 1].Contents[0].Rotation = 0.0;        // rotation in radians
```

**Setting a field in a cell:**
```csharp
Field field = new Field("%<\\AcVar Date \\f \"M/d/yyyy\">%");
ObjectId fieldId = db.AddField(field);
tr.AddNewlyCreatedDBObject(field, true);

table.Cells[2, 2].FieldId = fieldId;
// Or via Contents: table.Cells[2, 2].Contents[0].FieldId = fieldId;
```

**Setting typed values:**
```csharp
table.Cells[2, 0].Value = 42.5;
table.Cells[2, 0].SetValue(42.5, ParseOption.SetDefaultFormat);

// Read value back
object val = table.Cells[2, 0].Value;
object valFmt = table.Cells[2, 0].GetValue(FormatOption.ForExpression);
table.Cells[2, 0].ResetValue();  // clear value
```

**Formulas (via Contents):**
```csharp
table.Cells[4, 2].Contents[0].Formula = "=Sum(C3:C5)";
bool hasFormula = table.Cells[4, 2].Contents[0].HasFormula;
```

**Multiple content items per cell:**
```csharp
CellContentsCollection contents = table.Cells[2, 0].Contents;
int count = contents.Count;

contents.Add();                  // append new content slot
contents.InsertAt(0);            // insert at index
contents.RemoveAt(1);            // remove at index
contents.Move(0, 1);             // reorder
contents.Clear();                // remove all content

// Access individual content
CellContent c = contents[0];
c.TextString = "Text";
c.TextHeight = 2.5;
c.ContentColor = Color.FromColorIndex(ColorMethod.ByAci, 1);  // red
```

**Block attribute values in cells:**
```csharp
string attrVal = table.Cells[2, 1].GetBlockAttributeValue(attDefId);
table.Cells[2, 1].SetBlockAttributeValue(attDefId, "NewValue");
// Or via Contents: table.Cells[2, 1].Contents[0].GetBlockAttributeValue(attDefId);
```

## Cell Formatting

Formatting is accessed through the `CellRange` base class (which `Cell` inherits from), so these properties work on both individual cells and ranges.

**Alignment:**
```csharp
table.Cells[2, 0].Alignment = CellAlignment.MiddleCenter;
```

**Text height and style:**
```csharp
table.Cells[2, 0].TextHeight = 2.5;
table.Cells[2, 0].TextStyleId = styleId;

// Per-content text height
table.Cells[2, 0].Contents[0].TextHeight = 3.0;
table.Cells[2, 0].Contents[0].TextStyleId = styleId;
```

**Colors:**
```csharp
using Autodesk.AutoCAD.Colors;

// Content (text) color
table.Cells[2, 0].ContentColor = Color.FromColorIndex(ColorMethod.ByAci, 1); // red

// Background color
table.Cells[2, 0].BackgroundColor = Color.FromColorIndex(ColorMethod.ByAci, 5); // blue
table.Cells[2, 0].IsBackgroundColorNone = false; // must be false to show background
```

**Cell margins (via Borders):**
```csharp
CellBorders borders = table.Cells[2, 0].Borders;
borders.Top.Margin = 1.5;
borders.Bottom.Margin = 1.5;
borders.Left.Margin = 2.0;
borders.Right.Margin = 2.0;
```

**Grid lines (borders):**
```csharp
CellBorder topEdge = table.Cells[2, 0].Borders.Top;
topEdge.LineWeight = LineWeight.LineWeight050;
topEdge.Color = Color.FromColorIndex(ColorMethod.ByAci, 7);  // white
topEdge.IsVisible = true;
topEdge.Linetype = linetypeId;
topEdge.LineStyle = GridLineStyle.Single;     // Single or Double
topEdge.DoubleLineSpacing = 2.0;             // for Double line style

// Available borders: Top, Bottom, Left, Right, Horizontal, Vertical
```

**Content rotation:**
```csharp
table.Cells[2, 0].Contents[0].Rotation = Math.PI / 2;  // 90 degrees
```

**Data type and format:**
```csharp
table.Cells[2, 0].DataType = new DataTypeParameter(
    Autodesk.AutoCAD.DatabaseServices.DataType.Double,
    Autodesk.AutoCAD.DatabaseServices.UnitType.Distance);
table.Cells[2, 0].DataFormat = "%lu2%pr2";  // 2 decimal places
table.Cells[2, 0].Contents[0].DataFormat = "%lu2%pr2";
```

**Cell style and state:**
```csharp
table.Cells[2, 0].Style = "_DATA";    // cell style name: "_TITLE", "_HEADER", "_DATA", or custom
table.Cells[2, 0].State = CellStates.None;
table.Cells[2, 0].ContentLayout = CellContentLayout.Flow;
table.Cells[2, 0].IsMergeAllEnabled = true;
```

**Apply formatting to a range:**
```csharp
CellRange range = CellRange.Create(table, 2, 0, 4, 2);  // rows 2-4, cols 0-2
range.Alignment = CellAlignment.MiddleLeft;
range.TextHeight = 2.0;
range.ContentColor = Color.FromColorIndex(ColorMethod.ByAci, 3);
range.BackgroundColor = Color.FromColorIndex(ColorMethod.ByAci, 254);
range.IsBackgroundColorNone = false;
```

## Row and Column Operations

**Access counts:**
```csharp
int rowCount = table.Rows.Count;
int colCount = table.Columns.Count;
```

**Insert rows/columns:**
```csharp
table.InsertRows(2, 8.0, 3);      // insert 3 rows at index 2, height 8.0
table.InsertColumns(1, 40.0, 2);   // insert 2 columns at index 1, width 40.0

// Insert and inherit formatting from an existing row/column
table.InsertRowsAndInherit(3, 2, 1);      // insert 1 row at index 3, inherit from row 2
table.InsertColumnsAndInherit(2, 1, 1);   // insert 1 col at index 2, inherit from col 1
```

**Delete rows/columns:**
```csharp
table.DeleteRows(2, 1);       // delete 1 row starting at index 2
table.DeleteColumns(1, 2);    // delete 2 columns starting at index 1
```

**Resize rows/columns:**
```csharp
// Individual row height
table.Rows[2].Height = 12.0;
double minH = table.Rows[2].MinimumHeight;

// Individual column width
table.Columns[1].Width = 60.0;
double minW = table.Columns[1].MinimumWidth;

// Column name
table.Columns[0].Name = "ID";
string name = table.Columns[0].Name;

// Uniform sizing
table.SetRowHeight(8.0);      // all rows same height
table.SetColumnWidth(40.0);   // all columns same width

// Resize entire table
table.SetSize(10, 5);         // resize to 10 rows, 5 columns
table.Height = 200.0;         // overall table height
table.Width = 300.0;          // overall table width
```

## Cell Merging

```csharp
// Merge a range of cells (topRow, leftCol, bottomRow, rightCol)
CellRange range = CellRange.Create(table, 2, 0, 2, 2);
table.MergeCells(range);

// Unmerge
table.UnmergeCells(range);

// Check if a cell is merged and get its merge range
Cell cell = table.Cells[2, 0];
CellRange mergeRange = cell.GetMergeRange();
bool? isMerged = mergeRange.IsMerged;
```

## Table Styles

Table styles are stored in the `TableStyleDictionary`. The `TableStyle` object defines default formatting for title, header, and data rows.

**Create a new table style:**
```csharp
using Autodesk.AutoCAD.DatabaseServices;
using Autodesk.AutoCAD.Colors;

Database db = HostApplicationServices.WorkingDatabase;
using (Transaction tr = db.TransactionManager.StartTransaction())
{
    TableStyle style = new TableStyle();
    style.Description = "Custom pipe schedule style";

    // Flow direction
    style.FlowDirection = FlowDirection.TopToBottom;

    // Suppress title/header rows
    style.IsTitleSuppressed = false;
    style.IsHeaderSuppressed = false;

    // Cell margins
    style.HorizontalCellMargin = 1.5;
    style.VerticalCellMargin = 1.5;

    // Text height per row type (RowType: TitleRow=1, HeaderRow=2, DataRow=4)
    style.SetTextHeight(3.5, (int)RowType.TitleRow);
    style.SetTextHeight(2.5, (int)RowType.HeaderRow);
    style.SetTextHeight(2.0, (int)RowType.DataRow);

    // Text style per row type
    style.SetTextStyle(textStyleId, (int)RowType.DataRow);

    // Alignment per row type
    style.SetAlignment(CellAlignment.MiddleCenter, (int)RowType.TitleRow);
    style.SetAlignment(CellAlignment.MiddleCenter, (int)RowType.HeaderRow);
    style.SetAlignment(CellAlignment.MiddleLeft, (int)RowType.DataRow);

    // Colors per row type
    style.SetColor(Color.FromColorIndex(ColorMethod.ByAci, 7), (int)RowType.TitleRow);
    style.SetBackgroundColorNone(true, (int)RowType.DataRow);

    // Grid line weights (GridLineType: OuterGridLines=1, InnerGridLines=2, HorizontalGridLines=4,
    //   VerticalGridLines=8, BottomGridLines=16, All combinations via bitflags)
    style.SetGridLineWeight(LineWeight.LineWeight050,
        (int)GridLineType.OuterGridLines, (int)RowType.DataRow);
    style.SetGridColor(Color.FromColorIndex(ColorMethod.ByAci, 7),
        (int)GridLineType.InnerGridLines, (int)RowType.DataRow);
    style.SetGridVisibility(true,
        (int)GridLineType.OuterGridLines, (int)RowType.DataRow);

    // Per cell-style margins
    style.SetMargin(CellMargins.Left, 2.0, "_DATA");
    style.SetMargin(CellMargins.Right, 2.0, "_DATA");
    style.SetMargin(CellMargins.Top, 1.0, "_HEADER");
    style.SetMargin(CellMargins.Bottom, 1.0, "_HEADER");

    // Post to database
    ObjectId styleId = style.PostTableStyleToDatabase(db, "MyTableStyle");
    tr.AddNewlyCreatedDBObject(style, true);
    tr.Commit();
}
```

**Apply a table style:**
```csharp
DBDictionary styleDict = (DBDictionary)tr.GetObject(
    db.TableStyleDictionaryId, OpenMode.ForRead);
if (styleDict.Contains("MyTableStyle"))
{
    table.TableStyle = styleDict.GetAt("MyTableStyle");
}

// Read current style name (read-only)
string styleName = table.TableStyleName;
```

**TableStyle properties reference:**
- `Name` (string, get/set)
- `Description` (string, get/set)
- `FlowDirection` (FlowDirection, get/set)
- `IsTitleSuppressed` (bool, get/set)
- `IsHeaderSuppressed` (bool, get/set)
- `HorizontalCellMargin` (double, get/set)
- `VerticalCellMargin` (double, get/set)
- `Template` (ObjectId, get/set)
- `BitFlags` (int, get/set)
- `CellStyles` (ArrayList, get) - list of cell style names

**TableStyle methods (per RowType):**
- `TextStyle(RowType)` -> ObjectId
- `SetTextStyle(ObjectId, int rowTypes)`
- `TextHeight(RowType)` -> double / `TextHeight(string cellStyle)` -> double
- `SetTextHeight(double, int rowTypes)` / `SetTextHeight(double, string cellStyle)`
- `Alignment(RowType)` -> CellAlignment
- `SetAlignment(CellAlignment, int rowTypes)`
- `Color(RowType)` -> Color / `SetColor(Color, int rowTypes)`
- `BackgroundColor(RowType)` -> Color / `SetBackgroundColor(Color, int rowTypes)`
- `IsBackgroundColorNone(RowType)` -> bool / `SetBackgroundColorNone(bool, int rowTypes)`
- `GridLineWeight(GridLineType, RowType)` -> LineWeight
- `SetGridLineWeight(LineWeight, int gridLineTypes, int rowTypes)`
- `GridColor(GridLineType, RowType)` -> Color
- `SetGridColor(Color, int gridLineTypes, int rowTypes)`
- `GridVisibility(GridLineType, RowType)` -> bool
- `SetGridVisibility(bool, int gridLineTypes, int rowTypes)`
- `DataType(RowType)` -> DataType / `UnitType(RowType)` -> UnitType
- `SetDataType(DataType, UnitType, RowType)`
- `Format(RowType)` -> string / `SetFormat(string, RowType)`
- `PostTableStyleToDatabase(Database, string styleName)` -> ObjectId

**TableStyle methods (per cell style name):**
- `CellClass(string)` -> CellClass / `SetCellClass(CellClass, string)`
- `Margin(CellMargins, string)` -> double / `SetMargin(CellMargins, double, string)`
- `GridDoubleLineSpacing(GridLineType, string)` -> double / `SetGridDoubleLineSpacing(double, GridLineType, string)`
- `GridLineStyle(GridLineType, string)` -> GridLineStyle / `SetGridLineStyle(GridLineStyle, GridLineType, string)`
- `GridLinetype(GridLineType, string)` -> ObjectId / `SetGridLinetype(ObjectId, GridLineType, string)`

## Table Properties Reference

**Table (inherits BlockReference):**
- `TableStyle` (ObjectId, get/set) - table style reference
- `TableStyleName` (string, get) - resolved style name
- `Position` (Point3d, get/set) - inherited from BlockReference, insertion point
- `Height` (double, get/set) - overall table height
- `Width` (double, get/set) - overall table width
- `MinimumTableHeight` (double, get) - minimum allowed height
- `MinimumTableWidth` (double, get) - minimum allowed width
- `Direction` (Vector3d, get/set) - table direction vector
- `FlowDirection` (FlowDirection, get/set) - TopToBottom or BottomToTop
- `Cells` (CellRange, get) - access all cells; use `Cells[row, col]` for individual `Cell`
- `Rows` (RowsCollection, get) - access rows; `Rows.Count`, `Rows[i].Height`
- `Columns` (ColumnsCollection, get) - access columns; `Columns.Count`, `Columns[i].Width`
- `BreakEnabled` (bool, get/set) - enable table breaking
- `BreakOptions` (TableBreakOptions, get/set) - break behavior flags
- `BreakFlowDirection` (TableBreakFlowDirection, get/set) - break flow direction
- `HasSubSelection` (bool, get) - whether cells are sub-selected
- `SubSelection` (CellRange, get/set) - current sub-selection

**Row (inherits CellRange):**
- `Height` (double, get/set)
- `MinimumHeight` (double, get)

**Column (inherits CellRange):**
- `Width` (double, get/set)
- `MinimumWidth` (double, get)
- `Name` (string, get/set)

**Cell (inherits CellRange):**
- `Row` (int, get) - row index
- `Column` (int, get) - column index
- `TextString` (string, get/set) - cell text
- `Value` (object, get/set) - typed value
- `FieldId` (ObjectId, get/set) - field reference
- `BlockTableRecordId` (ObjectId, get/set) - block reference
- `DataLink` (ObjectId, get/set) - data link reference
- `ContentTypes` (CellContentTypes, get) - what content the cell has
- `CellType` (TableCellType, get) - cell type
- `AttachmentPoint` (Point3d, get) - cell attachment point
- `ToolTip` (string, get/set)
- `Contents` (CellContentsCollection, get) - multi-content access

**CellRange (base for Cell, Row, Column):**
- `Alignment` (CellAlignment?, get/set)
- `TextHeight` (double?, get/set)
- `TextStyleId` (ObjectId?, get/set)
- `ContentColor` (Color, get/set)
- `BackgroundColor` (Color, get/set)
- `IsBackgroundColorNone` (bool?, get/set)
- `DataType` (DataTypeParameter?, get/set)
- `DataFormat` (string, get/set)
- `ContentLayout` (CellContentLayout?, get/set)
- `State` (CellStates?, get/set)
- `Style` (string, get/set) - cell style name
- `IsMergeAllEnabled` (bool?, get/set)
- `IsEmpty` (bool?, get)
- `IsMerged` (bool?, get)
- `IsLinked` (bool?, get)
- `IsContentEditable` (bool?, get)
- `IsFormatEditable` (bool?, get)
- `Borders` (CellBorders, get)
- `TopRow` / `BottomRow` / `LeftColumn` / `RightColumn` (int, get)
- `TopLeft` / `BottomRight` (Cell, get)
- `ParentTable` (Table, get)
- `CanInsertRow` / `CanInsertColumn` (bool, get)
- `CanDeleteRows` / `CanDeleteColumns` (bool, get)
- Static: `CellRange.Create(Table, int topRow, int leftCol, int bottomRow, int rightCol)`

**CellContent (via `Cell.Contents[i]`):**
- `TextString` (string, get/set)
- `Value` (object, get/set)
- `TextHeight` (double, get/set)
- `TextStyleId` (ObjectId, get/set)
- `ContentColor` (Color, get/set)
- `Rotation` (double, get/set) - radians
- `Scale` (double, get/set) - block scale
- `IsAutoScale` (bool, get/set) - auto-fit block
- `FieldId` (ObjectId, get/set)
- `BlockTableRecordId` (ObjectId, get/set)
- `Formula` (string, get/set) - e.g. "=Sum(C3:C5)"
- `HasFormula` (bool, get)
- `DataType` (DataTypeParameter, get/set)
- `DataFormat` (string, get/set)
- `ContentTypes` (CellContentTypes, get)
- `Overrides` (CellProperties, get/set)

**CellBorders / CellBorder (via `Cell.Borders`):**
- `CellBorders` has: `Top`, `Bottom`, `Left`, `Right`, `Horizontal`, `Vertical` (all CellBorder)
- `CellBorder` has: `Color`, `LineWeight?`, `LineStyle?`, `Linetype?`, `IsVisible?`, `Margin?`, `DoubleLineSpacing?`, `Overrides?`

## Enums

**CellAlignment:** TopLeft=1, TopCenter=2, TopRight=3, MiddleLeft=4, MiddleCenter=5, MiddleRight=6, BottomLeft=7, BottomCenter=8, BottomRight=9

**FlowDirection:** NotSet=0, LeftToRight=1, RightToLeft=2, TopToBottom=3, BottomToTop=4, ByStyle=5

**TableBreakOptions (flags):** None=0, EnableBreaking=1, RepeatTopLabels=2, RepeatBottomLabels=4, AllowManualPositions=8, AllowManualHeights=16

**TableBreakFlowDirection:** Right=1, DownOrUp=2, Left=4

**GridLineStyle:** Single, Double

## Gotchas

- **Call `GenerateLayout()` after populating** the table and before committing. Without it the table may not render correctly.
- **Row 0 is the title row, row 1 is the header row** (when not suppressed). Data rows start at index 2 by default. If the title is suppressed, the header is row 0 and data starts at row 1.
- **`SetSize(rows, cols)` replaces the old `NumRows`/`NumColumns` setters** which are obsolete. Use `Rows.Count` and `Columns.Count` to read the current size.
- **Use the modern `Cells[row, col]` API** rather than the old method-based API (e.g., `SetTextString(row, col, text)` is obsolete). The old methods still work but are marked `[Obsolete]`.
- **`Table` inherits from `BlockReference`**, so `Position` sets the insertion point. The table grows downward from this point when `FlowDirection` is `TopToBottom`.
- **`CellRange` properties are nullable** (e.g., `Alignment` is `CellAlignment?`). When reading a range that spans cells with different values, the property returns `null`.
- **Table must be open `ForWrite`** before modifying cells, rows, columns, or table properties. Open it via `tr.GetObject(tableId, OpenMode.ForWrite)`.
- **`RecomputeTableBlock(true)` forces a visual update** if the table appearance is stale after programmatic changes. Usually `GenerateLayout()` is sufficient.
- **`SuppressRegenerateTable(true)`** can improve performance when making many changes in a batch. Call `SuppressRegenerateTable(false)` when done, then `GenerateLayout()`.
- **Block content in cells:** set `IsAutoScale = true` to fit the block to the cell, or set `Scale` manually. The `BlockTableRecordId` must reference a valid block definition.
- **Table styles use `int rowTypes` as a bitmask** cast from `RowType` (TitleRow=1, HeaderRow=2, DataRow=4). Combine with bitwise OR for multiple row types.
- **Cell style names** are strings: `"_TITLE"`, `"_HEADER"`, `"_DATA"` are the built-in names. Custom cell styles can be added to a `TableStyle`.
