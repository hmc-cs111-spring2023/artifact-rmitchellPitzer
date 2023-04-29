import tkinter
import tkinter.messagebox
import customtkinter
from tkinter import BOTH, END, LEFT
from ics import Calendar, Event
import datetime
from dateutil import tz
import re

## Import statements

# Code used includes a javascript/html calendar schedule, altered from:
# https://codyhouse.co/gem/schedule-template





## DSL PART 1: MAKING/OUTPUTTING A .ICS FILE



# List of acceptable Colors and Days for users to input

listOfAcceptableColors = ["tomato", "flamingo", "tangerine", "sage", "basil", "peacock", "blueberry", "lavender", "grape", "graphite"]
listOfAcceptableDays = [
        "monday",
        "tuesday",
        "wednesday",
        "thursday",
        "friday",
        "saturday",
        "sunday",
        "m",
        "tu",
        "w",
        "th",
        "f",
        "sa",
        "su"
    ]


# Function to parse user input.
# First checks if the user is using natural language syntax or no natural language syntax, and
# Evaluates the input string from there. 
# Errors are returned instead of being thrown so it can be displayed in a popup box in customtkinter
# Returns an array containing an event name, description, start time, end time, days it occurs on, and color for the event in the preview.

def parseInput(inputStr):
    returnedArr = []
    if inputStr[0] == "\"":
        noKeywords = inputStr[1:]
        indexOfEnd = noKeywords.find("\"")
        eventName = noKeywords[0:indexOfEnd]
        noKeywords = noKeywords[indexOfEnd + 2:]
        descText = ""
        startTime = ""
        endTime = ""
        if noKeywords[0] == ("\""):
            noKeywords = noKeywords[1:]
            indexOfEnd = noKeywords.find("\"")
            descText = noKeywords[0:indexOfEnd]
            noKeywords = noKeywords[indexOfEnd + 2:]
        if noKeywords[0].isdigit():
            indexOfEnd = noKeywords.find(":") + 5
            startTime = noKeywords[0:indexOfEnd]
            noKeywords = noKeywords[indexOfEnd+1:]
            print(noKeywords)
            indexOfEnd = noKeywords.find(":") + 5
            endTime = noKeywords[0:indexOfEnd]
            noKeywords = noKeywords[indexOfEnd+1:]
            color = ""
            for colorList in listOfAcceptableColors:
                if colorList in noKeywords:
                    color = colorList
                    noKeywords = noKeywords.replace(color, "")
                    break
            dayArr = []
            noKeywords = noKeywords.lower()
            for day in listOfAcceptableDays:
                if day in noKeywords:
                    dayArr += [day]
                    noKeywords.replace(day, "")
            returnedArr = [eventName, descText, startTime, endTime, dayArr, color]
            return returnedArr
            
            
        else:
            return (f"ERROR: Couldn't find a time in {noKeywords} \n Example input: \"CS111\" \"Domain Specific Languages. Occurs ever Monday and Wednesday from 1:15 pm to 2:30 pm.\" 1:15pm 2:30pm Monday Wednesday Friday orange", -1)

    
    print("Skipping conditional")
    eventName, desc = parseEventName(inputStr)
    if desc == -1:
        return (eventName, desc)
    testStr = inputStr[desc:]
    descText, indexOfFrom = parseDesc(testStr)
    if indexOfFrom == -1:
        return (descText, indexOfFrom)
    testStr = testStr[indexOfFrom:]

    startTime, endTime, indexOfTo = parseTime(testStr)
    if indexOfTo == -1:
        return (startTime, indexOfTo)
    testStr = testStr[indexOfTo:]
    listOfDays, indexOfColor = parseDays(testStr)
    if indexOfColor == -1:
        return (listOfDays, indexOfColor)
    testStr = testStr[indexOfColor:]
    color = parseColor(testStr)
    returnedArr = [eventName, descText, startTime, endTime, listOfDays, color]
    return returnedArr 



# Function to parse the name of an event from a string starting with "EVENT "
# Returns a tuple of either an error message and error status, or a event name with the index of the description

