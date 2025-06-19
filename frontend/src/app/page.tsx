"use client";
// frontend/src/app/page.tsx
import GenerationForm from "./GenerationForm";
import { useState, useEffect } from "react";
import {
  DndContext,
  closestCenter,
  KeyboardSensor,
  PointerSensor,
  useSensor,
  useSensors,
  DragEndEvent,
} from '@dnd-kit/core';
import {
  arrayMove,
  SortableContext,
  sortableKeyboardCoordinates,
  verticalListSortingStrategy,
} from '@dnd-kit/sortable';
import {
  useSortable,
} from '@dnd-kit/sortable';
import { CSS } from '@dnd-kit/utilities';

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

// Sortable Slide Item Component
const SortableSlideItem: React.FC<{
  slideKey: string;
  slideData: SlideData;
  index: number;
  currentSlide: number;
  onSlideClick: (index: number) => void;
}> = ({ slideKey, slideData, index, currentSlide, onSlideClick }) => {
  const {
    attributes,
    listeners,
    setNodeRef,
    transform,
    transition,
    isDragging,
  } = useSortable({ id: slideKey });

  const style = {
    transform: CSS.Transform.toString(transform),
    transition,
  };

  return (
    <div
      ref={setNodeRef}
      style={style}
      className={`relative ${isDragging ? 'z-50' : 'z-0'}`}
      {...attributes}
    >
      <button
        onClick={() => onSlideClick(index)}
        className={`p-4 rounded-lg border-2 transition-all text-left hover:shadow-md w-full ${
          index === currentSlide
            ? 'border-blue-500 bg-blue-50'
            : 'border-gray-200 hover:border-gray-300'
        } ${isDragging ? 'opacity-50 scale-105 shadow-xl' : ''}`}
      >
        <div className="flex items-center space-x-3">
          {/* Drag Handle */}
          <div
            {...listeners}
            className="cursor-grab active:cursor-grabbing p-1 rounded hover:bg-gray-100 transition-colors"
            title="Drag to reorder"
          >
            <svg width="12" height="12" viewBox="0 0 12 12" fill="none" className="text-gray-400">
              <circle cx="3" cy="3" r="1" fill="currentColor" />
              <circle cx="9" cy="3" r="1" fill="currentColor" />
              <circle cx="3" cy="6" r="1" fill="currentColor" />
              <circle cx="9" cy="6" r="1" fill="currentColor" />
              <circle cx="3" cy="9" r="1" fill="currentColor" />
              <circle cx="9" cy="9" r="1" fill="currentColor" />
            </svg>
          </div>
          
          <div className="text-2xl">
            {slideIcons[slideKey] || "📋"}
          </div>
          <div>
            <div className="font-medium text-gray-800 text-sm">
              Slide {index + 1}
            </div>
            <div className="text-gray-600 text-xs whitespace-normal">
              {slideData.title}
            </div>
          </div>
        </div>
      </button>
    </div>
  );
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
  const [slideOrder, setSlideOrder] = useState<string[]>([]);

  // Initialize slide order when result changes
  useEffect(() => {
    if (result) {
      const initialOrder = Object.keys(result).sort();
      setSlideOrder(initialOrder);
    }
  }, [result]);

  // Set up drag and drop sensors
  const sensors = useSensors(
    useSensor(PointerSensor),
    useSensor(KeyboardSensor, {
      coordinateGetter: sortableKeyboardCoordinates,
    })
  );

  // Handle drag end
  const handleDragEnd = (event: DragEndEvent) => {
    const { active, over } = event;

    if (over && active.id !== over.id) {
      const oldIndex = slideOrder.indexOf(active.id as string);
      const newIndex = slideOrder.indexOf(over.id as string);
      
      const newSlideOrder = arrayMove(slideOrder, oldIndex, newIndex);
      setSlideOrder(newSlideOrder);
      
      // Update current slide if the currently viewed slide was moved
      if (currentSlide === oldIndex) {
        setCurrentSlide(newIndex);
      } else if (currentSlide === newIndex) {
        setCurrentSlide(oldIndex);
      } else if (currentSlide > Math.min(oldIndex, newIndex) && currentSlide <= Math.max(oldIndex, newIndex)) {
        // Adjust current slide if it's between the moved positions
        if (oldIndex < newIndex) {
          setCurrentSlide(currentSlide - 1);
        } else {
          setCurrentSlide(currentSlide + 1);
        }
      }
    }
  };

  // Get ordered slides based on slideOrder
  const getOrderedSlides = () => {
    if (!result || slideOrder.length === 0) return [];
    return slideOrder.map(key => [key, result[key]] as [string, SlideData]);
  };

  const handleExportPDF = async () => {
    if (!result || !clientInfo) {
      alert('Missing data for PDF export');
      return;
    }

    setIsExporting(true);
    
    try {
      // Create reordered result object for PDF export
      const reorderedResult: { [key: string]: SlideData } = {};
      slideOrder.forEach((key, index) => {
        // Use new slide keys to maintain order in PDF
        reorderedResult[`slide${index + 1}`] = result[key];
      });

      const formData = new FormData();
      formData.append('client_name', clientInfo.client_name);
      formData.append('client_website', clientInfo.client_website);
      formData.append('industry', clientInfo.industry);
      formData.append('qbr_content', JSON.stringify(reorderedResult));

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

  const slides = getOrderedSlides();
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

        {/* Slide Overview with Drag & Drop */}
        <div className="mt-8 bg-white rounded-xl shadow-lg p-6">
          <h3 className="text-xl font-semibold text-gray-800 mb-4">
            Slide Overview
            <span className="text-sm text-gray-500 ml-2 font-normal">
              (Drag to reorder slides)
            </span>
          </h3>
          <DndContext
            sensors={sensors}
            collisionDetection={closestCenter}
            onDragEnd={handleDragEnd}
          >
            <SortableContext items={slideOrder} strategy={verticalListSortingStrategy}>
              <div className="grid grid-cols-2 md:grid-cols-3 gap-4">
                {slides.map(([slideKey, data], index) => (
                  <SortableSlideItem
                    key={slideKey}
                    slideKey={slideKey}
                    slideData={data}
                    index={index}
                    currentSlide={currentSlide}
                    onSlideClick={setCurrentSlide}
                  />
                ))}
              </div>
            </SortableContext>
          </DndContext>
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

  // Test function to load sample data
  const loadTestData = () => {
    const testData = {
      slide1: {
        title: "Executive Summary",
        content: [
          "Strong performance across all key metrics this quarter",
          "Revenue growth of 25% compared to previous quarter",
          "Customer satisfaction scores increased to 4.8/5"
        ]
      },
      slide2: {
        title: "Key Metrics",
        content: [
          "Total Revenue: $2,500,000",
          "Total Purchases: 15,000",
          "Average Order Value: $166.67",
          "Customer Retention Rate: 85%"
        ]
      },
      slide3: {
        title: "Performance Analysis",
        content: [
          "Marketing campaigns showed 15% improvement in conversion rates",
          "Website traffic increased by 40% year-over-year",
          "Mobile app engagement up 60%"
        ]
      },
      slide4: {
        title: "Customer Insights",
        content: [
          "Top customer segments: Technology (40%), Healthcare (25%), Finance (20%)",
          "Geographic distribution: North America (60%), Europe (25%), Asia (15%)",
          "Customer feedback indicates high satisfaction with product quality"
        ]
      },
      slide5: {
        title: "Recommendations",
        content: [
          "Expand marketing efforts in high-performing channels",
          "Invest in mobile app development for enhanced user experience",
          "Consider expansion into emerging markets"
        ]
      },
      slide6: {
        title: "Next Steps",
        content: [
          "Launch new product features by end of Q2",
          "Implement customer feedback improvements",
          "Prepare for Q3 expansion initiatives"
        ]
      }
    };

    setResult(testData);
    setClientInfo({
      client_name: "Test Company",
      client_website: "https://testcompany.com",
      industry: "E-Commerce"
    });
  };

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
        <div>
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
          
          {/* Test Button */}
          <div className="max-w-2xl mx-auto p-6 mt-4">
            <div className="text-center">
              <button
                onClick={loadTestData}
                className="bg-purple-600 hover:bg-purple-700 text-white font-bold py-3 px-6 rounded-lg transition-colors"
              >
                🧪 Load Test Data (Demo Drag & Drop)
              </button>
              <p className="text-gray-500 text-sm mt-2">
                Click to load sample slides and test the drag-and-drop reordering feature
              </p>
            </div>
          </div>
        </div>
      )}
    </main>
  );
}
