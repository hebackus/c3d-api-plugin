<!-- ObjectARX and Managed .NET > ObjectARX: Managed .NET Developer's Guide > Getting Started with Microsoft Visual Studio (.NET) > Load an Assembly (.NET) > Application Initialization and Load-Time Optimization (.NET) -->
<!-- Source: https://help.autodesk.com/cloudhelp/2026/ENU/OARX-DevGuide-Managed/files/GUID-FA3B4125-F7BD-4E89-969F-9DCC90AC6977.htm -->

# Application Initialization and Load-Time Optimization (.NET)

Managed applications can choose to perform initialization or termination tasks by implementing the optional Autodesk.AutoCAD.Runtime.IExtensionApplication interface. 

The interface Autodesk.AutoCAD.Runtime.IExtensionApplication provides the Initialize() and Terminate() methods. Since managed applications cannot be manually unloaded, any implementation of the Terminate() method is called when the AutoCAD program closes. 

If your application defines a large number of data types, you can optimize its load-time performance by implementing IExtensionApplication and using two optional custom attributes. These attributes—ExtensionApplication and CommandClass—help the AutoCAD program find the application's initialization routine and command handlers. 

Any managed application can use these attributes. However, their optimizing effects are measurable only in larger applications. 

## Use the ExtensionApplication and CommandClass Attributes

When the AutoCAD program loads a managed application, it queries the application's assembly for an ExtensionApplication attribute. If this attribute is found, the AutoCAD program sets the attribute's associated type as the application's entry point. If no such attribute is found, AutoCAD searches all exported types for an IExtensionApplication implementation. If no implementation is found, the AutoCAD program skips the application-specific initialization step. 

The ExtensionApplication attribute can be attached to only one type. The type to which it is attached must implement the IExtensionApplication interface. 

In addition to searching for an implementation of IExtensionApplication in an application, the AutoCAD program queries the application's assembly for one or more CommandClass attributes. If instances of this attribute are found, the AutoCAD program searches only their associated types for command methods. Otherwise, it searches all exported types. 

A CommandClass attribute may be declared for any type that defines an AutoCAD command handler. If an application uses the CommandClass attribute, it must declare an instance of this attribute for every type that contains an AutoCAD command handler method. 

The following procedure describes how these attributes are used. 

  1. Define a type that implements Autodesk.AutoCAD.Runtime.IExtensionApplication. 

If you do not need to perform initialization or termination tasks, provide blank implementations of the interface methods. 

  2. In the assembly context, declare an ExtensionApplication attribute. 
  3. Pass the type that implements the IExtensionApplication interface to the ExtensionApplication attribute. 
  4. In the assembly context, declare a CommandClass attribute for each class that defines AutoCAD command methods. 
  5. Pass the type of the command method's class to the CommandClass attribute. 

Note: These attributes must be declared in the assembly context. 

### C#
    
    
    ...
    using Autodesk.AutoCAD.Runtime;
    using Autodesk.AutoCAD.Interop;
    using Autodesk.AutoCAD.ApplicationServices;
    using Autodesk.AutoCAD.DatabaseServices;
    
    [assembly: ExtensionApplication(typeof(HelloWorld.HelloWorldApp))]
    [assembly: CommandClass(typeof(HelloWorld.HelloWorldCommands))]
    
    namespace HelloWorld
    {
        public class HelloWorldApp : Autodesk.AutoCAD.Runtime.IExtensionApplication
        {
            ...
        }
    
        public class HelloWorldCommands
        {
            // Defines a command that prompts a message on the AutoCAD
            // command line.
            [CommandMethod("HELLO")]
            public void HelloCommand()
            {
                ...
            }
        }
    }

### VB.NET
    
    
    ...
    Imports Autodesk.AutoCAD.Runtime
    Imports Autodesk.AutoCAD.Interop
    Imports Autodesk.AutoCAD.ApplicationServices
    Imports Autodesk.AutoCAD.DatabaseServices
    
    <Assembly: ExtensionApplication(GetType(HelloWorld.HelloWorldApp))>
    <Assembly: CommandClass(GetType(HelloWorldCommands))>
    
    Namespace HelloWorld
        Public Class HelloWorldApp
            Implements Autodesk.AutoCAD.Runtime.IExtensionApplication
            ...
        End Class
    
        Public Class HelloWorldCommands
            ' Defines a command that prompts a message on the AutoCAD
            ' command line.
            <Autodesk.AutoCAD.Runtime.CommandMethod("HELLO")>
            Public Sub HelloCommand()
                ...
            End Sub
        End Class
    End Namespace
