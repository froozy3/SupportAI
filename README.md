
# SupportAI — Quick Start
![image](https://github.com/user-attachments/assets/e97b6577-bf25-430d-8923-2c877f631f57)



## 0. Create `.env` file

Create a `.env` file in the project root with your environment variables, for example:

```env
COHERE_API_KEY=your_cohere_api_key_here
DATABASE_URL=postgresql+asyncpg://postgres:postgres@db:5432/postgres
```


## 1. Clone repository

```bash
git clone https://github.com/froozy3/SupportAI.git
Then open the SupportAI folder in your IDE (VSCode, PyCharm, etc.)
```

## 2. Building and launching containers

```bash
docker-compose build
docker-compose up -d
```

## 3. Applying Database Migrations

```bash
docker exec -it supportai-backend-1 sh
cd /backend
alembic upgrade head
exit
```

## 4. Check if it’s working

- Backend is available at: [http://localhost:8000](http://localhost:8000)
- Frontend is available at: [http://localhost:3000](http://localhost:3000)
- *FAQ Context Data*

The application uses a predefined set of FAQ answers stored in the `FAQ_DATA` variable.  
Only the following answers are included in the context for AI retrieval:

| Question                                        | Answer                                         |
|------------------------------------------------|-----------------------------------------------|
| How can I get a refund?                         | To get a refund, submit a request within 14 days. |
| What are your working hours?                    | We work from 9 AM to 6 PM on weekdays.         |
| How can I change my password?                   | You can change your password via 'Forgot Password?'. |
| How long does delivery take?                    | Delivery takes 3 to 5 business days.           |
| How can I contact support?                      | Support is available by phone and chat.        |
| How long does registration take?                | Registration takes no more than 2 minutes.     |
| How can I recover my account?                   | To recover your account, use your email or phone number. |

This means the AI will only answer questions related to these specific FAQ entries. You can combined asks.


  
## 5. Running Tests

### Backend Tests

To run backend tests, execute:

```bash
docker exec -it supportai-backend-1 sh
cd /backend
pytest





### Important Tips

- After changing models or migrations, always run step 3 (`alembic upgrade head`).
- When rebuilding containers, make sure to repeat steps 2 and 3.


