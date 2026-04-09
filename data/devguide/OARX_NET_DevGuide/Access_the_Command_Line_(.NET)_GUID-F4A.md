<!-- ObjectARX and Managed .NET > ObjectARX: Managed .NET Developer's Guide > Control the AutoCAD Environment (.NET) > Access the Command Line (.NET) -->
<!-- Source: https://help.autodesk.com/cloudhelp/2026/ENU/OARX-DevGuide-Managed/files/GUID-F4A36181-39FB-4923-A2AF-3333945DB289.htm -->

# Access the Command Line (.NET)

You can send commands directly to the command line by using the SendStringToExecute method. The SendStringToExecute method sends a single string to the command line. The string must contain the arguments to the command listed in the order expected by the prompt sequence of the executed command. 

A blank space or the ASCII equivalent of a carriage return in the string is equivalent to pressing Enter on the keyboard. Unlike the AutoLISP environment, invoking the SendStringToExecute method with no argument is invalid. 

Commands executed with SendStringToExecute are asynchronous and are not invoked until the .NET command has ended. If you need to execute a command immediately (synchronously), you should: 

  * Use the SendCommand method which is part of the COM Automation library which can be access using .NET COM Interop 
  * P/Invoke the unmanaged acedCommand or acedCmd method for native AutoCAD commands and commands defined with the ObjectARX or .NET API 
  * P/Invoke the unmanaged acedInvoke method for commands defined through AutoLISP 

## Send a command to the command line

The following example creates a circle with a center of (2, 2, 0) and a radius of 4. The drawing is then zoomed to all the geometry in the drawing. Notice that there is a space at the end of the string which represents the final Enter to begin execution of the command. 

### C#
    
    
    using Autodesk.AutoCAD.ApplicationServices;
    using Autodesk.AutoCAD.Runtime;
     
    [CommandMethod("SendACommandToAutoCAD")]
    public static void SendACommandToAutoCAD()
    {
      Document acDoc = Application.DocumentManager.MdiActiveDocument;
     
      // Draws a circle and zooms to the extents or 
      // limits of the drawing
      acDoc.SendStringToExecute("._circle 2,2,0 4 ", true, false, false);
      acDoc.SendStringToExecute("._zoom _all ", true, false, false);
    }

### VB.NET
    
    
    Imports Autodesk.AutoCAD.ApplicationServices
    Imports Autodesk.AutoCAD.Runtime
     
    <CommandMethod("SendACommandToAutoCAD")> _
    Public Sub SendACommandToAutoCAD()
      Dim acDoc As Document = Application.DocumentManager.MdiActiveDocument
     
      '' Draws a circle and zooms to the extents or 
      '' limits of the drawing
      acDoc.SendStringToExecute("._circle 2,2,0 4 ", True, False, False)
      acDoc.SendStringToExecute("._zoom _all ", True, False, False)
    End Sub

### VBA/ActiveX Code Reference
    
    
    Sub SendACommandToAutoCAD()
       ' Draws a circle and zooms to the extents or 
       ' limits of the drawing
       ThisDrawing.SendCommand "._Circle 2,2,0 4 "
       ThisDrawing.SendCommand "._zoom a "
    End Sub
