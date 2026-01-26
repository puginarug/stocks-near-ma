/**
 * Main Application Logic - Coordinates all modules
 */

import { fetchStocks } from './api.js';
import { renderTable, initTableSorting } from './table.js';
import {
    applyFilters,
    calculateStatistics,
    updateStatisticsDisplay,
    initFilters,
    getFilterSettings,
    parseCustomTickers
} from './filters.js';

// Application state
let state = {
    allStocks: [],
    filteredStocks: [],
    customTickers: null
};

/**
 * Initialize the application
 */
async function init() {
    console.log('Initializing Stock MA Monitor...');

    // Initialize UI components
    initTableSorting();
    initFilters(handleFilterChange);
    initButtons();

    // Load initial data
    await loadData();

    // Hide loading overlay
    hideLoading();

    console.log('Application initialized successfully');
}

/**
 * Load stock data from API
 */
async function loadData() {
    try {
        showLoading('Loading stock data...');

        const response = await fetchStocks(state.customTickers);

        state.allStocks = response.stocks;
        state.filteredStocks = applyFilters(state.allStocks, getFilterSettings());

        updateUI();

        // Update last update time
        const now = new Date();
        document.getElementById('lastUpdate').textContent =
            `Last updated: ${now.toLocaleString()}`;

        // Show processing time if available
        if (response.processing_time) {
            console.log(`Data loaded in ${response.processing_time}s (Cache hit: ${response.cache_hit})`);
            showLoadingProgress(
                `Loaded ${response.total_count} stocks in ${response.processing_time}s ${response.cache_hit ? '(cached)' : '(parallel processing)'}`
            );
        }

    } catch (error) {
        console.error('Error loading data:', error);
        alert('Failed to load stock data. Please check if the backend server is running on http://localhost:8000');
        hideLoading();
    }
}

/**
 * Update UI with current state
 */
function updateUI() {
    // Apply filters
    state.filteredStocks = applyFilters(state.allStocks, getFilterSettings());

    // Render table
    renderTable(state.filteredStocks);

    // Update statistics (use all stocks for stats, not filtered)
    const stats = calculateStatistics(state.allStocks);
    updateStatisticsDisplay(stats);
}

/**
 * Handle filter changes
 * @param {Object} filters - New filter settings
 */
function handleFilterChange(filters) {
    console.log('Filters changed:', filters);
    updateUI();
}

/**
 * Initialize button event listeners
 */
function initButtons() {
    // Refresh button
    document.getElementById('refreshBtn').addEventListener('click', async () => {
        await loadData();
    });

    // Add custom tickers button
    document.getElementById('addTickersBtn').addEventListener('click', async () => {
        const input = document.getElementById('customTickers').value;
        const customTickers = parseCustomTickers(input);

        if (customTickers) {
            state.customTickers = customTickers;
            console.log('Adding custom tickers:', customTickers);
            await loadData();
        } else {
            alert('Please enter valid ticker symbols (comma-separated)');
        }
    });

    // Allow Enter key in custom tickers input
    document.getElementById('customTickers').addEventListener('keypress', async (e) => {
        if (e.key === 'Enter') {
            document.getElementById('addTickersBtn').click();
        }
    });
}

/**
 * Show loading overlay
 * @param {string} message - Loading message
 */
function showLoading(message = 'Loading...') {
    const overlay = document.getElementById('loadingOverlay');
    overlay.classList.remove('hidden');
    showLoadingProgress(message);
}

/**
 * Hide loading overlay
 */
function hideLoading() {
    const overlay = document.getElementById('loadingOverlay');
    overlay.classList.add('hidden');
}

/**
 * Update loading progress message
 * @param {string} message - Progress message
 */
function showLoadingProgress(message) {
    const progressEl = document.getElementById('loadingProgress');
    if (progressEl) {
        progressEl.textContent = message;
    }
}

/**
 * Handle sort changes from table
 */
document.addEventListener('sortChanged', () => {
    updateUI();
});

// Initialize app when DOM is loaded
if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
} else {
    init();
}
