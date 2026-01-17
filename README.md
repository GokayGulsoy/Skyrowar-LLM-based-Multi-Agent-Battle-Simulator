# Skyrowar-LLM-based-Multi-Agent-Battle-Simulator

Repository that contains the implementation of the CENG 568 Multi-Agent Systems Course Project: Skyrowar: The LLM-Based Multi-Agent Card Game-Playing Framework. 

Directory Structure of the project is as follows:

```bash
Multi_Agent_Systems_Project
│   main.py
│   requirements.txt
│
├───agents
│       team_generation_agent.py
│       team_lead_agent.py
│       team_manager_agent.py
│       __init__.py
│
├───game
│       game.py
│       __init__.py
│
└───utils
│       agent_model_factory.py
│       api_model_checker.py
│       __init__.py
│
├───Experimental Results
│       Compared_models.txt
│       Experiment_A1.txt
│       Experiment_A2.txt
│       Experiment_A3.txt
│       Experiment_B1.txt
│       Experiment_B2.txt
│       Experiment_B3.txt
│       Experiment_C1.txt
│       Experiment_C2.txt
│       Experiment_C3.txt
│       Experiment_E1.txt
│       Experiment_E2.txt
│       Experiment_E3.txt
│       Experiment_E4.txt
│       Experiment_E5.txt
````

## Setup & Installation

Clone the repository and change directory to root directory of the project as follows:

```bash
git clone https://github.com/GokayGulsoy/Skyrowar-LLM-based-Multi-Agent-Battle-Simulator.git
cd Multi_Agent_Systems_Project
````

## Create a Virtual Environment

Create a virtual environment and activate it via executing following commands:

###  On Windows

```bash
python -m venv <name_of_virtual_environment> 
venv\Scripts\activate
````

###  On macOS & Linux

```bash
python -m venv <name_of_virtual_environment> 
source venv/bin/activate
````

## Install Dependencies

Install the dependecies required to run the project are installed as follows:

```bash
pip install -r requirements.txt
````

## Configure API keys

Environment variables must be set up for the LLM providers you intent to use. You can set this in your OS environment variables permanently, via using terminal (which only persists for existing terminal session), or in .env file

### Required Keys

- `OPENAI_API_KEY` (for OpenAI models) 
- `GOOGLE_API_KEY` (for Gemini models)
- `ANTHROPIC_API_KEY` (for Claude models)
- `GROQ_API_KEY` (for Llama models)

#### Example (Mac/Linux)

Setup in your either profile file (~/.bashrc in Linux) or existing terminal session 

```bash
export OPENAI_API_KEY="sk-..."
export GOOGLE_API_KEY="AIza..."
```

### Example (Windows CMD)

Setup in your either environment variable settings or existing terminal session

```bash
set OPENAI_API_KEY="sk-..."
set GOOGLE_API_KEY="AIza..."
```

## Usage 

### Run the Battle Simulation

To start the simulation with default settings (Team A: gpt-4o vs Team B: gpt-4o-min, 5 episodes, difficulty 1.0):

```bash
python main.py
```

#### Custom Configuration

models, number of episodes, and difficulty scaling can be customized using command-line arguments:

```bash
python main.py --model-a "gpt-4o" --model-b "gpt-4o"-mini" --episodes 10 --difficulty 1.5
```

To get detailed usage instructions for command line arguments execute: 

```bash
python main.py --help
```

**Arguments**
- `--model-a`: Model ID for Team A
- `--model-b`: Model ID for Team B
- `--episodes`: Number of games to simulate (Default: 5)
- `--difficulty`: Stat Multiplier for Team B (Defualt: 1.0)

## Check Available Models

To verify which models are available and accessible with your current API keys, use the utility script:

```bash
python -m utils.api_model_checker --api-provider openai
```

To get detailed usage instructions for command line arguments execute:

```bash
python -m utils.api_model_checker --help
```

Supported providers: `openai`,`google`,`anthropic`,`llama`

Link to Research Paper: [Syrowar: The LLM-based Multi-Agent Card Game-Playing Framework]()



