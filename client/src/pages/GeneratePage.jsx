import { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import api from '../api/axios';
import toast from 'react-hot-toast';
import FlashcardFlip from '../components/FlashcardFlip';
import FlashcardList from '../components/FlashcardList';
import StatsBar from '../components/StatsBar';
import ExportButtons from '../components/ExportButtons';

const SUBJECTS = [
  'Computer Science', 'Mathematics', 'Physics', 'Chemistry',
  'Biology', 'History', 'Geography', 'Literature', 'Other',
];

export default function GeneratePage() {
  const [subject, setSubject] = useState('');
  const [content, setContent] = useState('');
  const [file, setFile] = useState(null);
  const [numCards, setNumCards] = useState(15);
  const [loading, setLoading] = useState(false);
  const [flashcards, setFlashcards] = useState([]);
  const [viewMode, setViewMode] = useState('flip');
  const [decks, setDecks] = useState([]);
  const [selectedDeck, setSelectedDeck] = useState('');
  const navigate = useNavigate();

  useEffect(() => {
    api.get('/decks').then(({ data }) => setDecks(data.decks)).catch(() => {});
  }, []);

  const handleGenerate = async (e) => {
    e.preventDefault();
    if (!subject) { toast.error('Please select a subject'); return; }
    if (!content && !file) { toast.error('Please enter content or upload a file'); return; }

    setLoading(true);
    try {
      let response;

      if (file) {
        const formData = new FormData();
        formData.append('subject', subject);
        formData.append('file', file);
        formData.append('num_cards', numCards);
        if (selectedDeck) formData.append('deck_id', selectedDeck);
        response = await api.post('/ai/generate', formData, {
          headers: { 'Content-Type': 'multipart/form-data' },
        });
      } else {
        response = await api.post('/ai/generate', {
          subject,
          content,
          num_cards: numCards,
          deck_id: selectedDeck || undefined,
        });
      }

      const cards = response.data.flashcards.map((c, i) => ({ ...c, id: c.id || i + 1 }));
      setFlashcards(cards);
      toast.success(`Generated ${cards.length} flashcards!`);
    } catch (err) {
      toast.error(err.response?.data?.error || 'Failed to generate flashcards');
    } finally {
      setLoading(false);
    }
  };

  const loadDemo = () => {
    setContent(`Photosynthesis is the process by which plants convert light energy into chemical energy. This process occurs in the chloroplasts of plant cells, specifically in structures called thylakoids. The overall equation for photosynthesis is: 6CO2 + 6H2O + light energy → C6H12O6 + 6O2.

The process consists of two main stages: the light-dependent reactions and the light-independent reactions (Calvin cycle). In the light-dependent reactions, chlorophyll absorbs light energy and converts it into ATP and NADPH. These reactions also produce oxygen as a byproduct.

The Calvin cycle uses the ATP and NADPH produced in the light reactions to convert carbon dioxide into glucose. This process does not directly require light but depends on the products of the light reactions.

Factors affecting photosynthesis include light intensity, carbon dioxide concentration, temperature, and water availability. Understanding photosynthesis is crucial for comprehending how energy flows through ecosystems.`);
    setSubject('Biology');
  };

  // Group flashcards by section
  const sectionGroups = {};
  flashcards.forEach((card) => {
    const section = card.section || 'General';
    if (!sectionGroups[section]) sectionGroups[section] = [];
    sectionGroups[section].push(card);
  });

  return (
    <div className="max-w-7xl mx-auto px-4 py-8">
      <h1 className="text-3xl font-bold text-gray-800 mb-8">Generate Flashcards</h1>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
        {/* Input Section */}
        <div className="bg-white rounded-2xl shadow-md p-6">
          <h2 className="text-xl font-bold text-gray-800 mb-5">Input Content</h2>
          <form onSubmit={handleGenerate} className="space-y-4">
            <div>
              <label className="block text-sm font-semibold text-gray-700 mb-1">Subject</label>
              <select
                value={subject}
                onChange={(e) => setSubject(e.target.value)}
                className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-green-500 text-gray-800"
                required
              >
                <option value="">Select a subject</option>
                {SUBJECTS.map((s) => <option key={s} value={s}>{s}</option>)}
              </select>
            </div>

            <div>
              <label className="block text-sm font-semibold text-gray-700 mb-1">Content</label>
              <textarea
                value={content}
                onChange={(e) => setContent(e.target.value)}
                placeholder="Paste your text content here..."
                className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-green-500 text-gray-800 resize-y min-h-[200px]"
              />
            </div>

            <div>
              <label className="block text-sm font-semibold text-gray-700 mb-1">Or upload a file (PDF / TXT)</label>
              <input
                type="file"
                accept=".pdf,.txt"
                onChange={(e) => setFile(e.target.files[0])}
                className="w-full text-gray-700 file:mr-4 file:py-2 file:px-4 file:rounded-lg file:border-0 file:text-sm file:font-semibold file:bg-green-50 file:text-green-700 hover:file:bg-green-100"
              />
            </div>

            <div className="grid grid-cols-2 gap-4">
              <div>
                <label className="block text-sm font-semibold text-gray-700 mb-1">Number of Cards</label>
                <select
                  value={numCards}
                  onChange={(e) => setNumCards(Number(e.target.value))}
                  className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-green-500 text-gray-800"
                >
                  {[5, 10, 15, 20, 30].map((n) => (
                    <option key={n} value={n}>{n} cards</option>
                  ))}
                </select>
              </div>
              <div>
                <label className="block text-sm font-semibold text-gray-700 mb-1">Save to Deck</label>
                <select
                  value={selectedDeck}
                  onChange={(e) => setSelectedDeck(e.target.value)}
                  className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-green-500 text-gray-800"
                >
                  <option value="">Don't save</option>
                  {decks.map((d) => <option key={d.id} value={d.id}>{d.title}</option>)}
                </select>
              </div>
            </div>

            <div className="flex gap-3">
              <button
                type="submit"
                disabled={loading}
                className="flex-1 py-3 bg-gradient-to-r from-green-800 to-green-600 text-white font-bold rounded-xl hover:opacity-90 transition disabled:opacity-50"
              >
                {loading ? (
                  <span className="flex items-center justify-center gap-2">
                    <span className="spinner !w-5 !h-5 !border-2 !border-white/30 !border-t-white" />
                    Generating...
                  </span>
                ) : (
                  'Generate Flashcards'
                )}
              </button>
              <button
                type="button"
                onClick={loadDemo}
                className="px-5 py-3 border-2 border-green-700 text-green-700 rounded-xl font-semibold hover:bg-green-50 transition"
              >
                Demo
              </button>
            </div>
          </form>
        </div>

        {/* Flashcards Section */}
        <div className="bg-white rounded-2xl shadow-md p-6">
          <div className="flex items-center justify-between mb-5">
            <h2 className="text-xl font-bold text-gray-800">Generated Flashcards</h2>
            {flashcards.length > 0 && (
              <div className="flex gap-1">
                <button
                  onClick={() => setViewMode('flip')}
                  className={`px-4 py-1.5 rounded-full text-sm font-semibold border-2 transition ${
                    viewMode === 'flip'
                      ? 'bg-green-700 text-white border-green-700'
                      : 'border-green-700 text-green-700 hover:bg-green-50'
                  }`}
                >
                  Flip
                </button>
                <button
                  onClick={() => setViewMode('list')}
                  className={`px-4 py-1.5 rounded-full text-sm font-semibold border-2 transition ${
                    viewMode === 'list'
                      ? 'bg-green-700 text-white border-green-700'
                      : 'border-green-700 text-green-700 hover:bg-green-50'
                  }`}
                >
                  List
                </button>
              </div>
            )}
          </div>

          <StatsBar flashcards={flashcards} />

          {flashcards.length === 0 ? (
            <div className="text-center text-gray-400 py-16">
              <p className="text-lg">Your generated flashcards will appear here</p>
            </div>
          ) : (
            <div className="space-y-6 max-h-[600px] overflow-y-auto pr-2">
              {Object.entries(sectionGroups).map(([section, cards]) => (
                <div key={section}>
                  {Object.keys(sectionGroups).length > 1 && (
                    <div className="bg-gray-100 text-gray-600 px-4 py-2 rounded-lg font-bold text-sm mb-3">
                      {section}
                    </div>
                  )}
                  <div className={viewMode === 'flip'
                    ? 'grid grid-cols-1 gap-5'
                    : 'space-y-4'
                  }>
                    {cards.map((card) =>
                      viewMode === 'flip' ? (
                        <FlashcardFlip key={card.id} card={card} />
                      ) : (
                        <FlashcardList key={card.id} card={card} />
                      )
                    )}
                  </div>
                </div>
              ))}
            </div>
          )}
        </div>
      </div>

      {/* Export Section */}
      {flashcards.length > 0 && (
        <div className="bg-white rounded-2xl shadow-md p-6 mt-8">
          <h2 className="text-xl font-bold text-gray-800 mb-4">Export Options</h2>
          <ExportButtons flashcards={flashcards} />
        </div>
      )}
    </div>
  );
}
