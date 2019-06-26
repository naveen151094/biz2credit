# Import inbuild module
import math
import json
import os

# Build a class object
class customerPortal(object):
    # Assign a init constructor and pass it
    def __init__(self):
        pass
    # Assign a public class for customers details
    class _customer_details(object):
        def __init__(self,name,user_id,latitiude,longitude,distanceFromReference):
            self.name = name
            self.user_id = user_id
            self.latitude = latitiude
            self.longitude = longitude
            self.distanceFromReference = distanceFromReference
    # Change the value from degree to radaian
    def _degtorad(self,deg):
        return deg*math.pi/180
    # Define the function to calculate distance in KMs from Longitute and Latitiute
    def _getDistanceBetweenTwoPoints(self,lat1,long1,lat2,long2):
        #Radius of earth=6371 KM
        radius_of_earth = 6371
        difference_lat = self._degtorad(lat2-lat1)
        difference_long = self._degtorad(long2-long1)
        #using haversrine algorithm to calculate distannce
        delta_attitude = math.pow(math.sin(difference_lat/2),2) + math.pow(math.sin(difference_long),2) * math.cos(self._degtorad(lat1))*math.cos(self._degtorad(lat2))
        delta_theeta = 2 * math.atan2(math.sqrt(delta_attitude),math.sqrt(1-delta_attitude))
        distance_kms = radius_of_earth * delta_theeta
        return distance_kms

    def getCustomersNearby(self,reference_lat,reference_long,threshold_distance_km,input_file_location,output_file_directory):
        """
        The GPS coordinates for Dublin area is 53.339428, -6.257664
        Longitude=53.339428
        Latitiuate=-6.257664
        Threshold Distance=100 km
        """
        reference_lat = 53.339428
        reference_long = -6.257664
        threshold_distance_km = 100
        # Read the input customers file from desktop 
        input_file_location ='C:\\Users\\Naveen Kumar\\Desktop\\Customers _Assignment_Coding Challenge (Upto 6 Years).txt'
        # Write the customers output result file at desktop 
        output_file_directory = 'C:\\Users\\Naveen Kumar\\Desktop\\'
        # Make an empty customer list
        customer_list = []
        #Open the input file as json_file and read it line by line
        with open(input_file_location) as json_file:
            for line in json_file:
                line_data = json.loads(line)
                distanceFromReference = self._getDistanceBetweenTwoPoints(reference_lat,reference_long,float(line_data['latitude']),float(line_data['longitude']))
                # Compare each line distance with threshold distance and then appends to customer_list
                if (distanceFromReference <= threshold_distance_km):
                    customer = self._customer_details(line_data['name'],line_data['user_id'],line_data['latitude'],line_data['longitude'],distanceFromReference)
                    customer_list.append(customer)
        # Save result file as "biz2credit_results.txt" at output_file_directory location 
        output_file_path = output_file_directory + 'biz2credit_results.txt' 
        # If same file name already exist, then automattically remove it and save as a new output file
        if (os.path.exists(output_file_path)):
            os.remove(output_file_path)
        output_data={}
        # Sort the resultant distance based on user_id and append to output_data dictionary
        for customer in customer_list:
            output_data[customer.user_id] = customer.name
        output_sorted_keys = sorted(output_data)
        output_print_data = []
        for key in output_sorted_keys:
            temp = {}
            temp["user_id"]= key
            temp["name"] = output_data[key]
            output_print_data.append(temp)
        print(output_print_data)
        # Write an output file as json format
        with open(output_file_path,"w+") as outfile:
            json.dump(output_print_data,outfile)
    