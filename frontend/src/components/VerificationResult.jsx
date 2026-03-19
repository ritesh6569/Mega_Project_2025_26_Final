import React, { useEffect, useState } from 'react';
import { ShieldCheck, AlertOctagon, RotateCcw, Cpu, Fingerprint, Eye } from 'lucide-react';
import './VerificationResult.css';

const VerificationResult = ({ result, onReset }) => {
  const isVerified = result.verified;
  const confidence = result.confidence_percentage;
  const score = result.similarity_score;
  const summary = result.extracted_features_summary;

  return (
    <div className="result-container fade-in-up">
      <div className="result-header">
        <div className={`status-badge ${isVerified ? 'verified' : 'failed'}`}>
          {isVerified ? <ShieldCheck size={24} /> : <AlertOctagon size={24} />}
          <span>{isVerified ? 'Authentic' : 'Suspicious'}</span>
        </div>
        <h2>{isVerified ? 'Document Verified' : 'Tampering Detected'}</h2>
        <p className="subtitle">
          {isVerified 
            ? 'The document structure and features appear genuine.' 
            : 'Anomalies found in texture or structural integrity.'}
        </p>
      </div>

      <div className="metrics-grid">
        <div className="metric-card glass-panel">
          <span className="metric-label">Confidence</span>
          <span className="metric-value">{confidence.toFixed(1)}%</span>
        </div>
        
        <div className="metric-card glass-panel">
          <span className="metric-label">AI Similarity</span>
          <span className="metric-value">{score.toFixed(3)}</span>
        </div>
      </div>

      <div className="summary-section glass-panel">
        <div className="summary-header">
          <Fingerprint size={20} color="var(--primary)" />
          <h3>AI Analysis Summary</h3>
        </div>
        <p>{summary}</p>
        
        {result.extracted_text && (
          <div className="ocr-section">
            <div className="ocr-header">
                <Eye size={20} color="var(--secondary)" /> 
                <h3>Extracted Text</h3>
            </div>
            <div className="ocr-content">
              {result.extracted_text}
            </div>
          </div>
        )}
      </div>

      <button className="btn btn-secondary reset-btn" onClick={onReset}>
        <RotateCcw size={20} /> Verify Another Document
      </button>
    </div>
  );
};

export default VerificationResult;
