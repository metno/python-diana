#!/usr/bin/env python

# Copyright (C) 2012 met.no
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA  02110-1301  USA

import datetime, sys
from metno.bdiana import BDiana, InputFile

def print_field_groups_and_fields(controller, model):

    refTimes = list(controller.getFieldReferenceTimes())
    refTimes.sort()

    modelName, fieldGroups = controller.getFieldGroups(model, refTimes[-1], False)
    
    fieldGroups = map(lambda g: (g.groupName, g.fieldNames), fieldGroups)
    fieldGroups.sort()

    for groupName, fieldNames in fieldGroups:
    
        print "  ", groupName
        fieldNames.sort()

        for fieldName in fieldNames:
        
            print "   ", fieldName

if __name__ == "__main__":

    if not 1 <= len(sys.argv) <= 2:
    
        sys.stderr.write("Usage: %s [setup file]\n" % sys.argv[0])
        sys.stderr.write("Writes the available fields described by the setup file, if specified.\n")
        sys.exit(1)
    
    bdiana = BDiana(log_level = 5)
    
    if len(sys.argv) == 2:
        setup_path = sys.argv[1]
    else:
        setup_path = bdiana.default_setup_file()
    
    if not bdiana.setup(setup_path):
        print "Failed to parse", setup_path
        sys.exit(1)
    
    info = bdiana.getFieldModels()
    groups = []

    for di in info:
    
        models = di.modelNames
        groups.append((di.groupName, models))
    
    groups.sort()
    fieldManager = bdiana.controller.getFieldManager()

    for group, models in groups:

        if group == "ARKIV":
            continue

        print group
        models.sort()
        
        for model in models:

            print " ", model
        
        print

    sys.exit()

