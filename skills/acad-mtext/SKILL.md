---
name: acad-mtext
description: MText (multiline text), DBText (single-line text) - creation, formatting codes, columns, fragment parsing, text styles
---

# AutoCAD Text (MText and DBText)

Use this skill when creating or modifying text objects - multiline text (MText), single-line text (DBText), text styles, and formatted text content.

## MText Creation

```csharp
using (Transaction tr = db.TransactionManager.StartTransaction())
{
    BlockTableRecord btr = (BlockTableRecord)tr.GetObject(
        db.CurrentSpaceId, OpenMode.ForWrite);

    MText mtext = new MText();
    mtext.Location = new Point3d(100, 200, 0);
    mtext.Width = 200.0;
    mtext.TextHeight = 2.5;
    mtext.Contents = "Line 1\\PLine 2";  // \\P = paragraph break
    mtext.Attachment = AttachmentPoint.TopLeft;
    mtext.TextStyleId = db.Textstyle;  // current text style

    btr.AppendEntity(mtext);
    tr.AddNewlyCreatedDBObject(mtext, true);
    tr.Commit();
}
```

## MText Properties

**Content:**
- `Contents` (string, get/set) - text with formatting codes
- `ContentsRTF` (string, get/set) - RTF format content
- `Text` (string, get-only) - plain text without formatting

**Geometry:**
- `Location` (Point3d, get/set) - insertion point
- `Width` (double, get/set) - text boundary width
- `Height` (double, get/set) - text boundary height
- `Rotation` (double, get/set) - rotation in radians
- `Normal` (Vector3d, get/set) - normal vector
- `Direction` (Vector3d, get/set) - direction vector

**Text styling:**
- `TextHeight` (double, get/set) - character height
- `TextStyleId` (ObjectId, get/set) - text style reference
- `TextStyleName` (string, get-only) - text style name
- `Attachment` (AttachmentPoint, get/set) - alignment point
- `FlowDirection` (FlowDirection, get/set) - text direction

**Size (read-only):**
- `ActualWidth` (double, get) - computed width
- `ActualHeight` (double, get) - computed height
- `Ascent` (double, get)
- `Descent` (double, get)

**Line spacing:**
- `LineSpacingStyle` (LineSpacingStyle, get/set) - AtLeast (1) or Exactly (2)
- `LineSpacingFactor` (double, get/set)
- `LineSpaceDistance` (double, get/set)

**Background fill:**
- `BackgroundFill` (bool, get/set) - enable background
- `BackgroundFillColor` (Color, get/set)
- `BackgroundScaleFactor` (double, get/set)
- `BackgroundTransparency` (Transparency, get/set)
- `UseBackgroundColor` (bool, get/set)
- `ShowBorders` (bool, get/set)

## MText Columns

```csharp
// Static columns (fixed count)
mtext.SetStaticColumns(150.0, 10.0, 3);  // width, gutter, count

// Dynamic columns (auto-flow based on height)
mtext.SetDynamicColumns(150.0, 10.0, true);  // width, gutter, autoHeight

// Read column settings
ColumnType colType = mtext.ColumnType;       // NoColumns, StaticColumns, DynamicColumns
int count = mtext.ColumnCount;
double width = mtext.ColumnWidth;
double gutter = mtext.ColumnGutterWidth;
bool autoHt = mtext.ColumnAutoHeight;
bool reversed = mtext.ColumnFlowReversed;

// Per-column heights (static columns)
mtext.SetColumnHeight(0, 100.0);
double h = mtext.GetColumnHeight(0);
```

## MText Formatting Codes

Common formatting codes used in `Contents` string:

| Code | Effect | Example |
|------|--------|---------|
| `\\P` | Paragraph break (new line) | `"Line 1\\PLine 2"` |
| `{\\fArial;text}` | Font change | `"{\\fArial\|b1;Bold Arial}"` |
| `{\\H2.5;text}` | Height change | `"{\\H3.0;Big text}"` |
| `{\\C1;text}` | Color change (ACI) | `"{\\C1;Red text}"` |
| `{\\W1.5;text}` | Width factor | `"{\\W2.0;Wide text}"` |
| `{\\O text\\o}` | Overline on/off | |
| `{\\L text\\l}` | Underline on/off | |
| `{\\K text\\k}` | Strikethrough on/off | |
| `{\\Q30;text}` | Oblique angle | `"{\\Q15;Slanted}"` |
| `{\\T1.5;text}` | Tracking (letter spacing) | |
| `\\S` | Stacking (fractions) | `"\\S1/2;"` |
| `\\A` | Alignment (0=bottom, 1=center, 2=top) | `"\\A1;centered"` |

