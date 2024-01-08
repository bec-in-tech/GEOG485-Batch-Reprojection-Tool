import arcpy

try:
    # Define the target folder and data path of feature class with
    # the desired projection
    targetFolder = arcpy.GetParameterAsText(0)
    targetFC = arcpy.GetParameterAsText(1)

    # Define the workspace environment & allow overwrites
    arcpy.env.workspace = targetFolder
    arcpy.env.overwriteOutput = True

    # Describe the target feature class and get its spatial reference
    targetDesc = arcpy.Describe(targetFC)
    targetSR = targetDesc.SpatialReference
    targetSRName = targetSR.Name

    # Print the spatial reference name of the target feature class
    print(f"Target Spatial Reference: {targetSR.Name}")

    # List the projected feature classes
    projectedFC = []

    # List the feature classes in the target folder
    fcList = arcpy.ListFeatureClasses()

    # Loop through the list of feature classes
    for featureClass in fcList:
        # Get the spatial reference of the feature classes
        featureClassDesc = arcpy.Describe(featureClass)
        featureClassSR = featureClassDesc.SpatialReference

        # Print the spatial reference name of the feature classes
        print(f"{featureClass} is {featureClassSR.Name}\n")

        # Determine whether the spatial reference of featureClass(s) match
        # the spatial reference of the targetFC.
        # Spatial references that don't match will be reprojected.
        if featureClassSR.Name != targetSR.Name:
            print(f"Spatial reference does not match {targetSR.Name}.\n")

            # Reproject the feature class to the target spatial reference
            # and create a new feature class with "_projected" appended to the name
            outputFC = featureClass.replace(".shp", "_projected.shp")

            # Use the Project tool to reproject the unmatching feature classes
            arcpy.management.Project(featureClass, outputFC, targetSR)
            print(f"Reprojection complete for {featureClass}. \nNew feature class: {outputFC}\n")

            # If the reprojection was successful, add to the projectedFC list
            if arcpy.Exists(outputFC):
                projectedFC.append(featureClass)

        else:
            print(f"Spatial reference matches.\n")

    # Use the string join method to convert the projectedFC list into a string separated by commas
    # therefore also removing the square brackets in the list
    projectedFCString = ", ".join(projectedFC)

    # Add a single message with the names of the reprojected feature classes
    arcpy.AddMessage(f"Projected {projectedFCString}")

except Exception as e:
    print(f"Error: {str(e)}")
