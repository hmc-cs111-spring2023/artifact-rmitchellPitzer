### **Hello!** 
This is a Domain Specific Language for previewing and viewing ICS files called ICS Specific Language.

## IMPORTANT: Make sure to have Python updated with the TKinter and ICS libraries installed. 
 
 
 ### Install instructions 
You can download the file from the final-release branch! This will give you a zip file. Extract the folder to anywhere and in a terminal navigate to the directory containing main.py and run "python main.py". 

### Usage
Once opened, you will have the option to input text in a textbox on the left side of the app. On the right side there will be instructions for what is acceptable syntax. Users have the option to either output a .ics file or a HTML preview. This HTML preview can be viewed by opening it in a browser. 

### Documentation

Events are input in the textbox, separated by new lines. A event will take in the following arguments:
- An event name, 
- An optional description,
- A start time,
- A end time,
- A list of days it occurs on,
- An optional background color

#### Event Names
A event name can be specified by wrapping the name in quotation marks and either using the EVENT keyword or not using it. Some examples are:
- EVENT "CS111"

or by 

- "CS111"

#### Description
A description is optional, and if left blank will result in an empty description for the event. It follows the same formatting for event names:
- EVENT "CS111" DESC "Domain Specific Languages. Occurs ever Monday and Wednesday from 1:15 pm to 2:30 pm."
or by 
- "CS111" "Domain Specific Languages. Occurs ever Monday and Wednesday from 1:15 pm to 2:30 pm."

To make an event without a description just leave out DESC and the quotation marks, and jump to the next section

#### Start Time and End Time 
A start time and end time are used to determine the duration of the event. This is in 12 hour format. An example input is below:
- EVENT "CS111" DESC "Domain Specific Languages. Occurs ever Monday and Wednesday from 1:15 pm to 2:30 pm." FROM 1:15pm TO 2:30pm 

or by 

- "CS111" "Domain Specific Languages. Occurs ever Monday and Wednesday from 1:15 pm to 2:30 pm." 1:15pm 2:30pm

It's important to have no space between the timestamp and the am/pm

#### Days
An event can occur on any number of weekdays. The options for weekdays are as follows:
- "monday",
- "tuesday",
- "wednesday",
- "thursday",
- "friday",
- "saturday",
- "sunday",
- "m",
- "tu",
- "w",
- "th",
- "f",
- "sa",
- "su"

M/TU/W/TH/F/SA/SU refer to shorter versions of weekdays. They can be used interchangably.
An example can be seen below: 

- EVENT "CS111" DESC "Domain Specific Languages. Occurs ever Monday and Wednesday from 1:15 pm to 2:30 pm." FROM 1:15pm TO 2:30pm ON Monday Wednesday

or by

- "CS111" "Domain Specific Languages. Occurs ever Monday and Wednesday from 1:15 pm to 2:30 pm." 1:15pm 2:30pm M W
 
#### Event Color/Labels
Unfortunately importing to different calendar apps won't support the background colors. This is either due to how the apps are made or due to the limitations of the .ics file format. However, these colors are supported in the schedule preview present in this DSL.
The options for colors are as follows: 
- "tomato", 
- "flamingo", 
- "tangerine", 
- "banana",
- "sage", 
- "basil", 
- "peacock", 
- "blueberry", 
- "lavender", 
- "grape", 
- "graphite"

These correspond to the labels available on Google Calendar. For more information click [here](https://support.google.com/calendar/answer/12377581?hl=en&co=GENIE.Platform%3DAndroid)

An example of the input can be seen below:
- EVENT "CS111" DESC "Domain Specific Languages. Occurs ever Monday and Wednesday from 1:15 pm to 2:30 pm." FROM 1:15pm TO 2:30pm ON Monday Wednesday COLOR flamingo

or by

- "CS111" "Domain Specific Languages. Occurs ever Monday and Wednesday from 1:15 pm to 2:30 pm." 1:15pm 2:30pm M W flamingo


#### Wrap Up And More Information

After this you should have two different events written in different ways!

Some more information on the DSL: There will be a popup message indicating if a preview write or a ics write was successful or failed. Moving the schedule.html outside of the folder will cause it to lose css/javascript functionality.

Thank you so much!