Static formatting code properties (all string, get-only):
`MText.BlockBegin`, `MText.BlockEnd`, `MText.ParagraphBreak`, `MText.LineBreak`, `MText.FontChange`, `MText.HeightChange`, `MText.WidthChange`, `MText.ColorChange`, `MText.TrackChange`, `MText.ObliqueChange`, `MText.AlignChange`, `MText.UnderlineOn`, `MText.UnderlineOff`, `MText.OverlineOn`, `MText.OverlineOff`, `MText.StrikethroughOn`, `MText.StrikethroughOff`, `MText.StackStart`, `MText.NonBreakSpace`

## MText Fragment Parsing

Use `ExplodeFragments` to iterate through formatted text fragments:

```csharp
mtext.ExplodeFragments(FragmentCallback, null);

private static MTextFragmentCallbackStatus FragmentCallback(
    MTextFragment fragment, object userData)
{
    // Each fragment has its own formatting
    string text = fragment.Text;
    Point3d loc = fragment.Location;
    double height = fragment.CapsHeight;
    bool bold = fragment.Bold;
    bool italic = fragment.Italic;
    bool underline = fragment.Underlined;
    bool overline = fragment.Overlined;
    bool strikethrough = fragment.Strikethrough;
    double widthFactor = fragment.WidthFactor;
    double oblique = fragment.ObliqueAngle;
    double tracking = fragment.TrackingFactor;
    EntityColor color = fragment.Color;
    Vector3d direction = fragment.Direction;
    Vector3d normal = fragment.Normal;
    Point2d extents = fragment.Extents;
    string ttFont = fragment.TrueTypeFont;
    string shxFont = fragment.ShxFont;
    string bigFont = fragment.BigFont;
    bool stackTop = fragment.StackTop;
    bool stackBottom = fragment.StackBottom;

    // Underline/overline geometry
    Point3d[] underlinePts = fragment.GetUnderLinePoints();
    Point3d[] overlinePts = fragment.GetOverLinePoints();
    Point3d[] strikePts = fragment.GetStrikethroughPoints();

    return MTextFragmentCallbackStatus.Continue;  // or Terminate
}
```

Delegate signature: `delegate MTextFragmentCallbackStatus MTextFragmentCallback(MTextFragment fragment, object userData)`

Overloads:
- `ExplodeFragments(MTextFragmentCallback enumerator)`
- `ExplodeFragments(MTextFragmentCallback enumerator, object userData)`
- `ExplodeFragments(MTextFragmentCallback enumerator, object userData, WorldDraw context)`

## MText Methods

- `GetBoundingPoints()` -> `Point3dCollection` - corner points of bounding box
- `SetAttachmentMovingLocation(AttachmentPoint)` - reposition based on new attachment
- `ConvertFieldToText()` - convert embedded fields to static text
- `getMTextWithFieldCodes()` -> string - get text preserving field codes
- `CorrectSpelling()` -> int - launch spell checker
- `SetContentsRtf(string)` -> int - set RTF content

## DBText (Single-Line Text)

```csharp
DBText text = new DBText();
text.Position = new Point3d(100, 200, 0);
text.TextString = "Hello World";
text.Height = 2.5;
text.Rotation = 0.0;
text.TextStyleId = db.Textstyle;
text.WidthFactor = 1.0;
text.Oblique = 0.0;

btr.AppendEntity(text);
tr.AddNewlyCreatedDBObject(text, true);
```

**Properties:**
- `Position` (Point3d, get/set) - base insertion point
- `AlignmentPoint` (Point3d, get/set) - alignment reference point
- `TextString` (string, get/set) - the text content
- `Height` (double, get/set) - character height
- `Rotation` (double, get/set) - rotation in radians
- `WidthFactor` (double, get/set) - width scale
- `Oblique` (double, get/set) - oblique angle in radians
- `Thickness` (double, get/set) - extrusion thickness
- `Normal` (Vector3d, get/set)
- `TextStyleId` (ObjectId, get/set)
- `TextStyleName` (string, get-only)
- `Justify` (AttachmentPoint, get/set) - justification
- `HorizontalMode` (TextHorizontalMode, get/set)
- `VerticalMode` (TextVerticalMode, get/set)
- `IsMirroredInX` (bool, get/set)
- `IsMirroredInY` (bool, get/set)
- `IsDefaultAlignment` (bool, get-only)

