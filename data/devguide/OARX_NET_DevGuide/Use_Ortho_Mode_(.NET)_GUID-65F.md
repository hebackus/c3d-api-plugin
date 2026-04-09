<!-- ObjectARX and Managed .NET > ObjectARX: Managed .NET Developer's Guide > Control the AutoCAD Environment (.NET) > Draw With Precision (.NET) > Use Ortho Mode (.NET) -->
<!-- Source: https://help.autodesk.com/cloudhelp/2026/ENU/OARX-DevGuide-Managed/files/GUID-65FBB486-54C8-4746-8834-99524F9F23D3.htm -->

# Use Ortho Mode (.NET)

As you draw lines or move objects, you can use Ortho mode to restrict the cursor to the horizontal or vertical axis. The orthogonal alignment is dependent on the current snap angle and UCS. Ortho mode works with activities that require you to specify a second point, such as when using the GetDistance or GetAngle methods. You can use Ortho not only to establish vertical or horizontal alignment but also to enforce parallelism or create regular offsets. 

By allowing AutoCAD to impose orthogonal restraints, you can draw more quickly. For example, you can create a series of perpendicular lines by turning on Ortho mode before you start drawing. Because the lines are constrained to the horizontal and vertical axes, you can draw faster, knowing that the lines are perpendicular. 

The following statements turn Ortho mode on. Unlike the grid and snap settings, Ortho mode is maintained in the Database object instead of the active viewport. 

## C#
    
    
    Application.DocumentManager.MdiActiveDocument.Database.Orthomode = true;

## VB.NET
    
    
    Application.DocumentManager.MdiActiveDocument.Database.Orthomode = True

## VBA/ActiveX Code Reference
    
    
    ThisDrawing.ActiveViewport.OrthoOn = True
