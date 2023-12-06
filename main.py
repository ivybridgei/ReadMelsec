import time
import logging
from datetime import datetime
from pymelsec import Type3E
from pymelsec.constants import DT
from pymelsec.tag import Tag

logging.basicConfig(filename="plc_communication.log", level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

prev_flag2 = 0
prev_flag3 = 0
i = 1

with Type3E(host="192.168.66.100", port=5002, plc_type='Q') as plc:
 try:
    plc.set_access_opt(comm_type="binary")

    while True:
     # try:
       # plc.set_access_opt(comm_type="binary")
       timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
       # print(f"Start - {timestamp}")
       # logging.info(f"Start - {timestamp}")
    
       read_result_flag = plc.read(devices=[
            Tag(device="M3303", type=DT.BIT),
            Tag(device="M3200", type=DT.BIT),
            Tag(device="M3218", type=DT.BIT),
       ])
       
       for tag in read_result_flag:
          if tag.device == "M3303" :
            flag1=tag.value
            
          if tag.device == "M3200" :
            flag2=tag.value

            
          if tag.device == "M3218" :
            flag3=tag.value            
        
       if flag2 == 1 and prev_flag2 == 0 :
         j = 3
         print(f"Panel {i}")
         logging.info(f"Panel {i}")
         i = i+1
         prev_flag2 = flag2

       if  flag3 == 0 and prev_flag3 == 1 :
         #flag3 == 0 and prev_flag3 == 1 or flag1 != 0
         read_result = plc.read(devices=[
            # Tag(device="M3217", type=DT.BIT),
            # Tag(device="M3218", type=DT.BIT),
            # Tag(device="M3280", type=DT.BIT),
            # Tag(device="D1684", type=DT.SWORD),
            Tag(device="D258", type=DT.SWORD),
         ])

         for tag in read_result:
            # if tag.device == "D1684" :
                # print(f"L Shift: {tag.value}")
                # logging.info(f"L Shift: {tag.value}")
                # logging.info(f"L Shift - {timestamp}") 
                
            if tag.device == "D258" :
                
                print(f"X{j} Shift: {tag.value}")
                logging.info(f"X{j} Shift: {tag.value}")
                j = j-1
                # logging.info(f"R Shift - {timestamp}\n")
            prev_flag3 = flag3
         
       if flag3 == 1 and prev_flag3 == 0 :
         # print(f"flag3 - {flag3}")
         # logging.info(f"Next - {timestamp}")             
         prev_flag3 = 1  
         
       if flag2 == 0 and prev_flag2 == 1 :
         print(f"Next - {timestamp}")
         # logging.info(f"Next - {timestamp}")             
         prev_flag2 = 0
                
 except Exception as e:
        print(f"An error occurred: {e}")
        logging.error(f"An error occurred: {e}")               
                