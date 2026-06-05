import NavigationMenu from '../navigation/NavigationMenu';
import Breadcrumbs from '../navigation/Breadcrumbs';

export default function DashboardShell({ children }) {
  return (
    <div>
      <NavigationMenu />
      <Breadcrumbs />
      {children}
    </div>
  );
}
