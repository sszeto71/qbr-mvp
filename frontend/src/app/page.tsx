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
  const [result, setResult] = useState<{ [key: string]: SlideData } | null>(null);
  const [totalRevenue, setTotalRevenue] = useState<number>(0);
  const [totalPurchases, setTotalPurchases] = useState<number>(0);
  const [averageOrderValue, setAverageOrderValue] = useState<number>(0);
  console.log('Result in page.tsx:', result);

  console.log('Page component rendered');

  // Add logs to check data and qbr_content
  console.log("Result:", result);
  if (result) {
    try {
      console.log("qbr_content:", result.slide1?.content);
    } catch (error) {
      console.error("Error accessing qbr_content:", error);
    }
  }

  return (
    <main>
      {result ? (
        <ResultsDisplay result={result} setResult={setResult} />
      ) : (
        <GenerationForm setResult={(data: any) => {
          console.log("Data from GenerationForm:", data); // Log the data received
          console.log("Data type:", typeof data);
          console.log("Data keys:", data ? Object.keys(data) : "No data");
          
          if (data && data.error) {
            console.error("Backend returned error:", data.error);
            // Still try to handle the response gracefully
          }
          
          if (data && data.qbr_content) {
            try {
              console.log("qbr_content found, type:", typeof data.qbr_content);
              console.log("qbr_content value:", data.qbr_content);
              // Parse the JSON string
              const qbrContent = JSON.parse(data.qbr_content);
              console.log("Parsed qbrContent:", qbrContent);
              // Transform qbr_content to the expected format
              const formattedResult = qbrContent;
              setResult(formattedResult);
            } catch (parseError) {
              console.error("Error parsing qbr_content:", parseError);
              console.error("qbr_content value that failed:", data.qbr_content);
              // Set an empty result to prevent crash
              setResult({});
            }
          } else {
            console.error("qbr_content is undefined in data:", data);
            console.error("Available data keys:", data ? Object.keys(data) : "No data");
            // Set an empty result to prevent crash
            setResult({});
          }
          setTotalRevenue(data?.total_revenue || 0);
          setTotalPurchases(data?.total_purchases || 0);
          setAverageOrderValue(data?.average_order_value || 0);
        }} />
      )}
      {totalRevenue > 0 && (
        <div className="max-w-4xl mx-auto p-6">
          <h2 className="text-2xl font-semibold mb-4 text-blue-600 border-b pb-2">Key Metrics</h2>
          <ul className="space-y-2">
            <li className="flex items-start">
              <span className="text-blue-500 mr-2">•</span>
              <span className="text-gray-700">Total Revenue: ${totalRevenue.toFixed(2)}</span>
            </li>
            <li className="flex items-start">
              <span className="text-blue-500 mr-2">•</span>
              <span className="text-gray-700">Total Purchases: {totalPurchases}</span>
            </li>
            <li className="flex items-start">
              <span className="text-blue-500 mr-2">•</span>
              <span className="text-gray-700">Average Order Value: ${averageOrderValue.toFixed(2)}</span>
            </li>
          </ul>
        </div>
      )}
    </main>
  );
}
