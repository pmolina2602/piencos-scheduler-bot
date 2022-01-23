DATE_FORMAT = "%d-%m-%Y"
LONG_DATE_FORMAT = "%d %B %Y"
TIME_FORMAT = "%H:%M"

HELP_MESSAGE = """Easy configuration if you are not Jose or dumb:


Commands:

/start -> Will welcome you with a friendly message

/help -> Will show this message

/addtimezone <timezone> -> To add a time zone with expected format, example: America/Mexico_City

/deltimezone <timezone> -> To delete a time zone with expected format, example: America/Mexico_City

/timezones -> To show registered time zones (WIP: to improve with flags and be nicer)

/schedulegameplay <game> <date> <time> <timezone> -> This is to schedule a gameplay specifying the game without spaces, date, time and a timezone.
This will show a message with the time for al registered time zones.

Example: /schedulegameplay Halo 23-05-2022 15:30 America/Buenos_Aires

It will not save the schedule, just shows the message.

Note: Date format dd-mm-YY and time format hh:mm


WIP: Save registered time zones on a file so it does not clear after new deploy



    BASURAS
"""