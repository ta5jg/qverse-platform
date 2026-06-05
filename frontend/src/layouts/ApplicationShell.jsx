import Sidebar from '../components/Sidebar';
import Topbar from '../components/Topbar';
import NotificationCenter from '../components/NotificationCenter';

export default function ApplicationShell({ children }) {
  return (
    <>
      <Sidebar />
      <Topbar />
      <NotificationCenter />
      <main>
        {children}
      </main>
    </>
  );
}
