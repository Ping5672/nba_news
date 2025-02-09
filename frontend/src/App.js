import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import NewsList from './components/NewsList';
import NewsDetail from './components/NewsDetail';

function App() {
  return (
    <Router>
      <div className="container mx-auto">
        <Routes>
          <Route path="/" element={<NewsList />} />
          <Route path="/news/:newsUrl" element={<NewsDetail />} />
        </Routes>
      </div>
    </Router>
  );
}

export default App;