def parseEventName(inputStr):
    indexOfEvent = ""
    indexOfDesc = ""
    if ("EVENT \"") not in inputStr:
        return (f"ERROR: Couldn't find EVENT keyword in {inputStr} \n Example input: EVENT \"CS111\" DESC \"Domain Specific Languages. Occurs ever Monday and Wednesday from 1:15 pm to 2:30 pm.\" FROM 1:15pm TO 2:30pm ON Monday Wednesday Friday COLOR orange", -1)

    indexOfEvent = inputStr.index("EVENT \"")
    if ("\" DESC \"") not in inputStr:
        if ("\" FROM ") not in inputStr:
            return (f"ERROR: Couldn't find DESC or FROMkeyword \n Example input: EVENT \"CS111\" DESC \"Domain Specific Languages. Occurs ever Monday and Wednesday from 1:15 pm to 2:30 pm.\" FROM 1:15pm TO 2:30pm ON Monday Wednesday Friday COLOR orange", -1)

        else:
            indexOfDesc = inputStr.index("\" FROM ")
    else:
        indexOfDesc = inputStr.index("\" DESC \"")
    eventName = inputStr[indexOfEvent+7: indexOfDesc]
    return (eventName, indexOfDesc)


# Function to parse the description of an event from a string starting with "DESC "
# Returns a tuple of either an error message and error status, or a event description with the index of the next keyword, from.    

def parseDesc(inputStrDesc):
    if ("DESC \"") not in inputStrDesc:
        if ("\" FROM ") not in inputStrDesc: 
            return (f"ERROR: Couldn't find FROM or DESC keyword in {inputStrDesc} \n Example input: EVENT \"CS111\" DESC \"Domain Specific Languages. Occurs ever Monday and Wednesday from 1:15 pm to 2:30 pm.\" FROM 1:15pm TO 2:30pm ON Monday Wednesday Friday COLOR orange", -1)

        else:
            indexOfFrom = inputStrDesc.index("\" FROM ")
            desc = ""
            return(desc, indexOfFrom)
 
    indexOfDesc = inputStrDesc.index("\" DESC \"")
    if ("\" FROM ") not in inputStrDesc: 
        return (f"ERROR: Couldn't find FROM keyword in {inputStrDesc} \n Example input: EVENT \"CS111\" DESC \"Domain Specific Languages. Occurs ever Monday and Wednesday from 1:15 pm to 2:30 pm.\" FROM 1:15pm TO 2:30pm ON Monday Wednesday Friday COLOR orange", -1)


    indexOfFrom = inputStrDesc.index("\" FROM ")
    desc = inputStrDesc[indexOfDesc+8:indexOfFrom]
    return(desc, indexOfFrom)


# Function to parse the start time and end time of an event from a string starting with "FROM "
# Returns a tuple of a start time, end time, and index of On, the next keyword, or an error with an error code.

def parseTime(inputStrTime):
    if ("\" FROM ") not in inputStrTime: 
        return (f"ERROR: Couldn't find FROM keyword in {inputStrTime} \n Example input: EVENT \"CS111\" DESC \"Domain Specific Languages. Occurs ever Monday and Wednesday from 1:15 pm to 2:30 pm.\" FROM 1:15pm TO 2:30pm ON Monday Wednesday Friday COLOR orange",-1 )
    indexOfFrom = inputStrTime.index("\" FROM ")
    if (" TO ") not in inputStrTime: 
        return (f"ERROR: Couldn't find TO keyword in {inputStrTime} \n Example input: EVENT \"CS111\" DESC \"Domain Specific Languages. Occurs ever Monday and Wednesday from 1:15 pm to 2:30 pm.\" FROM 1:15pm TO 2:30pm ON Monday Wednesday Friday COLOR orange", -1)
    indexOfTo = inputStrTime.index(" TO ")
    if (" ON ") not in inputStrTime: 
        return (f"ERROR: Couldn't find TO keyword in {inputStrTime} \n Example input: EVENT \"CS111\" DESC \"Domain Specific Languages. Occurs ever Monday and Wednesday from 1:15 pm to 2:30 pm.\" FROM 1:15pm TO 2:30pm ON Monday Wednesday Friday COLOR orange", -1, -1)
    indexOfOn = inputStrTime.index(" ON ")
    startTime = inputStrTime[indexOfFrom+7:indexOfTo]
    endTime = inputStrTime[indexOfTo+4:indexOfOn]
    return (startTime, endTime, indexOfOn)

# Function to parse the days an event occurs on, starting with the keyword "ON"
# Returns a tuple containing a list of the days an event occurs on, as well as the index of when COLOR occurs.

