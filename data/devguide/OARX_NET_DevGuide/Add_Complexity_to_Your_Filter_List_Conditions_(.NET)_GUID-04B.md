<!-- ObjectARX and Managed .NET > ObjectARX: Managed .NET Developer's Guide > Create and Edit AutoCAD Entities (.NET) > Work With Selection Sets (.NET) > Remove Objects From a Selection Set (.NET) > Add Complexity to Your Filter List Conditions (.NET) -->
<!-- Source: https://help.autodesk.com/cloudhelp/2026/ENU/OARX-DevGuide-Managed/files/GUID-04B8192E-B0D8-4731-A882-AE92B7CFAE22.htm -->

# Add Complexity to Your Filter List Conditions (.NET)

When you specify multiple selection criteria, AutoCAD assumes the selected object must meet each criterion. You can qualify your criteria in other ways. For numeric items, you can specify relational operations (for example, the radius of a circle must be _greater than or equal_ to 5.0). And for all items, you can specify logical operations (for example, Text or MText). 

Use a -4 DXF code or the constant DxfCode.Operator to indicate a relational operator in a selection filter. The operator is expressed as a string. The allowable relational operators are shown in the following table. 

Relational operators for selection set filter lists   
---  
Operator  |  Description   
"*" |  Anything goes (always true)   
"=" |  Equals   
"!=" |  Not equal to   
"/=" |  Not equal to   
"<>" |  Not equal to   
"<" |  Less than   
"<=" |  Less than or equal to   
">" |  Greater than   
">=" |  Greater than or equal to   
"&" |  Bitwise AND (integer groups only)   
"&=" |  Bitwise masked equals (integer groups only)   
  
Logical operators in a selection filter are also indicated by a -4 group code or the constant DxfCode.Operator, and the operator is a string, but the operators must be paired. The opening operator is preceded by a less-than symbol (<), and the closing operator is followed by a greater-than symbol (>). The following table lists the logical operators allowed in selection set filtering. 

Logical grouping operators for selection set filter lists   
---  
Starting operator  |  Encloses  |  Ending operator   
"<AND"  |  One or more operands  |  "AND>"  
"<OR" |  One or more operands  |  "OR>"  
"<XOR" |  Two operands  |  "XOR>"  
"<NOT" |  One operand  |  "NOT>"  
  
## Select a circle whose radius is greater than or equal to 5.0

The following example selects circles whose radius is greater than or equal to 5.0. 

### C#
    
    
    using Autodesk.AutoCAD.Runtime;
    using Autodesk.AutoCAD.ApplicationServices;
    using Autodesk.AutoCAD.DatabaseServices;
    using Autodesk.AutoCAD.EditorInput;
     
    [CommandMethod("FilterRelational")]
    public static void FilterRelational()
    {
        // Get the current document editor
        Editor acDocEd = Application.DocumentManager.MdiActiveDocument.Editor;
    
        // Create a TypedValue array to define the filter criteria
        TypedValue[] acTypValAr = new TypedValue[3];
        acTypValAr.SetValue(new TypedValue((int)DxfCode.Start, "CIRCLE"), 0);
        acTypValAr.SetValue(new TypedValue((int)DxfCode.Operator, ">="), 1);
        acTypValAr.SetValue(new TypedValue(40, 5), 2);
    
        // Assign the filter criteria to a SelectionFilter object
        SelectionFilter acSelFtr = new SelectionFilter(acTypValAr);
    
        // Request for objects to be selected in the drawing area
        PromptSelectionResult acSSPrompt;
        acSSPrompt = acDocEd.GetSelection(acSelFtr);
    
        // If the prompt status is OK, objects were selected
        if (acSSPrompt.Status == PromptStatus.OK)
        {
            SelectionSet acSSet = acSSPrompt.Value;
    
            Application.ShowAlertDialog("Number of objects selected: " +
                                        acSSet.Count.ToString());
        }
        else
        {
            Application.ShowAlertDialog("Number of objects selected: 0");
        }
    }

### VB.NET
    
    
    Imports Autodesk.AutoCAD.Runtime
    Imports Autodesk.AutoCAD.ApplicationServices
    Imports Autodesk.AutoCAD.DatabaseServices
    Imports Autodesk.AutoCAD.EditorInput
     
    <CommandMethod("FilterRelational")> _
    Public Sub FilterRelational()
        '' Get the current document editor
        Dim acDocEd As Editor = Application.DocumentManager.MdiActiveDocument.Editor
    
        '' Create a TypedValue array to define the filter criteria
        Dim acTypValAr(2) As TypedValue
        acTypValAr.SetValue(New TypedValue(DxfCode.Start, "CIRCLE"), 0)
        acTypValAr.SetValue(New TypedValue(DxfCode.Operator, ">="), 1)
        acTypValAr.SetValue(New TypedValue(40, 5), 2)
    
        '' Assign the filter criteria to a SelectionFilter object
        Dim acSelFtr As SelectionFilter = New SelectionFilter(acTypValAr)
    
        '' Request for objects to be selected in the drawing area
        Dim acSSPrompt As PromptSelectionResult
        acSSPrompt = acDocEd.GetSelection(acSelFtr)
    
        '' If the prompt status is OK, objects were selected
        If acSSPrompt.Status = PromptStatus.OK Then
            Dim acSSet As SelectionSet = acSSPrompt.Value
    
            Application.ShowAlertDialog("Number of objects selected: " & _
                                        acSSet.Count.ToString())
        Else
            Application.ShowAlertDialog("Number of objects selected: 0")
        End If
    End Sub

