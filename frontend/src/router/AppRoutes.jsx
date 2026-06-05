import EnterpriseHome from '../pages/EnterpriseHome';
import EnterpriseMarketplace from '../pages/EnterpriseMarketplace';
import EnterpriseControlCenter from '../pages/EnterpriseControlCenter';

export const AppRoutes = [
  { path: '/', element: EnterpriseHome },
  { path: '/marketplace', element: EnterpriseMarketplace },
  { path: '/control-center', element: EnterpriseControlCenter },
];
