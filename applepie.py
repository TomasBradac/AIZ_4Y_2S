import json
import matplotlib.pyplot as plt


with open('result.json', 'r') as file:
    data = json.load(file)


selected_teacher = 'Nora Newbie'


filtered_data = [item for item in data if item['teacher_name'] == selected_teacher]


event_lengths = {}
for item in filtered_data:
    event_type = item['event_type']
    lesson_length = item['lesson_length']
    if event_type in event_lengths:
        event_lengths[event_type] += lesson_length
    else:
        event_lengths[event_type] = lesson_length


event_types = list(event_lengths.keys())
lesson_lengths_values = list(event_lengths.values())


plt.figure(figsize=(8, 8))
plt.pie(lesson_lengths_values, labels=event_types, autopct='%1.1f%%', startangle=140)
plt.title(f'Total Lesson Length by Event Type for {selected_teacher}')
plt.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.


plt.show()
