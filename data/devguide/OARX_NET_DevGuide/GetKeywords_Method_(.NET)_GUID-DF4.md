<!-- ObjectARX and Managed .NET > ObjectARX: Managed .NET Developer's Guide > Control the AutoCAD Environment (.NET) > Prompt for User Input (.NET) > GetKeywords Method (.NET) -->
<!-- Source: https://help.autodesk.com/cloudhelp/2026/ENU/OARX-DevGuide-Managed/files/GUID-DF40DD82-FD27-43C5-B7D2-E75646B2E47E.htm -->

# GetKeywords Method (.NET)

The GetKeywords method prompts the user for input of a keyword at the Command prompt. The PromptKeywordOptions object allows you to control the input entered and how the prompt message appears. The Keywords property of the PromptKeywordOptions object allows you to define keywords that can be entered at the Command prompt. 

Note: The underscore character ("_") has a special meaning and can't be used as a keyword or as part of a keyword. 

## Get a keyword from the user at the command line

The following example forces the user to enter a keyword by setting the property AllowNone to false, which disallows NULL input (pressing Enter). The Keywords property is used to add the valid keywords allowed. 

### C#
    
    
    using Autodesk.AutoCAD.ApplicationServices;
    using Autodesk.AutoCAD.EditorInput;
    using Autodesk.AutoCAD.Runtime;
     
    [CommandMethod("GetKeywordFromUser")]
    public static void GetKeywordFromUser()
    {
        Document acDoc = Application.DocumentManager.MdiActiveDocument;
    
        PromptKeywordOptions pKeyOpts = new PromptKeywordOptions("");
        pKeyOpts.Message = "\nEnter an option ";
        pKeyOpts.Keywords.Add("Line");
        pKeyOpts.Keywords.Add("Circle");
        pKeyOpts.Keywords.Add("Arc");
        pKeyOpts.AllowNone = false;
    
        PromptResult pKeyRes = acDoc.Editor.GetKeywords(pKeyOpts);
    
        Application.ShowAlertDialog("Entered keyword: " +
                                    pKeyRes.StringResult);
    }

### VB.NET
    
    
    Imports Autodesk.AutoCAD.ApplicationServices
    Imports Autodesk.AutoCAD.EditorInput
    Imports Autodesk.AutoCAD.Runtime
     
    <CommandMethod("GetKeywordFromUser")> _
    Public Sub GetKeywordFromUser()
        Dim acDoc As Document = Application.DocumentManager.MdiActiveDocument
    
        Dim pKeyOpts As PromptKeywordOptions = New PromptKeywordOptions("")
        pKeyOpts.Message = vbLf & "Enter an option "
        pKeyOpts.Keywords.Add("Line")
        pKeyOpts.Keywords.Add("Circle")
        pKeyOpts.Keywords.Add("Arc")
        pKeyOpts.AllowNone = False
    
        Dim pKeyRes As PromptResult = acDoc.Editor.GetKeywords(pKeyOpts)
    
        Application.ShowAlertDialog("Entered keyword: " & _
                                    pKeyRes.StringResult)
    End Sub

### VBA/ActiveX Code Reference
    
    
    Sub GetKeywordFromUser()
        Dim keyWord As String
        ThisDrawing.Utility.InitializeUserInput 1, "Line Circle Arc"
        keyWord = ThisDrawing.Utility.GetKeyword _
                  (vbCrLf & "Enter an option [Line/Circle/Arc]: ")
        MsgBox keyWord, , "GetKeyword Example"
    End Sub

A more user-friendly keyword prompt is one that provides a default value if the user presses Enter (NULL input). Notice the minor modifications to the following example. 

### C#
    
    
    using Autodesk.AutoCAD.ApplicationServices;
    using Autodesk.AutoCAD.EditorInput;
    using Autodesk.AutoCAD.Runtime;
     
    [CommandMethod("GetKeywordFromUser2")]
    public static void GetKeywordFromUser2()
    {
        Document acDoc = Application.DocumentManager.MdiActiveDocument;
    
        PromptKeywordOptions pKeyOpts = new PromptKeywordOptions("");
        pKeyOpts.Message = "\nEnter an option ";
        pKeyOpts.Keywords.Add("Line");
        pKeyOpts.Keywords.Add("Circle");
        pKeyOpts.Keywords.Add("Arc");
        pKeyOpts.Keywords.Default = "Arc";
        pKeyOpts.AllowNone = true;
    
        PromptResult pKeyRes = acDoc.Editor.GetKeywords(pKeyOpts);
    
        Application.ShowAlertDialog("Entered keyword: " +
                                    pKeyRes.StringResult);
    }

### VB.NET
    
    
    Imports Autodesk.AutoCAD.ApplicationServices
    Imports Autodesk.AutoCAD.EditorInput
    Imports Autodesk.AutoCAD.Runtime
    <CommandMethod("GetKeywordFromUser2")> _
    Public Sub GetKeywordFromUser2()
        Dim acDoc As Document = Application.DocumentManager.MdiActiveDocument
    
        Dim pKeyOpts As PromptKeywordOptions = New PromptKeywordOptions("")
        pKeyOpts.Message = vbLf & "Enter an option "
        pKeyOpts.Keywords.Add("Line")
        pKeyOpts.Keywords.Add("Circle")
        pKeyOpts.Keywords.Add("Arc")
        pKeyOpts.Keywords.Default = "Arc"
        pKeyOpts.AllowNone = True
    
        Dim pKeyRes As PromptResult = acDoc.Editor.GetKeywords(pKeyOpts)
    
        Application.ShowAlertDialog("Entered keyword: " & _
                                    pKeyRes.StringResult)
    End Sub

### VBA/ActiveX Code Reference
    
    
    Sub GetKeywordFromUser2()
        Dim keyWord As String
        ThisDrawing.Utility.InitializeUserInput 0, "Line Circle Arc"
        keyWord = ThisDrawing.Utility.GetKeyword _
                  (vbCrLf & "Enter an option [Line/Circle/Arc] <Arc>: ")
        If keyWord = "" Then keyWord = "Arc"
        MsgBox keyWord, , "GetKeyword Example"
    End Sub
