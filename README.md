<img width="1536" height="1024" alt="ChatGPT Image Jul 27, 2026, 03_20_02 PM" src="https://github.com/user-attachments/assets/bec0b5ef-9a28-4d92-a31b-0e9586ecb548" />

<img width="1536" height="1024" alt="ChatGPT Image Jul 28, 2026, 06_14_07 AM" src="https://github.com/user-attachments/assets/39b10b80-36eb-4dbf-b29d-e0b8a90ff11e" />

<img width="1579" height="996" alt="ChatGPT Image Jul 27, 2026, 12_45_16 PM" src="https://github.com/user-attachments/assets/df70ff0a-b9b0-4951-ac33-6ebc5635a80f" />

<img width="1892" height="960" alt="chat_bot_metrics_dashboard_UI" src="https://github.com/user-attachments/assets/d957a1eb-def2-4408-8105-85370ae3c343" />

<img width="1877" height="918" alt="image-1" src="https://github.com/user-attachments/assets/664ab3f1-c0ee-4668-8504-37b57aece747" />


Based on above architecture diagrams, the request flow for the chatbot application is as follows:

**Request Flow**
**1. User accesses the Dashboard**
The User/Browser sends an HTTP request to the Flask Dashboard Application.
Port: 3000
The dashboard UI is displayed to the user.

**Flow:**

User/Browser
      │
HTTP :3000
      ▼
Flask Dashboard (Port 3000)

**2. User submits a chatbot question**
The user enters a question in the dashboard.
The Dashboard sends the request to the Chatbot Flask Application.

API Call

HTTP Port: 5000

**Flow:**
Flask Dashboard
      │
HTTP :5000
(Get Chat API)
      ▼
Flask Chatbot Service

3. Chatbot processes the request

After receiving the request, the chatbot performs several internal operations.

**3.1 Intent Classification**
Determines what the user is asking.
Identifies the application (THA, TKA, Shoulder, etc.).
Chooses the appropriate processing logic.

Chatbot
   │
   ▼
Intent Classifier

**3.2 Document Q&A / Smart Chat**
Handles conversational logic.
Maintains chat history.
Performs logging.
Chatbot
  │
   ▼
Document Q&A
Smart Chat
Logging

**4. Retrieve vector embeddings (RAG Search)**

If the question requires semantic search:

Chatbot queries ChromaDB.
Uses HTTP Port 8000.

Chatbot
      │
HTTP :8000
(Vector Search)
      ▼
ChromaDB

**ChromaDB:**

Searches embeddings.
Returns the most relevant documents.

**5. Query MySQL Database**

If structured dashboard metrics are required:

The chatbot queries the MySQL database.

TCP Port: 3306

**Examples:**

Coverage
Unit Tests
ASAN
Defort Metrics
Peer Reviews

Chatbot
      │
TCP :3306
      ▼
MySQL Database

**6. Call Ollama LLM**

After retrieving context from ChromaDB and MySQL:

The chatbot sends the prompt to the Ollama LLM.

Remote Port: 11434

Chatbot
      │
HTTP :11434
      ▼
Ollama LLM

**The LLM:**

Reads the prompt.
Uses retrieved context.
Generates the final answer.

**7. Chatbot prepares the response**

The chatbot combines:

User Question
Database Results
ChromaDB Context
LLM Response

It formats the final response.

**8. Response returned to Dashboard**

The chatbot sends the generated response back to the Dashboard.

Chatbot
      │
HTTP :5000
      ▼
Dashboard

**9. Dashboard displays the response**

The Dashboard renders the answer in the chat window.

Dashboard
      │
HTTP :3000
      ▼
User/Browser

**Overall End-to-End Request Flow**
1. User → Flask Dashboard (Port 3000)

2. Dashboard → Chatbot API (HTTP 5000)

3. Chatbot
      ├── Intent Classification
      ├── Document Q&A / Smart Chat
      ├── Query MySQL (TCP 3306)
      ├── Query ChromaDB (HTTP 8000)
      └── Call Ollama LLM (HTTP 11434)

4. Ollama generates the response.

5. Chatbot formats the final response.

6. Chatbot → Dashboard

7. Dashboard → User
