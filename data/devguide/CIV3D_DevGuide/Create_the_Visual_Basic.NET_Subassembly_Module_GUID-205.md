<!-- Developer's Guide > API Developer's Guide > Converting VBA Subassemblies to .NET > Procedure > Create the Visual Basic.NET Subassembly Module -->
<!-- Source: https://help.autodesk.com/cloudhelp/2026/ENU/Civil3D-DevGuide/files/GUID-2056985F-F01B-4782-B6C6-FCC2A7D36D52.htm -->

# Create the Visual Basic.NET Subassembly Module

Start by creating the module for your subassembly. You can add a new module to the C3DStockSubassemblies project, or you can create your own .NET subassembly project and add the new class module there. New projects should use the Visual Studio "Class Library" template, and should reference the following files: 

  * acdbmgd.dll
  * acmgd.dll
  * AecBaseMgd.dll
  * AeccDbMgd.dll

Be sure to include CodeSpecific.vb, SATemplate.vb, and Utilties.vb in your project as well. 

Add the following framework to the Visual Basic subassembly class module:
    
    
    Public Class UserDefinedSA
    Inherits SATemplate
        ' Member Variables.
        Protected Overrides Sub GetLogicalNamesImplement(ByVal corridorState As Autodesk.Civil.Runtime.CorridorState)
            ' Todo
        End Sub
        Protected Overrides Sub GetInputParametersImplement(ByVal corridorState As CorridorState)
            ' Todo
        End Sub
        Protected Overrides Sub GetOutputParametersImplement(ByVal corridorState As CorridorState)
            ' Todo
        End Sub
        Protected Overrides Sub DrawImplement(ByVal corridorState As CorridorState)
             ' Todo
        End Sub
    End Class
    

Note that:

  * The class must inherit from SATemplate.
  * You must override the DrawImplement() method, otherwise the subassembly will do nothing.
  * The other overridden methods may be removed if they are not used.
  * You can add your own functions and subroutines within the class's scope.
