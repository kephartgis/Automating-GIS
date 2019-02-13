#-------------------------------------------------------------------------------
# Name:        script00_FileFormatting.py
#-------------------------------------------------------------------------------


def main():
    import arcpy, os, sys
    table = arcpy.GetParameterAsText(0)
    workspace = arcpy.GetParameterAsText(1)

#    try:
    fcs = []
    arcpy.env.workspace = workspace
    for tbl in arcpy.ListTables():
        fcs.append(tbl)
	    
        # add fields
        #for item in fcs:
            #arcpy.AddMessage("\nAdding Fields\n - Adding dissolve field")
            #arcpy.AddField_management(table,field_type="DOUBLE")
            #arcpy.CalculateField_management(item,"Mileage",'!End_Point! - !Begin_Point!','PYTHON_9.3')

        #fcs = []
        #arcpy.env.workspace = workspace
        #for tbl in arcpy.ListTables():
        #    fcs.append(tbl)

        #dropFields1 = ["Mileage", "LOC_ERROR", "Shape_Length"]
        #dropFields2 = ["SourceError"]
        #memoryFeature="in_memory"+"\\"+"myMemoryFeature"
	
        # convert and add fields
        #for fc in fcs:
        #    fieldList = []
        #    fieldList = [f.name for f in arcpy.ListFields(fc)]
    arcpy.AddMessage("\nAdding Fields\n - Adding dissolve field")
    arcpy.AddField_management(field_name="TEST",field_type="DOUBLE")

#    except Exception, e:
#        # If an error occurred, arcpy.AddMessage(line number and error message)
#        import traceback, sys
#        tb = sys.exc_info()[2]
#        arcpy.AddError("script00_File Formatting Script Error: Line %i" % tb.tb_lineno)
#        arcpy.AddError(e)

#finally:
#    arcpy.AddMessage("\nScript complete")


#if __name__ == '__main__':
#    main()
