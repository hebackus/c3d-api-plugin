<!-- ObjectARX and Managed .NET > ObjectARX: Managed .NET Developer's Guide > Getting Started with Microsoft Visual Studio (.NET) > Exercises: Create Your First Project (.NET) > Exercise: Create a New Project (.NET) -->
<!-- Source: https://help.autodesk.com/cloudhelp/2026/ENU/OARX-DevGuide-Managed/files/GUID-23E33075-3C36-48CA-B937-B85606B77F71.htm -->

# Exercise: Create a New Project (.NET)

In this exercise, you will create a new project named “MyFirstProject” and reference the files of the AutoCAD .NET API. 

## To create a new project named “MyFirstProject”

  1. In Microsoft Visual Studio 2022, on the Start window, click Create a New Project. 

If the Start window isn't displayed, click File menu  New  Project to create a new project. 

  2. In the Create a New Project dialog box, from the Language drop-down list, select C# (or Visual Basic). 
  3. From the Platforms drop-down list, select Windows. 
  4. From the Project Types drop-down list, select Library. 
  5. In the Templates list, select Class Library - A project for creating a class library that targets .NET or .NET Standard. 

  
  

  6. Click Next. 
  7. In the Configure Your New Project dialog box, click in the Project Name box and enter **MyFirstProject**. 

  
  

  8. In the Location box, click Browse to specify a new location or accept the default location. 

Tip: To change the default location for new projects, display the Options dialog box and select the Projects and Solutions folder from the navigation pane. Click the ellipsis button to the right of the Visual Studio Projects Location and browse to a new default location. 

  9. Optionally, in the Solution Name box, enter a name for the new solution that the project will be added to. 
  10. Optionally, check or clear the Place Solution and Project in the Same Directory check box to create a sub-folder under the solution for the project. 
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

  16. Save and reopen the project in Visual Studio 2022.
