import React, { useEffect, useState } from 'react';
import { RotateCcw, Eye, ShieldCheck } from 'lucide-react';
import './VerificationResult.css';

const VerificationResult = ({ result, onReset }) => {
  return (
    <div className="result-container fade-in-up">
      {result.blockchain_proof && (
        <div className="blockchain-proof glass-panel" style={{ marginTop: '1.5rem', border: '1px solid var(--primary)', background: 'rgba(59, 130, 246, 0.05)', padding: '1rem', borderRadius: '12px' }}>
          <div className="proof-header" style={{ display: 'flex', alignItems: 'center', gap: '0.75rem', marginBottom: '0.75rem' }}>
            <ShieldCheck size={18} color="var(--primary)" />
            <h3 style={{ fontSize: '1rem', color: 'var(--primary)', margin: 0 }}>Blockchain Sealed & Immutable</h3>
          </div>
          <div className="proof-details" style={{ fontSize: '0.85rem', color: 'var(--text-muted)' }}>
            <div style={{ marginBottom: '0.4rem' }}>
              <strong>Block Hash:</strong> 
              <code style={{ display: 'block', background: 'rgba(0,0,0,0.3)', padding: '0.5rem', borderRadius: '4px', marginTop: '0.25rem', wordBreak: 'break-all', color: 'var(--secondary)' }}>
                {result.blockchain_proof.block_hash}
              </code>
            </div>
            <div style={{ display: 'flex', justifyContent: 'space-between', marginTop: '0.5rem' }}>
              <span>Index: #{result.blockchain_proof.block_index}</span>
              <span>Status: {result.blockchain_proof.is_valid ? '✅ Valid' : '❌ Tampered'}</span>
            </div>
          </div>
        </div>
      )}

      {result.extracted_text && (
        <div className="ocr-section glass-panel" style={{ marginTop: '2rem', padding: '1.5rem', borderRadius: '12px' }}>
          <div className="ocr-header" style={{ display: 'flex', alignItems: 'center', gap: '0.75rem', marginBottom: '1rem' }}>
              <Eye size={20} color="var(--secondary)" /> 
              <h3 style={{ margin: 0 }}>Extracted Text</h3>
          </div>
          <div className="ocr-content" style={{ fontSize: '1.2rem', lineHeight: '1.6', color: 'white' }}>
            {result.extracted_text}
          </div>
        </div>
      )}

      <button className="btn btn-secondary reset-btn" style={{ marginTop: '2rem' }} onClick={onReset}>
        <RotateCcw size={20} /> Verify Another Document
      </button>
    </div>
  );
};

export default VerificationResult;
