<!-- ObjectARX and Managed .NET > ObjectARX: Managed .NET Developer's Guide > Control the AutoCAD Environment (.NET) > Control the Drawing Windows (.NET) > Update the Geometry in the Document Window (.NET) -->
<!-- Source: https://help.autodesk.com/cloudhelp/2026/ENU/OARX-DevGuide-Managed/files/GUID-4271D259-52E6-42B2-8F2B-7219186CE115.htm -->

# Update the Geometry in the Document Window (.NET)

Many of the actions you perform through the AutoCAD .NET API modify what is displayed in the drawing area. Not all of these actions immediately update the display of the drawing. This is designed so you can make several changes to the drawing without waiting for the display to be updated after every single action. Instead, you can bundle your actions together and make a single call to update the display when you have finished. 

The methods that will update the display are UpdateScreen (Application and Editor objects) and Regen (Editor object). 

The UpdateScreen method redraws the application or document windows. The Regen method regenerates the graphical objects in the drawing window, and recomputes the screen coordinates and view resolution for all objects. It also re-indexes the drawing database for optimum display and object selection performance. 

## C#
    
    
    // Redraw the drawing
    Application.UpdateScreen();
    Application.DocumentManager.MdiActiveDocument.Editor.UpdateScreen();
     
    // Regenerate the drawing
    Application.DocumentManager.MdiActiveDocument.Editor.Regen();

## VB.NET
    
    
    '' Redraw the drawing
    Application.UpdateScreen()
    Application.DocumentManager.MdiActiveDocument.Editor.UpdateScreen()
     
    '' Regenerate the drawing
    Application.DocumentManager.MdiActiveDocument.Editor.Regen()

## VBA/ActiveX Code Reference
    
    
    '' Redraw the drawing
    ThisDrawing.Application.Update
     
    '' Regenerate the drawing
    ThisDrawing.Regen
