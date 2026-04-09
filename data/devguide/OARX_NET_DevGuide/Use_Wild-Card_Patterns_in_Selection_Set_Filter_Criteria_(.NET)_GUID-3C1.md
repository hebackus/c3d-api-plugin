<!-- ObjectARX and Managed .NET > ObjectARX: Managed .NET Developer's Guide > Create and Edit AutoCAD Entities (.NET) > Work With Selection Sets (.NET) > Remove Objects From a Selection Set (.NET) > Use Wild-Card Patterns in Selection Set Filter Criteria (.NET) -->
<!-- Source: https://help.autodesk.com/cloudhelp/2026/ENU/OARX-DevGuide-Managed/files/GUID-3C1A759C-BB88-41A7-B1DE-697C493C92C8.htm -->

# Use Wild-Card Patterns in Selection Set Filter Criteria (.NET)

Symbol names and strings in selection filters can include wild-card patterns. 

The following table identifies the wild-card characters recognized by AutoCAD, and what each means in the context of a string: 

Wild-card characters   
---  
Character  |  Definition   
# (pound)  |  Matches any single numeric digit   
@ (at)  |  Matches any single alphabetic character   
. (period)  |  Matches any single non-alphanumeric character   
* (asterisk)  |  Matches any character sequence, including an empty one, and it can be used anywhere in the search pattern: at the beginning, middle, or end   
? (question mark)  |  Matches any single character   
~ (tilde)  |  If it is the first character in the pattern, it matches anything except the pattern   
[...] |  Matches any one of the characters enclosed   
[~...] |  Matches any single character not enclosed   
\- (hyphen)  |  Used inside brackets to specify a range for a single character   
, (comma)  |  Separates two patterns   
` (reverse quote)  |  Escapes special characters (reads next character literally)   
  
Use a reverse quote (`) to indicate that a character is not a wildcard, but is to be taken literally. For example, to specify that only an anonymous block named “*U2” be included in the selection set, use the value“`*U2”. 

## Select MText where a specific word appears in the text

The following example defines a selection filter that selects MText objects that contain the text string of “The”. 

### C#
    
    
    using Autodesk.AutoCAD.Runtime;
    using Autodesk.AutoCAD.ApplicationServices;
    using Autodesk.AutoCAD.DatabaseServices;
    using Autodesk.AutoCAD.EditorInput;
     
    [CommandMethod("FilterMtextWildcard")]
    public static void FilterMtextWildcard()
    {
        // Get the current document editor
        Editor acDocEd = Application.DocumentManager.MdiActiveDocument.Editor;
    
        // Create a TypedValue array to define the filter criteria
        TypedValue[] acTypValAr = new TypedValue[2];
        acTypValAr.SetValue(new TypedValue((int)DxfCode.Start, "MTEXT"), 0);
        acTypValAr.SetValue(new TypedValue((int)DxfCode.Text, "*The*"), 1);
    
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
     
    <CommandMethod("FilterMtextWildcard")> _
    Public Sub FilterMtextWildcard()
        '' Get the current document editor
        Dim acDocEd As Editor = Application.DocumentManager.MdiActiveDocument.Editor
    
        '' Create a TypedValue array to define the filter criteria
        Dim acTypValAr(1) As TypedValue
        acTypValAr.SetValue(New TypedValue(DxfCode.Start, "MTEXT"), 0)
        acTypValAr.SetValue(New TypedValue(DxfCode.Text, "*The*"), 1)
    
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
    
    
    Sub FilterMtextWildcard()
        Dim sset As AcadSelectionSet
        Dim FilterType(1) As Integer
        Dim FilterData(1) As Variant
        Set sset = ThisDrawing.SelectionSets.Add("SS1")
     
        FilterType(0) = 0
        FilterData(0) = "MTEXT"
        FilterType(1) = 1
        FilterData(1) = "*The*"
     
        sset.SelectOnScreen FilterType, FilterData
     
        MsgBox "Number of objects selected: " & sset.Count
     
        ' Remove the selection set at the end
        sset.Delete
    End Sub
