<!-- ObjectARX and Managed .NET > ObjectARX: Managed .NET Developer's Guide > Basics of the AutoCAD .NET API (.NET) > Understand the AutoCAD Object Hierarchy (.NET) > The Application Object (.NET) -->
<!-- Source: https://help.autodesk.com/cloudhelp/2026/ENU/OARX-DevGuide-Managed/files/GUID-06F95957-9A08-4036-BFB6-541C5B5F3A15.htm -->

# The Application Object (.NET)

The Application object is the root object of the AutoCAD .NET API. From the Application object, you can access the main window as well as any open drawing. Once you have a drawing, you can then access the objects in the drawing. 

For example, the Application object has a DocumentManager property that returns the DocumentCollection object. This object provides access to the drawings that are currently open in AutoCAD and allows you to create, save and open drawing files. Other properties of the Application object provide access to the application-specific data such as InfoCenter, the main window, and the status bar. The MainWindow property allows access to the application name, size, location, and visibility. 

While most of the properties of the Application object allow access to objects in the AutoCAD .NET API, there are some that reference objects in the AutoCAD ActiveX® Automation. These properties include a COM version of the application object (AcadApplication), the menubar (MenuBar), loaded menugroups (MenuGroups), and preferences (Preferences). 

| 

DocumentManager
     Container for all the document objects (there is a document object for each drawing that is open). 
DocumentWindowCollection
     Container for all the document window objects (there is a document window object for each document object in the DocumentManager). 
InfoCenter
     Contains a reference to the InfoCenter toolbar. 
MainWindow
     Contains a reference to the application window object of AutoCAD. 
MenuBar
     Contains a reference to the MenuBar COM object for the menubar in AutoCAD. 
MenuGroups
     Contains a reference to the MenuGroups COM object which contains the customization group name for each loaded CUIx file. 
Preferences
     Contains a reference to the Preferences COM object which allows you to modify many of the settings in the Options dialog box. 
Publisher
     Contains a reference to the Publisher object which is used for publishing drawings. 
StatusBar
     Contains a reference to the StatusBar object for the application window. 
UserConfigurationManager
     Contains a reference to the UserConfigurationManager object which allows you to work with user saved profiles.   
---|---
