/**
 * Table Module - Handles rendering and sorting of stock data table
 */

let currentSortColumn = 'distance_abs';
let currentSortDirection = 'asc';

/**
 * Render stock data table
 * @param {Array} stocks - Array of stock data objects
 * @param {number} threshold - Current MA threshold for highlighting
 */
export function renderTable(stocks, threshold = 5) {
    const tableBody = document.getElementById('tableBody');

    if (!stocks || stocks.length === 0) {
        tableBody.innerHTML = '<tr><td colspan="6" style="text-align: center;">No data available</td></tr>';
        return;
    }

    // Sort stocks
    const sortedStocks = sortStocks(stocks, currentSortColumn, currentSortDirection);

    // Use DocumentFragment for efficient DOM updates
    const fragment = document.createDocumentFragment();

    sortedStocks.forEach(stock => {
        const row = createTableRow(stock, threshold);
        fragment.appendChild(row);
    });

    tableBody.innerHTML = '';
    tableBody.appendChild(fragment);

    // Update displayed count
    document.getElementById('displayedCount').textContent = `Showing ${stocks.length} stocks`;
}

/**
 * Create a table row for a stock
 * @param {Object} stock - Stock data object
 * @param {number} threshold - Current MA threshold for highlighting
 * @returns {HTMLElement} Table row element
 */
function createTableRow(stock, threshold = 5) {
    const row = document.createElement('tr');

    // Highlight row if near MA (using dynamic threshold)
    const isNearMA = stock.distance_abs <= threshold;
    if (isNearMA) {
        row.classList.add('near-ma-highlight');
    }

    // Symbol
    const symbolCell = document.createElement('td');
    symbolCell.textContent = stock.symbol;
    row.appendChild(symbolCell);

    // Price
    const priceCell = document.createElement('td');
    priceCell.textContent = `$${stock.price.toFixed(2)}`;
    row.appendChild(priceCell);

    // 150-Day MA
    const maCell = document.createElement('td');
    maCell.textContent = `$${stock.ma_150.toFixed(2)}`;
    row.appendChild(maCell);

    // Distance (%)
    const distanceCell = document.createElement('td');
    distanceCell.textContent = `${stock.distance_percent > 0 ? '+' : ''}${stock.distance_percent.toFixed(2)}%`;
    row.appendChild(distanceCell);

    // Direction (with color coding)
    const directionCell = document.createElement('td');
    directionCell.textContent = stock.direction;
    directionCell.classList.add(
        stock.direction === 'ABOVE' ? 'direction-above' : 'direction-below'
    );
    row.appendChild(directionCell);

    // Near MA indicator (using dynamic threshold)
    const nearMACell = document.createElement('td');
    nearMACell.textContent = isNearMA ? '🔔' : '';
    row.appendChild(nearMACell);

    return row;
}

/**
 * Sort stocks by column
 * @param {Array} stocks - Array of stock data
 * @param {string} column - Column to sort by
 * @param {string} direction - Sort direction ('asc' or 'desc')
 * @returns {Array} Sorted stocks
 */
function sortStocks(stocks, column, direction) {
    const sorted = [...stocks].sort((a, b) => {
        let aVal = a[column];
        let bVal = b[column];

        // Handle boolean values
        if (typeof aVal === 'boolean') {
            aVal = aVal ? 1 : 0;
            bVal = bVal ? 1 : 0;
        }

        // Handle string values
        if (typeof aVal === 'string') {
            return direction === 'asc'
                ? aVal.localeCompare(bVal)
                : bVal.localeCompare(aVal);
        }

        // Handle numeric values
        return direction === 'asc' ? aVal - bVal : bVal - aVal;
    });

    return sorted;
}

/**
 * Initialize table sorting
 */
export function initTableSorting() {
    const headers = document.querySelectorAll('.stock-table th[data-sort]');

    headers.forEach(header => {
        header.addEventListener('click', () => {
            const column = header.dataset.sort;

            // Toggle direction if same column, otherwise default to asc
            if (column === currentSortColumn) {
                currentSortDirection = currentSortDirection === 'asc' ? 'desc' : 'asc';
            } else {
                currentSortColumn = column;
                currentSortDirection = 'asc';
            }

            // Update header indicators
            updateSortIndicators(column, currentSortDirection);

            // Trigger table re-render (will be called from app.js)
            const event = new CustomEvent('sortChanged', {
                detail: { column, direction: currentSortDirection }
            });
            document.dispatchEvent(event);
        });
    });
}

/**
 * Update sort direction indicators in table headers
 * @param {string} column - Active sort column
 * @param {string} direction - Sort direction
 */
function updateSortIndicators(column, direction) {
    const headers = document.querySelectorAll('.stock-table th[data-sort]');

    headers.forEach(header => {
        const headerColumn = header.dataset.sort;
        const text = header.textContent.replace(/[▲▼]/g, '').trim();

        if (headerColumn === column) {
            header.textContent = `${text} ${direction === 'asc' ? '▲' : '▼'}`;
        } else {
            header.textContent = text;
        }
    });
}

/**
 * Get current sort settings
 * @returns {Object} Current sort column and direction
 */
export function getSortSettings() {
    return {
        column: currentSortColumn,
        direction: currentSortDirection
    };
}
