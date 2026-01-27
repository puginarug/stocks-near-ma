/**
 * API Client for Stock MA Monitor
 * Fetches data from JSONBin.io (serverless architecture)
 */

// CONFIGURATION: Update these values after creating your JSONBin
const JSONBIN_BIN_ID = '6978c370ae596e708ffa6f81'; // Replace with your JSONBin ID
const JSONBIN_API_KEY = '$2a$10$PlFK/m9fo0ESQct8jIhgP.I9X7Mnn.oVH2Vo41AZA3lW34897bl6y'; // Replace with your JSONBin API key (optional for read-only)

const JSONBIN_URL = `https://api.jsonbin.io/v3/b/${JSONBIN_BIN_ID}/latest`;

/**
 * Fetch stock data from JSONBin.io
 * @returns {Promise<Object>} Stock data with metadata
 */
export async function fetchStocks() {
    try {
        const response = await fetch(JSONBIN_URL, {
            method: 'GET',
            headers: {
                'X-Master-Key': JSONBIN_API_KEY
            }
        });

        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }

        const result = await response.json();

        // JSONBin.io returns data in a 'record' property
        return {
            stocks: result.record.stocks || [],
            metadata: result.record.metadata || {},
            total_count: result.record.metadata?.total_count || 0,
            processing_time: result.record.metadata?.processing_time || 0,
            last_updated: result.record.metadata?.last_updated || null,
            cache_hit: true // Always from cache in this architecture
        };
    } catch (error) {
        console.error('Error fetching stock data:', error);
        throw error;
    }
}

/**
 * Get statistics from the fetched data
 * @param {Array} stocks - Array of stock data
 * @returns {Object} Statistics
 */
export function calculateStatistics(stocks) {
    return {
        total: stocks.length,
        nearMA: stocks.filter(s => s.near_ma).length,
        above: stocks.filter(s => s.direction === 'ABOVE').length,
        below: stocks.filter(s => s.direction === 'BELOW').length
    };
}

/**
 * Health check (for local testing)
 * @returns {Promise<Object>} Health status
 */
export async function checkHealth() {
    try {
        const response = await fetch(JSONBIN_URL, {
            method: 'HEAD',
            headers: {
                'X-Master-Key': JSONBIN_API_KEY
            }
        });
        return {
            status: response.ok ? 'ok' : 'error',
            message: response.ok ? 'JSONBin.io is accessible' : 'Cannot reach JSONBin.io'
        };
    } catch (error) {
        return {
            status: 'error',
            message: error.message
        };
    }
}