def parseDays(inputStrDay):
    if (" ON ") not in inputStrDay:
        return (f"ERROR: Couldn't find TO keyword in {inputStrDay} \n Example input: EVENT \"CS111\" DESC \"Domain Specific Languages. Occurs ever Monday and Wednesday from 1:15 pm to 2:30 pm.\" FROM 1:15pm TO 2:30pm ON Monday Wednesday Friday COLOR orange", -1) 
    indexOfOn = inputStrDay.index(" ON ")
    if (" COLOR ") not in inputStrDay: 
        return (f"ERROR: Couldn't find TO COLOR in {inputStrDay} \n Example input: EVENT \"CS111\" DESC \"Domain Specific Languages. Occurs ever Monday and Wednesday from 1:15 pm to 2:30 pm.\" FROM 1:15pm TO 2:30pm ON Monday Wednesday Friday COLOR orange", -1) 
    indexOfColor = inputStrDay.index(" COLOR ")
    days = inputStrDay[indexOfOn + 4: indexOfColor].lower()
    listOfAcceptableDays = [
        "monday",
        "tuesday",
        "wednesday",
        "thursday",
        "friday",
        "saturday",
        "sunday",
        "m",
        "tu",
        "w",
        "th",
        "f",
        "sa",
        "su"
    ]
    if "all" in days:
        return (["all"], indexOfColor)
    listOfDays = []

    for day in listOfAcceptableDays:
        if day in days:
            listOfDays += [day]
            days = days.replace(day, "")
    if len(listOfDays) == 0:
        return (f"ERROR: Couldn't find any days in {inputStrDay} \n Example input: EVENT \"CS111\" DESC \"Domain Specific Languages. Occurs ever Monday and Wednesday from 1:15 pm to 2:30 pm.\" FROM 1:15pm TO 2:30pm ON Monday Wednesday Friday COLOR orange", -1) 
    return(listOfDays, indexOfColor)


# Function to parse the color an event occurs on, starting with the keyword "COLOR"
# Returns a single string for a color, as this is the last item in the input we don't have to return a new index.
# Also contains cases for if the last character is a newline.
            
def parseColor(inputStrColor):
    indexOfColor = inputStrColor.index(" COLOR ")
    if "\n" in inputStrColor:
        indexOfNewLine = inputStrColor.index("\n")
        return inputStrColor[indexOfColor + 7:indexOfNewLine]
    else:
        return inputStrColor[indexOfColor + 7:]


# Function to parse the user input given a string input of multiple lines in the syntax made.
# This also checks if errors occur in sendToInput.
# Will return a list of parsed events

def parseUserInput(lines):
    parsedInput = []
    lines = lines.split("\n")
    for line in lines:
        line = " ".join(line.split())
        if len(line) != 0 and line != "\n":
            sendToInput = parseInput(line)
            if isinstance(sendToInput, tuple):
                return sendToInput 
            parsedInput += [sendToInput]
    print(parsedInput)
    return parsedInput


#Function to convert a timestamp format of 00:00_m or 0:00_m to a 12 hour timestamp.
# Useful when calculating start times/start days for events when making the .ics file.

def convertToTime(startTime):
    in_time = datetime.datetime.strptime(startTime, "%I:%M%p")
    out_time = datetime.datetime.strftime(in_time, "%H:%M")
    return out_time

# Function to get the unix timestamp from a given weekday and time.
# For instance, giving createDateTime "Wednesday, 2pm" will determine
# Whether Wednesday, 2pm will occur later in the week or if it's already
# occured. It will then check what the next day/time this event will occur on, and returns that.
# Example: Wednesday, 1:30 pm. Right now it's Saturday the 29'th, so the next Wednesday is 
# the 3'rd. Return the timestamp of Wednesday the 3'rd at 1:30 pm.

def createDateTime(day, time):
    currentDate = datetime.datetime.today()
    currentDayOfWeek = currentDate.weekday()
    oneDay = 60 * 60 * 24
    newEvent = ""
    weekDayHash = {
        'sunday': 6,
        'monday': 0,
        'tuesday': 1,
        'wednesday': 2,
        'thursday': 3,
        'friday': 4,
        'saturday': 5,
        'su': 6,
        'm': 0,
        'tu': 1,
        'w': 2,
        'th': 3,
        'f': 4,
        'sa': 5,
    }
    usedTime = convertToTime(time)
    currentTime = tz.gettz()  

    if weekDayHash[day] > currentDayOfWeek:
        add = (oneDay * (weekDayHash[day] - currentDayOfWeek))
        print(add)
        newEvent = datetime.datetime.fromtimestamp(currentDate.timestamp() + add)
        newEvent = newEvent.replace(hour=int(usedTime[0:2]), minute=int(usedTime[3:5]), second=0, microsecond=0, tzinfo = currentTime)
    else:
        add = (oneDay * ((7 + weekDayHash[day] - currentDayOfWeek)%7))
        print(add)
        newEvent = newEvent = datetime.datetime.fromtimestamp(currentDate.timestamp() + add)
        newEvent = newEvent.replace(hour=int(usedTime[0:2]), minute=int(usedTime[3:5]), second=0, microsecond=0, tzinfo = currentTime)

    return newEvent



