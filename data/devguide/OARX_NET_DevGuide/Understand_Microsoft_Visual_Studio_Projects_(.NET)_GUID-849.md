<!-- ObjectARX and Managed .NET > ObjectARX: Managed .NET Developer's Guide > Getting Started with Microsoft Visual Studio (.NET) > Understand Microsoft Visual Studio Projects (.NET) -->
<!-- Source: https://help.autodesk.com/cloudhelp/2026/ENU/OARX-DevGuide-Managed/files/GUID-8495F47A-04DF-479C-9C0D-A5EE214E92F1.htm -->

# Understand Microsoft Visual Studio Projects (.NET)

Project files created with Microsoft Visual Studio are not specific to AutoCAD, but do contain specific project settings that you will need to be familiar with in order to create a DLL assembly file that can be loaded into AutoCAD. This guide focuses on creating projects for Visual C#® with and without the AutoCAD .NET Wizard. 

Note: Visual Basic® (VB) .NET projects can be created, but the guide focuses primarily on C# since it is more prevalent in the industry. 

A project is a collection of code and resource files; class modules, WPF windows, and Windows forms that work together to perform a given function. When a project is created, a solution is also created which contains the project you are creating. A solution is used to reference one or more projects. Usually you do not have to work with a solution directly unless you want to reference the exposed functionality of other projects. 

An example of a multi-project solution is when you have a new project and an existing project that contain a set of methods, functions, and classes that you want to use with a new project. 

A solution can contain any combination of C# and VB.NET projects. Using different types of projects in a single solution allows each developer to use the programming language of his or her choice. 

Project and solution files have the following file extensions: 

  * **CSPROJ** \- Microsoft Visual C# project file 
  * **VBPROJ** \- Microsoft Visual Basic (VB) .NET project file 
  * **SLN** \- Microsoft Visual Studio solution file
