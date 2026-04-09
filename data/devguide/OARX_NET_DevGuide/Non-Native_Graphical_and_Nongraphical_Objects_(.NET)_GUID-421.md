<!-- ObjectARX and Managed .NET > ObjectARX: Managed .NET Developer's Guide > Basics of the AutoCAD .NET API (.NET) > Understand the AutoCAD Object Hierarchy (.NET) > Non-Native Graphical and Nongraphical Objects (.NET) -->
<!-- Source: https://help.autodesk.com/cloudhelp/2026/ENU/OARX-DevGuide-Managed/files/GUID-4213EB7F-C21F-4361-BF12-176F897F44C8.htm -->

# Non-Native Graphical and Nongraphical Objects (.NET)

The AutoCAD .NET API is a cross implementation of ObjectARX and ActiveX Automation. While you can use ActiveX Automation from an ObjectARX application, the AutoCAD .NET API provides direct access to the objects of the ActiveX Automation library. As you work with objects using the native AutoCAD .NET API, you can also access the equivalent COM object from a property. In some cases, the COM object is the only way to access an AutoCAD feature programmatically. Some examples of properties that expose COM objects through the AutoCAD .NET API are, Preferences, Menubar, MenuGroups, AcadObject and AcadApplication. 

Note: When working with COM objects, you will want to make sure you reference the AutoCAD type library. 

The Preferences property of the Application object provides access to a set of COM objects, each corresponding to a tab in the Options dialog box. Together, these objects provide access to all the registry-stored settings in the Options dialog box. You can also set and modify options (and system variables that are not part of the Options dialog box) with the SetSystemVariable and GetSystemVariable methods of the Application object. 

Accessing COM objects is useful if you are working with existing code that might have been originally developed for VB or VBA, or even when working with a third-party library that might work with the AutoCAD ActiveX Automation library with the AutoCAD .NET API. Like the Preferences object, you can also access utilities which translate coordinates or define a new point based on an angle and distance using the Utility object which can be accessed from the AcadApplication COM object which is the equivalent of the Application object in the AutoCAD .NET API. 

Note: When working with both the AutoCAD .NET API and ActiveX Automation, and you create custom functions that might need to return an object, it is recommended to return an ObjectId instead of the object itself.
