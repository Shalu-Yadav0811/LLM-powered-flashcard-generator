import { useState } from 'react';

const difficultyColors = {
  Easy: 'bg-emerald-400',
  Medium: 'bg-amber-400',
  Hard: 'bg-red-400',
};

export default function FlashcardFlip({ card, onEdit }) {
  const [flipped, setFlipped] = useState(false);

  return (
    <div
      className={`flip-card cursor-pointer ${flipped ? 'flipped' : ''}`}
      onClick={() => setFlipped(!flipped)}
    >
      <div className="flip-card-inner shadow-lg rounded-2xl">
        {/* Front */}
        <div className="flip-card-front bg-white">
          <div className="bg-gradient-to-r from-green-800 to-green-600 text-white px-5 py-4 rounded-t-2xl flex items-center justify-between">
            <span className="font-bold text-sm truncate mr-2">
              Card {card.id} - {card.topic || 'No topic'}
            </span>
            <span className={`${difficultyColors[card.difficulty] || 'bg-gray-400'} text-white text-xs px-3 py-1 rounded-full font-semibold`}>
              {card.difficulty}
            </span>
          </div>
          <div className="flex-1 flex items-center justify-center p-6 text-gray-800">
            <p className="text-center text-lg font-medium">{card.question}</p>
          </div>
          <p className="text-center text-sm text-green-700 pb-4">Click to reveal answer</p>
        </div>

        {/* Back */}
        <div className="flip-card-back bg-white">
          <div className="bg-gradient-to-r from-green-800 to-green-600 text-white px-5 py-4 rounded-t-2xl flex items-center justify-between">
            <span className="font-bold text-sm">Answer</span>
            <span className={`${difficultyColors[card.difficulty] || 'bg-gray-400'} text-white text-xs px-3 py-1 rounded-full font-semibold`}>
              {card.difficulty}
            </span>
          </div>
          <div className="flex-1 flex items-center justify-center p-6 text-gray-800">
            <p className="text-center">{card.answer}</p>
          </div>
          <div className="flex justify-between items-center px-5 pb-4">
            <p className="text-sm text-green-700">Click to see question</p>
            {onEdit && (
              <button
                onClick={(e) => { e.stopPropagation(); onEdit(card); }}
                className="text-sm px-4 py-1.5 border border-green-700 text-green-700 rounded-lg font-semibold hover:bg-green-700 hover:text-white transition"
              >
                Edit
              </button>
            )}
          </div>
        </div>
      </div>
    </div>
  );
}
