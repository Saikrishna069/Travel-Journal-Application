# 🛠️ Operations & Maintenance Guide

## 1. Environment Variables Configuration

| Variable | Scope | Default Value | Description |
| :--- | :--- | :--- | :--- |
| `MONGO_URI` | Backend | `mongodb://mongo:27017` | MongoDB connection string |
| `DATABASE_NAME` | Backend | `travel_journal_db` | Main application database name |
| `SECRET_KEY` | Backend | Required | Secret key for JWT token signing |
| `OPENAI_API_KEY` | Backend | Optional | Key for AI Chat Assistant (falls back to built-in agent if omitted) |
| `VITE_API_URL` | Frontend | `http://localhost:8000` | Backend API base URL |

## 2. Database Backup & Restore

### Backup MongoDB Collections
```bash
docker exec -t travel_mongo mongodump --out /data/db/backup
```

### Restore MongoDB Collections
```bash
docker exec -t travel_mongo mongorestore /data/db/backup
```

## 3. Logs & Diagnostics

### View Real-time Container Logs
```bash
# View backend logs
docker logs -f travel_backend

# View frontend Nginx logs
docker logs -f travel_frontend

# View MongoDB logs
docker logs -f travel_mongo
```

## 4. Troubleshooting Checklist

- **CORS Error in Frontend:** Ensure `VITE_API_URL` matches the backend endpoint and `allow_origins` in `app/main.py` is configured correctly.
- **Database Connection Failed:** Verify `travel_mongo` container status using `docker ps`.
- **Image Upload Failures:** Ensure the `uploads/` directory has write permissions inside the backend container.
