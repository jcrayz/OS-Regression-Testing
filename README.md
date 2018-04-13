# regrOS

*Still to be completed*

# All-American Regress Team

Jenna Cray, Blake Gordon, Christopher Chen

## Installation

*Install the product (to be completed)*

Once the installation is completed, *(open the command prompt and cd into the root directory/open the shortcut in the
folder to open the command prompt. To be completed)*, then execute the command `python -m allamericanregress --install`.

This command will install the windows service to ensure our program will be run when your computer performs an update.
Additionally, the install will ensure that the database and supporting files are created.

## Register Test Suite

Once the program is installed, register the desired test suites with our program.
To do this there are two different ways.

#### 1. From the Web App (Recommended)

Run the web app (see [Web App](#web-app) section to know how to run the web app).  Then open a web browser and direct it to
http://127.0.0.1:5000/ and fill out the required fields. The required fields are the Path, Name, and Command.
The author is an optional field and meant for the name of who created the test suite.
    
* **Path:** The absolute path of where the test suite is located. Be sure to type the path as you would see it with 
spaces, e.g. C:\Users\allamericanregress\My Documents\Test Suite.jar   
* **Name:** The name of the test suite (this can be anything), e.g. Java Test Suite
* **Command:** The command for how to execute the test suite from the command line. Substitute '$1' for the path to the 
test suite, e.g. java -jar $1
* **Author (optional):** The name of the developer that created the program or test suite

Once the fields are filled out, click submit. The test suite will be executed when they are initially registered. 
If the command returns an **Exit Code** of 0 then it is assumed that all of the tests passed. If any other **Exit Code** 
is returned, it is assumed that one or more of the tests failed. All of the results will be able to be viewed in the 
web app. 

![register test executable](/screenshots/Register.png "Register Test Executable")

#### 2. From the Command Line

cd to where regrOS is installed on your machine. Once at the command line, execute 
`python -m allamericanregress --register --path '{path}' --name '{name}' --command '{command}' --author '{author}'` 
where {path}, {name}, {command}, and {author} are as specified above.


## View and Understand the Results

Run the web app (see [Web App](#web-app) section to know how to run the web app) and open a web browser to 
http://127.0.0.1:5000/ to view the results. The home (or index) page will show the most recent results at the top of 
the page. The table displays the ID Number of the registered test suite, the Name of the test suite, the Last Result of 
when it was executed (either Pass or Fail), the operating system’s version number that the test suite last passed on, 
the date that the test suite last passed, and a button to execute the individual test.

![results table](/screenshots/Results.png "Results Table")

If there is a failure of any test, click the Failure Logs link at the top of the page. This page shows any failure of 
any test suite, at any time. This table shows the ID Number of the registered test suite, the Name of the test suite, 
the Execution ID of the execution record for when the test suite was executed, the Execution Date of when the test 
suite was executed, the version of the Operating System that the executed test suite failed on, the returned Exit Code 
from the execution, and the Message or the command line output from the execution. 

![failure logs](/screenshots/Failures.png "Failure Logs")

## Web App

#### Run the Web App

From the command line, cd to where regrOS is installed on your machine. Once at the command line, execute `regrOS.exe 
--webapp` and keep the command prompt open. This will run the web app so that it is accessible on 
any web browser of the local machine at http://127.0.0.1:5000/

![command line](/screenshots/CommandLine.png "Command Line")

#### Stop Running the Web App

To stop the running of the web app, return to the command prompt that the web app began running on and press Ctrl + C

## Manual Execution

#### 1. From the Web App (Recommended)

Run the web app (see [Web App](#web-app) section to know how to run the web app) and open a web browser to 
http://127.0.0.1:5000/ to be able to execute all of the tests, only the failed tests, or an individual test. In the 
results table, the last column contains an execute button that will execute the individual test suite of the column. 
To execute all of the test suites that failed on the most previous execution, press the Execute Failed button at the 
bottom of the results table. To execute all of the test suites registered, press the Execute All button at the bottom 
of the results table. 

#### 2. From the Command Line

cd to where regrOS is installed on your machine. Once at the command line, execute 
`python -m allamericanregress --execute-tests` to execute all registered tests. 

## Delete Registered Test Suite

#### 1. From the Web App (Recommended)

To remove a registered test suite from the web app, be sure that it is running (see [Web App](#web-app) section to know 
how to run the web app). With the web app running, navigate to http://127.0.0.1:5000/ in the browser of your local 
machine. On the home (or index) page of the web app, there will be a table of all the registered test suites at the 
bottom of the page. In the last column of each row, there is a Delete button. Click the button in the row of the record 
you wish to delete, and this will delete the registered test suite and the logs associated with the test suite. 

![delete test suite](/screenshots/Registered.png "Delete Test Suite")

#### 2. From the Command Line

To remove a registered test suite from the command line, be sure you are in the directory of regrOS, and execute 
`python -m allamericanregress --delete {id}` where {id} is the generated ID Number for the test suite. This can be 
found on the web app, or by executing `python -m allamericanregress --list` to view the list of all the registered 
test suites.

## Uninstall

*To be completed*