**Methods:**
- `AdjustAlignment(Database)` - recalculate alignment
- `ConvertFieldToText()` - convert embedded fields
- `getTextWithFieldCodes()` -> string
- `CorrectSpelling()` -> int

## Text Styles

```csharp
// Create new text style
TextStyleTableRecord style = new TextStyleTableRecord();
style.Name = "MyStyle";
style.FileName = "arial.ttf";          // or "romans.shx"
style.BigFontFileName = "";            // for CJK fonts
style.TextSize = 0.0;                  // 0 = variable height
style.XScale = 1.0;                    // width factor
style.ObliquingAngle = 0.0;
style.IsVertical = false;

TextStyleTable tst = (TextStyleTable)tr.GetObject(
    db.TextStyleTableId, OpenMode.ForWrite);
ObjectId styleId = tst.Add(style);
tr.AddNewlyCreatedDBObject(style, true);

// Font descriptor (alternative to FileName)
style.Font = new FontDescriptor("Arial", false, false, 0, 0);
```

**TextStyleTableRecord properties:**
- `Name` (string, inherited from SymbolTableRecord)
- `FileName` (string, get/set) - TTF or SHX font file
- `BigFontFileName` (string, get/set) - big font for CJK
- `Font` (FontDescriptor, get/set) - font descriptor
- `TextSize` (double, get/set) - fixed size (0 = variable)
- `PriorSize` (double, get/set) - previous text size
- `XScale` (double, get/set) - width factor
- `ObliquingAngle` (double, get/set) - oblique angle
- `IsVertical` (bool, get/set) - vertical text
- `IsShapeFile` (bool, get/set) - shape file
- `FlagBits` (byte, get/set)

## Enums

**AttachmentPoint:**
TopLeft=1, TopCenter=2, TopRight=3, MiddleLeft=4, MiddleCenter=5, MiddleRight=6, BottomLeft=7, BottomCenter=8, BottomRight=9, BaseLeft=10, BaseCenter=11, BaseRight=12, BaseAlign=13, BottomAlign=14, MiddleAlign=15, TopAlign=16, BaseFit=17, BottomFit=18, MiddleFit=19, TopFit=20, BaseMid=21, BottomMid=22, MiddleMid=23, TopMid=24

**FlowDirection:** NotSet=0, LeftToRight=1, RightToLeft=2, TopToBottom=3, BottomToTop=4, ByStyle=5

**ColumnType:** NoColumns=0, StaticColumns=1, DynamicColumns=2

**LineSpacingStyle:** AtLeast=1, Exactly=2

**TextHorizontalMode:** TextLeft=0, TextCenter=1, TextRight=2, TextAlign=3, TextMid=4, TextFit=5

**TextVerticalMode:** TextBase=0, TextBottom=1, TextVerticalMid=2, TextTop=3

## Gotchas

- MText paragraph break is `\P` (backslash-P). In a C# regular string literal write it as `"\\P"` (the `\\` escape = one backslash). In a verbatim string literal write it as `@"\P"`. Do NOT use `"\\\\P"` — that produces a double backslash and won't render as a line break
- `AttachmentPoint` enum is shared between MText and DBText but means different things - MText uses it for `Attachment`, DBText uses it for `Justify`
- DBText requires setting BOTH `HorizontalMode`/`VerticalMode` AND `AlignmentPoint` for non-default justification; `Position` alone only works for left-justified text
- Call `AdjustAlignment(db)` on DBText after changing alignment modes
- MText `Width` of 0 means no wrapping (single line); set a non-zero width for multiline text
- `TextHeight` on MText is the character height; `Height` is the overall bounding box height
- `ActualWidth`/`ActualHeight` are only valid after the MText has been added to the database
- MText formatting codes use curly braces `{}` for scope - mismatched braces corrupt the text
- `TextStyleId` must reference an existing `TextStyleTableRecord` - use `db.Textstyle` for the current style
