![Contributors][contributors-shield]
![Forks][forks-shield]
![Stargazers][stars-shield]
![Issues][issues-shield]
[![LinkedIn][linkedin-shield]](https://www.linkedin.com/in/louisanhtran/)



<!-- Logo of website -->
<div align="center">

  <img src="https://effvision.com/wp-content/uploads/2024/06/artificial-intelligence-new-technology-science-futuristic-abstract-human-brain-ai-technology-cpu-central-processor-unit-chipset-big-data-machine-learning-cyber-mind-domination-generative-ai-scaled-1.jpg" width="500">

</div>

<!-- Introduction of project -->

<div align="center">
  
# LLM-Powered Contextual Search & Summarization - Frontend

</div>

<h2 align="center" style="text-decoration: none;">Document processing AI Application</h2>

## About The Application :

This application is designed to efficiently process contextual and semantic search, as well as summarization, on large PDF documents. The list of main features offered by the application is shown below:

- [x] Indexing large documents efficiently using parallel processing and a distributed vector database.
- [x] Allowing accurate semantic search (not just keyword-based) on those documents.
- [x] A well-designed AI pipeline for optimizing costs by reducing unnecessary LLM calls.
- [x] Caching responses using an in-memory DB (Redis) to minimize costs and enhance user experience.
- [x] PDF documents are encrypted and securely stored in an AWS S3 bucket.
- [x] A clean and user-friendly interface built with Streamlit.

## Built With

This section outlines the technologies and tools used to develop the application.

* Backend: ![fastapi-shield][fastapi-shield]
* Frontend: ![fastapi-shield][streamlit-shield]
* AI/ML Framework: ![fastapi-shield][langchain-shield]
* LLM Provider: OpenAI
* Chat model: gpt-4o
* Embedding model: text-embedding-ada-002
* Vector database: Pinecone
* PDF Document storage: AWS S3 Bucket
* Caching: Redis
* Parsing large PDFs document: PyMuPDF

## Quick Application run using Docker

1. Install Docker:

  - Ensure Docker is installed on your machine. If not, download and install it from [Docker](https://docs.docker.com/engine/install/)

2. Create a Project Directory:
  - In your home directory, create a new directory for the project
    ```
    mkdir ai-app
    ```
  - Navigate to the newly created directory:
    ```
    cd ai-app
    ```
3. Clone the Project and Set Up Environment Variables

  - Clone the backend repository to your local machine:
     ```
     git clone https://github.com/LouisAnhTran/llm-powered-contextual-search-and-summarization-backend.git 
     ```
  - IMPORTANT! -> Navigate to the backend directory and paste the .env file containing all necessary credentials for the application.
  - Go back to the ai-app directory and clone the frontend repository:
     ```
     git clone https://github.com/LouisAnhTran/llm-powered-contextual-search-and-summarization-frontend.git
     ```
4. Create a docker-compose.yml File:
   - Create a docker-compose.yml file in ai-app directory with the following content:
     ```yml
      version: '3.8'

      services:
        redis:
          image: redis
          container_name: redis
          ports:
            - "6379:6379"
      
        backend:
          image: semantic-search-and-text-summarization-app-backend
          build:
            context: ./backend
            dockerfile: Dockerfile
          ports:
            - "8080:8080"
          env_file:
            - ./backend/.env
          depends_on:
            - redis
      
        frontend:
          image: semantic-search-and-text-summarization-app-frontend
          build:
            context: ./streamlit_frontend
            dockerfile: Dockerfile
          ports:
            - "8501:8501"
          environment:
            - BACKEND_API_URL=http://backend:8080/api/v1
            - TENANT='staple_ai_client'
          depends_on:
            - backend

     ```
  6. Run the application:
  - Run the following command to spin up three Docker containers (backend, frontend, and Redis server) to test the application:
   ```
    docker-compose up --build 
   ```
  - To stop all running containers, press CTRL + C, then run:
  ```
    docker-compose down
  ```



<!-- GETTING STARTED -->
## Run application on Localhost (Without Docker)

### Prerequisites

1. Backend Setup Required:
   
- Before setting up the frontend, ensure the Backend is running. First, access the [Backend repository](https://github.com/LouisAnhTran/llm-powered-contextual-search-and-summarization-backend) and follow the setup instructions to get it up and running. Once the Backend is ready, return to this repository to proceed with the frontend setup.

3. Poetry:
  - Use the following command to check whether poetry is installed in your machine
```
poetry --version
```
  - If poetry is not yet installed in your machine, please follow the link below to install Poetry, which is a common tool for dependency management and packaging in Python, specially for AI Applications.
[Poetry](https://python-poetry.org/docs/)

3. Clone the project to your local machine.

  ``` 
  git clone https://github.com/LouisAnhTran/llm-powered-contextual-search-and-summarization-frontend.git
  ```


### Installation


1. Install Dependencies:
  ```sh
  poetry install
  ```

2. Create an Python virtual environment 

  ```sh
  poetry shell
  ```

4. Run the application
  ```sh
  poetry run streamlit run chatbot.py --server.fileWatcherType=watchdog   
  ```

## Architecture: 

### System Architecture:
   
![Screenshot 2025-02-15 at 12 20 59 AM](https://github.com/user-attachments/assets/6c1596c7-355a-45a2-8844-8c2f2f243850)


<!-- ACKNOWLEDGMENTS -->
## References:

- [FastAPI](https://fastapi.tiangolo.com/)

- [Redis](https://redis.io/)

- [Pipecone](https://www.pinecone.io/)

- [Streamlit](https://streamlit.io/)

<!-- MARKDOWN LINKS & IMAGES -->
<!-- https://www.markdownguide.org/basic-syntax/#reference-style-links -->
[contributors-shield]: https://img.shields.io/github/contributors/othneildrew/Best-README-Template.svg?style=for-the-badge
[contributors-url]: https://github.com/othneildrew/Best-README-Template/graphs/contributors
[forks-shield]: https://img.shields.io/github/forks/othneildrew/Best-README-Template.svg?style=for-the-badge
[forks-url]: https://github.com/othneildrew/Best-README-Template/network/members
[stars-shield]: https://img.shields.io/github/stars/othneildrew/Best-README-Template.svg?style=for-the-badge
[stars-url]: https://github.com/othneildrew/Best-README-Template/stargazers
[issues-shield]: https://img.shields.io/github/issues/othneildrew/Best-README-Template.svg?style=for-the-badge
[issues-url]: https://github.com/othneildrew/Best-README-Template/issues
[license-shield]: https://img.shields.io/github/license/othneildrew/Best-README-Template.svg?style=for-the-badge
[license-url]: https://github.com/othneildrew/Best-README-Template/blob/master/LICENSE.txt
[linkedin-shield]: https://img.shields.io/badge/-LinkedIn-black.svg?style=for-the-badge&logo=linkedin&colorB=555
[linkedin-url]: https://linkedin.com/in/othneildrew
[product-screenshot]: images/screenshot.png


[fastapi-shield]: https://img.shields.io/badge/FastAPI-005571?style=for-the-badge&logo=fastapi
[streamlit-shield]: https://img.shields.io/badge/-Streamlit-FF4B4B?style=flat&logo=streamlit&logoColor=white
[langchain-shield]: https://img.shields.io/badge/LangChain-ffffff?logo=langchain&logoColor=green











