#!/usr/bin/env python3
import csv
from icalendar import Calendar, Event, Alarm
from datetime import datetime
from random import randint
import argparse
from datetime import timedelta

parser = argparse.ArgumentParser()
parser.add_argument('input', type=str, help='Input csv file containing calendar events')
parser.add_argument('output', type=str, help='Output ics file')
args = parser.parse_args()

def csv2ical(input_file, output_file):
    """csv2ical
    Convert a cvs file with event information to ical, which can be imported into
    Google Calendar, Microsoft Outlook and etc.
    Parameters
    ----------
    input_file : str
    output_file : str
    Returns
    -------
    Empty
    """
    ### set reminder before shift start ####
    reminderHours = 1
    duration = timedelta(minutes=-int(45))

    with open(input_file) as csv_file:
        reader = csv.reader(csv_file)
        
        # required to be compliant:
        cal = Calendar()
        cal.add('prodid', '-//'+input_file+'//mxm.dk//')
        cal.add('version', '2.0')
        cal.add('X-WR-TIMEZONE', 'Asia/Hong_Kong')
        cal.add('X-WR-CALNAME', '更表')
        cal.add('X-WR-CALDESC', '更表')
        cal.add('CALSCALE', 'GREGORIAN')

        for n, row in enumerate(reader):
            #Skip header row
            if n == 0:
                continue
            
            summary = ''
            # Clean up potential whitespace from input
            time_str = row[2].strip() if len(row) > 2 else ''
            
            if time_str == '':
                dtstart = datetime.strptime(row[1].strip()+' 13:00', '%Y/%m/%d %H:%M')
                set_alarm = False
            else:
                dtstart = datetime.strptime(row[1].strip()+' '+time_str, '%Y/%m/%d %H:%M')
                set_alarm = True
                
            dtend = dtstart + timedelta(minutes=495)

            # 修正邏輯：無論時間格式是 "07:30" 還是 "7:30" 都能正確對應摘要
            if set_alarm:
                # 嘗試將時間字串統一格式化為 HH:MM 進行比對
                try:
                    formatted_time = datetime.strptime(time_str, '%H:%M').strftime('%H:%M')
                except ValueError:
                    formatted_time = time_str # 若格式不符則維持原樣
                
                if formatted_time == "07:30":
                    summary = "早"
                elif formatted_time == "15:10":
                    summary = "中"
                elif formatted_time == "23:20":
                    summary = "夜"
                else:
                    summary = time_str
            
            description = row[5].strip() if len(row) > 5 else ''
            location = row[4].strip() if len(row) > 4 else ''

            event = Event()
            event.add('summary', summary)
            event.add('dtstart', dtstart)
            event.add('dtend', dtend)
            event.add('description', description)
            event.add('location', location)
            event['uid'] = str(randint(1,10**30)) + datetime.now().strftime('%Y%m%dT%H%M%S') + '___n8henrie.com'

            if set_alarm == True :
                alarm=Alarm()
                alarm.add('ACTION','DISPLAY')
                alarm.add('DESCRIPTION','Reminder')
                # The only way to convince Outlook to do it correctly
                alarm.add("trigger", timedelta(hours=-reminderHours))
                alarm.add('REPEAT','3')
                alarm.add('DURATION',duration)
                event.add_component(alarm)
                
            cal.add_component(event)

    with open(output_file, 'wb') as out_f:
        out_f.write(cal.to_ical())
        out_f.close()

def main(args):
    csv2ical(args.input, args.output)

if __name__ == "__main__":
    main(parser.parse_args())
