import React, { useState, useEffect } from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import { FileText, BarChart3, Users, Menu, X, Plus, Shield, Home, Award, CheckCircle } from 'lucide-react';
import Login from './pages/Login';
import AdminLogin from './pages/AdminLogin';
import AdminDashboard from './pages/AdminDashboard';
import StudentDashboard from './pages/StudentDashboard';
import LegacyVerificationRequest from './pages/LegacyVerificationRequest';
import PublicVerification from './pages/PublicVerification';
import Upload from './pages/Upload';
import Dashboard from './pages/Dashboard';
import ManualReview from './pages/ManualReview';
import CertificateIssuance from './pages/CertificateIssuance';

// Simple authentication state management
const getStoredUser = () => {
  const user = localStorage.getItem('user');
  return user ? JSON.parse(user) : null;
};

function App() {
  const [user, setUser] = useState(getStoredUser());
  const [userRole, setUserRole] = useState(user?.role || null);
  const [loading, setLoading] = useState(false);
  const [mobileMenuOpen, setMobileMenuOpen] = useState(false);

  useEffect(() => {
    // Check for stored user on mount
    const storedUser = getStoredUser();
    if (storedUser) {
      setUser(storedUser);
      setUserRole(storedUser.role);
    }
    setLoading(false);
  }, []);

  const handleAuthSuccess = (userData) => {
    console.log('Auth success with userData:', userData);
    setUser(userData);
    setUserRole(userData.role);
    localStorage.setItem('user', JSON.stringify(userData));
  };

  const handleSignOut = () => {
    setUser(null);
    setUserRole(null);
    localStorage.removeItem('user');
    localStorage.removeItem('access_token');
    localStorage.removeItem('refresh_token');
  };

  if (loading) {
    return (
      <div className="min-h-screen bg-gray-50 flex items-center justify-center">
        <div className="text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600 mx-auto mb-4"></div>
          <p className="text-gray-600">Loading...</p>
        </div>
      </div>
    );
  }

  if (!user) {
    return <Login onAuthSuccess={handleAuthSuccess} />;
  }

  // Role-based routing
  const getDefaultRoute = () => {
    console.log('Getting default route for userRole:', userRole);
    switch (userRole) {
      case 'university_admin':
        return '/admin/dashboard';
      case 'student':
        return '/student/dashboard';
      case 'employer':
        return '/verify';
      default:
        return '/login';
    }
  };

  console.log('App render - user:', user, 'userRole:', userRole);

  return (
    <Router>
      <div className="min-h-screen bg-gray-50">
        {/* Navigation */}
        <nav className="bg-white shadow-lg">
          <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
            <div className="flex justify-between h-16">
              <div className="flex items-center">
                <Shield className="h-8 w-8 text-blue-600 mr-2" />
                <span className="text-xl font-bold text-gray-900">Certificate Verifier</span>
              </div>
              
            {/* Role-based Navigation */}
            <div className="flex items-center space-x-4">
              {!user && (
                <a
                  href="/admin/login"
                  className="text-sm text-gray-700 hover:text-blue-600 px-3 py-2 rounded-md flex items-center"
                >
                  <Shield className="h-4 w-4 mr-1" />
                  Admin Login
                </a>
              )}
              {userRole === 'university_admin' && (
                  <>
                    <div className="hidden md:flex items-center space-x-4">
                      <a
                        href="/admin/dashboard"
                        className="text-sm text-gray-700 hover:text-blue-600 px-3 py-2 rounded-md flex items-center"
                      >
                        <Home className="h-4 w-4 mr-1" />
                        Dashboard
                      </a>
                      <a
                        href="/admin/issue-certificate"
                        className="text-sm text-gray-700 hover:text-blue-600 px-3 py-2 rounded-md flex items-center"
                      >
                        <Award className="h-4 w-4 mr-1" />
                        Issue Certificate
                      </a>
                      <a
                        href="/admin/legacy-verification"
                        className="text-sm text-gray-700 hover:text-blue-600 px-3 py-2 rounded-md flex items-center"
                      >
                        <CheckCircle className="h-4 w-4 mr-1" />
                        Legacy Verification
                      </a>
                    </div>
                    
                    {/* Mobile menu button */}
                    <button
                      onClick={() => setMobileMenuOpen(!mobileMenuOpen)}
                      className="md:hidden text-gray-700 hover:text-blue-600"
                    >
                      <Menu className="h-6 w-6" />
                    </button>
                  </>
                )}
                
                <span className="text-sm text-gray-700 hidden sm:block">
                  Welcome, {user?.full_name} ({userRole})
                </span>
                <button
                  onClick={handleSignOut}
                  className="bg-red-600 text-white px-4 py-2 rounded-md hover:bg-red-700"
                >
                  Sign Out
                </button>
              </div>
            </div>
          </div>
        </nav>

        {/* Mobile Navigation Menu */}
        {mobileMenuOpen && (userRole === 'university_admin' || userRole === 'super_admin') && (
          <div className="md:hidden bg-white border-b border-gray-200">
            <div className="px-4 py-2 space-y-1">
              <a
                href="/admin/dashboard"
                className="block px-3 py-2 text-sm text-gray-700 hover:text-blue-600 hover:bg-gray-50 rounded-md flex items-center"
                onClick={() => setMobileMenuOpen(false)}
              >
                <Home className="h-4 w-4 mr-2" />
                Dashboard
              </a>
              <a
                href="/admin/issue-certificate"
                className="block px-3 py-2 text-sm text-gray-700 hover:text-blue-600 hover:bg-gray-50 rounded-md flex items-center"
                onClick={() => setMobileMenuOpen(false)}
              >
                <Award className="h-4 w-4 mr-2" />
                Issue Certificate
              </a>
              <a
                href="/admin/legacy-verification"
                className="block px-3 py-2 text-sm text-gray-700 hover:text-blue-600 hover:bg-gray-50 rounded-md flex items-center"
                onClick={() => setMobileMenuOpen(false)}
              >
                <CheckCircle className="h-4 w-4 mr-2" />
                Legacy Verification
              </a>
            </div>
          </div>
        )}

        <Routes>
          {/* Public routes */}
          <Route path="/verify/:attestationId" element={<PublicVerification />} />
          <Route path="/login" element={<Login onAuthSuccess={handleAuthSuccess} />} />
          <Route path="/admin/login" element={<AdminLogin onAuthSuccess={handleAuthSuccess} />} />
          
          {/* University Admin routes */}
          <Route 
            path="/admin/dashboard" 
            element={
              (userRole === 'university_admin' || userRole === 'super_admin') ? 
                <AdminDashboard /> : 
                <Navigate to={getDefaultRoute()} replace />
            } 
          />
          <Route 
            path="/admin/issue-certificate" 
            element={
              (userRole === 'university_admin' || userRole === 'super_admin') ? 
                <CertificateIssuance /> : 
                <Navigate to={getDefaultRoute()} replace />
            } 
          />
          <Route 
            path="/admin/legacy-verification" 
            element={
              (userRole === 'university_admin' || userRole === 'super_admin') ? 
                <ManualReview /> : 
                <Navigate to={getDefaultRoute()} replace />
            } 
          />
          
          {/* Student routes */}
          <Route 
            path="/student/dashboard" 
            element={
              userRole === 'student' ? 
                <StudentDashboard /> : 
                <Navigate to={getDefaultRoute()} replace />
            } 
          />
          <Route 
            path="/student/legacy-verification" 
            element={
              userRole === 'student' ? 
                <LegacyVerificationRequest /> : 
                <Navigate to={getDefaultRoute()} replace />
            } 
          />
          
          {/* Employer/Verifier routes */}
          <Route 
            path="/verify" 
            element={
              userRole === 'employer' ? 
                <Upload /> : 
                <Navigate to={getDefaultRoute()} replace />
            } 
          />
          
          {/* Root route - redirect to appropriate dashboard */}
          <Route path="/" element={<Navigate to={getDefaultRoute()} replace />} />
          <Route path="/dashboard" element={<Dashboard />} />
          <Route path="/reviews" element={<ManualReview />} />
          <Route path="/issue" element={<CertificateIssuance />} />
          
          {/* Catch all route */}
          <Route path="*" element={<Navigate to={getDefaultRoute()} replace />} />
        </Routes>
      </div>
    </Router>
  );
}

export default App;