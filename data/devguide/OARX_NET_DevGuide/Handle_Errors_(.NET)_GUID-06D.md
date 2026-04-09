<!-- ObjectARX and Managed .NET > ObjectARX: Managed .NET Developer's Guide > Develop Applications (.NET) > Handle Errors (.NET) -->
<!-- Source: https://help.autodesk.com/cloudhelp/2026/ENU/OARX-DevGuide-Managed/files/GUID-06DF188F-C832-4406-93E7-99F008B9F124.htm -->

# Handle Errors (.NET)

Most development environments provide default error handling. For .NET, the default reaction to an error is to display an error message and terminate the application. While this behavior is adequate during the development, it is not productive for the user. 

Errors raised during execution should be handled and not left to the user to encounter whenever possible. When designing an application, you should catch all possible errors and then determine how to respond to them. In some situations an error can be safely ignored, while in others you will need to handle the error with a specific response in order for the application to continue. 

When you catch an error, the default error message is suppressed and the application does not automatically terminate. With the default error message suppressed, you can display a custom error message or have the application handle the error. 

In general, error handling is necessary whenever user input is required, during file I/O operations, and when a database or object is being accessed. Even if you are sure a file or object is available, there may be conditions you have not thought of that could cause errors. 

Note: Most of the code examples provided in this documentation do not use error handling or the error handling is limited in scope. This keeps the examples simple and to the point. However, as with all programming languages, proper error handling is essential for a robust application.
