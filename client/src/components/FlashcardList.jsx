const difficultyColors = {
  Easy: 'bg-emerald-100 text-emerald-700',
  Medium: 'bg-amber-100 text-amber-700',
  Hard: 'bg-red-100 text-red-700',
};

export default function FlashcardList({ card, onEdit, onDelete }) {
  return (
    <div className="bg-white rounded-xl shadow-md hover:shadow-lg transition overflow-hidden">
      <div className="bg-gradient-to-r from-green-800 to-green-600 text-white px-5 py-3 flex items-center justify-between">
        <span className="font-bold text-sm truncate mr-2">
          Card {card.id} - {card.topic || 'No topic'}
        </span>
        <span className={`${difficultyColors[card.difficulty] || 'bg-gray-100 text-gray-600'} text-xs px-3 py-1 rounded-full font-semibold`}>
          {card.difficulty}
        </span>
      </div>
      <div className="p-5 space-y-3">
        <div>
          <span className="text-xs font-semibold text-gray-400 uppercase">Question</span>
          <p className="text-gray-800 mt-1">{card.question}</p>
        </div>
        <div>
          <span className="text-xs font-semibold text-gray-400 uppercase">Answer</span>
          <p className="text-gray-700 mt-1">{card.answer}</p>
        </div>
      </div>
      {(onEdit || onDelete) && (
        <div className="border-t px-5 py-3 flex justify-end gap-2">
          {onEdit && (
            <button
              onClick={() => onEdit(card)}
              className="text-sm px-4 py-1.5 border border-green-700 text-green-700 rounded-lg font-semibold hover:bg-green-700 hover:text-white transition"
            >
              Edit
            </button>
          )}
          {onDelete && (
            <button
              onClick={() => onDelete(card.id)}
              className="text-sm px-4 py-1.5 border border-red-400 text-red-400 rounded-lg font-semibold hover:bg-red-500 hover:text-white transition"
            >
              Delete
            </button>
          )}
        </div>
      )}
    </div>
  );
}
