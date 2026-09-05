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
      #print(row[2]) 
      if row[2] == '':
           dtstart = datetime.strptime(row[1]+' 13:00', '%Y/%m/%d %H:%M')
           set_alarm = False 
      else: 
           dtstart = datetime.strptime(row[1]+' '+row[2], '%Y/%m/%d %H:%M')
           set_alarm = True 
      dtend = dtstart + timedelta(minutes=495) 
      if len(row[2]) == 5:
          if row[2] =="07:30":
            summary = "早" 
          if row[2] =="15:10":
            summary = "中"
          if row[2] == "23:20":
            summary = "夜"
          if summary == '':
            summary = row[2]    
      description = row[5].strip()
      location = row[4].strip()
     
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
         #'返工啦')
         # The only way to convince Outlook to do it correctly
         alarm.add("trigger", timedelta(hours=-reminderHours))
         #alarm.add("TRIGGER;RELATED=START", "-PT{0}H".format(reminderHours))
         alarm.add('REPEAT','3')
         alarm.add('DURATION',duration)
         event.add_component(alarm)
         #event['uid'] = str(randint(1,10**30)) + datetime.now().strftime('%Y%m%dT%H%M%S') + '___n8henrie.com'

      cal.add_component(event)
    with open(output_file, 'wb') as out_f:
      out_f.write(cal.to_ical())
      out_f.close()


def main(args):
  csv2ical(args.input, args.output)
  

if __name__ == "__main__":
  main(parser.parse_args())
