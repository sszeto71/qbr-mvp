"use client";
// frontend/src/app/page.tsx
import GenerationForm from "./GenerationForm";
import { useState } from "react";

interface SlideData {
  title: string;
  content: string[];
}

interface ClientInfo {
  client_name: string;
  client_website: string;
  industry: string;
}

interface ResultsDisplayProps {
  result: { [key: string]: SlideData } | null;
  setResult: (result: { [key: string]: SlideData } | null) => void;
  clientInfo: ClientInfo | null;
}

// Slide icons mapping
const slideIcons: { [key: string]: string } = {
  slide1: "🎯", // Executive Summary
  slide2: "📊", // Key Metrics
  slide3: "📈", // Performance Analysis
  slide4: "👥", // Customer Insights
  slide5: "🚀", // Recommendations
  slide6: "🗓️", // Next Steps
};

const SlideNavigation: React.FC<{
  currentSlide: number;
  totalSlides: number;
  onSlideChange: (slide: number) => void;
}> = ({ currentSlide, totalSlides, onSlideChange }) => (
  <div className="flex justify-between items-center mb-6">
    <button
      onClick={() => onSlideChange(Math.max(0, currentSlide - 1))}
      disabled={currentSlide === 0}
      className="px-4 py-2 bg-blue-500 text-white rounded-lg disabled:bg-gray-300 disabled:cursor-not-allowed hover:bg-blue-600 transition-colors"
    >
      ← Previous
    </button>
    
    <div className="flex items-center space-x-2">
      <div className="text-sm text-gray-500 bg-gray-100 px-3 py-1 rounded-full">
        {currentSlide + 1} of {totalSlides}
      </div>
      {Array.from({ length: totalSlides }, (_, i) => (
        <button
          key={i}
          onClick={() => onSlideChange(i)}
          className={`w-3 h-3 rounded-full transition-colors ${
            i === currentSlide ? 'bg-blue-500' : 'bg-gray-300 hover:bg-gray-400'
          }`}
        />
      ))}
    </div>
    
    <button
      onClick={() => onSlideChange(Math.min(totalSlides - 1, currentSlide + 1))}
      disabled={currentSlide === totalSlides - 1}
      className="px-4 py-2 bg-blue-500 text-white rounded-lg disabled:bg-gray-300 disabled:cursor-not-allowed hover:bg-blue-600 transition-colors"
    >
      Next →
    </button>
  </div>
);