### VBA/ActiveX Code Reference
    
    
    Sub FilterRelational()
        Dim sset As AcadSelectionSet
        Dim FilterType(2) As Integer
        Dim FilterData(2) As Variant
        Set sset = ThisDrawing.SelectionSets.Add("SS1")
        FilterType(0) = 0: FilterData(0) = "Circle"
        FilterType(1) = -4: FilterData(1) = ">="
        FilterType(2) = 40: FilterData(2) = 5#
     
        sset.SelectOnScreen FilterType, FilterData
     
        MsgBox "Number of objects selected: " & sset.Count
     
        ' Remove the selection set at the end
        sset.Delete
    End Sub

## Select either Text or MText

The following example specifies that either Text or MText objects can be selected. 

### C#
    
    
    using Autodesk.AutoCAD.Runtime;
    using Autodesk.AutoCAD.ApplicationServices;
    using Autodesk.AutoCAD.DatabaseServices;
    using Autodesk.AutoCAD.EditorInput;
     
    [CommandMethod("FilterForText")]
    public static void FilterForText()
    {
        // Get the current document editor
        Editor acDocEd = Application.DocumentManager.MdiActiveDocument.Editor;
    
        // Create a TypedValue array to define the filter criteria
        TypedValue[] acTypValAr = new TypedValue[4];
        acTypValAr.SetValue(new TypedValue((int)DxfCode.Operator, "<or"), 0);
        acTypValAr.SetValue(new TypedValue((int)DxfCode.Start, "TEXT"), 1);
        acTypValAr.SetValue(new TypedValue((int)DxfCode.Start, "MTEXT"), 2);
        acTypValAr.SetValue(new TypedValue((int)DxfCode.Operator, "or>"), 3);
    
        // Assign the filter criteria to a SelectionFilter object
        SelectionFilter acSelFtr = new SelectionFilter(acTypValAr);
    
        // Request for objects to be selected in the drawing area
        PromptSelectionResult acSSPrompt;
        acSSPrompt = acDocEd.GetSelection(acSelFtr);
    
        // If the prompt status is OK, objects were selected
        if (acSSPrompt.Status == PromptStatus.OK)
        {
            SelectionSet acSSet = acSSPrompt.Value;
    
            Application.ShowAlertDialog("Number of objects selected: " +
                                        acSSet.Count.ToString());
        }
        else
        {
            Application.ShowAlertDialog("Number of objects selected: 0");
        }
    }

### VB.NET
    
    
    Imports Autodesk.AutoCAD.Runtime
    Imports Autodesk.AutoCAD.ApplicationServices
    Imports Autodesk.AutoCAD.DatabaseServices
    Imports Autodesk.AutoCAD.EditorInput
     
    <CommandMethod("FilterForText")> _
    Public Sub FilterForText()
        '' Get the current document editor
        Dim acDocEd As Editor = Application.DocumentManager.MdiActiveDocument.Editor
    
        '' Create a TypedValue array to define the filter criteria
        Dim acTypValAr(3) As TypedValue
        acTypValAr.SetValue(New TypedValue(DxfCode.Operator, "<or"), 0)
        acTypValAr.SetValue(New TypedValue(DxfCode.Start, "TEXT"), 1)
        acTypValAr.SetValue(New TypedValue(DxfCode.Start, "MTEXT"), 2)
        acTypValAr.SetValue(New TypedValue(DxfCode.Operator, "or>"), 3)
    
        '' Assign the filter criteria to a SelectionFilter object
        Dim acSelFtr As SelectionFilter = New SelectionFilter(acTypValAr)
    
        '' Request for objects to be selected in the drawing area
        Dim acSSPrompt As PromptSelectionResult
        acSSPrompt = acDocEd.GetSelection(acSelFtr)
    
        '' If the prompt status is OK, objects were selected
        If acSSPrompt.Status = PromptStatus.OK Then
            Dim acSSet As SelectionSet = acSSPrompt.Value
    
            Application.ShowAlertDialog("Number of objects selected: " & _
                                        acSSet.Count.ToString())
        Else
            Application.ShowAlertDialog("Number of objects selected: 0")
        End If
    End Sub

### VBA/ActiveX Code Reference
    
    
    Sub FilterForText()
        Dim sset As AcadSelectionSet
        Dim FilterType(3) As Integer
        Dim FilterData(3) As Variant
        Set sset = ThisDrawing.SelectionSets.Add("SS1")
     
        FilterType(0) = -4: FilterData(0) = "<or"
        FilterType(1) = 0: FilterData(1) = "TEXT"
        FilterType(2) = 0: FilterData(2) = "MTEXT"
        FilterType(3) = -4: FilterData(3) = "or>"
     
        sset.SelectOnScreen FilterType, FilterData
     
        MsgBox "Number of objects selected: " & sset.Count
     
        ' Remove the selection set at the end
        sset.Delete
    End Sub
