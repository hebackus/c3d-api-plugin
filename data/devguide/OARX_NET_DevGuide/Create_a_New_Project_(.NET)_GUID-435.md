<!-- ObjectARX and Managed .NET > ObjectARX: Managed .NET Developer's Guide > Getting Started with Microsoft Visual Studio (.NET) > Work with Microsoft Visual Studio Projects (.NET) > Create a New Project (.NET) -->
<!-- Source: https://help.autodesk.com/cloudhelp/2026/ENU/OARX-DevGuide-Managed/files/GUID-43564EB9-F843-4771-823C-573495EE23E0.htm -->

# Create a New Project (.NET)

New projects are created based on a project template. When creating a new project that will be built into a DLL assembly that will be loaded into AutoCAD, use the Class Library template that comes with Microsoft Visual Studio or one of the AutoCAD Managed project application templates that get installed with the AutoCAD .NET Wizard. Both types of templates are available for the VB.NET and C# programming languages. After a new project is created, you will need to reference the files that make up the AutoCAD .NET API. 

## Procedures

**To create a new project using a standard template**

  1. In Microsoft Visual Studio, on the Start window, click Create a New Project. 

If the Start window isn't displayed, click File menu  New  Project to create a new project. 

  2. In the Create a New Project dialog box, from the Language drop-down list, select C# (or Visual Basic). 
  3. From the Platforms drop-down list, select Windows. 
  4. From the Project Types drop-down list, select Library. 
  5. In the Templates list, select Class Library - A project for creating a class library that targets .NET or .NET Standard. 

To utilize forms in your application, Select WPF Class Library - A project for creating a class library that targets a .NET WPF Application. 

Warning: Make sure to not select the Class Library (.NET Framework) or Class Library (Universal Windows) template. 

Note: If you created a C# or VB Class Library, it can be changed to a WPF Class Library by editing the project file and adding the attribute <UseWPF>true</UseWPF> to the PropertyGroup element. 

  
  

  6. Click Next. 
  7. In the Configure Your New Project dialog box, click in the Project Name box and enter a name for the new project. 

  
  

  8. In the Location box, enter a location or click Browse to select a folder for the new project. 
  9. In the Solution Name box, enter a name for the new solution that the project will be added to. 
  10. Optionally, clear the Place Solution and Project in the Same Directory check box to create a sub-folder under the solution for the project. 
  11. Click Next. 
  12. In the Additional Information dialog box, from the Framework drop-down list, select .NET 8.0 (Long Term Support). 

  
  

  13. Click Create. 
  14. On the Solution Explorer, right-click over the project's node and choose **Edit Project File**. 
  15. In the editor window, add the following in bold within the Project element and below the ProjectGroup element. 
         
         <Project Sdk="Microsoft.NET.Sdk">
         
           <PropertyGroup>
             <TargetFramework>net8.0</TargetFramework>
             <ImplicitUsings>enable</ImplicitUsings>
             <Nullable>enable</Nullable>
           </PropertyGroup>
         
          ** <ItemGroup>
             <FrameworkReference Include="Microsoft.WindowsDesktop.App"></FrameworkReference>
           </ItemGroup>
         **</Project>

Note: TargetFramework can also be updated from net8.0 to net8.0-windows to target the Windows OS and utilize Windows related libraries. Instead of editing the value directly in the project's file, the value can be made under the Application section of the Project Properties window. 

  16. Save and close the project file. 

**To create a new project using an AutoCAD Managed template**

Before using one of the AutoCAD Managed templates, you must first download and install the latest release of the ObjectARX SDK. 

  1. In Microsoft Visual Studio, click File menu  New  Project (or click File menu  New Project). 
  2. In the Create a New Project dialog box, click in the Search box and enter **AutoCAD**. 
  3. From the Templates list, select AutoCAD <release> C Sharp Plug-in (or AutoCAD <release> VB Plug-in). 

  
  

  4. Click Next. 
  5. In the Configure Your New Project dialog box, click in the Project Name box and enter a name for the new project. 

  
  

  6. In the Location box, enter a location or click Browse to select a folder for the new project. 
  7. In the Solution Name box, enter a name for the new solution that the project will be added to. 
  8. Optionally, clear the Place Solution and Project in the Same Directory check box to create a sub-folder under the solution for the project. 
  9. Click Create. 
  10. In the AutoCAD .NET Wizard Configurator dialog box, specify the libraries to reference to the project. 

  
  

  11. Click OK.
