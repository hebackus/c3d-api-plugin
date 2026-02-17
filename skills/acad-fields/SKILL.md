---
name: acad-fields
description: Fields (dynamic text) - creation from field codes, evaluation options, embedding in MText and attributes, field state management
---

# AutoCAD Fields (Dynamic Text)

Use this skill when creating or managing field objects - dynamic text that updates based on object properties, system variables, dates, formulas, or other data sources.

## Field Class

**Namespace:** `Autodesk.AutoCAD.DatabaseServices`
**Base class:** `DBObject`

### Constructors
- `Field()` - empty field
- `Field(string fieldCode)` - field from field code string
- `Field(string fieldCode, bool textField)` - field code with text field flag

### Creating a Field

```csharp
// Create a field that shows the current date
Field dateField = new Field("%<\\AcVar Date \\f \"M/d/yyyy\">%");

// Create a field that shows an object property
Field propField = new Field(
    string.Format("%<\\AcObjProp Object(%<\\_ObjId {0}>%).Area \\f \"%lu2%pr2\">%",
        entityId.Handle));

// Set evaluation options
dateField.EvaluationOption = FieldEvaluationOptions.OnOpen
    | FieldEvaluationOptions.OnSave
    | FieldEvaluationOptions.OnPlot;

// Evaluate the field
dateField.Evaluate();
```

### Properties

- `Value` (object, get) - current evaluated value
- `DataType` (DataType, get) - type of the field value
- `Format` (string, get/set) - format string
- `IsTextField` (bool, get) - whether this is a text field
- `EvaluatorId` (string, get/set) - evaluator plugin ID
- `EvaluationOption` (FieldEvaluationOptions, get/set) - when to evaluate
- `EvaluationStatus` (FieldEvaluationStatusResult, get) - current eval status
- `State` (FieldState, get) - internal state flags
- `FilingOption` (FieldFilingOptions, get/set)
- `HyperLink` (HyperLink, get/set)

### Methods

**Field code management:**
- `SetFieldCode(string fieldCode)` - set the field code
- `GetFieldCode()` -> string - get plain field code
- `GetFieldCode(FieldCodeFlags flags)` -> string - get field code with options

**Field code with children:**
- `SetFieldCodeWithChildren(FieldCodeWithChildren fieldCode)`
- `SetFieldCodeWithChildren(FieldCodeFlags flag, FieldCodeWithChildren fieldCode)`
- `GetFieldCodeWithChildren()` -> `FieldCodeWithChildren`
- `GetFieldCodeWithChildren(FieldCodeFlags flags)` -> `FieldCodeWithChildren`

**Children:**
- `GetChildren()` -> `Field[]`
- `GetChildrenIds()` -> `ObjectId[]`

**Evaluation:**
- `Evaluate()` - evaluate with defaults
- `Evaluate(int evaluationOptions, Database database)` - evaluate with options
- `ConvertToTextField()` - freeze field as static text
- `GetStringValue()` -> string - get formatted string value

**Data storage:**
- `GetData(string key)` -> object
- `SetData(string key, object data)`
- `SetData(string key, object data, bool recursive)`

**Static:**
- `Field.FindField(string text, int iSearchFrom, ref int nStartPos, ref int nEndPos)` -> bool

## Common Field Code Patterns

```csharp
// Object property (area of a polyline)
string areaField = string.Format(
    "%<\\AcObjProp Object(%<\\_ObjId {0}>%).Area \\f \"%lu2%pr2\">%",
    entity.Handle);

// System variable
string dateField = "%<\\AcVar Date \\f \"M/d/yyyy\">%";
string fileNameField = "%<\\AcVar FileName>%";
string scaleField = "%<\\AcVar CANNOSCALE \\f \"%sc\">%";

// Formula field
string formulaField = "%<\\AcExpr (1 + 2) * 3>%";

// Sheet set fields
string sheetTitle = "%<\\AcSm SheetSet.Title>%";
string sheetNumber = "%<\\AcSm Sheet.Number>%";

// Diesel expression
string dieselField = "%<\\AcDiesel $(getvar,dwgname)>%";
```

## Embedding Fields in MText

```csharp
MText mtext = new MText();
// Embed a field in MText content using field code syntax
mtext.Contents = "Area: %<\\AcObjProp Object(%<\\_ObjId "
    + entity.Handle + ">%).Area \\f \"%lu2%pr2\">%";
```

## FieldCodeWithChildren

For managing nested/compound fields. **Implements `IDisposable` — always `Dispose()` when done.**

```csharp
using (FieldCodeWithChildren fcc = field.GetFieldCodeWithChildren())
{
    string code = fcc.FieldCode;
    Field[] children = fcc.Children;

    // Modify
    fcc.FieldCode = "new field code";
    fcc.Add(0, childField);  // add child at index

    field.SetFieldCodeWithChildren(fcc);
}  // Dispose() called automatically
```

## Evaluation Status

```csharp
FieldEvaluationStatusResult status = field.EvaluationStatus;
FieldEvaluationStatus evalStatus = status.Status;
int errorCode = status.ErrorCode;
string errorMsg = status.ErrorMessage;

// Construct status manually
var result = new FieldEvaluationStatusResult(
    FieldEvaluationStatus.Success, 0, "");
```

## Enums

**FieldEvaluationOptions** (flags):
Disable=0, OnOpen=1, OnSave=2, OnPlot=4, OnEtransmit=8, OnRegen=16, OnDemand=32, Automatic=63

**FieldEvaluationStatus:**
NotYetEvaluated=1, Success=2, EvaluatorNotFound=4, SyntaxError=8, InvalidCode=16, InvalidContext=32, OtherError=64

**FieldEvaluationContext:**
Open=1, Save=2, Plot=4, Etransmit=8, Regen=16, Demand=32, Preview=64

**FieldState** (flags):
Initialized=1, Compiled=2, Modified=4, Evaluated=8, HasCache=16, HasFormattedString=32

**FieldCodeFlags** (flags):
FieldCode=1, EvaluatedText=2, EvaluatedChildren=4, ObjectReference=8, AddMarkers=16, EscapeBackslash=32, StripOptions=64, PreserveFields=128, TextField=256

**FieldFilingOptions** (flags):
SkipFilingResult=1

## Gotchas

- Field codes use `%<` and `>%` as delimiters - these MUST be present
- Object references in field codes use Handle values (not ObjectId) - handles are persistent across sessions, ObjectIds are not
- `Evaluate()` must be called explicitly for programmatically created fields; automatic evaluation only happens based on `EvaluationOption` triggers
- `ConvertToTextField()` permanently freezes the field - it cannot be converted back to a dynamic field
- Field codes are case-sensitive for evaluator names (`\\AcVar`, `\\AcObjProp`, `\\AcExpr`, etc.)
- Nested fields (fields within field codes) use `%<\\_ObjId>%` syntax for object references
- `GetFieldCode()` without flags returns the raw field code; use `FieldCodeFlags.EvaluatedText` to get the current display value
- The `\\f` format specifier in field codes uses AutoCAD format strings, not .NET format strings
