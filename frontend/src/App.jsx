import EnterpriseLayout from './layouts/EnterpriseLayout';
import AppRouter from './routes/AppRouter';

export default function App() {
  return (
    <EnterpriseLayout>
      <AppRouter />
    </EnterpriseLayout>
  );
}
