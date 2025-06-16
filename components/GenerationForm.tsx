import React from 'react';
import { useState } from 'react';

interface GenerationFormProps {
 setResult: (result: { [key: string]: any } | null) => void;
}

const GenerationForm: React.FC<GenerationFormProps> = ({ setResult }) => {
  const [clientName, setClientName] = useState('');
  const [clientWebsite, setClientWebsite] = useState('');
  const [industry, setIndustry] = useState('');
  const [customerDataFiles, setCustomerDataFiles] = useState<File[]>([]);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    console.log("handleSubmit called");
    const formData = new FormData();
    formData.append('clientName', clientName);
    formData.append('clientWebsite', clientWebsite);
    formData.append('industry', industry);
    customerDataFiles.forEach(file => {
      formData.append('customer_data_files', file);
    });

    try {
      const url = 'http://localhost:8003/api/generate';
      console.log(`Sending POST request to ${url}`);
      const response = await fetch(url, {
        method: 'POST',
        body: formData,
      });

      if (!response.ok) {
        console.error(`HTTP error! status: ${response.status}`);
      }

      const result = await response.json();
      console.log('API response from GenerationForm:', result);
      if (typeof setResult === 'function') {
        setResult(result);
      }
    } catch (error) {
      console.error('Fetch error:', error);
    }
  };

  return (
    <form onSubmit={handleSubmit}>
      <div>
        <label htmlFor="clientName">Client Name:</label>
        <input
          type="text"
          id="clientName"
          value={clientName}
          onChange={(e) => setClientName(e.target.value)}
        />
      </div>
      <div>
        <label htmlFor="clientWebsite">Client Website:</label>
        <input
          type="text"
          id="clientWebsite"
          value={clientWebsite}
          onChange={(e) => setClientWebsite(e.target.value)}
        />
      </div>
      <div>
        <label htmlFor="industry">Industry:</label>
        <select
          id="industry"
          value={industry}
          onChange={(e) => setIndustry(e.target.value)}
        >
          <option value="Retail/E-Commerce">Retail/E-Commerce</option>
          <option value="Finance/Banking">Finance/Banking</option>
          <option value="Media/Publishing">Media/Publishing</option>
        </select>
      </div>
      <div>
        <label htmlFor="customerDataFiles">Customer Data Files:</label>
        <input
          type="file"
          id="customerDataFiles"
          multiple
          onChange={(e) => {
            if (e.target.files) {
              setCustomerDataFiles(Array.from(e.target.files));
            }
          }}
        />
      </div>
      <button type="submit">Generate</button>
    </form>
  );
};

export default GenerationForm;