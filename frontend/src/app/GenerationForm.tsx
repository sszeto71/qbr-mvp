"use client";
// frontend/src/app/GenerationForm.tsx
import React, { useState } from 'react';

interface SlideData {
  title: string;
  content: string[];
}

interface GenerationFormProps {
  setResult: (result: { [key: string]: SlideData } | null) => void;
}

const GenerationForm: React.FC<GenerationFormProps> = ({ setResult }) => {
  const [clientName, setClientName] = useState('');
  const [clientWebsite, setClientWebsite] = useState('');
  const [industry, setIndustry] = useState('');
  const [customerDataFiles, setCustomerDataFiles] = useState<File[]>([]);
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);

    const formData = new FormData();
    formData.append('client_name', clientName);
    formData.append('client_website', clientWebsite);
    formData.append('industry', industry);
    customerDataFiles.forEach((file) => {
      formData.append('customer_data_files', file);
    });

    try {
      console.log('Form data being sent:', Object.fromEntries(formData));
      console.log('Sending request to http://localhost:8000/api/generate');
      const response = await fetch('http://localhost:8000/api/generate', {
        method: 'POST',
        body: formData,
      });
      console.log('Received response:', response);

      if (!response.ok) {
        console.error('HTTP error! Status:', response.status);
        throw new Error(`HTTP error! Status: ${response.status}`);
      }

      const data = await response.json();
      console.log('Received data:', data);
      setResult(data);
    } catch (error) {
      console.error('Fetch Error:', error);
      // Handle error appropriately
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="max-w-2xl mx-auto p-6">
      <h1 className="text-3xl font-bold mb-8 text-center">QBR Generator</h1>
      
      <form onSubmit={handleSubmit} className="bg-white p-8 rounded-lg shadow-lg">
        <div className="mb-6">
          <label htmlFor="clientName" className="block text-gray-700 text-sm font-bold mb-2">Client Name:</label>
          <input
            type="text"
            id="clientName"
            value={clientName}
            onChange={(e) => setClientName(e.target.value)}
            required
            className="shadow appearance-none border rounded w-full py-3 px-4 text-gray-700 leading-tight focus:outline-none focus:shadow-outline focus:border-blue-500"
            placeholder="Enter client name"
          />
        </div>
        
        <div className="mb-6">
          <label htmlFor="clientWebsite" className="block text-gray-700 text-sm font-bold mb-2">Client Website:</label>
          <input
            type="url"
            id="clientWebsite"
            value={clientWebsite}
            onChange={(e) => setClientWebsite(e.target.value)}
            required
            className="shadow appearance-none border rounded w-full py-3 px-4 text-gray-700 leading-tight focus:outline-none focus:shadow-outline focus:border-blue-500"
            placeholder="https://example.com"
          />
        </div>
        
        <div className="mb-6">
          <label htmlFor="industry" className="block text-gray-700 text-sm font-bold mb-2">Industry:</label>
          <input
            type="text"
            id="industry"
            value={industry}
            onChange={(e) => setIndustry(e.target.value)}
            required
            className="shadow appearance-none border rounded w-full py-3 px-4 text-gray-700 leading-tight focus:outline-none focus:shadow-outline focus:border-blue-500"
            placeholder="e.g., Technology, Healthcare, Finance"
          />
        </div>
        
        <div className="mb-8">
          <label htmlFor="customerDataFiles" className="block text-gray-700 text-sm font-bold mb-2">Customer Data Files:</label>
          <input
            type="file"
            id="customerDataFiles"
            multiple
            accept=".pdf,.csv"
            onChange={(e) => {
              if (e.target.files) {
                setCustomerDataFiles(Array.from(e.target.files));
              }
            }}
            className="shadow appearance-none border rounded w-full py-3 px-4 text-gray-700 leading-tight focus:outline-none focus:shadow-outline focus:border-blue-500"
          />
          <p className="text-gray-500 text-xs mt-1">Upload PDF or CSV files containing customer data</p>
        </div>
        
        <button
          type="submit"
          disabled={loading}
          className="w-full bg-blue-500 hover:bg-blue-700 disabled:bg-blue-300 text-white font-bold py-3 px-4 rounded focus:outline-none focus:shadow-outline transition duration-200"
        >
          {loading ? 'Generating QBR...' : 'Generate QBR'}
        </button>
      </form>
    </div>
  );
};

export default GenerationForm;