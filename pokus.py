import json
import aiofiles
from typing import List, Union, Dict
from collections import defaultdict
import asyncio
import datetime

async def load_json_data(path):
    try:
        async with aiofiles.open(path, 'r', encoding ='utf-8') as file:
            data = await file.read()  
            return json.loads(data)  
    except FileNotFoundError:
        print(f"Provided file path does not exist.")
        return None
    except Exception as e:
        print(f"Error {e}")
        return None


async def user_attendance(data: Dict) -> List:
    sourceTable = []
    specific_group = "K-209"

    for item in data['data']['eventPresencePage']:
        is_teacher = item['invitationType']['name'] #In production 'name' use will be changed for ID
        
        if is_teacher == "organizátor": #In production use will be changed for ID
            user_groups = [group['group']['name'] for group in item['user']['membership']] #In production 'name' use will be changed for ID
            
            if specific_group in user_groups:
                row = {}
                row["membership"] = specific_group
                row['teacher_name'] = item['user']['fullname']
                row['teacher_id'] = item['user']['id']
                row["event_type"] = item['event']['eventType']['name']
                row["invitation_type"] = item['invitationType']['name']
                event_start = datetime.datetime.fromisoformat(item['event']['startdate'])
                event_end = datetime.datetime.fromisoformat(item['event']['enddate'])
                row["lesson_length"] = (event_end - event_start).total_seconds() / 60 #in minutes
                sourceTable.append(row)
            #-------TODO-------
        
            #add if statement for special group
                #teachers in special group
            #search by ID not by name
   
    print(sourceTable)
    

    with open('result.json',"w", encoding='utf-8') as outputFile:
        json.dump(sourceTable, outputFile)


async def main():
    data = await load_json_data('data.json')
    await user_attendance(data)

asyncio.run(main())