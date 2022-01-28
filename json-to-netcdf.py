from argparse import ArgumentParser
from copy import deepcopy
import numpy as np
import numbers
import json
import re

from netCDF4 import Dataset

argparser = ArgumentParser(description="Parse JSON format to netCDF format.")
argparser.add_argument("input", help="Input JSON file path.")
argparser.add_argument("output", help="Output netCDF file path.")
args = argparser.parse_args()

def parse(json, nc_root, hierarchy):
    hierarchy = deepcopy(hierarchy)
    cur_group = nc_data["/" + "/".join(hierarchy)] if len(hierarchy) > 0 else nc_data

    for name, data in json.items():
        if isinstance(data, dict):
            nc_root.createGroup("/" + "/".join(hierarchy + [name]))
            parse(data, nc_root, hierarchy + [name])
        elif isinstance(data, list) and not all(isinstance(x, numbers.Number) for x in data):
            for obj, i in zip(data, range(len(data))):
                nc_root.createGroup("/" + "/".join(hierarchy + [name + "[" + str(i) + "]"]))
                parse(obj, nc_root, hierarchy + [name + "[" + str(i) + "]"])
        elif isinstance(data, list):
            np_data = np.array(data)
            dims = np_data.shape
            dim_names = ["DIM" + str(d) + "_" + name for d in range(len(dims))]
            for dim_name, dim in zip(dim_names, dims):
                cur_group.createDimension(dim_name, dim);
            nc_var = nc_root.createVariable("/" + "/".join(hierarchy + [name]), np_data.dtype, tuple(dim_names))
            nc_var[:] = np_data
        elif isinstance(data, numbers.Number) and not isinstance(data, bool):
            np_data = np.array(data)
            nc_var = nc_root.createVariable("/" + "/".join(hierarchy + [name]), np_data.dtype)
            nc_var[:] = np_data
        else:
            try:
                setattr(cur_group, name, data)
            except:
                setattr(cur_group, name, str(data))

def walktree(root):
    yield root.groups.values()
    for value in root.groups.values():
        yield from walktree(value)

with open(args.input) as json_file:
    json_data = json.loads(json_file.read())
nc_data = Dataset(args.output, "w", format="NETCDF4")
parse(json_data, nc_data, [])
print(nc_data)
for children in walktree(nc_data):
    for child in children:
        print(child)
nc_data.close()
