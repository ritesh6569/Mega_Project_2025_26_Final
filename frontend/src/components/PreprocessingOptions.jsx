import React, { useState } from 'react';
import { Settings, Check, Zap, Image as ImageIcon, Sparkles, Filter, Scissors } from 'lucide-react';
import './PreprocessingOptions.css';

const techniquesList = [
  { id: 'resizing', name: 'Smart Resizing', desc: 'Standardizes dimensions for consistent feature extraction.', icon: <Scissors size={20} /> },
  { id: 'grayscale', name: 'Grayscale Conversion', desc: 'Removes color noise to focus on structural patterns.', icon: <ImageIcon size={20} /> },
  { id: 'noise_removal', name: 'Gaussian Noise Filter', desc: 'Smooths the image to eliminate digital artifacts.', icon: <Zap size={20} /> },
  { id: 'equalization', name: 'Histogram Equalization', desc: 'Optimizes contrast for better edge detection.', icon: <Sparkles size={20} /> },
  { id: 'edge_detection', name: 'Canny Edge Detection', desc: 'Highlights document borders and text outlines.', icon: <Filter size={20} /> },
];

const PreprocessingOptions = ({ onNext, onBack }) => {
  const [selected, setSelected] = useState(['resizing', 'grayscale']);

  const toggleTechnique = (id) => {
    setSelected(prev => 
      prev.includes(id) ? prev.filter(t => t !== id) : [...prev, id]
    );
  };

  return (
    <div className="options-container glass-panel fade-in-up">
      <div className="options-header">
        <Settings className="header-icon" />
        <h2>Configure Preprocessing</h2>
        <p>Select the enhancement techniques to apply before AI verification.</p>
      </div>

      <div className="techniques-grid">
        {techniquesList.map(tech => (
          <div 
            key={tech.id} 
            className={`tech-card ${selected.includes(tech.id) ? 'selected' : ''}`}
            onClick={() => toggleTechnique(tech.id)}
          >
            <div className="tech-icon-wrapper">{tech.icon}</div>
            <div className="tech-info">
              <h3>{tech.name}</h3>
              <p>{tech.desc}</p>
            </div>
            <div className="checkbox">
              {selected.includes(tech.id) && <Check size={16} />}
            </div>
          </div>
        ))}
      </div>

      <div className="options-footer">
        <button className="btn btn-secondary" onClick={onBack}>Back</button>
        <button 
          className="btn btn-primary" 
          disabled={selected.length === 0}
          onClick={() => onNext(selected)}
        >
          Run Extraction & Verify
        </button>
      </div>
    </div>
  );
};

export default PreprocessingOptions;
