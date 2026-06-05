import { enterpriseRoutes } from './enterpriseRoutes';

export default function AppRouter() {
  return (
    <div>
      <h1>Q-Verse Router V9</h1>
      <pre>{JSON.stringify(enterpriseRoutes, null, 2)}</pre>
    </div>
  );
}
