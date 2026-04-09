<!-- ObjectARX and Managed .NET > ObjectARX: Managed .NET Developer's Guide > Use Events (.NET) -->
<!-- Source: https://help.autodesk.com/cloudhelp/2026/ENU/OARX-DevGuide-Managed/files/GUID-61F01DC0-F385-43A2-8040-140C051B171E.htm -->

# Use Events (.NET)

Events are notifications, or messages, that are sent out by AutoCAD® to inform you about the current state of the session, or alert you that something has happened. For example, when a drawing is saved the BeginSave event is triggered. There are other events triggered when a drawing is closed, a command is started or even when a system variable is changed. Given this information you could write a subroutine, or event handler, that uses these events to track changes to a drawing or the amount of time a user spends working on a particular drawing.
