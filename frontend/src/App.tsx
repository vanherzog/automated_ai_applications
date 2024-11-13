import React from 'react';
import DynamicSplitLayout from './DynamicSplitLayout';

// Add global styles
import './App.css';

const App: React.FC = () => {
  return (
    <div className="app-container">
      <DynamicSplitLayout />
    </div>
  );
};

export default App;