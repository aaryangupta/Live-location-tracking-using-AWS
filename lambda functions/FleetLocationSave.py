import json
import boto3

def lambda_handler(event, context):
    # Initialize the AWS Location Service client
    location_service = boto3.client('location')
    
    # Iterate over all records in the event
    for record in event.get('records', []):
        try:
            # Extract necessary information from each record
            device_id = record['deviceId']
            latitude = record['latitude']
            longitude = record['longitude']
            timestamp = record['timestamp']

            # Define your tracker name
            tracker_name = 'FleetTracker'  # Replace with your actual tracker name

            # Send the location data to AWS Location Service Tracker
            response = location_service.batch_update_device_position(
                TrackerName=tracker_name,
                Updates=[
                    {
                        'DeviceId': device_id,
                        'Position': [longitude, latitude],
                        'SampleTime': timestamp
                    }
                ]
            )
            print("Location data sent successfully:", response)

        except KeyError as e:
            print(f"Missing key in record: {e}")
        except Exception as e:
            print("Error sending location data:", str(e))

    return {
        'statusCode': 200,
        'body': json.dumps('Location data processed successfully!')
    }