# Function to return a new calendar object.
# This will take in an already parsed eventarr, and for each
# event, go through each of the days, inserting them as new events on the calendar.
# Each event will have the attributes for start time/end time, name, and description. 
# I also wanted to experiment and see if it would be possible to add background colors to events,
# But this seems to not be supported by both the .ics library and by Google Calendar. There
# Is still a way to view the color of the event by appending the color to the end of the uid. 
# This way, if a preview is made using the .ics file instead of the parsed input, background colors
# can be obtained.

def makeNewCalendar(eventArr):
    c = Calendar()
    for event in eventArr:
        if len(event) != 0 and event != "\n":
            for occurDay in event[4]:
                newEvent = Event()
                newEvent.name = event[0]
                newEvent.description = event[1]
                startTime = event[2]
                endTime = event[3]
                color = event[5]
                usedStartTime = str(createDateTime(occurDay, startTime))
                usedEndTime = str(createDateTime(occurDay, endTime))
                newEvent.begin = usedStartTime
                newEvent.end = usedEndTime
                newEvent.uid = newEvent.uid + color
                c.events.add(newEvent)
    return c



# Function to mark RRULE in each event.
# This will take in a calendar object, read in the contents line by line, and where events
# occur, add a rule to make them occur each week. This is then returned.


def markRRULE(cal):
    lineArr = []
    for line in cal:
        lineArr += [line]
    pointer = 0 

    while pointer < len(lineArr):
        if "DTSTART:" in lineArr[pointer]:
            lineArr.insert(pointer + 1, "RRULE:FREQ=WEEKLY;\n")
            pointer += 1
        pointer += 1
    return lineArr

# Function to make the calendar and save to file!
# This will take in an unparsed, input string, and return either an error code, or will write
# to file as output.ics


def makeCalendar(inputStr):
    attrs = parseUserInput(inputStr)
    if isinstance(attrs, tuple):
        return attrs 
    cal = makeNewCalendar(attrs)
    returnedCal = markRRULE(cal)

    with open("output.ics", "w") as txt_file:
        for line in returnedCal:
            txt_file.write("".join(line))
    







## DSL PART 2: WRITING A HTML PREVIEW SCHEDULE TO FILE




    
# Function to convert from 12 hour timestamp to 24 hour timestamp.
# I got a bit lazy here as I was on a time crunch, but essentially
# it just uses regex to match the format of 00:00_m/0:00_m, and
# convers that to a 24 hour format.
# This is helpful when making the previews as that takes in 24 hour input.


def convert_to_24hour(time_str):
    hour, minute, am_pm = re.findall('\d+|\w+', time_str)
    hour = int(hour)
    if am_pm == 'pm' and hour != 12:
        hour += 12
    elif am_pm == 'am' and hour == 12:
        hour = 0
    elif am_pm == 'Pm' and hour != 12:
        hour += 12
    elif am_pm == 'Am' and hour == 12:
        hour = 0
    elif am_pm == 'pM' and hour != 12:
        hour += 12
    elif am_pm == 'aM' and hour == 12:
        hour = 0
    elif am_pm == 'PM' and hour != 12:
        hour += 12
    elif am_pm == 'AM' and hour == 12:
        hour = 0
    
    return f'{hour:02d}:{minute}'



# Hash tables corresponding to the background colors of events and the days of the week.

colorHash = {"tomato":"#d60004", "flamingo":"#e37d72", "tangerine":"#f25027", "banana":"#f3c127", "sage":"#35b57a", "basil":"#0d803f", "peacock":"#0899e6", "blueberry":"#3f50b7", "lavender":"#7885cf", "grape":"#8f20ae", "graphite":"#616161"}
inputColor = "tomato"
dayHash = {
        "monday":"Monday",
        "tuesday":"Tuesday",
        "wednesday": "Wednesday",
        "thursday": "Thursday",
        "friday": "Friday",
        "saturday": "Saturday",
        "sunday": "Sunday",
        "m": "Monday",
        "tu": "Tuesday",
        "w": "Wednesday",
        "th": "Thursday",
        "f": "Friday",
        "sa": "Saturday",
        "su": "Sunday"
}


