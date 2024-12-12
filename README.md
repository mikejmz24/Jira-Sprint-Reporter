# Jira Sprint Reporter

Jira Sprint Reporter is a command line tool designed to generate sprint reports for Scrum teams. This tool guides you through a series of prompts to enter your team details, select the sprint, and specify the Confluence space and page where the report should be printed.

## Features
- Only works for Scrum teams
- Interactive CLI to input team, sprint, Confluence space, and page
- Python-based project managed by Poetry

## Getting Started

### Prerequisites
- A Mac with Homebrew installed
- Python installed (version 3.7 or higher)

### Installation

#### Step 1: Install Poetry
You can install Poetry using Homebrew by running the following commands:

```bash
brew install poetry
```

#### Step 2: Clone the Repository
Clone the project repository from GitHub:

```bash
git clone https://github.com/mikejmz24/Jira-Sprint-Reporter.git
cd Jira-Sprint-Reporter
```

#### Step 3: Initialize the Project
Navigate to the project directory and initialize the Poetry environment

```bash
poetry shell
```

Then, install the project dependencies:

```bash
poetry install
```

### Running the Application
To run the CLI applicatoin, execute the following command:

```bash
python main.py
```
Follow the on-screen prompts to input:
* The desired team
* The sprint 
* The Confluence space
* The Confluence page

### Building the Project
To build the project, you can use the following command:

```bash
poetry build
```

This will create a distribution package for the project.

### Running Tests
To run test using the Makefile, use the following command:

```bash
make test
```

This will execute all the tests defined for the project.

#### Example
Here is a quick example fo using the CLI:

1. Run the project:

```bash
python main.py
```

2. Follow the prompts:

```
Search for a team board that you woulld like to generate reports
Team A

Please select a team board:
[1] Team A board
Enter the number of the team board: 1
Excellent, we can continue! You team board number is: 01
Please select a sprint
[1] Team A Sprint 1
[2] Team A Sprint 2
Enter the number fo the sprint: 1
Excellent, we can continue! Your sprint number is: 1000001
Now finally enter the Confluence Space and Ancestor IDs where you would like to create the Sprint report
First enter the Confluence Space Key
~email@company.com
Now let's finish with the Confluence Ancestor ID
010203
```

3. The tool will then generate a sprint report and print it to the specified Confluence page.

### Closing the virtual environment
To close the poetry shell type

```bash
exit
```

#### Contributing
Contributions are welcome! Please fork the repository and submit a pull request for any improvement or bug fixes.

### License
This project is licensed under the MIT License. See the LICENSE file for details.
