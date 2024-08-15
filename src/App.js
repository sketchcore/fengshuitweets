import React, { useState, useEffect } from 'react';
import { format } from 'date-fns';
import './App.css';

function App() {
  const [tweets, setTweets] = useState([]);

  useEffect(() => {
    // In a real application, you'd fetch this data from an API or database
    const fetchTweets = async () => {
      const response = await fetch('/feng_shui_tips.json');
      const allTips = await response.json();
      const dailyTweets = allTips.slice(0, 6); // Get first 6 tweets
      setTweets(dailyTweets);
    };

    fetchTweets();
  }, []);

  return (
    <div className="container mx-auto px-4 py-8">
      <h1 className="text-4xl font-bold mb-8 text-center">Daily Feng Shui Tips</h1>
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        {tweets.map((tweet, index) => (
          <div key={index} className="bg-white shadow-lg rounded-lg p-6">
            <p className="text-gray-800 mb-4">{tweet}</p>
            <p className="text-sm text-gray-500">
              {format(new Date(), 'MMMM d, yyyy')} at {format(new Date(), 'h:mm a')}
            </p>
          </div>
        ))}
      </div>
    </div>
  );
}

export default App;