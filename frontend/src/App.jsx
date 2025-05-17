import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import { Toaster } from 'react-hot-toast';
import { useEffect } from 'react';
import LoginPage from './pages/LoginPage';
import UserListPage from './pages/UserListPage';
import DashboardPage from './pages/DashboardPage';
import Navbar from './components/Navbar';
import useAuthStore from './store/authStore';
import './index.css';

function PrivateRoute({ children }) {
  const { isAuthenticated, isLoading, checkAuth } = useAuthStore();

  useEffect(() => {
    checkAuth();
  }, [checkAuth]);

  if (isLoading) {
    return <div>載入中...</div>;
  }

  return isAuthenticated ? (
    <>
      <Navbar />
      {children}
    </>
  ) : (
    <Navigate to="/login" />
  );
}

function App() {
  return (
    <Router>
      <Toaster position="top-right" />
      <Routes>
        <Route path="/login" element={<LoginPage />} />
        <Route
          path="/"
          element={
            <PrivateRoute>
              <Navigate to="/dashboard" />
            </PrivateRoute>
          }
        />
        <Route
          path="/dashboard"
          element={
            <PrivateRoute>
              <DashboardPage />
            </PrivateRoute>
          }
        />
        <Route
          path="/users"
          element={
            <PrivateRoute>
              <UserListPage />
            </PrivateRoute>
          }
        />
      </Routes>
    </Router>
  );
}

export default App;
