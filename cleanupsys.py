from crate import client
import dbHandler
while True:
    try:
      ListOfContainer = dbHandler.GetListContainer()
      for each_container in ListOfContainer:
          dbHandler.UpdateContainerStatus(each_container, "fanning", "false")
          dbHandler.UpdateContainerStatus(each_container, "misting", "false") 
          print('fanning and misting is set to false in greenhouse as it reboot')
      break;
    except Exception as e:
         print ("Data Extraction Failed" + str(e))
         print('Retry ...')
         
