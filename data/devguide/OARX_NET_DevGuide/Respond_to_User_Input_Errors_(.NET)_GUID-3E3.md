<!-- ObjectARX and Managed .NET > ObjectARX: Managed .NET Developer's Guide > Develop Applications (.NET) > Handle Errors (.NET) > Respond to User Input Errors (.NET) -->
<!-- Source: https://help.autodesk.com/cloudhelp/2026/ENU/OARX-DevGuide-Managed/files/GUID-3E3E1526-E948-489B-94A4-B8F4A1546459.htm -->

# Respond to User Input Errors (.NET)

The user-input methods provide a certain amount of inherent error trapping in that they require the user to enter a certain type of data. If the user tries to enter some other data, AutoCAD rejects the input and re-prompts the user. Using the PromptXXXOption objects with the appropriate GetXXX or SelectXXX methods provide additional control of the user input but can also introduce additional conditions that must be verified before execution continues.
