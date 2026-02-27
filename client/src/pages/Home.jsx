import { Link } from 'react-router-dom';
import { useAuth } from '../hooks/useAuth';

export default function Home() {
  const { user } = useAuth();

  return (
    <div className="min-h-screen bg-gradient-to-br from-green-900 to-green-700 flex flex-col items-center justify-center px-4 text-white">
      <h1 className="text-5xl md:text-6xl font-bold mb-4 text-center drop-shadow-lg">
        FlashGen
      </h1>
      <p className="text-xl md:text-2xl text-green-100 mb-8 text-center max-w-2xl">
        Turn notes and documents into smart flashcards instantly — powered by AI
      </p>

      <div className="flex gap-4">
        {user ? (
          <Link
            to="/dashboard"
            className="px-8 py-4 bg-white text-green-800 font-bold rounded-xl text-lg hover:bg-green-50 transition shadow-lg"
          >
            Go to Dashboard
          </Link>
        ) : (
          <>
            <Link
              to="/register"
              className="px-8 py-4 bg-white text-green-800 font-bold rounded-xl text-lg hover:bg-green-50 transition shadow-lg"
            >
              Get Started
            </Link>
            <Link
              to="/login"
              className="px-8 py-4 border-2 border-white text-white font-bold rounded-xl text-lg hover:bg-white/10 transition"
            >
              Sign In
            </Link>
          </>
        )}
      </div>

      <div className="mt-16 grid md:grid-cols-3 gap-8 max-w-4xl w-full">
        {[
          { title: 'AI-Powered', desc: 'Generate flashcards from any text or PDF using Google Gemini AI' },
          { title: 'Smart Study', desc: 'Spaced repetition and quiz modes help you retain knowledge longer' },
          { title: 'Share & Export', desc: 'Export to Anki, JSON, CSV or share decks with friends' },
        ].map((feature) => (
          <div key={feature.title} className="bg-white/10 backdrop-blur rounded-xl p-6 text-center">
            <h3 className="text-xl font-bold mb-2">{feature.title}</h3>
            <p className="text-green-100 text-sm">{feature.desc}</p>
          </div>
        ))}
      </div>
    </div>
  );
}
