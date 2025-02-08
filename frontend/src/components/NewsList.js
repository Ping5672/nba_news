// frontend/src/components/NewsList.js
import React, { useState, useEffect } from 'react';
import axios from 'axios';

const NewsList = () => {
    const [news, setNews] = useState([]);
    
    useEffect(() => {
        const fetchNews = async () => {
            try {
                const response = await axios.get('/api/news/featured');
                setNews(response.data);
            } catch (error) {
                console.error('Error fetching news:', error);
            }
        };
        
        fetchNews();
    }, []);
    
    return (
        <div className="news-list">
            {news.map(item => (
                <article key={item.id} className="news-item">
                    <img src={item.image_url} alt={item.title} />
                    <h2>{item.title}</h2>
                    <p>{item.content}</p>
                </article>
            ))}
        </div>
    );
};

export default NewsList;