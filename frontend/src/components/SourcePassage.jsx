/**
 * Source Passage component for displaying retrieved context.
 */

import { useState } from 'react';

export default function SourcePassage({ passage, index }) {
  const [isExpanded, setIsExpanded] = useState(false);
  const { text, metadata, distance } = passage;
  const source = metadata?.source || metadata?.file || 'unknown';

  return (
    <div className="border border-border rounded-md mb-3 overflow-hidden">
      <button
        onClick={() => setIsExpanded(!isExpanded)}
        className="w-full px-4 py-3 text-left bg-bg-surface hover:bg-bg-page transition-colors flex justify-between items-center"
      >
        <span className="font-medium text-text-primary">
          Passage {index} (source: {source})
        </span>
        <span className="text-text-muted">
          {isExpanded ? '▲' : '▼'}
        </span>
      </button>
      
      {isExpanded && (
        <div className="px-4 py-3 bg-white border-t border-border">
          <p className="text-text-secondary mb-3 leading-relaxed whitespace-pre-wrap">
            {text}
          </p>
          <div className="text-sm text-text-muted">
            <span>distance: {distance.toFixed(4)}</span>
            {Object.entries(metadata || {}).map(([key, value]) => (
              <span key={key} className="ml-3">{key}: {value}</span>
            ))}
          </div>
        </div>
      )}
    </div>
  );
}
