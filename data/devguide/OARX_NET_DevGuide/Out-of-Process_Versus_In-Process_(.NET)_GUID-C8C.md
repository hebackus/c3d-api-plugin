<!-- ObjectARX and Managed .NET > ObjectARX: Managed .NET Developer's Guide > Basics of the AutoCAD .NET API (.NET) > Out-of-Process Versus In-Process (.NET) -->
<!-- Source: https://help.autodesk.com/cloudhelp/2026/ENU/OARX-DevGuide-Managed/files/GUID-C8C65D7A-EC3A-42D8-BF02-4B13C2EA1A4B.htm -->

# Out-of-Process Versus In-Process (.NET)

When you develop a new application, it can either run in or out-of-process. The AutoCAD .NET API is designed to run in-process only, which is different from the ActiveX Automation library which can be used in or -out-of-process. 

  * In-process applications are designed to run in the same process space as the host application. In this case, a DLL assembly is loaded into AutoCAD which is the host application. 
  * Out-of-process applications do not run in the same space as the host application. These applications are often built as stand-alone executables. 

If you need to create a stand-alone application to drive AutoCAD, it is best to create an application that uses the CreateObject and GetObject methods to create a new instance of an AutoCAD application or return one of the instances that is currently running. Once a reference to an AcadApplication is returned, you can then load your in-process .NET application into AutoCAD by using the SendCommand method that is a member of the ActiveDocument property of the AcadApplication. 

As an alternative to executing your .NET application in-process, could use COM interop for your application. 

Note: The ProgID for COM application access to AutoCAD 2026 is _AutoCAD.Application.25.1_. 

## C#
    
    
    using System;
    using System.Runtime.InteropServices;
     
    using Autodesk.AutoCAD.Interop;
    using Autodesk.AutoCAD.Runtime;
    using Autodesk.AutoCAD.ApplicationServices;
     
    [CommandMethod("ConnectToAcad")]
    public static void ConnectToAcad()
    {
     
      AcadApplication acAppComObj = null;
      const string strProgId = "AutoCAD.Application.25.1";
     
      // Get a running instance of AutoCAD
      try
      {
          acAppComObj = (AcadApplication)Marshal.GetActiveObject(strProgId);
      }
      catch // An error occurs if no instance is running
      {
          try
          {
              // Create a new instance of AutoCAD
              acAppComObj = (AcadApplication)Activator.CreateInstance(Type.GetTypeFromProgID(strProgId), true);
          }
          catch
          {
              // If an instance of AutoCAD is not created then message and exit
              System.Windows.Forms.MessageBox.Show("Instance of 'AutoCAD.Application'" +
                                                   " could not be created.");
     
              return;
          }
      }
     
      // Display the application and return the name and version
      acAppComObj.Visible = true;
      System.Windows.Forms.MessageBox.Show("Now running " + acAppComObj.Name + 
                                           " version " + acAppComObj.Version);
     
      // Get the active document
      AcadDocument acDocComObj;
      acDocComObj = acAppComObj.ActiveDocument;
     
      // Optionally, load your assembly and start your command or if your assembly
      // is demandloaded, simply start the command of your in-process assembly.
      acDocComObj.SendCommand("(command " + (char)34 + "NETLOAD" + (char)34 + " " +
                              (char)34 + "c:/myapps/mycommands.dll" + (char)34 + ") ");
     
      acDocComObj.SendCommand("MyCommand ");
    }

## VB.NET
    
    
    Imports System
    Imports System.Runtime.InteropServices
     
    Imports Autodesk.AutoCAD.Interop
    Imports Autodesk.AutoCAD.Runtime
    Imports Autodesk.AutoCAD.ApplicationServices
     
    <CommandMethod("ConnectToAcad")> _
    Public Sub ConnectToAcad()
      Dim acAppComObj As AcadApplication
      Dim strProgId As String = "AutoCAD.Application.25.1"
     
      On Error Resume Next
     
      '' Get a running instance of AutoCAD
      acAppComObj = GetObject(, strProgId)
     
      '' An error occurs if no instance is running
      If Err.Number > 0 Then
          Err.Clear()
     
          '' Create a new instance of AutoCAD
          acAppComObj = CreateObject(strProgId)
     
          '' Check to see if an instance of AutoCAD was created
          If Err.Number > 0 Then
             Err.Clear()
     
             '' If an instance of AutoCAD is not created then message and exit
             MsgBox("Instance of 'AutoCAD.Application' could not be created.")
     
             Exit Sub
          End If
      End If
     
      '' Display the application and return the name and version
      acAppComObj.Visible = True
      MsgBox("Now running " & acAppComObj.Name & " version " & acAppComObj.Version)
     
      '' Get the active document
      Dim acDocComObj As AcadDocument
      acDocComObj = acAppComObj.ActiveDocument
     
      '' Optionally, load your assembly and start your command or if your assembly
      '' is demandloaded, simply start the command of your in-process assembly.
      acDocComObj.SendCommand("(command " & Chr(34) & "NETLOAD" & Chr(34) & " " & _
                              Chr(34) & "c:/myapps/mycommands.dll" & Chr(34) & ") ")
     
      acDocComObj.SendCommand("MyCommand ")
    End Sub

## VBA/ActiveX Code Reference
    
    
    Sub ConnectToAcad()
        Dim acadApp As AcadApplication
        On Error Resume Next
     
        Set acadApp = GetObject(, "AutoCAD.Application.25.1")
        If Err Then
            Err.Clear
            Set acadApp = CreateObject("AutoCAD.Application.25.1")
            If Err Then
                MsgBox Err.Description
                Exit Sub
            End If
        End If
     
        acadApp.Visible = True
        MsgBox "Now running " + acadApp.Name + _
               " version " + acadApp.Version
     
        Dim acadDoc as AcadDocument
        Set acadDoc = acadApp.ActiveDocument
     
        '' Optionally, load your assembly and start your command or if your assembly
        '' is demandloaded, simply start the command of your in-process assembly.
        acadDoc.SendCommand("(command " & Chr(34) & "NETLOAD" & Chr(34) & " " & _
                            Chr(34) & "c:/myapps/mycommands.dll" & Chr(34) & ") ")
     
        acadDoc.SendCommand("MyCommand ")
    End Sub
