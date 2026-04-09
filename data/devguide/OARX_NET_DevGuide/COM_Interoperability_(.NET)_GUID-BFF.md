<!-- ObjectARX and Managed .NET > ObjectARX: Managed .NET Developer's Guide > About .NET and the AutoCAD .NET API (.NET) > Overview of Microsoft Visual Studio (.NET) > COM Interoperability (.NET) -->
<!-- Source: https://help.autodesk.com/cloudhelp/2026/ENU/OARX-DevGuide-Managed/files/GUID-BFFF308E-CC10-4C56-A81E-C15FB300EB70.htm -->

# COM Interoperability (.NET)

Microsoft Visual Studio can utilize both native .NET and COM interfaces in the same project. By utilizing COM interop, you can migrate existing code that might have been written in Visual Basic 6 or VBA without having to completely rewrite it. To access the AutoCAD automation objects from a project created in Microsoft Visual Studio, create references to the following files: 

  * The latest AutoCAD or AutoCAD-based Type Library, _acax25enu.tlb _, located at _< drive>:\Program Files\Common Files\Autodesk Shared_. 
  * The AutoCAD/ObjectDBX Common 25.0 Type Library, _axdb25enu.tlb_ , located at _< drive>:\Program Files\Common Files\Autodesk Shared_. 

Note: The previous mentioned type libraries are also available as part of the ObjectARX SDK. 

These references will make the following primary interop assemblies available: 

  * _Autodesk.AutoCAD.Interop.dll_ (for AutoCAD-specific types) 
  * _Autodesk.AutoCAD.Interop.Common.dll_ (for types shared by ObjectDBX™ host applications) 

The interop assemblies are located in the global assembly cache; they map automation objects to their .NET counterparts. 

After you reference the type libraries, you should import the Autodesk.AutoCAD.Interop and Autodesk.AutoCAD.Interop.Common namespaces into the code modules that will utilize the objects defined in the libraries, as in the following examples: 

### C# 
    
    
    using Autodesk.AutoCAD.Interop;
    using Autodesk.AutoCAD.Interop.Common;

### VB.NET
    
    
    Imports Autodesk.AutoCAD.Interop
    Imports Autodesk.AutoCAD.Interop.Common

can declare variables based on objects defined in the libraries, as in the following examples: 

### C#
    
    
    AcadApplication objAcApp;
    AcadLine objLine;

### VB.NET
    
    
    Dim objAcApp As AcadApplication
    Dim objLine As AcadLine

The interop assemblies can be helpful in making the transition from VBA to .NET. However, in order to take full advantage of everything that .NET and the AutoCAD .NET API have to offer, you will need to rewrite your existing VBA code. 

You can get a pointer to a COM object from the corresponding .NET object by using the following properties from the following objects: 

  * ApplicationServices.Application.AcadApplication 
  * DatabaseServices.Database.AcadDatabase 
  * ApplicationServices.Document.AcadDocument 

A COM object can be obtained from a .NET object using the FromAcadXxx static function. For example, Database.FromAcadDatabase gets the .NET database object from the COM database object. 

## Create and Reference the Application

AutoCAD .NET applications can utilize the same type library (_acax25enu.tlb_) as AutoCAD automation projects. The type library is located in _< drive>:\Program Files\Common Files\Autodesk Shared_. 

AutoCAD .NET applications also use the same version-dependent ProgID for the CreateObject, GetObject, and GetInterfaceObject functions. 

You can use the product ProgID to create a new instance of the AutoCAD application ("AutoCAD.Application"), and specify the major and minor number of the release to restrict your application to a specific release or all the releases that are binary compatible with each other. 

For example, 

  * CreateObject("AutoCAD.Application.25.1") attempts to create a new instance of AutoCAD 2026. 
  * CreateObject("AutoCAD.Application.25.0") attempts to create a new instance of AutoCAD 2025. 
  * CreateObject("AutoCAD.Application.25") attempts to create a new instance of AutoCAD 2025 or AutoCAD 2026. 
  * CreateObject("AutoCAD.Application.24.3") attempts to create a new instance of AutoCAD 2024, even if another release that shares the same major version of the product is installed. 
  * CreateObject("AutoCAD.Application.24.2") attempts to create a new instance of AutoCAD 2023, even if another release that shares the same major version of the product is installed. 
  * CreateObject("AutoCAD.Application.24.1") attempts to create a new instance of AutoCAD 2022, even if another release that shares the same major version of the product is installed. 
  * CreateObject("AutoCAD.Application.24.0") attempts to create a new instance of AutoCAD 2021, even if another release that shares the same major version of the product is installed. 
  * CreateObject("AutoCAD.Application.24") attempts to create a new instance of AutoCAD 2021, AutoCAD 2022, AutoCAD 2023, or . AutoCAD 2024
  * CreateObject("AutoCAD.Application.23.1") attempts to create a new instance of AutoCAD 2020, even if another release that shares the same major version of the product is installed. 
  * CreateObject("AutoCAD.Application.23.0") attempts to create a new instance of AutoCAD 2019, even if another release that shares the same major version of the product is installed. 
  * CreateObject("AutoCAD.Application.23") attempts to create a new instance of AutoCAD 2019 or AutoCAD 2020. 
  * CreateObject("AutoCAD.Application.22") attempts to create a new instance of AutoCAD 2018. 
  * CreateObject("AutoCAD.Application.21") attempts to create a new instance of AutoCAD 2017. 
  * CreateObject("AutoCAD.Application.20.1") attempts to create a new instance of AutoCAD 2016, even if another release that shares the same major version of the product is installed. 
  * CreateObject("AutoCAD.Application.20") attempts to create a new instance of AutoCAD 2015 or AutoCAD 2016. 

Note: You must have the corresponding release installed that you are trying to create an instance of. 

If you are using ActiveX/COM from an in-process DLL (Class Library) and want to reference the AutoCAD application object, you can use Autodesk.AutoCAD.ApplicationServices.Application.AcadApplication property.