# Function to make an event string in html.
# This will take in an eventArr, and use fstrings to create the
# Html file to be written in the preview file.
# Colors are optional in this, as it will by default show the blue/peacock color.

def makeEventStr(eventArr):
    print(eventArr)
    eventName = eventArr[0]
    color = ""
    if len(eventArr[5]) == 0 or eventArr[5] not in colorHash:
        color = "#0899e6"
    else:
        color = colorHash[eventArr[5]]
    startTime = convert_to_24hour(eventArr[2])
    endTime = convert_to_24hour(eventArr[3])
    returnedEventStr = f"\n<li class=\'cd-schedule__event\'>\n    <a data-start=\'{startTime}\' data-end=\'{endTime}\' data-content=\'event-abs-circuit\' style=\'background-color:{color};\' data-event=\'event-1\' href=\'#0\'>\n        <em class=\'cd-schedule__name\'>{eventName}</em>\n    </a>\n</li>\n".format(startTime, endTime, color, eventName)
    return returnedEventStr


# Function to write the new event to the html file.
# This will take in an html file, and a parsed single event.
# It will then search for each day the event occurs on, the
# indices of the days in the schedule template. After the schedule template,
# It will insert the new html we've written for the event.


def writeNewEvent(html, eventArr):
    textToWrite = makeEventStr(eventArr)
    for day in eventArr[4]:
        day = dayHash[day]
        html = (html[:html.index(f"<span>{day}</span></div>".format(day)) + len(f"<span>{day}</span></div>".format(day)) + 15]) + textToWrite + (html[html.index(f"<span>{day}</span></div>".format(day)) + len(f"<span>{day}</span></div>".format(day)) + 15:])
    return(html)


# Function to write all events. 
# Pretty straightforward, just takes in an html file and parsed event array
# And iterates through them, calling writeNewEvent.

def writeAllEvents(html, eventArrs):
    for event in eventArrs:
        html = writeNewEvent(html, event)
    return html


# Function to make the schedule!
# This will read in the template file saved which contains no events,
# Create the new html file based on this,
# Then write the html to file under "schedule.html"

def makeNewSchedule(eventArrs):
    with open(r'index_copy.html', "r") as f:
        html = f.read()
    newHtml = writeAllEvents(html, eventArrs)
    f = open("schedule.html", "w")
    f.write(newHtml)
    f.close()
    



## DSL PART 3: CUSTOMTKINTER APPLICATION


# Global variable to keep track of what text should be in the popup window.
# This could be an error, or a message saying it successfully worked.

errorCode = ""



# CustomTKinter appearance color schemes.

customtkinter.set_appearance_mode("System")  # Modes: "System" (standard), "Dark", "Light"
customtkinter.set_default_color_theme("blue")  # Themes: "blue" (standard), "green", "dark-blue"



# Class for the popup window.
# This references the global errorCode and displays that in a 
# Disabled textbox.

class ToplevelWindow(customtkinter.CTkToplevel):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.geometry("400x300")
        self.grid_columnconfigure(0, weight=1)
        global errorCode
        self.title("ICS Specific Language")
        self.textbox = customtkinter.CTkTextbox(self)
        self.textbox.insert(END,errorCode)
        self.textbox.configure(state="disabled")

        self.textbox.grid(row=0, column=0, rowspan=2, columnspan=2, padx=(20, 20), pady=(20, 20), sticky="nsew")
        self.textbox.grid_columnconfigure(0, weight=1)



# Class for the App, what the user interacts with most of the time.

