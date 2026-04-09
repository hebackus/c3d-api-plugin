<!-- ObjectARX and Managed .NET > ObjectARX: Managed .NET Developer's Guide > About .NET and the AutoCAD .NET API (.NET) > Overview of Microsoft Visual Studio (.NET) > Programming Differences Between C++ and .NET (.NET) -->
<!-- Source: https://help.autodesk.com/cloudhelp/2026/ENU/OARX-DevGuide-Managed/files/GUID-DB165894-208B-490E-8382-6BEF5BCA2452.htm -->

# Programming Differences Between C++ and .NET (.NET)

There are some distinct differences between ObjectARX classes and their .NET counterparts; these differences require some subtle but important code practice changes. 

The following sections offer general suggestions for working with the managed wrapper classes. 

## Memory Management and Dispose Pattern

C++ uses destructors to clean up resources. ObjectARX managed wrappers implement the IDisposable interface to do the same. The managed wrappers derive from the common base class DisposableWrapper, whose purpose is to manage the unmanaged memory. 

Because the underlying resources used by ObjectARX managed wrappers are unmanaged classes, you must actively call Dispose on the managed wrappers. Doing so releases the resources owned by base types all the way up the hierarchy. Do not rely on .NET garbage collection to free the memory used by unmanaged resources. 

## Object Identity

The ObjectARX managed wrappers do not guarantee that you receive the same .NET object every time you access a C++ object. For example, opening the same object in the database twice in succession yields two different wrappers. However, DisposableWrapper (the common base class for ObjectARX managed wrappers) overrides Equals and GetHashCode. Equals compares the underlying unmanaged pointers, and GetHashCode returns the underlying unmanaged pointer. This effectively ensures that .NET clients perceive these two different wrapper objects as identical. 

## Error Handling

ObjectARX uses the return value of functions to indicate error conditions. The preferred way of signaling error in .NET is to raise an exception. The ObjectARX managed wrappers translate ObjectARX error codes into exceptions. Some error codes are mapped to .NET native exceptions, while others are mapped to custom exception types exposed by the managed wrappers. 

## Get and Set Methods Versus Properties

Object properties are modeled as get and set methods in C++. On the other hand, .NET makes properties a primary abstraction of the execution environment. The ObjectARX managed wrappers map get and set methods to .NET properties appropriately. 

## Reactors Versus Events

ObjectARX uses reactors to model events. Because .NET makes events a primary abstraction, the ObjectARX managed wrappers map reactors to events. 

Unmanaged reactors require two classes: the event source class and the abstract reactor class. The event source class is instantiated by the system and exposes the addReactor() and removeReactor() functions. The client derives a concrete reactor class from the abstract reactor, instantiates the concrete reactor, and adds it to the event source. The event source calls virtual functions in the concrete reactor when events occur. 

The ObjectARX managed wrappers model the reactor pattern as one event source class with managed events. 

## Collections and Iteration

In ObjectARX, iteration methods are not standardized across classes. For the managed wrappers, two interfaces make iteration consistent. Collections implement IEnumerable. Iterators that are returned by GetEnumerator implement IEnumerator. 

If you explicitly call GetEnumerator method on a dynamic object, then you need to dispose it explicitly. See the example code: 
    
    
    Database db = HostApplicationServices.WorkingDatabase;
    dynamic dynamicDb = HostApplicationServices.WorkingDatabase;
    var lineTypeTable = dynamicDb.LinetypeTableId;
    var stEnumerator = lineTypeTable.GetEnumerator();
    stEnumerator.Dispose();

## Command Registration

ObjectARX allows extension applications to register commands with AutoCAD. This registration is implicit: the application must be run to find out what commands it wants to register. 

.NET encourages applications to use declarative style to define their behavior. The ObjectARX managed wrappers make command registration declarative. Custom attributes are used to denote command methods. See Command Definition (.NET) for code examples and detailed information. 

## Global Functions

Global functions do not exist in the ObjectARX managed wrappers, so many of the ObjectARX global functions map to new .NET objects or to new properties on existing objects. 

For example, one group of ObjectARX global functions is used by applications to interact with the AutoCAD command prompt. In the ObjectARX managed wrappers, a new CommandLinePrompt class encapsulates this functionality. 

Another category of ObjectARX global functions returns pointers to instance objects. For example, ObjectARX uses acdbTransactionManagerPtr() to return a pointer to the AcDbTransactionManager. Functions like this have been mapped to object properties in .NET, so the database now has a TransactionManager property.
