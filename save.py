# Exercise-3 TODOs:

	# Classify the clusters!
    	detected_objects_labels = []
    	detected_objects = []

    	for index, pts_list in enumerate(cluster_indices):
        	# Grab the points for the cluster from the extracted outliers (cloud_objects)
        	pcl_cluster = extracted_outliers.extract(pts_list)

        	# TODO: convert the cluster from pcl to ROS using helper function
		rosdata = pcl_to_ros(pcl_cluster)

        	# Extract histogram features
        	# TODO: complete this step just as is covered in capture_features.py
		chists = compute_color_histograms(rosdata, using_hsv=True)
            	normals = get_normals(rosdata)
            	nhists = compute_normal_histograms(normals)
            	feature = np.concatenate((chists, nhists))

        	# Make the prediction, retrieve the label for the result
        	# and add it to detected_objects_labels list
        	prediction = clf.predict(scaler.transform(feature.reshape(1,-1)))
        	label = encoder.inverse_transform(prediction)[0]
        	detected_objects_labels.append(label)

        	# Publish a label into RViz
        	label_pos = list(white_cloud[pts_list[0]])
        	label_pos[2] += .4
        	object_markers_pub.publish(make_label(label,label_pos, index))

        	# Add the detected object to the list of detected objects.
        	do = DetectedObject()
        	do.label = label
        	do.cloud = pcl_cluster
        	detected_objects.append(do)

    	rospy.loginfo('Detected {} objects: {}'.format(len(detected_objects_labels), detected_objects_labels))


    # Publish the list of detected objects
    # This is the output you'll need to complete the upcoming project!
    	detected_objects_pub.publish(detected_objects)

    # Suggested location for where to invoke your pr2_mover() function within pcl_callback()
    # Could add some logic to determine whether or not your object detections are robust
    # before calling pr2_mover()
    	try:
        	pr2_mover(detected_objects)
    	except rospy.ROSInterruptException:
        	pass