class App(customtkinter.CTk):
    def __init__(self):
        self.toplevel_window = None

        super().__init__()

        # configure window
        self.title("ICS Specific Language")
        self.geometry(f"{1100}x{580}")

        # configure grid layout
        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure((0, 2), weight=1)
        self.grid_rowconfigure((0, 0, 2), weight=1)

        # create left side/sidebar frame with widgets
        self.sidebar_frame = customtkinter.CTkFrame(self, corner_radius=20)
        self.sidebar_frame.grid(row=0, column=0, rowspan=4, sticky="nsew")
        self.sidebar_frame.grid_rowconfigure(2, weight=1)
        self.sidebar_frame.grid_columnconfigure(0, weight=1)
        self.logo_label = customtkinter.CTkLabel(self.sidebar_frame, text="ICS Specific Language", font=customtkinter.CTkFont(size=20, weight="bold"))
        self.logo_label.grid(row=0, column=0, padx=20, pady=(20, 10))
        self.sidebar_button_1 = customtkinter.CTkButton(self.sidebar_frame, command=self.outputPreviewFile, text="Render Preview")
        self.sidebar_button_1.grid(row=3, column=0, padx=20, pady=10)
        self.sidebar_button_2 = customtkinter.CTkButton(self.sidebar_frame, command=self.outputICSFile, text="Output ICS")
        self.sidebar_button_2.grid(row=4, column=0, padx=20, pady=10)
    

        
        # create textbox and display it in the left sidebar.
        self.textbox = customtkinter.CTkTextbox(self.sidebar_frame)
        self.textbox.grid(row=2, column=0, padx=(20, 20), pady=(20, 20), sticky="nsew")
        self.textbox.grid_columnconfigure(0, weight=1)

        
        #Create the documentation frame/readme frame on the right side of the app.
        self.intro_frame = customtkinter.CTkTextbox(self)
        self.intro_frame.insert(END, "Hello! \nThis is a Domain Specific Language for previewing and viewing ICS files. \n \nYou'll want to input events on the textbox in the left. A event will start with a event name, with an optional description. Events will need a start time, end time, days it occurs on, and an optional color flag. \n \n An example event would be: \n EVENT \"CS111\" DESC \"Domain Specific Languages. Occurs ever Monday and Wednesday from 1:15 pm to 2:30 pm.\" FROM 1:15pm TO 2:30pm ON Monday Wednesday Friday COLOR flamingo \n \nYou can also speed up the creation of the ics file by using no natural syntax. The same event can be made using: \n \n \"CS111\" \"Domain Specific Languages. Occurs ever Monday and Wednesday from 1:15 pm to 2:30 pm.\" 1:15pm 2:30pm M W F flamingo \n \nEvents and descriptions will need to be wrapped in quotations. Times will need to contain a 12 hour timestamp format with no space between the time and the am/pm. The possible day formats are each day of the week, with shorter versions being \"m\", \"tu\", \"w\", \"th\", \"f\", \"sa\", \"su\". Colors are optional, but must follow the colors available in Google Calendar. These are limited to \"tomato\", \"flamingo\", \"tangerine\", \"banana\", \"sage\", \"basil\", \"peacock\", \"blueberry\", \"lavender\", \"grape\", and \"graphite\". If a input is incorrect or has a syntax error, the error will appear in a dialogue box. \n \nThank you so much! ")
        self.intro_frame.configure(state="disabled")
        self.intro_frame.grid(row=0, rowspan=4,columnspan=4, column=1, padx=(20, 20), pady=(20, 0), sticky="nsew")


        # insert in the textbox the placeholder text, which is an example event.
        self.textbox.insert(END,"EVENT \"CS111\" DESC \"Domain Specific Languages. Occurs ever Monday and Wednesday from 1:15 pm to 2:30 pm.\" FROM 1:15pm TO 2:30pm ON Monday Wednesday COLOR flamingo")


    # Function to open a popup window.
    def open_input_dialog_event(self):
        if self.toplevel_window is None or not self.toplevel_window.winfo_exists():
            self.toplevel_window = ToplevelWindow(self)  # create window if its None or destroyed
        else:
            self.toplevel_window.focus()  # if window exists focus it


    # Function to make an ics file.
    # Will check if an error occured, and if so display that.
    # If not, it will display a message saying it ran
    # Successfully

    def outputICSFile(self):
        print(repr(self.textbox.get("0.0", END)))
        response = makeCalendar(self.textbox.get("0.0", END))
        global errorCode
        if isinstance(response, tuple):
            error, index = response
            errorCode = error
            self.open_input_dialog_event()
        else:
            errorCode = "Successfully output a calendar as a .ics file!"
            self.open_input_dialog_event()


    # Function to make the html preview file.
    # Will check if an error occured, and if so display that.
    # If not, it will display a message saying it ran
    # Successfully

    def outputPreviewFile(self):
        response = parseUserInput(self.textbox.get("0.0", END))
        global errorCode
        if isinstance(response, tuple):
            error, index = response
            errorCode = error
            self.open_input_dialog_event()
        makeNewSchedule(response)
        errorCode = "Successfully output a html file as a preview of your schedule!"
        self.open_input_dialog_event()




if __name__ == "__main__":
    app = App()
    app.mainloop()