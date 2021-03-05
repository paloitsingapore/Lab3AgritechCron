from datetime import datetime ,timedelta
import logging
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
import azure.functions as func
from azure.storage.blob import BlobServiceClient, BlobClient, ContainerClient
container_data = "lab3agritechpaloit"
CONNECT_STR="DefaultEndpointsProtocol=https;AccountName=lab3agritechpaloit;AccountKey=7y9wfjL59CGOGJWgWVno8L2XTaDoHjT1ASgIJaEEJlASVAWcQMZxKj/RaB4h/Q/WnRNw3NNBVjHtVX29labzuA==;EndpointSuffix=core.windows.net"

blob_service_client = BlobServiceClient.from_connection_string(CONNECT_STR)
container_client = blob_service_client.get_container_client(container_data)


def main(mytimer: func.TimerRequest) -> None:

    logging.info("hello how are you !")
    if mytimer.past_due:
        logging.info('The timer is past due!')

    
    sg = SendGridAPIClient('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')
    logging.info(blob_service_client)
    logging.info(container_client)
    container_prop = container_client.get_container_properties()
    logging.info('shobhit' + str(container_prop.last_modified))
    blob_last_modified = datetime.now() - timedelta(hours = 300)   
    for blob in container_client.list_blobs():
       logging.info("blob last modified: " + str(blob.last_modified))       
       if blob.last_modified.replace(tzinfo=None) > blob_last_modified:
           blob_last_modified = blob.last_modified.replace(tzinfo=None) 
       
    blob_last_upload = blob_last_modified.replace(tzinfo=None)  # Both Time should be without time stamp
    current_time = datetime.now()
    logging.info("curent time : " + str(current_time))
    time_delta = current_time - blob_last_upload
    logging.info("time delta : " + str(time_delta))
    hour_diff =  (time_delta.total_seconds()/3600)
    logging.info("hour diff : " + str(hour_diff))
    if hour_diff  > 2:
        message = Mail(
        from_email='sg-agritech_lab@palo-it.com',
        to_emails='fair.farm.notify@gmail.com',
        subject='No Data recevied in last 2 hours ',html_content='The is to notify you that no data has been recevied in last : ' + str(round(hour_diff,2)) + ' hours' )
        response = sg.send(message)
        print(response.status_code)
        print(response.body)
        print(response.headers)
    
