/**
 * Filters Module - Handles client-side filtering of stock data
 */

/**
 * Apply all filters to stock data
 * @param {Array} stocks - Array of stock data
 * @param {Object} filters - Filter settings
 * @returns {Array} Filtered stock data
 */
export function applyFilters(stocks, filters) {
    let filtered = [...stocks];

    // Apply near MA filter
    if (filters.nearMA) {
        filtered = filterNearMA(filtered);
    }

    // Apply direction filter
    if (filters.direction !== 'All') {
        filtered = filterDirection(filtered, filters.direction);
    }

    return filtered;
}

/**
 * Filter stocks that are near MA (±5%)
 * @param {Array} stocks - Array of stock data
 * @returns {Array} Filtered stocks
 */
export function filterNearMA(stocks) {
    return stocks.filter(stock => stock.near_ma === true);
}

/**
 * Filter stocks by direction (ABOVE or BELOW)
 * @param {Array} stocks - Array of stock data
 * @param {string} direction - Direction to filter by
 * @returns {Array} Filtered stocks
 */
export function filterDirection(stocks, direction) {
    if (direction === 'All') {
        return stocks;
    }
    return stocks.filter(stock => stock.direction === direction);
}

/**
 * Calculate statistics from stock data
 * @param {Array} stocks - Array of stock data
 * @returns {Object} Statistics object
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
 * Update statistics display
 * @param {Object} stats - Statistics object
 */
export function updateStatisticsDisplay(stats) {
    document.getElementById('totalCount').textContent = stats.total;
    document.getElementById('nearMACount').textContent = stats.nearMA;
    document.getElementById('aboveCount').textContent = stats.above;
    document.getElementById('belowCount').textContent = stats.below;
}

/**
 * Initialize filter event listeners
 * @param {Function} onFilterChange - Callback when filters change
 */
export function initFilters(onFilterChange) {
    const nearMAFilter = document.getElementById('nearMAFilter');
    const directionFilter = document.getElementById('directionFilter');

    nearMAFilter.addEventListener('change', () => {
        onFilterChange({
            nearMA: nearMAFilter.checked,
            direction: directionFilter.value
        });
    });

    directionFilter.addEventListener('change', () => {
        onFilterChange({
            nearMA: nearMAFilter.checked,
            direction: directionFilter.value
        });
    });
}

/**
 * Get current filter settings
 * @returns {Object} Current filter settings
 */
export function getFilterSettings() {
    return {
        nearMA: document.getElementById('nearMAFilter').checked,
        direction: document.getElementById('directionFilter').value
    };
}

/**
 * Parse custom tickers from input
 * @param {string} input - Comma-separated ticker input
 * @returns {string} Cleaned ticker string
 */
export function parseCustomTickers(input) {
    if (!input || !input.trim()) {
        return null;
    }

    const tickers = input
        .split(',')
        .map(t => t.trim().toUpperCase())
        .filter(t => t.length > 0);

    return tickers.length > 0 ? tickers.join(',') : null;
}
