import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import axios from 'axios';

const NewsList = () => {
    const [news, setNews] = useState([]);
    const navigate = useNavigate();
    
    useEffect(() => {
        const fetchNews = async () => {
            try {
                const response = await axios.get('http://localhost:8000/api/news/featured');
                setNews(response.data);
            } catch (error) {
                console.error('Error fetching news:', error);
            }
        };
        
        fetchNews();
    }, []);

    const handleNewsClick = (url) => {
        navigate(`/news/${encodeURIComponent(url)}`);
    };
    
    return (
        <div className="news-list">
            {news.map((item, index) => (
                <article 
                    key={index} 
                    className="news-item cursor-pointer hover:bg-gray-100 p-4"
                    onClick={() => handleNewsClick(item.url)}
                >
                    <img src={item.image_url} alt={item.title} className="w-full max-w-md" />
                    <h2 className="text-xl font-bold mt-2">{item.title}</h2>
                    <p className="text-gray-600">{item.published_time}</p>
                    <p className="mt-2">{item.content}</p>
                </article>
            ))}
        </div>
    );
};

export default NewsList;