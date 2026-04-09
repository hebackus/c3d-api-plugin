<!-- ObjectARX and Managed .NET > ObjectARX: Managed .NET Developer's Guide > Use Events (.NET) > Guidelines for Event Handlers (.NET) -->
<!-- Source: https://help.autodesk.com/cloudhelp/2026/ENU/OARX-DevGuide-Managed/files/GUID-FE7D58D5-28A0-4C98-A876-D4D48F06D0B2.htm -->

# Guidelines for Event Handlers (.NET)

It is important to remember that events simply provide information on the state or activities taking place within AutoCAD. Although event handlers can be written to respond to those events, AutoCAD might be in the middle of an operation when the event handler is triggered. Event handlers, therefore, have some restrictions on what they can do if they are to provide safe operations in conjunction with AutoCAD and its database. 

  * Do not rely on the sequence of events. 

When writing event handlers, do not rely on the sequence of events to happen in the exact order you think they occur. For example, if you issue an OPEN command, the events CommandWillStart, DocumentCreateStarted, DocumentCreated, and CommandEnded will all be triggered. However, they may not occur in that exact order each and everytime. The only thing you can rely on is that a most events occur in pairs, a beginning and ending event. 

  * Do not rely on the sequence of operations. 

If you delete object1 and then object2, do not rely on the fact that you will receive the ObjectErased event for object1 and then for object2. You may receive the ObjectErased event for object2 first. 

  * Do not attempt any interactive functions from an event handler. 

Attempting to execute interactive functions from within an event handler can cause serious problems, as AutoCAD may still be processing a command at the time the event is triggered. Therefore, you should always avoid requesting for input at the Command prompt, as well as object selection requests, and using the SendStringToExecute method from within event handlers. 

  * Do not launch a dialog box from within an event handler. 

Dialog boxes are considered interactive functions and can interfere with the current operation of AutoCAD. Message boxes and alert boxes are not considered interactive and can be issued safely; however issuing a message box within some event handlers such as EnterModal, LeaveModal, DocumentActivated, and DocumentToBeDeactivated can result in unexpected sequencing. 

  * You can write data to any object in the database, but modifying the object that issued the event should be avoided. 

Obviously, any object causing an event to be triggered could still be open and the operation currently in progress. Therefore, avoid modifying an object from an event handler for the same object. However, you can safely read information from the object triggering an event. 

  * Do not perform any action from an event handler that might trigger the same event. 

If you perform the same action in an event handler that triggers that same event, you will create an infinite loop. For example, you should never attempt to open an object from within the ObjectOpenedForModify event, or AutoCAD will simply continue to open objects. 

  * No events are fired while AutoCAD is displaying a modal dialog box.
