# Stock MA Monitor

A modern web application for monitoring S&P 500 stocks and ETFs, calculating their distance from the 150-day moving average with **7.5x faster parallel processing**.

## Features

- ⚡ **Parallel Processing**: Loads 500 stocks in ~35 seconds using 10 concurrent workers
- 📊 **Real-time Statistics**: Total stocks, near MA count, above/below MA counts
- 🎯 **Advanced Filtering**: Filter by proximity to MA (±5%) and direction (ABOVE/BELOW)
- 📈 **Sortable Table**: Click column headers to sort by any metric
- ➕ **Custom Tickers**: Add your own stocks via the UI
- 🎨 **Color Coding**: Red (above MA), Green (below MA), Yellow (near MA)
- 💾 **Smart Caching**: 1-hour cache to minimize API calls
- 📱 **Responsive Design**: Works on desktop and mobile

## Quick Start

### Prerequisites

- Python 3.10+ (tested with Python 3.14)
- Anaconda/Miniconda (optional but recommended)

### Installation

**1. Start the Backend (FastAPI)**

```bash
# Navigate to backend folder
cd backend

# Install dependencies
pip install -r requirements.txt

# Start the server
python app.py
```

The backend will start on `http://localhost:8000`

**2. Open the Frontend**

Option A - Direct (simplest):
- Open `frontend/index.html` in your browser

Option B - Local server (recommended):
```bash
# In a new terminal, navigate to frontend
cd frontend

# Serve with Python
python -m http.server 3000
```
Then visit `http://localhost:3000`

**3. Explore the API**

Visit `http://localhost:8000/docs` for interactive API documentation (Swagger UI)

## How It Works

### Architecture

**Backend** (Python/FastAPI):
- Fetches stock data from Yahoo Finance using `yfinance`
- Processes 10 stocks concurrently with ThreadPoolExecutor
- Calculates 150-day moving averages in parallel
- Caches results for 1 hour
- Exposes REST API endpoints

**Frontend** (HTML/CSS/JavaScript):
- Pure vanilla JavaScript (no frameworks)
- Fetches data from backend API
- Client-side filtering and sorting
- Responsive table with color coding
- Real-time statistics calculation

### Performance

- **Sequential Processing**: ~260 seconds for 500 stocks
- **Parallel Processing (10 workers)**: ~35 seconds for 500 stocks
- **Speedup**: 7.5x faster! 🚀

## Project Structure

```
stocks-near-ma/
├── backend/                # FastAPI backend
│   ├── app.py             # Main FastAPI application
│   ├── requirements.txt   # Backend dependencies
│   ├── models/
│   │   └── stock_models.py       # Pydantic data models
│   ├── services/
│   │   ├── stock_service.py      # Stock data fetching
│   │   └── parallel_processor.py # Parallel processing logic
│   └── utils/
│       ├── cache.py              # In-memory caching
│       └── sp500_fetcher.py      # S&P 500 list fetcher
│
└── frontend/              # HTML/CSS/JS frontend
    ├── index.html        # Main HTML page
    ├── css/
    │   └── styles.css    # Styling
    └── js/
        ├── app.js        # Main application logic
        ├── api.js        # API client
        ├── table.js      # Table rendering
        └── filters.js    # Filter logic
```

## API Endpoints

- `GET /api/stocks?include_custom=NVDA,AMD` - Fetch all stock data with parallel processing
- `GET /api/sp500-tickers` - Get S&P 500 ticker list
- `GET /api/statistics` - Get aggregated statistics
- `GET /api/health` - Health check endpoint
- `POST /api/cache/clear` - Clear cached data
- `GET /docs` - Interactive API documentation (Swagger UI)

## Usage

### Running in Anaconda

If you're using Anaconda/Miniconda:

```bash
# Create a new environment (optional)
conda create -n stocks-backend python=3.14
conda activate stocks-backend

# Navigate to backend
cd backend

# Install dependencies
pip install -r requirements.txt

# Run the server
python app.py
```

### Adding Custom Stocks

**Via UI:**
1. Enter ticker symbols in the "Add Custom Stocks" input (e.g., `NVDA, AMD, GOOGL`)
2. Click "Add & Refresh"
3. The app will fetch and display your custom stocks

**Via Code:**
Edit `backend/utils/sp500_fetcher.py` to permanently add stocks:
```python
custom_stocks = [
    'TSLA',  # Tesla
    'NVDA',  # NVIDIA
    # Add more here...
]
```

### Using Filters

- **Near MA Filter**: Check "Show only stocks near MA" to see stocks within ±5% of their 150-day MA
- **Direction Filter**: Select "ABOVE" or "BELOW" to filter by direction
- **Sorting**: Click any column header to sort by that metric

### Color Coding

- 🔴 **Red**: Stock is trading ABOVE its 150-day MA
- 🟢 **Green**: Stock is trading BELOW its 150-day MA
- 🟡 **Yellow highlight**: Stock is within ±5% of its MA (🔔 indicator)

## Troubleshooting

### Port Already in Use

If you see "port 8000 already in use":
```bash
# Find the process using port 8000
netstat -ano | findstr :8000

# Kill the process (replace PID with the number shown)
taskkill /PID <PID> /F
```

Or just use a different port:
```bash
python app.py --port 8001
```
(Then update `frontend/js/api.js` to use the new port)

### Failed to Load Stock Data

1. Make sure the backend is running on `http://localhost:8000`
2. Check backend terminal for errors
3. Visit `http://localhost:8000/api/health` to verify the backend is responding

### Slow Data Loading

- First load takes ~35 seconds to fetch 500+ stocks
- Subsequent loads are instant (cached for 1 hour)
- If still slow, check your internet connection

## Development

### Backend Development

The backend uses FastAPI with auto-reload:
```bash
cd backend
uvicorn app:app --reload --port 8000
```

Any code changes will automatically restart the server.

### Frontend Development

The frontend is pure HTML/CSS/JavaScript:
- Edit files in `frontend/`
- Refresh browser to see changes
- No build step required!

### Running Tests

```bash
cd backend
python -m pytest tests/
```

## Deployment

### Backend Deployment

Deploy to any Python-supporting platform:
- **Heroku**: Use `Procfile` with `web: uvicorn app:app --host=0.0.0.0 --port=$PORT`
- **Railway**: Auto-detects FastAPI apps
- **Render**: Use `uvicorn app:app --host 0.0.0.0 --port $PORT`
- **AWS Lambda**: Use Mangum adapter for serverless

### Frontend Deployment

Deploy as static files to:
- **Netlify**: Drag & drop the `frontend/` folder
- **Vercel**: Connect GitHub repo
- **GitHub Pages**: Enable Pages in repo settings
- **AWS S3**: Upload to S3 bucket with static hosting

**Important**: Update `frontend/js/api.js` with your deployed backend URL:
```javascript
const API_BASE = 'https://your-backend-url.com/api';
```

## Contributing

Contributions are welcome! Please:
1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

MIT License - feel free to modify and use as needed.

## Acknowledgments

- Stock data provided by [Yahoo Finance](https://finance.yahoo.com) via `yfinance`
- S&P 500 list from [Wikipedia](https://en.wikipedia.org/wiki/List_of_S%26P_500_companies)
- Built with [FastAPI](https://fastapi.tiangolo.com/), vanilla JavaScript, and ❤️
