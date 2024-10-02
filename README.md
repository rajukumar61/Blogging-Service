# Blogging-Service


```markdown
# Blogging Service

This project is a microservice-based blogging platform that allows users to submit blog entries and search for them. It leverages **Docker**, **RabbitMQ**, **Elasticsearch**, and **Kubernetes** for containerization and orchestration, and ensures scalability and asynchronous operations.

## Features
1. **Blog Submission API**:
   - Submit a blog entry with title, text, and user ID.
   - Submissions are handled asynchronously using a message queue.

2. **Queue Consumer**:
   - A consumer service reads blog submissions from the queue and writes them into an **Elasticsearch** database for indexing and search.

3. **Search API**:
   - Search for blogs based on a query, returning results from both the blog title and content.

4. **Elasticsearch**:
   - Data is stored in **Elasticsearch**, with mappings ensuring both `blog-title` and `blog-text` are stored and searchable as strings.

## Technical Stack
- **Programming Language**: Python
- **Queue**: RabbitMQ
- **Database**: Elasticsearch
- **Containerization**: Docker, Kubernetes
- **Framework**: Flask (for APIs)
- **Other Tools**: Docker Compose for easy service orchestration

---

## Architecture Overview

1. **API Service**: Handles blog submissions and search queries.
2. **RabbitMQ Queue**: Stores blog entries for asynchronous processing.
3. **Consumer Service**: Reads from RabbitMQ and indexes the blog into Elasticsearch.
4. **Elasticsearch**: A full-text search engine that allows for efficient searching of blog content.

---

## Project Structure

```
blogging-service/
├── api/
│   ├── Dockerfile               # API service docker configuration
│   ├── main.py                  # API service implementation
│   ├── requirements.txt         # API dependencies
├── consumer/
│   ├── Dockerfile               # Queue consumer docker configuration
│   ├── consumer.py              # Queue consumer service implementation
│   ├── requirements.txt         # Consumer dependencies
├── elasticsearch/
│   └── elasticsearch-mapping.json   # Elasticsearch mapping file for blog documents
├── k8s/
│   ├── api-deployment.yaml          # Kubernetes deployment for API service
│   ├── consumer-deployment.yaml     # Kubernetes deployment for Consumer service
│   ├── elasticsearch-deployment.yaml# Kubernetes deployment for Elasticsearch
│   ├── rabbitmq-deployment.yaml     # Kubernetes deployment for RabbitMQ
│   └── services.yaml                # Kubernetes services to expose APIs
├── docker-compose.yml           # Docker Compose for local development
└── README.md                    # Project documentation
```

---

## Prerequisites

To run this project, you'll need the following installed on your machine:
- [Docker](https://www.docker.com/)
- [Docker Compose](https://docs.docker.com/compose/)
- [Kubernetes (kubectl & minikube)](https://kubernetes.io/)

---

## Setup Instructions

### 1. Docker Compose Setup

To run the entire stack locally using Docker Compose, follow these steps:

1. Clone the repository:

    ```bash
    git clone https://github.com/your-repo/blogging-service.git
    cd blogging-service
    ```

2. Start the services using Docker Compose:

    ```bash
    docker-compose up --build
    ```

    This will start the following services:
    - **API** (Flask)
    - **RabbitMQ** (Message Queue)
    - **Consumer** (Queue processor)
    - **Elasticsearch** (Search engine)

3. The API service will be available at `http://localhost:5000/`.

### 2. Kubernetes Setup

If you prefer running the stack in a Kubernetes cluster, use the provided Kubernetes manifests:

1. Start minikube:

    ```bash
    minikube start
    ```

2. Apply the Kubernetes configuration files:

    ```bash
    kubectl apply -f k8s/
    ```

3. Expose the services to access them outside the cluster.

---

## API Endpoints

### 1. Blog Submission API

- **Endpoint**: `/submit`
- **Method**: `POST`
- **Description**: Accepts blog submissions (title, text, and user ID), adds them to RabbitMQ for processing by the consumer.
- **Request Body**:

    ```json
    {
        "blog_title": "My First Blog",
        "blog_text": "This is the content of my first blog post.",
        "user_id": "1"
    }
    ```

- **Example `curl` command**:

    ```bash
    curl -X POST -H "Content-Type: application/json" \
    -d '{"blog_title":"Test Blog","blog_text":"This is a test blog post.","user_id":"1"}' \
    http://localhost:5000/submit
    ```

### 2. Blog Search API

- **Endpoint**: `/search`
- **Method**: `GET`
- **Description**: Searches for blog entries where the query matches either the title or text.
- **Query Parameter**: `query` (The search term)
- **Example `curl` command**:

    ```bash
    curl "http://localhost:5000/search?query=Test"
    ```

---

## Elasticsearch Mapping

The Elasticsearch index has the following fields with appropriate mappings to handle full-text search:

```json
{
  "mappings": {
    "properties": {
      "blog_title": {
        "type": "text"
      },
      "blog_text": {
        "type": "text"
      },
      "user_id": {
        "type": "keyword"
      }
    }
  }
}
```

---

## Testing

You can test the service using `curl` commands or any API testing tool (Postman, Insomnia, etc.). Example curl commands are given above for submission and search.

---

## Improvements & Additional Features

1. **Scalability**: The service can easily scale by adding more consumer services to handle increased blog submission traffic.
2. **Logging**: Implement centralized logging for better monitoring and debugging.
3. **Authentication**: Add user authentication for secure blog submissions.
4. **Pagination**: Implement pagination in the search API for better performance with large datasets.
5. **Rate Limiting**: Introduce rate-limiting to prevent abuse of the API.

---

## Conclusion

This project provides a fully functional, scalable, and containerized blogging platform that supports asynchronous blog submission, indexing, and full-text search. It can be deployed locally using Docker Compose or orchestrated using Kubernetes for a production-ready setup.
```

---

### Key Sections to Modify:
1. **Clone URL**: Change the clone URL to your actual repository URL.
2. **Future Improvements**: If you add more features or improvements, you can update that section to reflect the changes.

Let me know if you need any further modifications!
