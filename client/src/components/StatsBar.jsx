export default function StatsBar({ flashcards }) {
  if (!flashcards || flashcards.length === 0) return null;

  const total = flashcards.length;
  const easy = flashcards.filter((c) => c.difficulty === 'Easy').length;
  const medium = flashcards.filter((c) => c.difficulty === 'Medium').length;
  const hard = flashcards.filter((c) => c.difficulty === 'Hard').length;

  return (
    <div className="flex justify-around bg-gray-50 rounded-xl p-5 mb-6">
      <div className="text-center">
        <div className="text-2xl font-bold text-green-800">{total}</div>
        <div className="text-sm text-gray-500">Total</div>
      </div>
      <div className="text-center">
        <div className="text-2xl font-bold text-emerald-500">{easy}</div>
        <div className="text-sm text-gray-500">Easy</div>
      </div>
      <div className="text-center">
        <div className="text-2xl font-bold text-amber-500">{medium}</div>
        <div className="text-sm text-gray-500">Medium</div>
      </div>
      <div className="text-center">
        <div className="text-2xl font-bold text-red-500">{hard}</div>
        <div className="text-sm text-gray-500">Hard</div>
      </div>
    </div>
  );
}
