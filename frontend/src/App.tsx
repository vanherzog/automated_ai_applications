// ParentComponent.tsx
import React from 'react';
import DynamicSplitLayout from './DynamicSplitLayout';

const ParentComponent: React.FC = () => {
  return (
    <div className="App">
      <DynamicSplitLayout
        job_description="This is a sample job description."
        application="This is a sample application text."
      />
    </div>
  );
};

export default ParentComponent;

// import React from 'react';
// import DynamicSplitLayout from './DynamicSplitLayout';
//
// function App() {
//   return (
//     <div className="App">
//       <DynamicSplitLayout
//         job_description="This is a sample job description."
//         application="This is a sample application text."
//       />
//     </div>
//   );
// }
//
// export default App;