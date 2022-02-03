# json-netcdf

`usage: json-netcdf.py [-h] input output`

json-netcdf converts between JSON files and netCDF4 files.

Since JSON and netCDF4 files are not 100% interchangable, there are some details that should be kept in mind when using this tool.

## JSON -> netCDF
1. Numeric array dimensions are added liberally - for any numeric array "X" with n dimensions, dimensions "DIM0_X", "DIM1_X", ..., "DIMn_X" will be created in the local group.
2. Non-numeric lists are convereted into JSON objects where each entry's name is the parent object's name plus its index. For example, an object named "OBJ" containing ["Hello", 1.1] would be converted into one group "OBJ" containing groups "OBJ[0]" and "OBJ[1]" - those 2 groups contain the data in the array.
