#-------------------------------------------------------------------------------
# Name:        script01_AddMileageField.py
#-------------------------------------------------------------------------------


def main():
    import arcpy, os, sys
    gdb = arcpy.GetParameterAsText(0)

    try:
        fcs = []
        arcpy.env.workspace = gdb
        for tbl in arcpy.ListTables():
            fcs.append(tbl)
	    
        # add fields
        for item in fcs:
            arcpy.AddMessage("\nAdding Fields\n - Adding field: Mileage")
            arcpy.AddField_management(in_table=item, field_name="Mileage",field_type="DOUBLE", field_precision="", field_scale="", \
	                                        field_length="", field_alias='Mileage', field_is_nullable="NULLABLE", field_is_required="NON_REQUIRED",
	                                        field_domain="")
            arcpy.CalculateField_management(item,"Mileage",'!End_Point! - !Begin_Point!','PYTHON_9.3')

    except Exception, e:
        # If an error occurred, arcpy.AddMessage(line number and error message)
        import traceback, sys
        tb = sys.exc_info()[2]
        arcpy.AddError("script01_AddMileageField Script Error: Line %i" % tb.tb_lineno)
        arcpy.AddError(e)

    finally:
        arcpy.AddMessage("\nScript complete")


if __name__ == '__main__':
    main()
