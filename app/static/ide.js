// In-browser IDE for Python Labs
// Uses Pyodide for Python execution in browser

let pyodide = null;
let loadingPyodide = false;

async function loadPyodide() {
    if (pyodide || loadingPyodide) return;
    loadingPyodide = true;
    const status = document.getElementById('exec-status');
    if (status) status.textContent = 'Loading Python environment...';
    
    // Load Pyodide from CDN
    const script = document.createElement('script');
    script.src = 'https://cdn.jsdelivr.net/pyodide/v0.24.1/full/pyodide.js';
    script.onload = async () => {
        pyodide = await loadPyodide();
        window.pyodide = pyodide;
        await pyodide.loadPackage(['numpy', 'pandas', 'scikit-learn', 'matplotlib']);
        loadingPyodide = false;
        if (status) status.textContent = 'Python ready!';
    };
    script.onerror = () => {
        loadingPyodide = false;
        if (status) status.textContent = 'Failed to load Python';
    };
    document.head.appendChild(script);
}

async function executePython(code, outputEl) {
    if (!pyodide) {
        await loadPyodide();
    }
    try {
        // Capture output
        pyodide.runPython(`
import sys
from io import StringIO
sys.stdout = StringIO()
sys.stderr = StringIO()
`);
        
        await pyodide.runPythonAsync(code);
        
        const stdout = pyodide.runPython('sys.stdout.getvalue()');
        const stderr = pyodide.runPython('sys.stderr.getvalue()');
        
        if (outputEl) {
            outputEl.innerHTML = '<pre class="text-green-400">' + escapeHtml(stdout) + '</pre>';
            if (stderr) {
                outputEl.innerHTML += '<pre class="text-red-400">' + escapeHtml(stderr) + '</pre>';
            }
        }
        return { success: true, output: stdout, error: stderr };
    } catch (err) {
        if (outputEl) {
            outputEl.innerHTML = '<pre class="text-red-400">' + escapeHtml(err.message) + '</pre>';
        }
        return { success: false, error: err.message };
    }
}

// Mock Rust execution - simulate since can't run native Rust in browser
async function executeRust(code, outputEl) {
    // Simulate compilation
    try {
        const lines = code.split('\n');
        let output = '';
        
        for (const line of lines) {
            // Detect println! macros
            const match = line.match(/println!\s*\(.*?"([^"]*)"\s*\)/);
            if (match) {
                output += match[1] + '\n';
            }
            // Detect print calls
            const match2 = line.match(/print!\s*\(.*?"([^"]*)"\s*\)/);
            if (match2) {
                output += match2[1];
            }
        }
        
        if (!output.trim()) {
            output = '// Compiled successfully (simulated output)\n// In production, use rustc compiled to WebAssembly';
        }
        
        if (outputEl) {
            outputEl.innerHTML = '<pre class="text-green-400">' + escapeHtml(output) + '</pre>';
        }
        return { success: true, output };
    } catch (err) {
        if (outputEl) {
            outputEl.innerHTML = '<pre class="text-red-400">' + err.message + '</pre>';
        }
        return { success: false, error: err.message };
    }
}

function escapeHtml(text) {
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
}

// Show/hide hints
function toggleHints(hintsId) {
    const hints = document.getElementById(hintsId);
    if (hints) {
        hints.classList.toggle('hidden');
    }
}

// Show solution
function showSolution(solutionEl) {
    if (solutionEl) {
        solutionEl.classList.remove('hidden');
    }
}

// Initialize
document.addEventListener('DOMContentLoaded', () => {
    loadPyodide();
});