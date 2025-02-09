import React, { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import axios from 'axios';

const NewsDetail = () => {
    const { newsUrl } = useParams();
    const navigate = useNavigate();
    const [article, setArticle] = useState(null);
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        const fetchArticle = async () => {
            try {
                const decodedUrl = decodeURIComponent(newsUrl);
                const response = await axios.get(`http://localhost:8000/api/news/${decodedUrl}`);
                setArticle(response.data);
            } catch (error) {
                console.error('Error fetching article:', error);
            } finally {
                setLoading(false);
            }
        };

        fetchArticle();
    }, [newsUrl]);

    if (loading) {
        return <div>Loading...</div>;
    }

    return (
        <div className="p-4 max-w-3xl mx-auto">
            <button 
                onClick={() => navigate('/')}
                className="mb-4 px-4 py-2 bg-blue-500 text-white rounded"
            >
                Back to List
            </button>
            
            {article && (
                <div>
                    <h1 className="text-2xl font-bold mb-4">{article.title}</h1>
                    <div className="prose">
                        {article.content.split('\n').map((p, i) => (
                            <p key={i} className="mb-4">{p}</p>
                        ))}
                    </div>
                    <div className="mt-4">
                        {article.tags?.map((tag, i) => (
                            <span 
                                key={i} 
                                className="bg-gray-200 px-2 py-1 rounded mr-2"
                            >
                                {tag}
                            </span>
                        ))}
                    </div>
                </div>
            )}
        </div>
    );
};

export default NewsDetail;