import { useState, useEffect } from 'react';
import { uploadImage, getSimilarMedicines } from './services/api';
import './styles/App.css';

function App() {
  const [uploadedFile, setUploadedFile] = useState(null);
  const [results, setResults] = useState(null);
  const [previewUrl, setPreviewUrl] = useState(null);
  const [isLoading, setIsLoading] = useState(false);
  const [similarMedicines, setSimilarMedicines] = useState({});
  const [loadingSimilar, setLoadingSimilar] = useState({});

  const handleFileUpload = (event) => {
    const file = event.target.files[0];
    setUploadedFile(file);
    
    if (file) {
      const url = URL.createObjectURL(file);
      setPreviewUrl(url);
      
      // Load image to get dimensions
      const img = new Image();
      img.onload = () => {
        // Clean up object URL after dimensions are obtained
        URL.revokeObjectURL(url);
      };
      img.src = url;
    }
  };

  // Clean up URL when component unmounts or when preview changes
  useEffect(() => {
    return () => {
      if (previewUrl) {
        URL.revokeObjectURL(previewUrl);
      }
    };
  }, [previewUrl]);

  const handleUpload = async () => {
    if (!uploadedFile) return;
    try {
      setIsLoading(true);
      // Reset similar medicines states
      setSimilarMedicines({});
      setLoadingSimilar({});
      const data = await uploadImage(uploadedFile);
      setResults(data);
    } catch (error) {
      setResults({ error: error.message });
    } finally {
      setIsLoading(false);
    }
  };

  const handleGetSimilar = async (medicineName, index) => {
    try {
      setLoadingSimilar(prev => ({ ...prev, [index]: true }));
      const similar = await getSimilarMedicines(medicineName);
      setSimilarMedicines(prev => ({ ...prev, [index]: similar }));
    } catch (error) {
      console.error(error);
    } finally {
      setLoadingSimilar(prev => ({ ...prev, [index]: false }));
    }
  };

  const clearSelection = () => {
    setUploadedFile(null);
    setPreviewUrl(null);
    setResults(null);
    setSimilarMedicines({}); // Clear similar medicines
    setLoadingSimilar({}); // Reset loading states
  };

  return (
    <div className="App">
      <div className="container">
        <div className="upload-section">
          <h2>Upload File</h2>
          {!uploadedFile ? (
            <div className="file-input-wrapper">
              <input
                type="file"
                onChange={handleFileUpload}
                accept=".jpg,.png"
                title=" "
              />
            </div>
          ) : (
            <>
              <div className="preview-container">
                <img src={previewUrl} alt="Preview" className="preview-image" />
                <button className="clear-selection" onClick={clearSelection}>✕</button>
              </div>
              <p>Selected file: {uploadedFile.name}</p>
              <button 
                className="upload-button"
                onClick={handleUpload}
              >
                Upload
              </button>
            </>
          )}
        </div>
        <div className="results-section">
          <h2>Results</h2>
          {isLoading ? (
            <div className="loading-container">
              <div className="loading-spinner"></div>
              <p>Processing image...</p>
            </div>
          ) : results ? (
            <div className="results-content">
              {results.Prescription && results.Prescription.map((item, index) => (
                <div key={index} className="prescription-card">
                  <div className="prescription-details">
                    <span className="medicine-name">{item[0]}</span>
                    <span className="description">{item[1]}</span>
                    <span className="dosage">{item[2]}</span>
                    <button 
                      className={`similar-button ${loadingSimilar[index] ? 'loading' : ''}`}
                      onClick={() => handleGetSimilar(item[3]?.info?.big_name, index)}
                      disabled={loadingSimilar[index] || item[3]?.status !== 'found'}
                    >
                      {loadingSimilar[index] ? '⟳' : '→'}
                    </button>
                  </div>
                  <div className="medicine-subtitle">
                    {item[3]?.status === 'found' ? item[3].info.big_name : 'Not found'}
                  </div>
                  {similarMedicines[index] && (
                    <div className="similar-medicines">
                      <h4>Similar Medicines:</h4>
                      <ul>
                        {similarMedicines[index]['similar_drugs'].map((med, i) => (
                          <li key={i}>{med['big_name']}</li>
                        ))}
                      </ul>
                    </div>
                  )}
                </div>
              ))}
            </div>
          ) : (
            <p>Upload a file to see results</p>
          )}
        </div>
      </div>
    </div>
  );
}

export default App;
