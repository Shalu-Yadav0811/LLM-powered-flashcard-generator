import { Link, useNavigate } from 'react-router-dom';
import { useAuth } from '../hooks/useAuth';
import { HiOutlineLogout, HiOutlineViewGrid, HiOutlineSparkles } from 'react-icons/hi';

export default function Navbar() {
  const { user, logout } = useAuth();
  const navigate = useNavigate();

  const handleLogout = () => {
    logout();
    navigate('/login');
  };

  return (
    <nav className="bg-green-900 text-white shadow-lg">
      <div className="max-w-7xl mx-auto px-4 py-3 flex items-center justify-between">
        <Link to="/dashboard" className="flex items-center gap-2 text-xl font-bold hover:opacity-90">
          <span className="text-2xl">&#x1F9E0;</span>
          FlashGen
        </Link>

        {user && (
          <div className="flex items-center gap-4">
            <Link
              to="/dashboard"
              className="flex items-center gap-1 px-3 py-2 rounded-lg hover:bg-green-800 transition text-sm font-medium"
            >
              <HiOutlineViewGrid className="text-lg" />
              My Decks
            </Link>
            <Link
              to="/generate"
              className="flex items-center gap-1 px-3 py-2 rounded-lg hover:bg-green-800 transition text-sm font-medium"
            >
              <HiOutlineSparkles className="text-lg" />
              Generate
            </Link>
            <div className="flex items-center gap-3 ml-4 pl-4 border-l border-green-700">
              <span className="text-sm text-green-200">Hi, {user.username}</span>
              <button
                onClick={handleLogout}
                className="flex items-center gap-1 px-3 py-2 rounded-lg hover:bg-red-700 transition text-sm font-medium"
              >
                <HiOutlineLogout className="text-lg" />
                Logout
              </button>
            </div>
          </div>
        )}
      </div>
    </nav>
  );
}
