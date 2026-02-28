document.addEventListener('DOMContentLoaded', function () {
    const newsContainer = document.querySelector('.news-carousel-container');
    const newsList = document.querySelector('.news-carousel-list');

    // Fetch news from backend API
    fetch('/api/news')
        .then(response => response.json())
        .then(newsItems => {
            newsItems.forEach(item => {
                const li = document.createElement('li');
                li.classList.add('news-item');
                li.innerHTML = `
                    <a href="${item.url}" target="_blank" rel="noopener noreferrer">
                        <img src="${item.image}" alt="${item.title}" />
                        <h4>${item.title}</h4>
                    </a>
                    <small>${item.date}</small>
                `;
                newsList.appendChild(li);
            });
        })
        .catch(error => {
            console.error('Error fetching news:', error);
            newsList.innerHTML = '<li class="news-item">Failed to load news.</li>';
        });

    // Simple swipe functionality
    let isDown = false;
    let startX;
    let scrollLeft;

    newsContainer.addEventListener('mousedown', (e) => {
        isDown = true;
        newsContainer.classList.add('active');
        startX = e.pageX - newsContainer.offsetLeft;
        scrollLeft = newsContainer.scrollLeft;
    });
    newsContainer.addEventListener('mouseleave', () => {
        isDown = false;
        newsContainer.classList.remove('active');
    });
    newsContainer.addEventListener('mouseup', () => {
        isDown = false;
        newsContainer.classList.remove('active');
    });
    newsContainer.addEventListener('mousemove', (e) => {
        if(!isDown) return;
        e.preventDefault();
        const x = e.pageX - newsContainer.offsetLeft;
        const walk = (x - startX) * 2; //scroll-fast
        newsContainer.scrollLeft = scrollLeft - walk;
    });
});
