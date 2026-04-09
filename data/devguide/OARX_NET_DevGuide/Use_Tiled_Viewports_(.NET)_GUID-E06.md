<!-- ObjectARX and Managed .NET > ObjectARX: Managed .NET Developer's Guide > Control the AutoCAD Environment (.NET) > Control the Drawing Windows (.NET) > Use Tiled Viewports (.NET) -->
<!-- Source: https://help.autodesk.com/cloudhelp/2026/ENU/OARX-DevGuide-Managed/files/GUID-E066A548-6A42-4F23-ADD2-EE8DA239139A.htm -->

# Use Tiled Viewports (.NET)

AutoCAD usually begins a new drawing using a single tiled viewport that fills the entire graphics area. You can split the drawing area of the Model tab to display several viewports simultaneously. For example, if you keep both the full and the detail views visible, you can see the effects of your detail changes on the entire drawing. In each tiled viewport, you can do the following: 

  * Zoom, set the Snap, Grid, and UCS icon modes, and restore named views in individual viewports 
  * Draw from one viewport to another when executing a command 
  * Name a configuration of viewports so you can reuse it 

You can display tiled viewports in various configurations. How you display the viewports depends on the number and size of the views you need to see. Tiled viewports in model space are stored in the Viewport table 

Tiled viewports are stored in the Viewports table. Each record in the Viewports table represents a single viewport and unlike other table records, there might be multiple Viewport table records with the same name. Each of the records with the same name are used to control which viewports are displayed. 

For example, the Viewport table records named "*Active" represent the tiled viewports that are currently displayed on the Model tab.
