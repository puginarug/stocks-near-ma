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

    // Apply search filter
    if (filters.search) {
        filtered = searchStocks(filtered, filters.search);
    }

    // Apply near MA filter
    if (filters.nearMA) {
        filtered = filterNearMA(filtered, filters.threshold || 5);
    }

    // Apply direction filter
    if (filters.direction !== 'All') {
        filtered = filterDirection(filtered, filters.direction);
    }

    return filtered;
}

/**
 * Filter stocks that are near MA based on threshold
 * @param {Array} stocks - Array of stock data
 * @param {number} threshold - Percentage threshold (default 5)
 * @returns {Array} Filtered stocks
 */
export function filterNearMA(stocks, threshold = 5) {
    return stocks.filter(stock => stock.distance_abs <= threshold);
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
 * Search stocks by symbol
 * @param {Array} stocks - Array of stock data
 * @param {string} query - Search query
 * @returns {Array} Filtered stocks matching the search
 */
export function searchStocks(stocks, query) {
    if (!query || !query.trim()) {
        return stocks;
    }

    const searchTerm = query.trim().toUpperCase();
    return stocks.filter(stock =>
        stock.symbol.toUpperCase().includes(searchTerm)
    );
}

/**
 * Calculate statistics from stock data
 * @param {Array} stocks - Array of stock data
 * @param {number} threshold - MA threshold percentage
 * @returns {Object} Statistics object
 */
export function calculateStatistics(stocks, threshold = 5) {
    return {
        total: stocks.length,
        nearMA: stocks.filter(s => s.distance_abs <= threshold).length,
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
    const searchInput = document.getElementById('searchStock');
    const clearSearchBtn = document.getElementById('clearSearchBtn');
    const thresholdSlider = document.getElementById('maThreshold');
    const thresholdValueSpan = document.getElementById('thresholdValue');
    const statThresholdValueSpan = document.getElementById('statThresholdValue');

    // Threshold slider
    thresholdSlider.addEventListener('input', () => {
        const value = thresholdSlider.value;
        thresholdValueSpan.textContent = value;
        statThresholdValueSpan.textContent = value;
        onFilterChange(getFilterSettings());
    });

    nearMAFilter.addEventListener('change', () => {
        onFilterChange(getFilterSettings());
    });

    directionFilter.addEventListener('change', () => {
        onFilterChange(getFilterSettings());
    });

    // Search input with debouncing for better performance
    let searchTimeout;
    searchInput.addEventListener('input', () => {
        clearTimeout(searchTimeout);
        searchTimeout = setTimeout(() => {
            onFilterChange(getFilterSettings());
        }, 300); // 300ms debounce
    });

    // Clear search button
    clearSearchBtn.addEventListener('click', () => {
        searchInput.value = '';
        onFilterChange(getFilterSettings());
    });

    // Allow Enter key to trigger search immediately
    searchInput.addEventListener('keypress', (e) => {
        if (e.key === 'Enter') {
            clearTimeout(searchTimeout);
            onFilterChange(getFilterSettings());
        }
    });
}

/**
 * Get current filter settings
 * @returns {Object} Current filter settings
 */
export function getFilterSettings() {
    const searchInput = document.getElementById('searchStock');
    const thresholdSlider = document.getElementById('maThreshold');
    return {
        search: searchInput ? searchInput.value : '',
        nearMA: document.getElementById('nearMAFilter').checked,
        direction: document.getElementById('directionFilter').value,
        threshold: parseFloat(thresholdSlider.value) || 5
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
