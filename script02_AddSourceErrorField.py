#-------------------------------------------------------------------------------
# Name:        script01_AddSourceErrorField.py
#-------------------------------------------------------------------------------


def main():
    import arcpy, os, sys
    gdb = arcpy.GetParameterAsText(0)

    try:
        fcs = []
        arcpy.env.workspace = gdb
        for fc in arcpy.ListFeatureClasses():
            fcs.append(fc)

        searchField = ["SourceError"]
	
        # add fields
        for fc in fcs:
            fieldList = []
            fieldList = [f.name for f in arcpy.ListFields(fc)]
            for field in searchField:
                if not field in fieldList and "LOC_ERROR" in fieldList:
                    arcpy.AddMessage("\nProcessing: "+ fc +"\n - Adding field: SourceError")
                    arcpy.AddField_management(in_table=fc, field_name="SourceError",field_type="TEXT", field_precision="", field_scale="", \
                                                        field_length="5", field_alias='SourceError', field_is_nullable="NULLABLE", field_is_required="NON_REQUIRED",
                                                        field_domain="")
                    arcpy.MakeFeatureLayer_management(fc,'calc1',"LOC_ERROR = 'NO ERROR'")
                    arcpy.CalculateField_management("calc1","SourceError","'No'",'PYTHON_9.3')
                    arcpy.MakeFeatureLayer_management(fc,'calc2',"LOC_ERROR <> 'NO ERROR'")
                    arcpy.CalculateField_management("calc2","SourceError","'Yes'",'PYTHON_9.3')
                    arcpy.Delete_management('calc1')
                    arcpy.Delete_management('calc2')
                else:
                    arcpy.AddMessage(" - SourceError field already present or LOC_ERROR not present")

    except Exception, e:
        # If an error occurred, arcpy.AddMessage(line number and error message)
        import traceback, sys
        tb = sys.exc_info()[2]
        arcpy.AddError("script02_AddSourceErrorField Script Error: Line %i" % tb.tb_lineno)
        arcpy.AddError(e)

    finally:
        arcpy.AddMessage("\nScript complete")


if __name__ == '__main__':
    main()





