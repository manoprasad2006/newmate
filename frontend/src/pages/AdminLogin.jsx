import React, { useState } from 'react';
import { User, Lock, Mail, Eye, EyeOff, Shield, Building, AlertTriangle } from 'lucide-react';

const AdminLogin = ({ onAuthSuccess }) => {
  const [formData, setFormData] = useState({
    email: '',
    password: '',
    admin_code: ''
  });
  const [showPassword, setShowPassword] = useState(false);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  const handleInputChange = (e) => {
    const { name, value } = e.target;
    setFormData(prev => ({
      ...prev,
      [name]: value
    }));
  };

  // Admin credentials for testing
  const adminCredentials = {
    'admin@certverifier.com': {
      password: 'admin123',
      admin_code: 'ADMIN2024',
      full_name: 'System Administrator',
      role: 'super_admin',
      institution: 'Certificate Verification System'
    },
    'superadmin@certverifier.com': {
      password: 'superadmin123',
      admin_code: 'SUPER2024',
      full_name: 'Super Administrator',
      role: 'super_admin',
      institution: 'Certificate Verification System'
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError('');

    try {
      // Validate required fields
      if (!formData.email || !formData.password || !formData.admin_code) {
        throw new Error('All fields are required');
      }

      // Check if admin exists
      const admin = adminCredentials[formData.email];
      if (!admin) {
        throw new Error('Invalid admin credentials');
      }

      // Verify password and admin code
      if (admin.password !== formData.password) {
        throw new Error('Invalid password');
      }

      if (admin.admin_code !== formData.admin_code) {
        throw new Error('Invalid admin code');
      }

      // Create admin user data
      const adminData = {
        id: 'admin_1',
        full_name: admin.full_name,
        email: formData.email,
        role: admin.role,
        institution: admin.institution,
        admin_code: admin.admin_code
      };

      console.log('Admin login successful:', adminData);
      onAuthSuccess(adminData);

    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-900 via-blue-800 to-indigo-900 flex flex-col justify-center py-12 sm:px-6 lg:px-8">
      <div className="sm:mx-auto sm:w-full sm:max-w-md">
        <div className="flex justify-center">
          <div className="bg-white p-3 rounded-full shadow-lg">
            <Shield className="h-12 w-12 text-blue-600" />
          </div>
        </div>
        <h2 className="mt-6 text-center text-3xl font-extrabold text-white">
          Admin Portal
        </h2>
        <p className="mt-2 text-center text-sm text-blue-100">
          Certificate Verification System - Administrative Access
        </p>
      </div>

      <div className="mt-8 sm:mx-auto sm:w-full sm:max-w-md">
        <div className="bg-white py-8 px-4 shadow-2xl sm:rounded-lg sm:px-10">
          <form className="space-y-6" onSubmit={handleSubmit}>
            {/* Admin Code */}
            <div>
              <label htmlFor="admin_code" className="block text-sm font-medium text-gray-700">
                Admin Access Code
              </label>
              <div className="mt-1 relative">
                <div className="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
                  <AlertTriangle className="h-5 w-5 text-gray-400" />
                </div>
                <input
                  id="admin_code"
                  name="admin_code"
                  type="text"
                  required
                  value={formData.admin_code}
                  onChange={handleInputChange}
                  className="appearance-none block w-full pl-10 pr-3 py-2 border border-gray-300 rounded-md placeholder-gray-400 focus:outline-none focus:ring-blue-500 focus:border-blue-500 sm:text-sm"
                  placeholder="Enter admin access code"
                />
              </div>
            </div>

            {/* Email */}
            <div>
              <label htmlFor="email" className="block text-sm font-medium text-gray-700">
                Admin Email
              </label>
              <div className="mt-1 relative">
                <div className="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
                  <Mail className="h-5 w-5 text-gray-400" />
                </div>
                <input
                  id="email"
                  name="email"
                  type="email"
                  autoComplete="email"
                  required
                  value={formData.email}
                  onChange={handleInputChange}
                  className="appearance-none block w-full pl-10 pr-3 py-2 border border-gray-300 rounded-md placeholder-gray-400 focus:outline-none focus:ring-blue-500 focus:border-blue-500 sm:text-sm"
                  placeholder="Enter admin email"
                />
              </div>
            </div>

            {/* Password */}
            <div>
              <label htmlFor="password" className="block text-sm font-medium text-gray-700">
                Password
              </label>
              <div className="mt-1 relative">
                <div className="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
                  <Lock className="h-5 w-5 text-gray-400" />
                </div>
                <input
                  id="password"
                  name="password"
                  type={showPassword ? 'text' : 'password'}
                  autoComplete="current-password"
                  required
                  value={formData.password}
                  onChange={handleInputChange}
                  className="appearance-none block w-full pl-10 pr-10 py-2 border border-gray-300 rounded-md placeholder-gray-400 focus:outline-none focus:ring-blue-500 focus:border-blue-500 sm:text-sm"
                  placeholder="Enter password"
                />
                <div className="absolute inset-y-0 right-0 pr-3 flex items-center">
                  <button
                    type="button"
                    onClick={() => setShowPassword(!showPassword)}
                    className="text-gray-400 hover:text-gray-500"
                  >
                    {showPassword ? <EyeOff className="h-5 w-5" /> : <Eye className="h-5 w-5" />}
                  </button>
                </div>
              </div>
            </div>

            {error && (
              <div className="bg-red-50 border border-red-200 text-red-600 px-4 py-3 rounded-md text-sm">
                {error}
              </div>
            )}

            {/* Admin Credentials */}
            <div className="bg-blue-50 border border-blue-200 p-4 rounded text-xs">
              <div className="flex items-center mb-2">
                <Building className="h-4 w-4 text-blue-600 mr-2" />
                <strong className="text-blue-800">Admin Credentials:</strong>
              </div>
              <div className="space-y-1 text-blue-700">
                <div><strong>Email:</strong> admin@certverifier.com</div>
                <div><strong>Password:</strong> admin123</div>
                <div><strong>Admin Code:</strong> ADMIN2024</div>
                <div className="mt-2 text-blue-600">--- OR ---</div>
                <div><strong>Email:</strong> superadmin@certverifier.com</div>
                <div><strong>Password:</strong> superadmin123</div>
                <div><strong>Admin Code:</strong> SUPER2024</div>
              </div>
            </div>

            <div>
              <button
                type="submit"
                disabled={loading}
                className="w-full flex justify-center py-3 px-4 border border-transparent rounded-md shadow-sm text-sm font-medium text-white bg-blue-600 hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500 disabled:opacity-50 transition-colors duration-200"
              >
                {loading ? (
                  <div className="flex items-center">
                    <div className="animate-spin rounded-full h-4 w-4 border-b-2 border-white mr-2"></div>
                    Authenticating...
                  </div>
                ) : (
                  'Access Admin Portal'
                )}
              </button>
            </div>

            {/* Security Notice */}
            <div className="bg-yellow-50 border border-yellow-200 p-3 rounded text-xs text-yellow-800">
              <div className="flex items-center">
                <AlertTriangle className="h-4 w-4 mr-2" />
                <strong>Security Notice:</strong>
              </div>
              <p className="mt-1">This is a restricted administrative area. All access attempts are logged and monitored.</p>
            </div>
          </form>
        </div>
      </div>
    </div>
  );
};

export default AdminLogin;
