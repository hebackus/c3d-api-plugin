<!-- ObjectARX and Managed .NET > ObjectARX: Managed .NET Developer's Guide > Use Events (.NET) > Register and Unregister Events (.NET) -->
<!-- Source: https://help.autodesk.com/cloudhelp/2026/ENU/OARX-DevGuide-Managed/files/GUID-5089A5B4-5553-4A4C-A88B-455AA29A0E96.htm -->

# Register and Unregister Events (.NET)

Before you can respond to an event, the event must be registered with AutoCAD. You register an event by creating a new event handler of the desired type and then assigning it to the object in which you want to register the event with. Once you are done with an event, it is best to unregister the event to minimize conflicts with other reactors as well as reduce the about of memory and CPU usage that AutoCAD requires to maintain your event handler. 

## Register an event

You register an event by appending an event handler to an event. The event handler object requires a procedure that you must have defined in your project. Most event handlers require a procedure that accepts two parameters, one of the type Object and another that represents the return arguments of the event. You register an event by using the VB.NET AddHandler statement or the C# += operator. 

The following code registers a procedure named appSysVarChanged with an object type of SystemVariableChangedEventHandler to the SystemVariableChanged event. The appSysVarChanged procedure accepts two parameters: Object and SystemVariableChangedEventArgs. The SystemVariableChangedEventArgs object returns the name of the system variable changed when the event is registered. 

### C#
    
    
    Application.SystemVariableChanged += 
                new SystemVariableChangedEventHandler(appSysVarChanged);

### VB.NET
    
    
    AddHandler Application.SystemVariableChanged, AddressOf appSysVarChanged

## Unregister an event

An event is unregistered by removing an event handler from the event in which it is assigned. You use the same syntax in which was used to register the event handler with an event with the exception you use RemoveHandler or the -= operator. 

The following code will unregister a procedure named appSysVarChanged with an object type of SystemVariableChangedEventHandler from the SystemVariableChanged event. 

### C#
    
    
    Application.SystemVariableChanged -= 
                new SystemVariableChangedEventHandler(appSysVarChanged);

### VB.NET
    
    
    RemoveHandler Application.SystemVariableChanged, AddressOf appSysVarChanged
