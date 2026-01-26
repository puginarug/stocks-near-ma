/**
 * API Client for Stock MA Monitor
 * Handles all communication with the backend API
 */

const API_BASE = 'http://localhost:8000/api';

/**
 * Fetch wrapper with error handling and retry logic
 */
async function fetchWithRetry(url, options = {}, retries = 3) {
    for (let i = 0; i < retries; i++) {
        try {
            const response = await fetch(url, options);

            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }

            return await response.json();
        } catch (error) {
            console.error(`Fetch attempt ${i + 1} failed:`, error);

            if (i === retries - 1) {
                throw error;
            }

            // Wait before retrying (exponential backoff)
            await new Promise(resolve => setTimeout(resolve, 1000 * Math.pow(2, i)));
        }
    }
}

/**
 * Fetch all stocks with optional custom tickers
 * @param {string|null} customTickers - Comma-separated custom tickers
 * @returns {Promise<Object>} Stock response data
 */
export async function fetchStocks(customTickers = null) {
    let url = `${API_BASE}/stocks`;

    if (customTickers) {
        url += `?include_custom=${encodeURIComponent(customTickers)}`;
    }

    return await fetchWithRetry(url);
}

/**
 * Fetch S&P 500 ticker list
 * @returns {Promise<Object>} Tickers response
 */
export async function fetchTickers() {
    return await fetchWithRetry(`${API_BASE}/sp500-tickers`);
}

/**
 * Fetch statistics for stocks
 * @param {string|null} tickers - Comma-separated tickers to analyze
 * @returns {Promise<Object>} Statistics response
 */
export async function fetchStatistics(tickers = null) {
    let url = `${API_BASE}/statistics`;

    if (tickers) {
        url += `?tickers=${encodeURIComponent(tickers)}`;
    }

    return await fetchWithRetry(url);
}

/**
 * Health check endpoint
 * @returns {Promise<Object>} Health status
 */
export async function checkHealth() {
    return await fetchWithRetry(`${API_BASE}/health`);
}

/**
 * Clear backend cache
 * @returns {Promise<Object>} Response message
 */
export async function clearCache() {
    return await fetchWithRetry(`${API_BASE}/cache/clear`, {
        method: 'POST'
    });
}
