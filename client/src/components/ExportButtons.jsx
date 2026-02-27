export default function ExportButtons({ flashcards }) {
  if (!flashcards || flashcards.length === 0) return null;

  const download = (content, filename, type) => {
    const blob = new Blob([content], { type });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = filename;
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    URL.revokeObjectURL(url);
  };

  const exportJSON = () => {
    download(JSON.stringify(flashcards, null, 2), 'flashcards.json', 'application/json');
  };

  const exportCSV = () => {
    const headers = ['ID', 'Question', 'Answer', 'Difficulty', 'Topic'];
    const rows = flashcards.map((c) => [
      c.id,
      `"${(c.question || '').replace(/"/g, '""')}"`,
      `"${(c.answer || '').replace(/"/g, '""')}"`,
      c.difficulty,
      `"${(c.topic || '').replace(/"/g, '""')}"`,
    ].join(','));
    download([headers.join(','), ...rows].join('\n'), 'flashcards.csv', 'text/csv');
  };

  const exportAnki = () => {
    const content = flashcards.map((c) => `${c.question}\t${c.answer}\t${c.topic}`).join('\n');
    download(content, 'flashcards_anki.txt', 'text/plain');
  };

  const exportTXT = () => {
    const content = flashcards.map((c) =>
      `Card ${c.id} [${c.difficulty}] - ${c.topic}\nQ: ${c.question}\nA: ${c.answer}\n`
    ).join('\n');
    download(content, 'flashcards.txt', 'text/plain');
  };

  const btnClass =
    'px-4 py-2 border-2 border-green-700 text-green-700 rounded-lg font-semibold hover:bg-green-700 hover:text-white transition text-sm';

  return (
    <div className="flex flex-wrap gap-3">
      <button onClick={exportJSON} className={btnClass}>JSON</button>
      <button onClick={exportCSV} className={btnClass}>CSV</button>
      <button onClick={exportAnki} className={btnClass}>Anki</button>
      <button onClick={exportTXT} className={btnClass}>TXT</button>
    </div>
  );
}
