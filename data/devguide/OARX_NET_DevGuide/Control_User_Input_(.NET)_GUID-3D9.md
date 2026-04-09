<!-- ObjectARX and Managed .NET > ObjectARX: Managed .NET Developer's Guide > Control the AutoCAD Environment (.NET) > Prompt for User Input (.NET) > Control User Input (.NET) -->
<!-- Source: https://help.autodesk.com/cloudhelp/2026/ENU/OARX-DevGuide-Managed/files/GUID-3D998905-0C24-4FF9-A9C7-7F361A591B80.htm -->

# Control User Input (.NET)

When collecting input from the user, you want to make sure you limit the type of information they can enter so you can get the desired response. The various prompt option objects are used to not only define the prompt displayed at the Command prompt, but also restrict the input that the user can provide. With some of the input methods, not only can you get a return value based on the type of method used but also get a keyword. 

For example, you can use the GetPoint method to have the user specify a point or respond with a keyword. This is how commands like LINE, CIRCLE, and PLINE work. 

## Get an integer value or a keyword

The following example prompts the user for a positive non-zero integer value or a keyword. 

### C#
    
    
    using Autodesk.AutoCAD.ApplicationServices;
    using Autodesk.AutoCAD.EditorInput;
    using Autodesk.AutoCAD.Runtime;
     
    [CommandMethod("GetIntegerOrKeywordFromUser")]
    public static void GetIntegerOrKeywordFromUser()
    {
        Document acDoc = Application.DocumentManager.MdiActiveDocument;
    
        PromptIntegerOptions pIntOpts = new PromptIntegerOptions("");
        pIntOpts.Message = "\nEnter the size or ";
    
        // Restrict input to positive and non-negative values
        pIntOpts.AllowZero = false;
        pIntOpts.AllowNegative = false;
    
        // Define the valid keywords and allow Enter
        pIntOpts.Keywords.Add("Big");
        pIntOpts.Keywords.Add("Small");
        pIntOpts.Keywords.Add("Regular");
        pIntOpts.Keywords.Default = "Regular";
        pIntOpts.AllowNone = true;
    
        // Get the value entered by the user
        PromptIntegerResult pIntRes = acDoc.Editor.GetInteger(pIntOpts);
    
        if (pIntRes.Status == PromptStatus.Keyword)
        {
            Application.ShowAlertDialog("Entered keyword: " +
                                        pIntRes.StringResult);
        }
        else
        {
            Application.ShowAlertDialog("Entered value: " +
                                        pIntRes.Value.ToString());
        }
    }

### VB.NET
    
    
    Imports Autodesk.AutoCAD.ApplicationServices
    Imports Autodesk.AutoCAD.EditorInput
    Imports Autodesk.AutoCAD.Runtime
     
    <CommandMethod("GetIntegerOrKeywordFromUser")> _
    Public Sub GetIntegerOrKeywordFromUser()
        Dim acDoc As Document = Application.DocumentManager.MdiActiveDocument
    
        Dim pIntOpts As PromptIntegerOptions = New PromptIntegerOptions("")
        pIntOpts.Message = vbCrLf & "Enter the size or "
    
        '' Restrict input to positive and non-negative values
        pIntOpts.AllowZero = False
        pIntOpts.AllowNegative = False
    
        '' Define the valid keywords and allow Enter
        pIntOpts.Keywords.Add("Big")
        pIntOpts.Keywords.Add("Small")
        pIntOpts.Keywords.Add("Regular")
        pIntOpts.Keywords.Default = "Regular"
        pIntOpts.AllowNone = True
    
        '' Get the value entered by the user
        Dim pIntRes As PromptIntegerResult = acDoc.Editor.GetInteger(pIntOpts)
    
        If pIntRes.Status = PromptStatus.Keyword Then
            Application.ShowAlertDialog("Entered keyword: " & _
                                        pIntRes.StringResult)
        Else
            Application.ShowAlertDialog("Entered value: " & _
                                        pIntRes.Value.ToString())
        End If
    End Sub

### VBA/ActiveX Code Reference
    
    
    Sub GetIntegerOrKeywordFromUser()
     
        ' The first parameter of InitializeUserInput (6)
        ' restricts input to positive and non-negative
        ' values. The second parameter is the list of
        ' valid keywords.
        ThisDrawing.Utility.InitializeUserInput 6, "Big Small Regular"
     
        ' Set the prompt string variable
        Dim promptStr As String
        promptStr = vbCrLf & "Enter the size or [Big/Small/Regular] <Regular>:"
     
        ' At the GetInteger prompt, entering a keyword or pressing
        ' ENTER without entering a value results in an error. To allow
        ' your application to continue and check for the error
        ' description, you must set the error handler to resume on error.
        On Error Resume Next
     
        ' Get the value entered by the user
        Dim returnInteger As Integer
        returnInteger = ThisDrawing.Utility.GetInteger(promptStr)
     
        ' Check for an error. If the error number matches the
        ' one shown below, then use GetInput to get the returned
        ' string; otherwise, use the value of returnInteger.
     
        If Err.Number = -2145320928 Then
            Dim returnString As String
            Debug.Print Err.Description
            returnString = ThisDrawing.Utility.GetInput()
            If returnString = "" Then        'ENTER returns null string
               returnString = "Regular"      'Set to default
            End If
            Err.Clear
        Else                                 'Otherwise,
            returnString = returnInteger     'Use the value entered
        End If
     
        ' Display the result
        MsgBox returnString, , "InitializeUserInput Example"
    End Sub
