"use client";
// frontend/src/app/page.tsx
import GenerationForm from "./GenerationForm";
import { useState } from "react";

interface SlideData {
  title: string;
  content: string[];
}

interface ResultsDisplayProps {
  result: { [key: string]: SlideData } | null;
  setResult: (result: { [key: string]: SlideData } | null) => void;
}

const ResultsDisplay: React.FC<ResultsDisplayProps> = ({ result, setResult }) => {
  if (!result) {
    return <div>No results yet.</div>;
  }
  return (
    <div className="max-w-4xl mx-auto p-6">
      <div className="mb-6">
        <button
          onClick={() => setResult(null)}
          className="bg-gray-500 hover:bg-gray-700 text-white font-bold py-2 px-4 rounded"
        >
          ← Back to Form
        </button>
      </div>
      
      <h1 className="text-3xl font-bold mb-8 text-center">Quarterly Business Review</h1>
      
      {Object.entries(result).map(([slideKey, data]) => (
        <div key={slideKey} className="mb-8 p-6 bg-white rounded-lg shadow-lg border">
          <h2 className="text-2xl font-semibold mb-4 text-blue-600 border-b pb-2">{data.title}</h2>
          <ul className="space-y-2">
            {data.content && Array.isArray(data.content) ? data.content.map((item, index) => (
              <li key={index} className="flex items-start">
                <span className="text-blue-500 mr-2">•</span>
                <span className="text-gray-700">{item}</span>
              </li>
            )) : <li className="text-gray-500 italic">No content available</li>}
          </ul>
        </div>
      ))}
    </div>
  );
};

export default function Home() {
  const [result, setResult] = useState<{ [key: string]: SlideData } | null>(
    null
  );
  console.log('Result in page.tsx:', result);

  console.log('Page component rendered');
  return (
    <main>
      {result ? (
        <ResultsDisplay result={result} setResult={setResult} />
      ) : (
        <GenerationForm  setResult={setResult}/>
      )}
    </main>
  );
}
