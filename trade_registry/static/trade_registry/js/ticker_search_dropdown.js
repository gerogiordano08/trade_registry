document.addEventListener('DOMContentLoaded', () => {
const tickerInput = document.getElementById('symbol');
const  nameInput = document.getElementById('name');
const list = document.getElementById('tickerDropdown');
const submitBtn = document.getElementById('submit-button');
let isTickerValid = false;
submitBtn.disabled = true;

const debounce = (fn, delayMs) => {
    let timeoutId;
    return (...args) => {
        if (timeoutId) {
            clearTimeout(timeoutId);
        }
        timeoutId = setTimeout(() => fn(...args), delayMs);
    };
};

const fetchTickers = async (e) => {
    const query = e.target.value;
    if (query.length < 2) {
        list.classList.add('d-none');
        return;
    }

    try {
        const response = await fetch(`/api/v1/search/finnhub/?q=${query}`);
        const data = await response.json();
        renderResults(data.results);
    } catch (err) {
        console.error("Error fetching tickers", err);
    }
};

const debouncedFetchTickers = debounce(fetchTickers, 500);

tickerInput.addEventListener('input', debouncedFetchTickers);

function renderResults(results) {
    list.innerHTML = '';
    if (results.length === 0) {
        list.classList.add('d-none');
        return;
    }

    results.forEach(item => {
        const li = document.createElement('li');
        li.className = 'list-group-item list-group-item-action d-flex justify-content-between align-items-center';
        li.style.cursor = 'pointer';
        
        li.innerHTML = `
            <div>
                <span class="fw-bold">${item.symbol}</span>
                <small class="text-muted d-block">${item.name}</small>
            </div>
        `;

        li.onclick = () => {
            tickerInput.value = item.symbol;
            nameInput.value = item.name
            list.classList.add('d-none');
            isTickerValid = true;
            submitBtn.disabled = false;
            list.classList.add('d-none');
        };
        list.appendChild(li);
    });
    list.classList.remove('d-none');
}


tickerInput.addEventListener('input', () => {
    isTickerValid = false;
    submitBtn.disabled = true;
});
});