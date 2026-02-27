import { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import api from '../api/axios';
import toast from 'react-hot-toast';
import FlashcardFlip from '../components/FlashcardFlip';
import FlashcardList from '../components/FlashcardList';
import FlashcardForm from '../components/FlashcardForm';
import StatsBar from '../components/StatsBar';
import ExportButtons from '../components/ExportButtons';
import { HiOutlineArrowLeft, HiOutlinePlus } from 'react-icons/hi';

const LANGUAGES = [
  { code: 'en', name: 'English' }, { code: 'es', name: 'Spanish' },
  { code: 'fr', name: 'French' }, { code: 'de', name: 'German' },
  { code: 'hi', name: 'Hindi' }, { code: 'zh-CN', name: 'Chinese' },
  { code: 'ar', name: 'Arabic' }, { code: 'ru', name: 'Russian' },
  { code: 'pt', name: 'Portuguese' }, { code: 'ja', name: 'Japanese' },
];

export default function DeckView() {
  const { id } = useParams();
  const navigate = useNavigate();
  const [deck, setDeck] = useState(null);
  const [loading, setLoading] = useState(true);
  const [viewMode, setViewMode] = useState('flip');
  const [editingCard, setEditingCard] = useState(null);
  const [showAddForm, setShowAddForm] = useState(false);
  const [targetLang, setTargetLang] = useState('en');
  const [translating, setTranslating] = useState(false);

  useEffect(() => {
    fetchDeck();
  }, [id]);

  const fetchDeck = async () => {
    try {
      const { data } = await api.get(`/decks/${id}`);
      setDeck(data.deck);
    } catch {
      toast.error('Failed to load deck');
      navigate('/dashboard');
    } finally {
      setLoading(false);
    }
  };

  const handleSaveEdit = async (cardData) => {
    try {
      await api.put(`/cards/${cardData.id}`, {
        question: cardData.question,
        answer: cardData.answer,
        difficulty: cardData.difficulty,
        topic: cardData.topic,
      });
      toast.success('Card updated!');
      setEditingCard(null);
      fetchDeck();
    } catch {
      toast.error('Failed to update card');
    }
  };

  const handleAddCard = async (cardData) => {
    try {
      await api.post(`/decks/${id}/cards`, {
        question: cardData.question,
        answer: cardData.answer,
        difficulty: cardData.difficulty,
        topic: cardData.topic,
      });
      toast.success('Card added!');
      setShowAddForm(false);
      fetchDeck();
    } catch {
      toast.error('Failed to add card');
    }
  };

  const handleDeleteCard = async (cardId) => {
    if (!window.confirm('Delete this flashcard?')) return;
    try {
      await api.delete(`/cards/${cardId}`);
      toast.success('Card deleted');
      fetchDeck();
    } catch {
      toast.error('Failed to delete card');
    }
  };

  const handleTranslate = async () => {
    if (!deck?.flashcards?.length) return;
    setTranslating(true);
    try {
      const translated = [];
      for (const card of deck.flashcards) {
        const [qRes, aRes] = await Promise.all([
          api.post('/ai/translate', { text: card.question, targetLang: targetLang }),
          api.post('/ai/translate', { text: card.answer, targetLang: targetLang }),
        ]);
        translated.push({
          ...card,
          question: qRes.data.translated,
          answer: aRes.data.translated,
        });
      }
      setDeck({ ...deck, flashcards: translated });
      toast.success('Translation complete!');
    } catch {
      toast.error('Translation failed');
    } finally {
      setTranslating(false);
    }
  };

  if (loading) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <div className="spinner" />
      </div>
    );
  }

  if (!deck) return null;

  const flashcards = deck.flashcards || [];

  return (
    <div className="max-w-6xl mx-auto px-4 py-8">
      {/* Header */}
      <div className="flex items-center gap-4 mb-8">
        <button
          onClick={() => navigate('/dashboard')}
          className="p-2 rounded-lg hover:bg-gray-100 transition"
        >
          <HiOutlineArrowLeft className="text-2xl text-gray-600" />
        </button>
        <div className="flex-1">
          <h1 className="text-3xl font-bold text-gray-800">{deck.title}</h1>
          <div className="flex items-center gap-3 mt-1">
            {deck.subject && (
              <span className="text-sm bg-green-100 text-green-700 px-3 py-1 rounded-full font-medium">
                {deck.subject}
              </span>
            )}
            <span className="text-sm text-gray-400">{flashcards.length} cards</span>
          </div>
        </div>
        <button
          onClick={() => setShowAddForm(true)}
          className="flex items-center gap-2 px-5 py-2.5 bg-green-700 text-white font-semibold rounded-xl hover:bg-green-800 transition"
        >
          <HiOutlinePlus className="text-lg" />
          Add Card
        </button>
      </div>

      {deck.description && (
        <p className="text-gray-500 mb-6">{deck.description}</p>
      )}

      <StatsBar flashcards={flashcards} />

      {/* View Toggle & Export */}
      {flashcards.length > 0 && (
        <div className="flex flex-wrap items-center justify-between gap-4 mb-6">
          <div className="flex gap-1">
            <button
              onClick={() => setViewMode('flip')}
              className={`px-4 py-1.5 rounded-full text-sm font-semibold border-2 transition ${
                viewMode === 'flip'
                  ? 'bg-green-700 text-white border-green-700'
                  : 'border-green-700 text-green-700 hover:bg-green-50'
              }`}
            >
              Flip Cards
            </button>
            <button
              onClick={() => setViewMode('list')}
              className={`px-4 py-1.5 rounded-full text-sm font-semibold border-2 transition ${
                viewMode === 'list'
                  ? 'bg-green-700 text-white border-green-700'
                  : 'border-green-700 text-green-700 hover:bg-green-50'
              }`}
            >
              List View
            </button>
          </div>
          <ExportButtons flashcards={flashcards} />
        </div>
      )}

      {/* Translate Section */}
      {flashcards.length > 0 && (
        <div className="flex items-center gap-3 mb-8 bg-gray-50 p-4 rounded-xl">
          <span className="text-sm font-semibold text-gray-700">Translate to:</span>
          <select
            value={targetLang}
            onChange={(e) => setTargetLang(e.target.value)}
            className="px-3 py-2 border border-gray-300 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-green-500 text-gray-800"
          >
            {LANGUAGES.map((l) => (
              <option key={l.code} value={l.code}>{l.name}</option>
            ))}
          </select>
          <button
            onClick={handleTranslate}
            disabled={translating}
            className="px-5 py-2 bg-green-700 text-white rounded-lg font-semibold text-sm hover:bg-green-800 transition disabled:opacity-50"
          >
            {translating ? 'Translating...' : 'Translate'}
          </button>
        </div>
      )}

      {/* Flashcards */}
      {flashcards.length === 0 ? (
        <div className="text-center py-16 text-gray-400">
          <p className="text-lg mb-4">No flashcards in this deck yet</p>
          <button
            onClick={() => setShowAddForm(true)}
            className="px-6 py-3 bg-green-700 text-white rounded-xl font-semibold hover:bg-green-800 transition"
          >
            Add your first card
          </button>
        </div>
      ) : (
        <div className={viewMode === 'flip'
          ? 'grid grid-cols-1 md:grid-cols-2 gap-6'
          : 'space-y-4'
        }>
          {flashcards.map((card) =>
            viewMode === 'flip' ? (
              <FlashcardFlip
                key={card.id}
                card={card}
                onEdit={setEditingCard}
              />
            ) : (
              <FlashcardList
                key={card.id}
                card={card}
                onEdit={setEditingCard}
                onDelete={handleDeleteCard}
              />
            )
          )}
        </div>
      )}

      {/* Edit Modal */}
      {editingCard && (
        <FlashcardForm
          card={editingCard}
          onSave={handleSaveEdit}
          onCancel={() => setEditingCard(null)}
        />
      )}

      {/* Add Card Modal */}
      {showAddForm && (
        <FlashcardForm
          card={{ question: '', answer: '', difficulty: 'Medium', topic: '' }}
          onSave={handleAddCard}
          onCancel={() => setShowAddForm(false)}
        />
      )}
    </div>
  );
}
