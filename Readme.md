# Neoj_LLMs

Neoj_LLMs is a sophisticated tool that facilitates seamless interaction with your Neo4j database, whether it's hosted locally or on a sandbox. This repository enables users to ask natural language questions about their databases, which are then intelligently translated into Neo4j Cypher Queries using Language Model Models (LLMs), making the querying process intuitive and accessible.

## Features

- **Database Connection:** Connect to your Neo4j database, whether it's locally hosted or on a sandbox.

- **Natural Language Queries:** Ask questions about your database using natural language, simplifying user interactions with the graph.

- **LLM Translation:** Leverage the power of Language Model Models to intelligently translate natural language queries into Neo4j Cypher Queries.

## Getting Started

Follow these steps to get started with Neoj_LLMs:

1. Clone the repository:
    ```bash
    git clone https://github.com/elmondhir/Neo4j-LLMS.git
    cd Neoj-LLMs
    ```

2. Install dependencies:
    ```bash
    pip install -r requirements.txt
    ```

3. Configure your Neo4j database connection details in the `config.py` file.

4. Set up the Hugging Face API key for LLM translation.

5. Run the application:
    ```bash
    python -B manage.py runserver
    ```

6. Open your browser and go to [http://localhost:8000](http://localhost:8000) to access the Neoj_LLMs interface.

## Usage

1. Connect to your Neo4j database by providing the necessary connection details.

2. Ask natural language questions about your database in the provided interface.

3. Neoj_LLMs will intelligently translate your natural language questions into Neo4j Cypher Queries using Language Model Models.

4. View and execute the generated Cypher Queries on your Neo4j database.

## Screenshots

### First you need to login to your neo4 instance:
![Alt text](screenshots/login.png?raw=true "Title")
### Then you chose which database you want to work with:
![Alt text](screenshots/select_db.png?raw=true "Title")
### Finally you input your prompt and HF token:
![Alt text](screenshots/example1.png?raw=true "Title")
## Running with Docker

To run Neoj_LLMs using Docker, make sure Docker is installed on your machine. If not, you can download and install Docker from the [official Docker website](https://www.docker.com/get-started).

Follow these steps:

1. Build the Docker image:
    ```bash
    docker-compose build
    ```

2. Start the application:
    ```bash
    docker-compose up
    ```

3. Open your browser and go to [http://localhost:8000](http://localhost:8000) to access the Neoj_LLMs interface.

## Contributing

We welcome contributions! If you find any issues or have suggestions for improvements, please open an issue or submit a pull request.
