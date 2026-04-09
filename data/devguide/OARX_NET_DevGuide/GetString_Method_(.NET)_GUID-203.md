<!-- ObjectARX and Managed .NET > ObjectARX: Managed .NET Developer's Guide > Control the AutoCAD Environment (.NET) > Prompt for User Input (.NET) > GetString Method (.NET) -->
<!-- Source: https://help.autodesk.com/cloudhelp/2026/ENU/OARX-DevGuide-Managed/files/GUID-203F2756-1BA6-4226-A505-B776ED8AF0FB.htm -->

# GetString Method (.NET)

The GetString method prompts the user for the input of a string at the Command prompt. The PromptStringOptions object allows you to control the input entered and how the prompt message appears. The AllowSpaces property of the PromptStringOptions object controls if spaces are allowed or not at the prompt. If set to false, pressing the Spacebar terminates the input. 

## Get a string value from the user at the command line

The following example displays the Enter Your Name prompt, and requires that the input from the user be terminated by pressing Enter (spaces are allowed in the input string). The entered string is displayed in a message box. 

### C#
    
    
    using Autodesk.AutoCAD.ApplicationServices;
    using Autodesk.AutoCAD.EditorInput;
    using Autodesk.AutoCAD.Runtime;
     
    [CommandMethod("GetStringFromUser")]
    public static void GetStringFromUser()
    {
        Document acDoc = Application.DocumentManager.MdiActiveDocument;
     
        PromptStringOptions pStrOpts = new PromptStringOptions("\nEnter your name: ");
        pStrOpts.AllowSpaces = true;
        PromptResult pStrRes = acDoc.Editor.GetString(pStrOpts);
     
        Application.ShowAlertDialog("The name entered was: " +
                                    pStrRes.StringResult);
    }

### VB.NET
    
    
    Imports Autodesk.AutoCAD.ApplicationServices
    Imports Autodesk.AutoCAD.EditorInput
    Imports Autodesk.AutoCAD.Runtime
     
    <CommandMethod("GetStringFromUser")> _
    Public Sub GetStringFromUser()
        Dim acDoc As Document = Application.DocumentManager.MdiActiveDocument
     
        Dim pStrOpts As PromptStringOptions = New PromptStringOptions(vbLf & _
                                                                     "Enter your name: ")
        pStrOpts.AllowSpaces = True
        Dim pStrRes As PromptResult = acDoc.Editor.GetString(pStrOpts)
     
        Application.ShowAlertDialog("The name entered was: " & _
                                    pStrRes.StringResult)
    End Sub

### VBA/ActiveX Code Reference
    
    
    Sub GetStringFromUser()
        Dim retVal As String
        retVal = ThisDrawing.Utility.GetString _
                                        (1, vbCrLf & "Enter your name: ")
        MsgBox "The name entered was: " & retVal
    End Sub