const ResultsDisplay: React.FC<ResultsDisplayProps> = ({ result, setResult, clientInfo }) => {
  const [isExporting, setIsExporting] = useState(false);
  const [currentSlide, setCurrentSlide] = useState(0);

  const handleExportPDF = async () => {
    if (!result || !clientInfo) {
      alert('Missing data for PDF export');
      return;
    }

    setIsExporting(true);
    
    try {
      const formData = new FormData();
      formData.append('client_name', clientInfo.client_name);
      formData.append('client_website', clientInfo.client_website);
      formData.append('industry', clientInfo.industry);
      formData.append('qbr_content', JSON.stringify(result));

      const response = await fetch('http://localhost:8000/api/export-pdf', {
        method: 'POST',
        body: formData,
      });

      if (response.ok) {
        // Create download link
        const blob = await response.blob();
        const url = window.URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = `QBR_${clientInfo.client_name.replace(/\s+/g, '_')}.pdf`;
        document.body.appendChild(a);
        a.click();
        document.body.removeChild(a);
        window.URL.revokeObjectURL(url);
      } else {
        const errorData = await response.json();
        throw new Error(errorData.message || 'Failed to export PDF');
      }
    } catch (error) {
      console.error('PDF export failed:', error);
      alert(`PDF export failed: ${error instanceof Error ? error.message : 'Unknown error'}`);
    } finally {
      setIsExporting(false);
    }
  };

  if (!result) {
    return <div>No results yet.</div>;
  }

  const slides = Object.entries(result);
  const currentSlideData = slides[currentSlide];
  
  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100 py-8">
      <div className="max-w-5xl mx-auto px-6">
        {/* Header */}
        <div className="mb-8 flex justify-between items-center">
          <button
            onClick={() => setResult(null)}
            className="bg-gray-600 hover:bg-gray-700 text-white font-medium py-2 px-4 rounded-lg transition-colors flex items-center gap-2"
          >
            ← Back to Form
          </button>
          
          <div className="text-center">
            <h1 className="text-3xl font-bold text-gray-800">Quarterly Business Review</h1>
            {clientInfo && (
              <p className="text-lg text-gray-600 mt-1">{clientInfo.client_name}</p>
            )}
          </div>
          
          <button
            onClick={handleExportPDF}
            disabled={isExporting}
            className={`${
              isExporting
                ? 'bg-gray-400 cursor-not-allowed'
                : 'bg-green-600 hover:bg-green-700'
            } text-white font-medium py-2 px-4 rounded-lg flex items-center gap-2 transition-colors`}
          >
            {isExporting ? (
              <>
                <div className="animate-spin rounded-full h-4 w-4 border-b-2 border-white"></div>
                Exporting...
              </>
            ) : (
              <>
                📄 Export PDF
              </>
            )}
          </button>
        </div>

        {/* Slide Navigation */}
        <SlideNavigation
          currentSlide={currentSlide}
          totalSlides={slides.length}
          onSlideChange={setCurrentSlide}
        />

        {/* Current Slide */}
        {currentSlideData && (
          <div className="bg-white rounded-2xl shadow-2xl p-8 min-h-[500px] border border-gray-200">
            {/* Slide Header */}
            <div className="flex items-center mb-8">
              <div className="text-4xl mr-4">
                {slideIcons[currentSlideData[0]] || "📋"}
              </div>
              <h2 className="text-3xl font-bold text-gray-800">
                {currentSlideData[1].title}
              </h2>
            </div>

            {/* Slide Content */}
            <div className="space-y-4">
              {currentSlideData[1].content && Array.isArray(currentSlideData[1].content) ? (
                currentSlideData[1].content.map((item, index) => (
                  <div
                    key={index}
                    className="flex items-start space-x-4 p-4 bg-gradient-to-r from-blue-50 to-indigo-50 rounded-lg border-l-4 border-blue-400 hover:shadow-md transition-shadow"
                  >
                    <div className="flex-shrink-0 w-8 h-8 bg-blue-100 rounded-full flex items-center justify-center">
                      <span className="text-blue-600 font-semibold text-sm">
                        {index + 1}
                      </span>
                    </div>
                    <p className="text-gray-700 text-lg leading-relaxed">
                      {item}
                    </p>
                  </div>
                ))
              ) : (
                <div className="text-center py-12">
                  <div className="text-6xl mb-4">📝</div>
                  <p className="text-gray-500 text-lg">No content available for this slide</p>
                </div>
              )}
            </div>
          </div>
        )}

        {/* Slide Overview */}
        <div className="mt-8 bg-white rounded-xl shadow-lg p-6">
          <h3 className="text-xl font-semibold text-gray-800 mb-4">Slide Overview</h3>
          <div className="grid grid-cols-2 md:grid-cols-3 gap-4">
            {slides.map(([slideKey, data], index) => (
              <button
                key={slideKey}
                onClick={() => setCurrentSlide(index)}
                className={`p-4 rounded-lg border-2 transition-all text-left hover:shadow-md ${
                  index === currentSlide
                    ? 'border-blue-500 bg-blue-50'
                    : 'border-gray-200 hover:border-gray-300'
                }`}
              >
                <div className="flex items-center space-x-3">
                  <div className="text-2xl">
                    {slideIcons[slideKey] || "📋"}
                  </div>
                  <div>
                    <div className="font-medium text-gray-800 text-sm">
                      Slide {index + 1}
                    </div>
                    <div className="text-gray-600 text-xs whitespace-normal">
                      {data.title}
                    </div>
                  </div>
                </div>
              </button>
            ))}
          </div>
        </div>
      </div>
    </div>
  );
};

export default function Home() {
  const [result, setResult] = useState<{ [key: string]: SlideData } | null>(null);
  const [clientInfo, setClientInfo] = useState<ClientInfo | null>(null);
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
      {totalRevenue > 0 && (
        <div className="max-w-4xl mx-auto p-6">
          <h2 className="text-2xl font-semibold mb-4 text-blue-600 border-b pb-2">Key Metrics</h2>
          <ul className="space-y-2">
            <li className="flex items-start">
              <span className="text-blue-500 mr-2">•</span>
              <span className="text-gray-700">Total Revenue: ${totalRevenue.toLocaleString('en-US', { minimumFractionDigits: 2, maximumFractionDigits: 2 })}</span>
            </li>
            <li className="flex items-start">
              <span className="text-blue-500 mr-2">•</span>
              <span className="text-gray-700">Total Purchases: {totalPurchases.toLocaleString('en-US')}</span>
            </li>
            <li className="flex items-start">
              <span className="text-blue-500 mr-2">•</span>
              <span className="text-gray-700">Average Order Value: ${averageOrderValue.toLocaleString('en-US', { minimumFractionDigits: 2, maximumFractionDigits: 2 })}</span>
            </li>
          </ul>
        </div>
      )}
      {result ? (
        <ResultsDisplay result={result} setResult={setResult} clientInfo={clientInfo} />
      ) : (
        <GenerationForm setResult={(data: any, clientInfo?: any) => {
          console.log("Data from GenerationForm:", data); // Log the data received
          console.log("Data type:", typeof data);
          console.log("Data keys:", data ? Object.keys(data) : "No data");
          console.log("Client info:", clientInfo);
          
          // Store client information for PDF export
          if (clientInfo) {
            setClientInfo(clientInfo);
          }
          
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
    </main>
  );
}
