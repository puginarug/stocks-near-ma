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
    getFilterSettings
} from './filters.js';

// Application state
let state = {
    allStocks: [],
    filteredStocks: []
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
    initThemeToggle();

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
        showLoading('Loading stock data from JSONBin.io...');

        const response = await fetchStocks();

        state.allStocks = response.stocks;
        state.filteredStocks = applyFilters(state.allStocks, getFilterSettings());

        updateUI();

        // Update last update time from metadata or use current time
        if (response.last_updated) {
            const lastUpdate = new Date(response.last_updated);
            document.getElementById('lastUpdate').textContent =
                `Last updated: ${lastUpdate.toLocaleString()}`;
        } else {
            const now = new Date();
            document.getElementById('lastUpdate').textContent =
                `Last updated: ${now.toLocaleString()}`;
        }

        // Show processing info if available
        if (response.processing_time) {
            console.log(`Data processed in ${response.processing_time}s via GitHub Actions`);
            showLoadingProgress(
                `Loaded ${response.total_count} stocks (processed in ${response.processing_time}s)`
            );
        }

    } catch (error) {
        console.error('Error loading data:', error);
        alert('Failed to load stock data from JSONBin.io. Please check your API configuration in api.js');
        hideLoading();
    }
}

/**
 * Update UI with current state
 */
function updateUI() {
    const filterSettings = getFilterSettings();

    // Apply filters
    state.filteredStocks = applyFilters(state.allStocks, filterSettings);

    // Render table
    renderTable(state.filteredStocks);

    // Update statistics (use all stocks for stats with current threshold)
    const stats = calculateStatistics(state.allStocks, filterSettings.threshold);
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
}

/**
 * Initialize theme toggle
 */
function initThemeToggle() {
    const themeToggle = document.getElementById('themeToggle');
    const body = document.body;

    // Check for saved theme preference or default to dark
    const savedTheme = localStorage.getItem('theme');
    if (savedTheme === 'dark' || !savedTheme) {
        body.classList.add('dark-theme');
        themeToggle.textContent = '☀️ Light Mode';
    } else {
        themeToggle.textContent = '🌙 Dark Mode';
    }

    // Toggle theme on click
    themeToggle.addEventListener('click', () => {
        body.classList.toggle('dark-theme');

        if (body.classList.contains('dark-theme')) {
            themeToggle.textContent = '☀️ Light Mode';
            localStorage.setItem('theme', 'dark');
        } else {
            themeToggle.textContent = '🌙 Dark Mode';
            localStorage.setItem('theme', 'light');
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
