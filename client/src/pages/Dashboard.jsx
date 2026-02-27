import { useState, useEffect } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import api from '../api/axios';
import toast from 'react-hot-toast';
import { HiOutlinePlus, HiOutlineTrash, HiOutlineCollection } from 'react-icons/hi';

export default function Dashboard() {
  const [decks, setDecks] = useState([]);
  const [loading, setLoading] = useState(true);
  const [showCreate, setShowCreate] = useState(false);
  const [newTitle, setNewTitle] = useState('');
  const [newSubject, setNewSubject] = useState('');
  const [newDescription, setNewDescription] = useState('');
  const navigate = useNavigate();

  useEffect(() => {
    fetchDecks();
  }, []);

  const fetchDecks = async () => {
    try {
      const { data } = await api.get('/decks');
      setDecks(data.decks);
    } catch {
      toast.error('Failed to load decks');
    } finally {
      setLoading(false);
    }
  };

  const createDeck = async (e) => {
    e.preventDefault();
    if (!newTitle.trim()) return;
    try {
      const { data } = await api.post('/decks', {
        title: newTitle,
        subject: newSubject,
        description: newDescription,
      });
      setDecks([data.deck, ...decks]);
      setNewTitle('');
      setNewSubject('');
      setNewDescription('');
      setShowCreate(false);
      toast.success('Deck created!');
    } catch {
      toast.error('Failed to create deck');
    }
  };

  const deleteDeck = async (id) => {
    if (!window.confirm('Are you sure you want to delete this deck?')) return;
    try {
      await api.delete(`/decks/${id}`);
      setDecks(decks.filter((d) => d.id !== id));
      toast.success('Deck deleted');
    } catch {
      toast.error('Failed to delete deck');
    }
  };

  if (loading) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <div className="spinner" />
      </div>
    );
  }

  return (
    <div className="max-w-6xl mx-auto px-4 py-8">
      <div className="flex items-center justify-between mb-8">
        <h1 className="text-3xl font-bold text-gray-800">My Decks</h1>
        <button
          onClick={() => setShowCreate(!showCreate)}
          className="flex items-center gap-2 px-5 py-3 bg-green-700 text-white font-semibold rounded-xl hover:bg-green-800 transition"
        >
          <HiOutlinePlus className="text-xl" />
          New Deck
        </button>
      </div>

      {showCreate && (
        <form onSubmit={createDeck} className="bg-white rounded-xl shadow-md p-6 mb-8 space-y-4">
          <input
            type="text"
            value={newTitle}
            onChange={(e) => setNewTitle(e.target.value)}
            placeholder="Deck title"
            className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-green-500 text-gray-800"
            required
          />
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <select
              value={newSubject}
              onChange={(e) => setNewSubject(e.target.value)}
              className="px-4 py-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-green-500 text-gray-800"
            >
              <option value="">Select subject</option>
              <option value="Computer Science">Computer Science</option>
              <option value="Mathematics">Mathematics</option>
              <option value="Physics">Physics</option>
              <option value="Chemistry">Chemistry</option>
              <option value="Biology">Biology</option>
              <option value="History">History</option>
              <option value="Geography">Geography</option>
              <option value="Literature">Literature</option>
              <option value="Other">Other</option>
            </select>
            <input
              type="text"
              value={newDescription}
              onChange={(e) => setNewDescription(e.target.value)}
              placeholder="Description (optional)"
              className="px-4 py-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-green-500 text-gray-800"
            />
          </div>
          <div className="flex gap-3">
            <button type="submit" className="px-6 py-2 bg-green-700 text-white rounded-lg font-semibold hover:bg-green-800 transition">
              Create
            </button>
            <button type="button" onClick={() => setShowCreate(false)} className="px-6 py-2 border border-gray-300 rounded-lg text-gray-600 hover:bg-gray-50 transition">
              Cancel
            </button>
          </div>
        </form>
      )}

      {decks.length === 0 ? (
        <div className="text-center py-20">
          <HiOutlineCollection className="mx-auto text-6xl text-gray-300 mb-4" />
          <h3 className="text-xl text-gray-500 mb-2">No decks yet</h3>
          <p className="text-gray-400 mb-6">Create your first deck or generate flashcards with AI</p>
          <div className="flex gap-4 justify-center">
            <button
              onClick={() => setShowCreate(true)}
              className="px-6 py-3 bg-green-700 text-white rounded-xl font-semibold hover:bg-green-800 transition"
            >
              Create a Deck
            </button>
            <Link
              to="/generate"
              className="px-6 py-3 border-2 border-green-700 text-green-700 rounded-xl font-semibold hover:bg-green-50 transition"
            >
              Generate with AI
            </Link>
          </div>
        </div>
      ) : (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {decks.map((deck) => (
            <div
              key={deck.id}
              className="bg-white rounded-xl shadow-md hover:shadow-lg transition cursor-pointer overflow-hidden"
            >
              <div
                onClick={() => navigate(`/decks/${deck.id}`)}
                className="p-6"
              >
                <div className="flex items-start justify-between mb-3">
                  <h3 className="text-lg font-bold text-gray-800 line-clamp-1">{deck.title}</h3>
                  {deck.subject && (
                    <span className="text-xs bg-green-100 text-green-700 px-2 py-1 rounded-full font-medium shrink-0 ml-2">
                      {deck.subject}
                    </span>
                  )}
                </div>
                {deck.description && (
                  <p className="text-gray-500 text-sm mb-3 line-clamp-2">{deck.description}</p>
                )}
                <div className="flex items-center justify-between text-sm text-gray-400">
                  <span>{deck.card_count} cards</span>
                  <span>{new Date(deck.updated_at).toLocaleDateString()}</span>
                </div>
              </div>
              <div className="border-t px-6 py-3 flex justify-end">
                <button
                  onClick={(e) => { e.stopPropagation(); deleteDeck(deck.id); }}
                  className="text-red-400 hover:text-red-600 transition"
                >
                  <HiOutlineTrash className="text-xl" />
                </button>
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}
