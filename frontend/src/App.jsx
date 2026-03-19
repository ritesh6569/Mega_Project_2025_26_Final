import React, { useState } from 'react';
import { Shield, Loader2 } from 'lucide-react';
import './App.css';
import UploadZone from './components/UploadZone';
import VerificationResult from './components/VerificationResult';
import PreprocessingOptions from './components/PreprocessingOptions';
import FeatureExtractionOptions from './components/FeatureExtractionOptions';

const STEPS = {
  UPLOAD: 'upload',
  PREPROCESSING: 'preprocessing',
  FEATURE_OPTIONS: 'feature_options',
  LOADING: 'loading',
  RESULT: 'result'
};

const VerificationFlow = () => {
  const [step, setStep] = useState(STEPS.UPLOAD);
  const [file, setFile] = useState(null);
  const [result, setResult] = useState(null);
  const [selectedTechniques, setSelectedTechniques] = useState([]);
  const [featureTechniques, setFeatureTechniques] = useState(['CNN', 'SIFT', 'HOG', 'LBP', 'ORB']);

  const handleUpload = (uploadedFile) => {
    setFile(uploadedFile);
    setStep(STEPS.PREPROCESSING);
  };

  const handlePreprocessingSelect = (techniques) => {
    setSelectedTechniques(techniques);
    setStep(STEPS.FEATURE_OPTIONS);
  };

  const handleFeatureSelect = async (techniques) => {
    setFeatureTechniques(techniques);
    setStep(STEPS.LOADING);
    
    const formData = new FormData();
    formData.append('document', file);
    formData.append('techniques', JSON.stringify(selectedTechniques));
    formData.append('feature_techniques', JSON.stringify(techniques));

    try {
      const response = await fetch('http://localhost:5000/api/verify', {
        method: 'POST',
        body: formData,
      });
      const data = await response.json();
      if (data.status === 'success') {
        setResult(data.data);
        setStep(STEPS.RESULT);
      } else {
        throw new Error(data.message || 'Verification failed');
      }
    } catch (error) {
      console.error('Verification failed:', error);
      alert(error.message || 'Verification failed. Please try again.');
      setStep(STEPS.UPLOAD);
    }
  };

  const resetFlow = () => {
    setStep(STEPS.UPLOAD);
    setFile(null);
    setResult(null);
    setSelectedTechniques([]);
  };

  return (
    <main className="app-main">
      <div className="content-wrapper">
        {step === STEPS.UPLOAD && (
          <div className="hero-main fade-in-up">
            <h1 className="section-title">Intelligent Document Verification</h1>
            <p style={{color: 'var(--text-muted)', marginBottom: '3rem'}}>Advanced AI-powered authenticity analysis with selective feature extraction.</p>
            <UploadZone onUpload={handleUpload} />
          </div>
        )}

        {step === STEPS.PREPROCESSING && (
          <PreprocessingOptions 
            onNext={handlePreprocessingSelect} 
            onBack={() => setStep(STEPS.UPLOAD)}
          />
        )}

        {step === STEPS.FEATURE_OPTIONS && (
          <FeatureExtractionOptions
            onNext={handleFeatureSelect}
            onBack={() => setStep(STEPS.PREPROCESSING)}
          />
        )}

        {step === STEPS.LOADING && (
          <div className="loading-container container-centered fade-in-up">
            <div className="scanner-overlay">
                <div className="scanner-line"></div>
            </div>
            <div className="loading-text" style={{textAlign: 'center', marginTop: '2rem'}}>
                <h2 style={{color: 'white', marginBottom: '0.5rem'}}>AI Analyzing Document...</h2>
                <p style={{color: 'var(--text-muted)'}}>Extracting features and validating authenticity models</p>
                <div style={{marginTop: '2rem', color: 'var(--primary)', display: 'flex', alignItems: 'center', justifyContent: 'center', gap: '0.75rem'}}>
                    <Loader2 className="animate-spin" />
                    <span>Processing Secure Connection</span>
                </div>
            </div>
          </div>
        )}

        {step === STEPS.RESULT && result && (
          <VerificationResult result={result} onReset={resetFlow} />
        )}
      </div>
    </main>
  );
};

function RootApp() {
  return (
    <div className="app-container">
      <div className="bg-blobs">
        <div className="blob blob-1"></div>
        <div className="blob blob-2"></div>
      </div>
      
      <VerificationFlow />
    </div>
  );
}

export default RootApp;
