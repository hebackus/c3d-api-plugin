<!-- ObjectARX and Managed .NET > ObjectARX: Managed .NET Developer's Guide > Develop Applications (.NET) > Handle Errors (.NET) > Trap Runtime Errors (.NET) > Use Try Statements (.NET) -->
<!-- Source: https://help.autodesk.com/cloudhelp/2026/ENU/OARX-DevGuide-Managed/files/GUID-A8D1137E-9283-4F1D-9B3E-89B90E5AA5A6.htm -->

# Use Try Statements (.NET)

In .NET, runtime errors can be trapped using a Try statement. This statement literally sets a trap for the system. When an error occurs in a Try statement, the default error handling for the system is bypassed and execution is redirected to its Catch clause. 

The Try statement has three forms: 

  * Try-Catch
  * Try-Finally
  * Try-Catch-Finally

## Try-Catch Statement

The Try-Catch statement is used when you want to respond to an error. This statement traps the error and instead of displaying a default error message and terminating the application, execution is moved to the Catch clause of the Try statement. 

The Catch clause can optional contain a single parameter which accepts an Exception object. The Exception object contains information about the error encountered. If the error that is encountered cannot be resolved, you should display a custom error message and exit the application gracefully. 

## Try-Finally Statement

The Try-Finally statement is used when you do not want to provide specific error handling. This statement traps an error, and displays the default error message without terminating the application. When an error is encountered, execution is moved from the Try statement to its Finally clause after Continue is clicked in the default message box. The Try-Finally statement is best used when an application is still being developed and debugged. 

## Try-Catch-Finally Statement

The Try-Catch-Finally statement is a combination of the Try-Catch and Try-Finally statements. This statement traps the error and instead of displaying a default error message and terminating the application, execution is moved to the Catch clause of the Try statement. After the code is executed in the Catch clause, execution is moved to the Finally clause which gives your application one last chance to either continue execution or to exit gracefully. 

## Test error handling without and with the Try-Catch-Finally statement

The following examples attempt to open a file named “Drawing123” on the C: drive. If the file is not found, an eFileNotFound error is thrown. The first command does not catch the error thrown by the ReadDwgFile method, so the default message box is displayed when the command is started in AutoCAD. The second command catches the error thrown using the Try-Catch-Finally statement. 

### C#
    
    
    using Autodesk.AutoCAD.Runtime;
    using Autodesk.AutoCAD.ApplicationServices;
    using Autodesk.AutoCAD.DatabaseServices;
     
    [CommandMethod("NoErrorHandler")]
    public void NoErrorHandler()
    {
      // Create a new database with no document window
      using (Database acDb = new Database(false, true))
      {
          // Read the drawing file named "Drawing123.dwg" on the C: drive.
          // If the "Drawing123.dwg" file does not exist, an eFileNotFound
          // exception is tossed and the program halts.
          acDb.ReadDwgFile("c:\\Drawing123.dwg", 
                           System.IO.FileShare.None, false, "");
      }
     
      // Message will not be displayed since the exception caused by
      // ReadDwgFile is not handled.
      Application.ShowAlertDialog("End of command reached");
    }
     
    [CommandMethod("ErrorTryCatchFinally")]
    public void ErrorTryCatchFinally()
    {
      // Create a new database with no document window
      using (Database acDb = new Database(false, true))
      {
          try
          {
              // Read the drawing file named "Drawing123.dwg" on the C: drive.
              // If the "Drawing123.dwg" file does not exist, an eFileNotFound
              // exception is tossed and the catch statement handles the error.
              acDb.ReadDwgFile("c:\\Drawing123.dwg",
                               System.IO.FileShare.None, false, "");
          }
          catch (Autodesk.AutoCAD.Runtime.Exception Ex)
          {
              Application.ShowAlertDialog("The following exception was caught:\n" +
                                          Ex.Message);
          }
          finally
          {
              // Message is displayed since the exception caused
              // by ReadDwgFile is handled.
              Application.ShowAlertDialog("End of command reached");
          }
      }
    }

### VB.NET
    
    
    Imports Autodesk.AutoCAD.Runtime
    Imports Autodesk.AutoCAD.ApplicationServices
    Imports Autodesk.AutoCAD.DatabaseServices
     
    <CommandMethod("NoErrorHandler")> _
    Public Sub NoErrorHandler()
      '' Create a new database with no document window
      Using acDb As Database = New Database(False, True)
          '' Read the drawing file named "Drawing123.dwg" on the C: drive.
          '' If the "Drawing123.dwg" file does not exist, an eFileNotFound
          '' exception is tossed and the program halts.
          acDb.ReadDwgFile("c:\Drawing123.dwg", _
                           System.IO.FileShare.None, False, "")
      End Using
     
      '' Message will not be displayed since the exception caused by
      '' ReadDwgFile is not handled.
      Application.ShowAlertDialog("End of command reached")
    End Sub
     
    <CommandMethod("ErrorTryCatchFinally")> _
    Public Sub ErrorTryCatchFinally()
      '' Create a new database with no document window
      Using acDb As Database = New Database(False, True)
          Try
              '' Read the drawing file named "Drawing123.dwg" on the C: drive.
              '' If the "Drawing123.dwg" file does not exist, an eFileNotFound
              '' exception is tossed and the catch statement handles the error.
              acDb.ReadDwgFile("c:\Drawing123.dwg", _
                               System.IO.FileShare.None, False, "")
          Catch Ex As Autodesk.AutoCAD.Runtime.Exception
              Application.ShowAlertDialog("The following exception was caught:" & _
                                          vbLf & Ex.Message)
          Finally
              '' Message is displayed since the exception caused
              '' by ReadDwgFile is handled.
              Application.ShowAlertDialog("End of command reached")
          End Try
      End Using
    End Sub
