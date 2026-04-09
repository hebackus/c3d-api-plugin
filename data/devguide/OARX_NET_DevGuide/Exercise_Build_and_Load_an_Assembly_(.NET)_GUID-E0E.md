<!-- ObjectARX and Managed .NET > ObjectARX: Managed .NET Developer's Guide > Getting Started with Microsoft Visual Studio (.NET) > Exercises: Create Your First Project (.NET) > Exercise: Build and Load an Assembly (.NET) -->
<!-- Source: https://help.autodesk.com/cloudhelp/2026/ENU/OARX-DevGuide-Managed/files/GUID-E0EA91B2-E833-477C-9F4F-B900E02891D5.htm -->

# Exercise: Build and Load an Assembly (.NET)

Now that you have created a project and defined a command, you are almost ready to execute the command in AutoCAD. Before you can execute the command in AutoCAD, you need to first compile or build a .NET assembly file for your project. 

If you want to distribute your project for others to use, you will need to build a .NET assembly from your project. 

Once a .NET assembly is built, you can then load it in AutoCAD with the NETLOAD command. 

## To build a project and load a .NET assembly

  1. In Microsoft Visual Studio, click Build menu  Build MyFirstProject. 

The project should build successfully, unless something is wrong with the code in the project. Look at the Output window for information on the build status of the project. The location of the _MyFirstProject.dll_ file that is built is also displayed in the Output window. 

  2. Start AutoCAD if it is not already running. 
  3. In AutoCAD, at the Command prompt, enter **netload**. 
  4. In the Choose .NET Assembly dialog box, browse to the location of the _MyFirstProject.dll_ that is displayed in the Output window in Microsoft Visual Studio and select it. Click Open. 
  5. At the Command prompt, enter **adskgreeting**. 

A new MText object is created at the coordinates 2,2 with the text string “Greetings, Welcome to AutoCAD .NET“.
