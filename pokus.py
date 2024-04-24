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
    user_attendance_data = data['data']['eventPresencePage']
    sourceTable = []
    
    for item in user_attendance_data:
        is_teacher = item['invitationType']['name']
        #print(is_teacher)
        if is_teacher == "organizátor":
            row = {}
            row['teacher_name'] = item['user']['fullname']
            row['teacher_id'] = item['user']['id']
            row["event_type"] = item['event']['eventType']['name']
            row["membership"] = [group['group']['name'] for group in item['user']['membership']]
            row["invitation_type"] = item['invitationType']['name']
            event_start = datetime.datetime.fromisoformat(item['event']['startdate'])
            event_end = datetime.datetime.fromisoformat(item['event']['enddate'])
            row["lesson_length"] = (event_end - event_start).total_seconds() / 60 #in minutes
            sourceTable.append(row)
   
    print(sourceTable)
    

    with open('resultX.json',"w", encoding='utf-8') as outputFile:
        json.dump(sourceTable, outputFile)


async def main():
    data = await load_json_data('data.json')
    await user_attendance(data)

asyncio.run(main())