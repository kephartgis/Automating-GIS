#-------------------------------------------------------------------------------
# Name:       script03_OverlayTool w Prep
#-------------------------------------------------------------------------------

def main():
    import arcpy, os, sys
    arcpy.AddMessage("\nOverlay Script Running")
    workspace = arcpy.GetParameterAsText(0)
    arcpy.env.workspace = workspace

    try:
        fcs = []
        arcpy.env.workspace = workspace
        for fc in arcpy.ListFeatureClasses():
            fcs.append(fc)

        dropFields1 = ["Mileage", "LOC_ERROR", "Shape_Length"]
        dropFields2 = ["SourceError"]
        memoryFeature="in_memory"+"\\"+"myMemoryFeature"
	
        # convert and add fields
        for fc in fcs:
            fieldList = []
            fieldList = [f.name for f in arcpy.ListFields(fc)]
            arcpy.CopyFeatures_management(fc, memoryFeature)
            arcpy.DeleteField_management(memoryFeature, dropFields1)
            arcpy.AddField_management(memoryFeature, fc+"SourceError","TEXT",field_length=5)                   
            arcpy.CalculateField_management(memoryFeature, fc+"SourceError",'!SourceError!','PYTHON_9.3')
            arcpy.DeleteField_management(memoryFeature, dropFields2)
            arcpy.TableToTable_conversion(memoryFeature,workspace,fc)
            arcpy.Delete_management(memoryFeature)


        listTBL = arcpy.ListTables()

        if len(listTBL) == 2:
            arcpy.AddMessage("\nOnly two tables present in workspace")
            arcpy.AddMessage("Overlay Process"+"\n - "+listTBL[0]+"\n - "+listTBL[1])
            arcpy.OverlayRouteEvents_lr(in_table=listTBL[0],
                            in_event_properties="Route_ID LINE Begin_Point End_Point",
                            overlay_table=listTBL[1],
                            overlay_event_properties="Route_ID LINE Begin_Point End_Point",
                            overlay_type="UNION",
                            out_table=os.path.join(workspace,"output1"),
                            out_event_properties="Route_ID LINE Begin_Point End_Point",
                            zero_length_events="NO_ZERO",
                            in_fields="FIELDS",
                            build_index="INDEX")
            arcpy.AddMessage(arcpy.GetMessages())

        elif len(listTBL) > 2:
            count = 1
            # overlay list[1] and list[2]
            arcpy.AddMessage("\nMore than two tables present in workspace")
            arcpy.AddMessage("\n~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
            arcpy.AddMessage("Overlay Process\n - "+listTBL[0]+"\n - "+listTBL[1])
            arcpy.OverlayRouteEvents_lr(in_table=listTBL[0],
                            in_event_properties="Route_ID LINE Begin_Point End_Point",
                            overlay_table=listTBL[1],
                            overlay_event_properties="Route_ID LINE Begin_Point End_Point",
                            overlay_type="UNION",
                            out_table=os.path.join(workspace,"output"+str(count)),
                            out_event_properties="Route_ID LINE Begin_Point End_Point",
                            zero_length_events="NO_ZERO",
                            in_fields="FIELDS",
                            build_index="INDEX")
            arcpy.AddMessage(arcpy.GetMessages())

            for tbl in listTBL:
                arcpy.AddMessage("\n~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
                if tbl == listTBL[0]:
                    arcpy.AddMessage("\nTable already used in overlay: "+tbl)
                elif tbl == listTBL[1]:
                    arcpy.AddMessage("\nTable already used in overlay: "+tbl)
                else:
                    arcpy.AddMessage("\n~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
                    arcpy.AddMessage("\nOverlay Process\n - "+os.path.join(workspace,"output"+str(count))+"\n - "+tbl+"\n - Output: "+os.path.join(workspace,"output"+str(count+1)))
                    arcpy.OverlayRouteEvents_lr(in_table=os.path.join(workspace,"output"+str(count)),
                                    in_event_properties="Route_ID LINE Begin_Point End_Point",
                                    overlay_table=tbl,
                                    overlay_event_properties="Route_ID LINE Begin_Point End_Point",
                                    overlay_type="UNION",
                                    out_table=os.path.join(workspace,"output"+str(count+1)),
                                    out_event_properties="Route_ID LINE Begin_Point End_Point",
                                    zero_length_events="NO_ZERO",
                                    in_fields="FIELDS",
                                    build_index="INDEX")
                    arcpy.AddMessage(arcpy.GetMessages())
                    count+=1


            # for item in list, if item is first or second, skip
            # else: count+=1, run overlay

        else:
            arcpy.AddError("\nFewer than 2 tables in given FGDB Workspace. Cannot run Overlay tool.")
            sys.exit()


    except Exception, e:
        import traceback, sys, os, arcpy
        tb = sys.exc_info()[2]
        arcpy.AddError("%s: Line %i"%(os.path.basename(__file__),tb.tb_lineno))
        arcpy.AddError(e)

        errors += "%s: Line %i\t%s"%(os.path.basename(__file__),tb.tb_lineno,e)

    finally:
        arcpy.AddMessage("\nScript completed")

if __name__ == '__main__':
    main()
