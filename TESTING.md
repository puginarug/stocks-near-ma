# Testing Guide - New Features

## What I Fixed

### 1. **Slider Now Works with Dynamic Threshold** ✅
- **How it works**: The JSONBin stores raw `distance_abs` values for each stock
- The slider filters and highlights stocks CLIENT-SIDE based on the threshold you choose
- No need to update JSONBin - the filtering happens in your browser!

**What changed:**
- Updated `table.js` to use dynamic threshold for row highlighting
- Updated `app.js` to pass threshold to table rendering
- The 🔔 indicator now updates based on slider position

### 2. **Dark Theme Improvements** ✅
- Added console logging to debug theme loading
- Added smooth transition when switching themes
- Theme preference saved in browser localStorage

## How to Test

### Test the Slider

1. **Open** [frontend/index.html](frontend/index.html) in your browser
2. **Refresh** the page (Ctrl+F5 or Cmd+Shift+R to clear cache)
3. **Look at** the slider - it should show "Near MA Threshold: ±5%"
4. **Move the slider** left (to 1%) or right (to 15%)
5. **Watch for changes:**
   - The number next to the slider should update in real-time
   - The "Near MA" stat card should update its count
   - Table rows with yellow highlighting should change based on threshold
   - The 🔔 indicator should appear/disappear based on threshold

**Example:**
- Slider at 1%: Only stocks within ±1% of MA get highlighted (fewer yellow rows)
- Slider at 15%: Stocks within ±15% of MA get highlighted (more yellow rows)

### Test Dark Theme

1. **Open** [frontend/index.html](frontend/index.html) in your browser
2. **Open browser console** (F12) to see theme logs
3. **Check initial state:**
   - Page should load with **dark theme** by default
   - Background should be dark (#1a1b1e)
   - Text should be light (#e9ecef)
   - Button in header should say "☀️ Light Mode"
4. **Click the theme toggle button** (top-right)
5. **Watch for:**
   - Smooth color transition (0.3s)
   - Background changes to light (#f5f5f5)
   - Text changes to dark (#212121)
   - Button text changes to "🌙 Dark Mode"
   - Console logs the theme change
6. **Refresh the page** - theme should persist (saved in localStorage)

### Expected Console Output

When you open the page, you should see:
```
Initializing Stock MA Monitor...
Saved theme: dark (or null on first load)
Applied dark theme
Loading stock data from JSONBin.io...
Data processed in 50.54s via GitHub Actions
Application initialized successfully
```

When you click the theme toggle:
```
Switched to light theme
```

## Troubleshooting

### Slider Not Updating

**Problem:** Slider moves but nothing changes
**Solution:**
1. Hard refresh (Ctrl+F5 or Cmd+Shift+R)
2. Clear browser cache
3. Check console for errors (F12)

### Dark Theme Not Showing

**Problem:** Page is still light-colored
**Solutions:**

1. **Check localStorage:**
   - Open console (F12)
   - Type: `localStorage.getItem('theme')`
   - If it says "light", reset it: `localStorage.setItem('theme', 'dark')`
   - Refresh page

2. **Check CSS loaded:**
   - Open DevTools (F12) → Elements tab
   - Click on `<body>` element
   - Check if it has class `dark-theme`
   - Look at Computed styles - background should be #1a1b1e

3. **Clear cache:**
   - Hard refresh with Ctrl+F5 (Windows) or Cmd+Shift+R (Mac)
   - Or clear all browser cache for localhost

4. **Check console logs:**
   - Should see "Applied dark theme" or "Applied light theme"
   - Should see "Saved theme: dark" or "Saved theme: null"

### Still Not Working?

**Check browser support:**
- Modern browsers (Chrome, Firefox, Safari, Edge) all support CSS custom properties
- If using Internet Explorer, upgrade to a modern browser

**Force dark theme manually:**
- Open console (F12)
- Type: `document.body.classList.add('dark-theme')`
- If this works, the issue is with the JavaScript initialization

## What the Slider Actually Does

The slider controls THREE things:

1. **Statistics Card** - "Near MA (±X%)" count updates
2. **Filter** - When "Show only stocks near MA" is checked, uses slider value
3. **Table Highlighting** - Yellow background and 🔔 indicator based on slider value

**Technical Details:**
- Slider range: 1% to 15% (step: 0.5%)
- Default: 5%
- Updates happen in real-time (no need to click a button)
- Uses `distance_abs` field from JSONBin data
- Client-side filtering (very fast, no API calls)

## Current Data in JSONBin

Your JSONBin now has:
- **524 stocks** (all S&P 500 + ETFs)
- **Near MA at 5%**: 179 stocks
- **Above MA**: 350 stocks
- **Below MA**: 174 stocks
- **Last updated**: 2026-01-27 17:03:27 UTC
- **Processing time**: 50.54 seconds

## Next Steps

If everything works:
1. Commit these changes to git
2. Push to GitHub
3. GitHub Actions will keep the data updated every 4 hours
4. Deploy to GitHub Pages (see [DEPLOYMENT.md](DEPLOYMENT.md))

If something doesn't work:
1. Check the console logs (F12)
2. Verify all files were saved and refreshed
3. Try in a different browser
4. Let me know what specific error you're seeing!
