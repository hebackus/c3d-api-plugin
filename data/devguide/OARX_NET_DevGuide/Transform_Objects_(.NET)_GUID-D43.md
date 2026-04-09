<!-- ObjectARX and Managed .NET > ObjectARX: Managed .NET Developer's Guide > Create and Edit AutoCAD Entities (.NET) > Edit Named and 2D Objects (.NET) > Transform Objects (.NET) -->
<!-- Source: https://help.autodesk.com/cloudhelp/2026/ENU/OARX-DevGuide-Managed/files/GUID-D4348E23-7ECB-48F6-90B7-FB7EF42DFA8D.htm -->

# Transform Objects (.NET)

You move, scale, rotate and mirror an object using a 4 by 4 transformation matrix represented by a Matrix3d object and the TransformBy method. You can also use the GetTransformedCopy method to create a copy of an entity and then apply the transformation to the copy. The Matrix3d object is part of the Geometry namespace. 

The first three columns of the matrix specify scale and rotation. The fourth column of the matrix is a translation vector. The following table demonstrates the transformation matrix configuration, where R = Rotation and T = Translation: 

Transformation matrix configuration   
---  
R00  |  R01  |  R02  |  T0   
R10  |  R11  |  R12  |  T1   
R20  |  R21  |  R22  |  T2   
0  |  0  |  0  |  1   
  
To transform an object, first initialize a Matrix3d object. You can initialize the transformation matrix using an array of doubles or starting with a matrix in which represents the World coordinate system or a user coordinate system. Once initialized, you then use the functions of the Matrix3d object to modify the scaling, rotation, or displacement transformation of the matrix. 

After the transformation matrix is complete, apply the matrix to the object using the TransformBy method. The following line of code demonstrates applying a matrix (dMatrix) to an object (acObj): 

### C#
    
    
    acObj.TransformBy(dMatrix);

### VB.NET
    
    
    acObj.TransformBy(dMatrix)

## Example of a rotation matrix

The following shows a single data array to define a transformation matrix, assigned to the variable dMatrix, which will rotate an entity by 90 degrees about the point (0, 0, 0). 

Rotation Matrix: 90 degrees about point (0, 0, 0)   
---  
0.0  |  -1.0  |  0.0  |  0.0   
1.0  |  0.0  |  0.0  |  0.0   
0.0  |  0.0  |  1.0  |  0.0   
0.0  |  0.0  |  0.0  |  1.0   
  
### C#

Initialize a transformation matrix with a data array in which contains the information to rotate an object 90 degrees. 
    
    
    double[] dMatrix = new double[16];
     
    dMatrix[0] = 0.0;
    dMatrix[1] = -1.0;
    dMatrix[2] = 0.0;
    dMatrix[3] = 0.0;
    dMatrix[4] = 1.0;
    dMatrix[5] = 0.0;
    dMatrix[6] = 0.0;
    dMatrix[7] = 0.0;
    dMatrix[8] = 0.0;
    dMatrix[9] = 0.0;
    dMatrix[10] = 1.0;
    dMatrix[11] = 0.0;
    dMatrix[12] = 0.0;
    dMatrix[13] = 0.0;
    dMatrix[14] = 0.0;
    dMatrix[15] = 1.0;
     
    Matrix3d acMat3d = new Matrix3d(dMatrix);

Initialize a transformation matrix without a data array and use the Rotation function to return a transformation matrix that rotates an object 90 degrees. 
    
    
    Matrix3d acMat3d = new Matrix3d();
     
    acMat3d = Matrix3d.Rotation(Math.PI / 2,
                                curUCS.Zaxis,
                                new Point3d(0, 0, 0));

### VB.NET

Initialize a transformation matrix with a data array in which contains the information to rotate an object 90 degrees. 
    
    
    Dim dMatrix(0 To 15) As Double
     
    dMatrix(0) = 0.0
    dMatrix(1) = -1.0
    dMatrix(2) = 0.0
    dMatrix(3) = 0.0
    dMatrix(4) = 1.0
    dMatrix(5) = 0.0
    dMatrix(6) = 0.0
    dMatrix(7) = 0.0
    dMatrix(8) = 0.0
    dMatrix(9) = 0.0
    dMatrix(10) = 1.0
    dMatrix(11) = 0.0
    dMatrix(12) = 0.0
    dMatrix(13) = 0.0
    dMatrix(14) = 0.0
    dMatrix(15) = 1.0
     
    Dim acMat3d As Matrix3d = New Matrix3d(dMatrix)

Initialize a transformation matrix without a data array and use the Rotation function to return a transformation matrix that rotates an object 90 degrees. 
    
    
    Dim acMat3d As Matrix3d = New Matrix3d()
     
    Matrix3d.Rotation(Math.PI / 2, _
                      curUCS.Zaxis, _
                      New Point3d(0, 0, 0))

## Additional examples of transformation matrices

The following are more examples of transformation matrices: 

Rotation Matrix: 45 degrees about point (5, 5, 0)   
---  
0.707107  |  -0.707107  |  0.0  |  5.0   
0.707107  |  0.707107  |  0.0  |  -2.071068   
0.0  |  0.0  |  1.0  |  0.0   
0.0  |  0.0  |  0.0  |  1.0   
  
Translation Matrix: move an entity by (10, 10, 0)   
---  
1.0  |  0.0  |  0.0  |  10.0   
0.0  |  1.0  |  0.0  |  10.0   
0.0  |  0.0  |  1.0  |  0.0   
0.0  |  0.0  |  0.0  |  1.0   
  
Scaling Matrix: scale by 10,10 at point (0, 0, 0)   
---  
10.0  |  0.0  |  0.0  |  0.0   
0.0  |  10.0  |  0.0  |  0.0   
0.0  |  0.0  |  10.0  |  0.0   
0.0  |  0.0  |  0.0  |  1.0   
  
Scaling Matrix: scale by 10,10 at point (2, 2, 0)   
---  
10.0  |  0.0  |  0.0  |  -18.0   
0.0  |  10.0  |  0.0  |  -18.0   
0.0  |  0.0  |  10.0  |  0.0   
0.0  |  0.0  |  0.0  |  1.0
