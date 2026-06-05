import React from 'react';
import ReactDOM from 'react-dom/client';
import App from './App';
import AppProvider from './providers/AppProvider';
import ThemeProvider from './providers/ThemeProvider';
import AuthProvider from './providers/AuthProvider';
import RouterProvider from './providers/RouterProvider';

ReactDOM.createRoot(document.getElementById('root')).render(
  <AppProvider>
    <ThemeProvider>
      <AuthProvider>
        <RouterProvider>
          <App />
        </RouterProvider>
      </AuthProvider>
    </ThemeProvider>
  </AppProvider>
);
